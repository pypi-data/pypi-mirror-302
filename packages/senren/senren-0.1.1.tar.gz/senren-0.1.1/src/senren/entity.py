from enum import Enum

from pydantic import BaseModel, Field

from senren.custom_exceptions import ProtoConversionError
from senren.feature_store.v1.specs import entity_pb2
from senren.logging_config import get_logger
from senren.metadata import CommonMetadata

logger = get_logger(__name__)


class EntityType(str, Enum):
    """Enumeration of supported entity types."""

    STRING = "STRING"
    INT32 = "INT32"
    INT64 = "INT64"

    def to_proto(self) -> entity_pb2.EntityType:
        """Convert the EntityType enum to its corresponding protobuf enum value."""
        return entity_pb2.EntityType.Value(self.name)


class EntityRef(BaseModel):
    """
    Represents a reference to an entity.

    Attributes:
        name (str): Name of the referenced entity.
    """

    name: str = Field(..., description="Name of the referenced entity")

    def to_proto(self) -> entity_pb2.EntityRef:
        """Convert the EntityRef object to its corresponding protobuf message."""
        try:
            return entity_pb2.EntityRef(name=self.name)
        except Exception as e:
            logger.error(f"Error converting EntityRef to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: entity_pb2.EntityRef) -> "EntityRef":
        """Create an EntityRef object from its corresponding protobuf message."""
        try:
            return cls(name=proto.name)
        except Exception as e:
            logger.error(f"Error converting proto to EntityRef: {e}")
            raise ProtoConversionError(proto, "from", str(e))


class Entity(BaseModel):
    """
    Represents an entity in the feature store.

    Attributes:
        metadata (CommonMetadata): Metadata for the entity.
        join_key (str): The key used to join this entity with other data.
        type (EntityType): The data type of the entity.
    """

    metadata: CommonMetadata = Field(..., description="Metadata for the entity")
    join_key: str = Field(..., description="The key used to join this entity with other data")
    type: EntityType = Field(..., description="The data type of the entity")

    def to_proto(self) -> entity_pb2.EntitySpec:
        """Convert the Entity object to its corresponding protobuf message."""
        try:
            return entity_pb2.EntitySpec(
                metadata=self.metadata.to_proto(),
                join_key=self.join_key,
                type=self.type.to_proto(),
            )
        except Exception as e:
            logger.error(f"Error converting Entity to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: entity_pb2.EntitySpec) -> "Entity":
        """Create an Entity object from its corresponding protobuf message."""
        try:
            return cls(
                metadata=CommonMetadata.from_proto(proto.metadata),
                join_key=proto.join_key,
                type=EntityType(entity_pb2.EntityType.Name(proto.type)),
            )
        except Exception as e:
            logger.error(f"Error converting proto to Entity: {e}")
            raise ProtoConversionError(proto, "from", str(e))

    def to_ref(self) -> EntityRef:
        """Convert the Entity to an EntityRef."""
        return EntityRef(name=f"{self.metadata.namespace}::{self.metadata.name}")
