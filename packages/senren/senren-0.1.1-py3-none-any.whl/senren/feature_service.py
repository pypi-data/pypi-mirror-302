from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, model_validator

from senren.custom_exceptions import ProtoConversionError
from senren.feature_reference import FeatureReference
from senren.feature_store.v1.specs import alerts_pb2, feature_service_pb2
from senren.feature_view import FeatureView
from senren.logging_config import get_logger
from senren.metadata import CommonMetadata
from senren.online_store import OnlineStore, OnlineStoreRef

logger = get_logger(__name__)


class Destination(BaseModel):
    """
    Represents a destination for feature data in a routing configuration.

    Attributes:
        online_store (Union[OnlineStore, OnlineStoreRef, str]): Reference to the online store.
        share (float): The share of traffic routed to this destination.
    """

    online_store: Union[OnlineStore, OnlineStoreRef, str] = Field(..., description="Reference to the online store")
    share: float = Field(..., description="The share of traffic routed to this destination")

    # The following comment is to suppress a false positive warning in PyCharm
    # See: https://youtrack.jetbrains.com/issue/PY-34368/
    # noinspection PyNestedDecorators
    @model_validator(mode="before")
    @classmethod
    def convert_online_store_to_ref(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Convert OnlineStore objects to OnlineStoreRef objects."""
        if "online_store" in values:
            v = values["online_store"]
            if isinstance(v, OnlineStore):
                values["online_store"] = OnlineStoreRef(name=v.metadata.name)
            elif isinstance(v, str):
                values["online_store"] = OnlineStoreRef(name=v)
        return values

    def to_proto(self) -> feature_service_pb2.Destination:
        """
        Convert the Destination object to its corresponding protobuf message.

        Returns:
            feature_service_pb2.Destination: The protobuf representation of the destination.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            if isinstance(self.online_store, str):
                online_store_proto = OnlineStoreRef(name=self.online_store).to_proto()
            else:
                online_store_proto = self.online_store.to_proto()
            return feature_service_pb2.Destination(online_store=online_store_proto, share=self.share)
        except Exception as e:
            logger.error(f"Error converting Destination to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: feature_service_pb2.Destination) -> "Destination":
        """
        Create a Destination object from its corresponding protobuf message.

        Args:
            proto (feature_service_pb2.Destination): The protobuf message to convert.

        Returns:
            Destination: The created Destination object.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return cls(
                online_store=OnlineStoreRef.from_proto(proto.online_store),
                share=proto.share,
            )
        except Exception as e:
            logger.error(f"Error converting proto to Destination: {e}")
            raise ProtoConversionError(proto, "from", str(e))


class RoutingConfig(BaseModel):
    """
    Represents the routing configuration for a feature service.

    Attributes:
        destinations (List[Destination]): List of destinations for feature data.
    """

    destinations: List[Destination] = Field(..., description="List of destinations for feature data")

    def to_proto(self) -> feature_service_pb2.RoutingConfig:
        """
        Convert the RoutingConfig object to its corresponding protobuf message.

        Returns:
            feature_service_pb2.RoutingConfig: The protobuf representation of the routing config.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return feature_service_pb2.RoutingConfig(destinations=[d.to_proto() for d in self.destinations])
        except Exception as e:
            logger.error(f"Error converting RoutingConfig to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: feature_service_pb2.RoutingConfig) -> "RoutingConfig":
        """
        Create a RoutingConfig object from its corresponding protobuf message.

        Args:
            proto (feature_service_pb2.RoutingConfig): The protobuf message to convert.

        Returns:
            RoutingConfig: The created RoutingConfig object.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return cls(destinations=[Destination.from_proto(d) for d in proto.destinations])
        except Exception as e:
            logger.error(f"Error converting proto to RoutingConfig: {e}")
            raise ProtoConversionError(proto, "from", str(e))


class DeploymentConfig(BaseModel):
    """
    Represents the deployment configuration for a feature service.

    Attributes:
        partition_values (List[str]): List of partition values for the deployment.
        routing (RoutingConfig): Routing configuration for the deployment.
    """

    partition_values: List[str] = Field(..., description="List of partition values for the deployment")
    routing: RoutingConfig = Field(..., description="Routing configuration for the deployment")

    def to_proto(self) -> feature_service_pb2.DeploymentConfig:
        """
        Convert the DeploymentConfig object to its corresponding protobuf message.

        Returns:
            feature_service_pb2.DeploymentConfig: The protobuf representation of the deployment config.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return feature_service_pb2.DeploymentConfig(
                partition_values=self.partition_values, routing=self.routing.to_proto()
            )
        except Exception as e:
            logger.error(f"Error converting DeploymentConfig to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: feature_service_pb2.DeploymentConfig) -> "DeploymentConfig":
        """
        Create a DeploymentConfig object from its corresponding protobuf message.

        Args:
            proto (feature_service_pb2.DeploymentConfig): The protobuf message to convert.

        Returns:
            DeploymentConfig: The created DeploymentConfig object.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return cls(
                partition_values=list(proto.partition_values),
                routing=RoutingConfig.from_proto(proto.routing),
            )
        except Exception as e:
            logger.error(f"Error converting proto to DeploymentConfig: {e}")
            raise ProtoConversionError(proto, "from", str(e))


class Alert(BaseModel):
    """
    Represents an alert in the feature service.

    Attributes:
        name (str): Name of the alert.
        description (Optional[str]): Description of the alert.
    """

    name: str = Field(..., description="Name of the alert")
    description: Optional[str] = Field(None, description="Description of the alert")

    def to_proto(self) -> alerts_pb2.Alert:
        """
        Convert the Alert object to its corresponding protobuf message.

        Returns:
            alerts_pb2.Alert: The protobuf representation of the alert.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return alerts_pb2.Alert(name=self.name, description=self.description)
        except Exception as e:
            logger.error(f"Error converting Alert to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: alerts_pb2.Alert) -> "Alert":
        """
        Create an Alert object from its corresponding protobuf message.

        Args:
            proto (alerts_pb2.Alert): The protobuf message to convert.

        Returns:
            Alert: The created Alert object.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return cls(name=proto.name, description=proto.description)
        except Exception as e:
            logger.error(f"Error converting proto to Alert: {e}")
            raise ProtoConversionError(proto, "from", str(e))


class FeatureService(BaseModel):
    """
    Represents a feature service in the feature store.

    Attributes:
        metadata (CommonMetadata): Metadata for the feature service.
        features (List[Union[FeatureReference, FeatureView]]): List of features or feature views included in the service
        deployment (Dict[str, DeploymentConfig]): Deployment configuration for different regions.
        alerts (List[Alert]): List of alerts associated with the feature service.
    """

    metadata: CommonMetadata = Field(..., description="Metadata for the feature service")
    features: List[Union[FeatureReference, FeatureView]] = Field(
        ..., description="List of features or feature views included in the service"
    )
    deployment: Dict[str, DeploymentConfig] = Field(..., description="Deployment configuration for different regions")
    alerts: List[Alert] = Field(default_factory=list, description="List of alerts associated with the feature service")

    # The following comment is to suppress a false positive warning in PyCharm
    # See: https://youtrack.jetbrains.com/issue/PY-34368/
    # noinspection PyNestedDecorators
    @model_validator(mode="before")
    @classmethod
    def validate_features(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if "features" in values:
            features = values["features"]
            validated_features = []
            for feature in features:
                if isinstance(feature, FeatureReference):
                    validated_features.append(feature)
                elif isinstance(feature, FeatureView):
                    validated_features.extend(
                        [
                            FeatureReference(
                                namespace=feature.metadata.namespace, feature_view=feature.metadata.name, name=f.name
                            )
                            for f in feature.features
                        ]
                    )
                else:
                    raise ValueError(f"Invalid feature type: {type(feature)}. Must be FeatureReference or FeatureView.")
            values["features"] = validated_features
        return values

    def to_proto(self) -> feature_service_pb2.FeatureServiceSpec:
        """
        Convert the FeatureService object to its corresponding protobuf message.

        Returns:
            feature_service_pb2.FeatureServiceSpec: The protobuf representation of the feature service.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return feature_service_pb2.FeatureServiceSpec(
                metadata=self.metadata.to_proto(),
                features=[
                    f.to_proto() for f in self.features
                ],  # self.features is now always a list of FeatureReference
                deployment={k: v.to_proto() for k, v in self.deployment.items()},
                alerts=[alert.to_proto() for alert in self.alerts],
            )
        except Exception as e:
            logger.error(f"Error converting FeatureService to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: feature_service_pb2.FeatureServiceSpec) -> "FeatureService":
        """
        Create a FeatureService object from its corresponding protobuf message.

        Args:
            proto (feature_service_pb2.FeatureServiceSpec): The protobuf message to convert.

        Returns:
            FeatureService: The created FeatureService object.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return cls(
                metadata=CommonMetadata.from_proto(proto.metadata),
                features=[FeatureReference.from_proto(f) for f in proto.features],
                deployment={k: DeploymentConfig.from_proto(v) for k, v in proto.deployment.items()},
                alerts=[Alert.from_proto(alert) for alert in proto.alerts],
            )
        except Exception as e:
            logger.error(f"Error converting proto to FeatureService: {e}")
            raise ProtoConversionError(proto, "from", str(e))
