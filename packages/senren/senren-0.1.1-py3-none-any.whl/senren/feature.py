from enum import Enum

from pydantic import BaseModel, Field

from senren.custom_exceptions import ProtoConversionError
from senren.feature_store.v1.specs import feature_pb2
from senren.logging_config import get_logger

logger = get_logger(__name__)


class FeatureType(str, Enum):
    """Enumeration of supported feature types."""

    BOOL = "BOOL"
    INT32 = "INT32"
    INT64 = "INT64"
    FLOAT = "FLOAT"
    DOUBLE = "DOUBLE"
    STRING = "STRING"
    TIMESTAMP = "TIMESTAMP"
    LIST_BOOL = "LIST_BOOL"
    LIST_BYTE = "LIST_BYTE"
    LIST_INT32 = "LIST_INT32"
    LIST_INT64 = "LIST_INT64"
    LIST_FLOAT = "LIST_FLOAT"
    LIST_DOUBLE = "LIST_DOUBLE"
    LIST_STRING = "LIST_STRING"


class Feature(BaseModel):
    """
    Represents a feature in the feature store.

    Attributes:
        name (str): The name of the feature.
        type (FeatureType): The data type of the feature.
    """

    name: str = Field(..., description="The name of the feature")
    type: FeatureType = Field(..., description="The data type of the feature")

    def to_proto(self) -> feature_pb2.FeatureSpec:
        """Convert the Feature object to its corresponding protobuf message."""
        try:
            return feature_pb2.FeatureSpec(name=self.name, type=feature_pb2.FeatureType.Value(self.type.value))
        except Exception as e:
            logger.error(f"Error converting Feature to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: feature_pb2.FeatureSpec) -> "Feature":
        """Create a Feature object from its corresponding protobuf message."""
        try:
            return cls(
                name=proto.name,
                type=FeatureType(feature_pb2.FeatureType.Name(proto.type)),
            )
        except Exception as e:
            logger.error(f"Error converting proto to Feature: {e}")
            raise ProtoConversionError(proto, "from", str(e))
