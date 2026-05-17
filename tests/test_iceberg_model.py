from datetime import datetime
from typing import Any, Dict, Type

import pytest

from icedantic.exceptions import IcebergTypeUnknown
from icedantic.model import IcebergBaseModel, IcebergField


class SomeIcebergModel(IcebergBaseModel):
    some_int: int
    some_field: datetime = IcebergField(iceberg_type="timestamp")


class FaultyIcebergModel(IcebergBaseModel):
    some_field: datetime = IcebergField(iceberg_type="pikachu")


@pytest.mark.parametrize(
    ("model_cls", "expected_schema", "attempt_mapping", "throw_on_unknown"),
    [
        (
            SomeIcebergModel,
            {
                "some_int": "integer",
                "some_field": "timestamp",
            },
            True,
            False,
        ),
        (
            FaultyIcebergModel,
            {
                "some_field": "pikachu",
            },
            True,
            False,
        ),
    ],
)
def test_iceberg_model_fields(
    model_cls: Type[IcebergBaseModel],
    expected_schema: Dict[str, Any],
    attempt_mapping: bool,
    throw_on_unknown: bool,
):
    print("throw_on_unknown", throw_on_unknown)
    assert (
        model_cls.model_iceberg_schema(
            attempt_mapping=attempt_mapping, throw_on_unknown=throw_on_unknown
        )
        == expected_schema
    )


@pytest.mark.parametrize(
    ("model_cls", "attempt_mapping", "throw_on_unknown", "expected_exception"),
    [
        (
            FaultyIcebergModel,
            True,
            True,
            IcebergTypeUnknown,
        )
    ],
)
def test_iceberg_model_schema_raises(
    model_cls: Type[IcebergBaseModel],
    attempt_mapping: bool,
    throw_on_unknown: bool,
    expected_exception: Type[Exception],
):
    with pytest.raises(expected_exception):
        model_cls.model_iceberg_schema(
            attempt_mapping=attempt_mapping, throw_on_unknown=throw_on_unknown
        )
