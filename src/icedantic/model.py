from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, get_type_hints
from uuid import UUID

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    SecretBytes,
    SecretStr,
)
from pyiceberg.types import (
    BinaryType,
    BooleanType,
    DateType,
    DecimalType,
    DoubleType,
    IcebergType,
    IntegerType,
    StringType,
    TimestampType,
    UUIDType,
)

_PYDANTIC_ICEBERG_TYPE_MAPPING: dict = {
    int: IntegerType,
    float: DoubleType,
    str: StringType,
    bool: BooleanType,
    bytes: BinaryType,
    datetime: TimestampType,
    date: DateType,
    Decimal: DecimalType,
    UUID: UUIDType,
    HttpUrl: StringType,
    SecretStr: StringType,
    SecretBytes: BinaryType,
    # list: ListType,
    # dict: MapType,
}

_ICEBERG_TYPE_NAME_MAPPING: dict = {
    IntegerType: "integer",
    DoubleType: "double",
    BooleanType: "boolean",
    TimestampType: "timestamp",
    DateType: "date",
    DecimalType: "decimal",
    UUIDType: "uuid",
    StringType: "string",
    BinaryType: "binary",
    # ListType: "map",
    # MapType: "map"
}


def IcebergField(
    *args,
    iceberg_type: IcebergType | None = None,
    **kwargs,
) -> Field:
    if iceberg_type is not None:
        if "json_schema_extra" not in kwargs:
            kwargs["json_schema_extra"] = {}
        kwargs["json_schema_extra"]["iceberg_type"] = iceberg_type

    return Field(*args, **kwargs)


class IcebergBaseModel(BaseModel):
    @classmethod
    def model_iceberg_schema(cls, by_alias: bool = True) -> Dict[str, Any]:
        """Generate the model schema that is compatible with Apache Iceberg.

        Args:
            by_alias (bool, optional): Whether to use aliased field names in the
                schema or not. Defaults to True.
            attempt_mapping (bool, optional): Attempt to map pydantic type to
                iceberg type in case no explicit `iceberg_type` was set.

        Returns:
            Dict[str, Any] The model's Apache Iceberg mapped schema
        """
        schema = {}
        type_hints = get_type_hints(cls)

        for field_name, field_info in cls.model_fields.items():
            field_key = field_name
            if by_alias and field_info.alias is not None:
                field_key = field_info.alias

            # Attempt to get explicit iceberg_type from json_schema_extra
            json_extra_schema = field_info.json_schema_extra or {}
            field_type = json_extra_schema.get("iceberg_type")

            # If no iceberg type was set explicitly,
            # attempt to map it
            if field_type is None:
                field_type = _PYDANTIC_ICEBERG_TYPE_MAPPING.get(
                    type_hints[field_name], None
                )

            # Finally, set type to unknown if all else failed
            field_type = (
                _ICEBERG_TYPE_NAME_MAPPING[field_type]
                if field_type is not None
                else "unknown"
            )

            schema[field_key] = field_type

        return schema
