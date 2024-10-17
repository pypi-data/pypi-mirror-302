from io import StringIO
import json
from typing import Dict, Optional, Any
import pandas as pd

from tangent_works.api.forecasting import ForecastingApi
from tangent_works.business_data.forecasting_configuration import (
    AutoForecastingConfiguration,
)
from tangent_works.business_data.forecasting_model import ForecastingModel
from tangent_works.business_logic.imputation import Imputer
from tangent_works.business_logic.time_scaling import TimeScaler
from tangent_works.utils.exceptions import TangentValidationError
from tangent_works.business_data.time_series import TimeSeries
from tangent_works.utils.python_client_utils import (
    send_rest_api_request,
    wait_for_job_to_finish,
)


class AutoForecastingApi:
    def __init__(
        self, time_series: TimeSeries, configuration: Optional[Dict[str, Any]] = None
    ):
        if not isinstance(time_series, TimeSeries):
            raise TangentValidationError("Invalid time-series object type.")

        if not isinstance(configuration, Dict) and configuration is not None:
            raise TangentValidationError("Invalid configuration object type.")

        self._configuration_dict = configuration if configuration else {}
        self._time_series = time_series
        self._configuration = self._create_build_configuration(
            self._configuration_dict, time_series
        )
        self._result_table = None
        self._rca_table = None

        self._forecasting = None

    def _create_build_configuration(
        self, configuration_input: Dict[str, Any], time_series: TimeSeries
    ) -> AutoForecastingConfiguration:
        configuration = configuration_input.copy()
        if "engine" in configuration and "max_offsets_depth" in configuration["engine"]:
            configuration["engine"]["offset_limit"] = (
                -1 * configuration["engine"]["max_offsets_depth"]
            )
            configuration["engine"].pop("max_offsets_depth")

        return AutoForecastingConfiguration.from_dict(configuration, time_series)

    @property
    def result_table(self) -> Optional[pd.DataFrame]:
        return self._result_table

    @property
    def rca_table(self) -> Optional[pd.DataFrame]:
        return self._rca_table

    @property
    def time_series(self) -> TimeSeries:
        return self._time_series

    @property
    def configuration(self) -> Dict[str, Any]:
        return self._configuration_dict

    @property
    def model(self) -> Optional[ForecastingModel]:
        return self._forecasting.model if self._forecasting else None

    def run(self, inplace: bool = True) -> None:
        self._result_table = None
        self._rca_table = None

        processed_time_series = self.preprocess_time_series()
        dataset_csv = processed_time_series.dataframe.to_csv(
            index=False, sep=",", decimal="."
        )

        metadata_dict = {
            "timestamp_column": processed_time_series.timestamp,
            "group_key_columns": processed_time_series.group_keys,
        }

        request_part = [
            ("dataset", ("dataset.csv", dataset_csv, "text/csv")),
            (
                "configuration",
                (
                    "configuration.json",
                    json.dumps(self._configuration_dict),
                    "application/json",
                ),
            ),
            (
                "metadata",
                (
                    "metadata.json",
                    json.dumps(metadata_dict),
                    "application/json",
                ),
            ),
        ]

        post_response = send_rest_api_request("POST", "/auto-forecast", request_part)
        job_id = post_response.json()["id"]
        wait_for_job_to_finish("auto-forecast", job_id)

        model_response = send_rest_api_request("GET", f"/auto-forecast/{job_id}/model")
        model_dict = model_response.json()
        model = ForecastingModel.from_dict(model_dict)
        self._forecasting = ForecastingApi.from_model(model)

        results_response = send_rest_api_request(
            "GET", f"/auto-forecast/{job_id}/results"
        )
        self._result_table = pd.read_csv(StringIO(results_response.text), sep=None)

        if not inplace:
            return self

    def preprocess_time_series(self) -> TimeSeries:
        processed_time_series = self.time_series
        processed_time_series = self._select_columns(processed_time_series)
        processed_time_series = self._run_time_scaling(processed_time_series)
        processed_time_series = self._run_imputation(processed_time_series)

        return processed_time_series

    # def rca(self, configuration: dict[str, Any] = None, inplace: bool = True) -> TimeSeries:
    #     pass

    def _select_columns(self, input_time_series: TimeSeries) -> TimeSeries:
        if self._configuration.columns:
            key_columns = set(
                [input_time_series.timestamp] + input_time_series.group_keys
            )
            columns = [
                column
                for column in self._configuration.columns
                if column not in key_columns
            ]
            columns = (
                [input_time_series.timestamp] + input_time_series.group_keys + columns
            )
            return self._time_series_from_dataframe(
                input_time_series.dataframe[columns]
            )
        else:
            return input_time_series

    def _run_time_scaling(self, input_time_series: TimeSeries) -> TimeSeries:
        if self._configuration.time_scale_configuration is not None:
            scaled_data = TimeScaler().resample(
                input_time_series, self._configuration.time_scale_configuration
            )
            return self._time_series_from_dataframe(scaled_data)
        else:
            return input_time_series

    def _run_imputation(self, input_time_series: TimeSeries) -> TimeSeries:
        if self._configuration.imputation_by_column is not None:
            imputed_data = Imputer().impute(
                input_time_series, self._configuration.imputation_by_column
            )
            return self._time_series_from_dataframe(imputed_data)
        else:
            return input_time_series

    def _time_series_from_dataframe(self, df: pd.DataFrame):
        return TimeSeries(
            df,
            timestamp_column=self.time_series.timestamp,
            group_key_columns=self.time_series.group_keys,
        )
