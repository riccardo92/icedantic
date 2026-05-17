from datetime import date, datetime
from decimal import Decimal
from typing import Any, Dict, get_type_hints
from uuid import UUID

from loguru import logger
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

from icedantic.exceptions import IcebergTypeUnknown

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


_ICEBERG_NAME_TYPE_MAPPING = {v: k for k, v in _ICEBERG_TYPE_NAME_MAPPING.items()}


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
    def model_iceberg_schema(
        cls,
        by_alias: bool = True,
        throw_on_unknown: bool = False,
        attempt_mapping: bool = True,
    ) -> Dict[str, Any]:
        """Generate the model schema that is compatible with Apache Iceberg.

        Args:
            by_alias (bool, optional): Whether to use aliased field names in the
                schema or not. Defaults to True.
            throw_on_unknown (bool, optional): Throw an exception if the specified
                `iceberg_type` isn't known to icedantic. Defaults to False.
            attempt_mapping (bool, optional): Attempt to map pydantic type to
                iceberg type in case no explicit `iceberg_type` was set or
                the `iceberg_type` was invalid. Defaults to True.

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
            field_type = json_extra_schema.get("iceberg_type", None)

            if field_type is not None:
                try:
                    _ICEBERG_NAME_TYPE_MAPPING[field_type]
                except KeyError:
                    logger.warning(
                        "`iceberg_type` was set but was not set to a icedantic-known type."
                    )

                    if throw_on_unknown:
                        raise IcebergTypeUnknown(
                            f"The iceberg type '{field_type}' is not known to icedantic. Throwing since `throw_on_unknown` was set to True."
                        )

            # If no iceberg type was set explicitly,
            # attempt to map it
            if field_type is None and attempt_mapping:
                logger.warning(
                    f"No `iceberg_type` set for field {field_name}. Attempting native mapping."
                )
                field_type = _ICEBERG_TYPE_NAME_MAPPING.get(
                    _PYDANTIC_ICEBERG_TYPE_MAPPING.get(type_hints[field_name], None),
                    None,
                )

            # Finally, set type to unknown if all else failed
            if field_type is None:
                if attempt_mapping:
                    logger.warning(
                        "A native mapping from pydantic to iceberg could not be made. Type will be set to 'unknown'."
                    )
                field_type = "unknown"

            schema[field_key] = field_type

        return schema
