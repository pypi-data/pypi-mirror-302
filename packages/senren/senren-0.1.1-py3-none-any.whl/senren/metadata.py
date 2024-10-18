from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from senren.custom_exceptions import ProtoConversionError
from senren.feature_store.v1.specs import metadata_pb2


class CommonMetadata(BaseModel):
    """
    Represents common metadata for Senren objects.

    Attributes:
        namespace (str): The namespace of the object.
        name (str): The name of the object.
        description (Optional[str]): An optional description of the object.
        owners (List[str]): A list of owners for the object.
        tags (Dict[str, str]): A dictionary of tags associated with the object.
    """

    namespace: str
    name: str
    description: Optional[str] = None
    owners: List[str] = Field(default_factory=list)
    tags: Dict[str, str] = Field(default_factory=dict)

    def to_proto(self) -> metadata_pb2.CommonMetadata:
        """
        Convert the CommonMetadata object to its corresponding protobuf message.

        Returns:
            metadata_pb2.CommonMetadata: The protobuf representation of the metadata.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return metadata_pb2.CommonMetadata(
                namespace=self.namespace,
                name=self.name,
                description=self.description,
                owners=self.owners,
                tags=self.tags,
            )
        except Exception as e:
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: metadata_pb2.CommonMetadata) -> "CommonMetadata":
        """
        Create a CommonMetadata object from its corresponding protobuf message.

        Args:
            proto (metadata_pb2.CommonMetadata): The protobuf message to convert.

        Returns:
            CommonMetadata: The created CommonMetadata object.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return cls(
                namespace=proto.namespace,
                name=proto.name,
                description=proto.description,
                owners=list(proto.owners),
                tags=dict(proto.tags),
            )
        except Exception as e:
            raise ProtoConversionError(proto, "from", str(e))
