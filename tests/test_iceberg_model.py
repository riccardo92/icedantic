from datetime import datetime
from typing import Any, Dict, Type

import pytest
from pyiceberg.types import TimestampType

from icedantic.model import IcebergBaseModel, IcebergField


class SomeIcebergModel(IcebergBaseModel):
    some_int: int
    some_field: datetime = IcebergField(iceberg_type=TimestampType)


@pytest.mark.parametrize(
    ("model_cls", "expected_schema"),
    [
        (
            SomeIcebergModel,
            {
                "some_int": "integer",
                "some_field": "timestamp",
            },
        )
    ],
)
def test_iceberg_model_fields(
    model_cls: Type[IcebergBaseModel], expected_schema: Dict[str, Any]
):
    assert model_cls.model_iceberg_schema() == expected_schema
