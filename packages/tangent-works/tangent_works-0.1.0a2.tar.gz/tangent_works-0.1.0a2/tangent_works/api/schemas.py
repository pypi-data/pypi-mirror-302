import os
import json
from jsonschema import validate, ValidationError
from tangent_works.utils.exceptions import TangentValidationError


def _load_schema():
    project_path = os.getenv("PROJECT_SRC_PATH")
    schema_path = os.path.join(project_path, "tangent_works", "api", "schemas.json") if project_path is not None else "tangent_works/api/schemas.json"

    with open(schema_path, "r") as file:
        schema = json.load(file)
    return schema


def _add_defintions_to_schema(sub_schema):
    sub_schema['definitions'] = _schema.copy()


def _get_schema_for_endpoint(schema_name):
    sub_schema = _schema[schema_name].copy()
    _add_defintions_to_schema(sub_schema)
    return sub_schema


def validate_schema(instance, schema):
    try:
        validate(instance=instance, schema=schema)
    except ValidationError as err:
        raise TangentValidationError(err.message) from err


_schema = _load_schema()

imputation_schema = _get_schema_for_endpoint('ImputeConfiguration')
time_scale_schema = _get_schema_for_endpoint('TimeScaleConfiguration')
forecasting_build_model_schema = _get_schema_for_endpoint('BuildConfiguration')
forecasting_build_normal_behavior_model_schema = _get_schema_for_endpoint('BuildNormalBehaviorConfiguration')
forecasting_predict_schema = _get_schema_for_endpoint('PredictConfiguration')
forecasting_rca_schema = _get_schema_for_endpoint('RCAConfiguration')
auto_forecasting_schema = _get_schema_for_endpoint('AutoForecastingConfiguration')
anomaly_detection_build_model_schema = _get_schema_for_endpoint('BuildAnomalyDetectionConfiguration')

_schema.clear()
