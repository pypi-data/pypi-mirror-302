from typing import ClassVar

from pydantic import BaseModel, Field

from senren.custom_exceptions import ProtoConversionError
from senren.feature import Feature
from senren.feature_store.v1.specs import feature_pb2
from senren.logging_config import get_logger

logger = get_logger(__name__)


class FeatureReference(BaseModel):
    """
    Represents a reference to a feature in a feature view.

    This class is used to uniquely identify a feature within the feature store,
    including its namespace, feature view, and name.

    Attributes:
        namespace (str): The namespace of the feature view.
        feature_view (str): The name of the feature view.
        name (str): The name of the feature.
    """

    namespace: str = Field(..., description="The namespace of the feature view")
    feature_view: str = Field(..., description="The name of the feature view")
    name: str = Field(..., description="The name of the feature")

    # Class variable to store the separator used in the string representation
    SEPARATOR: ClassVar[str] = "::"

    def to_proto(self) -> feature_pb2.FeatureReference:
        """
        Convert the FeatureReference object to its corresponding protobuf message.

        Returns:
            feature_pb2.FeatureReference: The protobuf representation of the feature reference.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return feature_pb2.FeatureReference(
                namespace=self.namespace, feature_view=self.feature_view, name=self.name
            )
        except Exception as e:
            logger.error(f"Error converting FeatureReference to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: feature_pb2.FeatureReference) -> "FeatureReference":
        """
        Create a FeatureReference object from its corresponding protobuf message.

        Args:
            proto (feature_pb2.FeatureReference): The protobuf message to convert.

        Returns:
            FeatureReference: The created FeatureReference object.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return cls(
                namespace=proto.namespace,
                feature_view=proto.feature_view,
                name=proto.name,
            )
        except Exception as e:
            logger.error(f"Error converting proto to FeatureReference: {e}")
            raise ProtoConversionError(proto, "from", str(e))

    @classmethod
    def from_feature(cls, feature: Feature, namespace: str, feature_view: str) -> "FeatureReference":
        """
        Create a FeatureReference from a Feature object and additional context.

        Args:
            feature (Feature): The Feature object to reference.
            namespace (str): The namespace of the feature view.
            feature_view (str): The name of the feature view.

        Returns:
            FeatureReference: A new FeatureReference object.
        """
        return cls(namespace=namespace, feature_view=feature_view, name=feature.name)

    def __str__(self) -> str:
        """
        Return a string representation of the FeatureReference.

        Returns:
            str: A string in the format "namespace::feature_view::name".
        """
        return f"{self.namespace}{self.SEPARATOR}{self.feature_view}{self.SEPARATOR}{self.name}"

    @classmethod
    def from_string(cls, reference_string: str) -> "FeatureReference":
        """
        Create a FeatureReference object from its string representation.

        Args:
            reference_string (str): A string in the format "namespace::feature_view::name".

        Returns:
            FeatureReference: The created FeatureReference object.

        Raises:
            ValueError: If the input string is not in the correct format.
        """
        parts = reference_string.split(cls.SEPARATOR)
        if len(parts) != 3:
            raise ValueError(f"Invalid feature reference string: {reference_string}")
        return cls(namespace=parts[0], feature_view=parts[1], name=parts[2])
