from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

import isodate
from google.protobuf.duration_pb2 import Duration
from google.protobuf.timestamp_pb2 import Timestamp
from pydantic import BaseModel, Field, model_validator

from senren.custom_exceptions import ProtoConversionError
from senren.entity import Entity, EntityRef
from senren.feature import Feature
from senren.feature_reference import FeatureReference
from senren.feature_store.v1.specs import feature_view_pb2
from senren.logging_config import get_logger
from senren.metadata import CommonMetadata

logger = get_logger(__name__)


class MaterializationConfig(BaseModel):
    """
    Configuration for materializing a feature view.

    Attributes:
        feature_start_time (datetime): Start time from which features should be materialized.
        schedule (timedelta): Schedule for materializing features.
        alerts (List[dict]): List of alerts associated with materialization.
    """

    feature_start_time: datetime = Field(..., description="Start time from which features should be materialized")
    schedule: timedelta = Field(..., description="Schedule for materializing features")
    alerts: List[dict] = Field(
        default_factory=list,
        description="List of alerts associated with materialization",
    )

    def to_proto(self) -> feature_view_pb2.MaterializationConfig:
        """
        Convert the MaterializationConfig to its protobuf representation.

        Returns:
            feature_view_pb2.MaterializationConfig: The protobuf representation of the materialization config.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            timestamp = Timestamp()
            timestamp.FromDatetime(self.feature_start_time)
            schedule_str = isodate.duration_isoformat(self.schedule)

            return feature_view_pb2.MaterializationConfig(
                feature_start_time=timestamp, schedule=schedule_str, alerts=self.alerts
            )
        except Exception as e:
            logger.error(f"Error converting MaterializationConfig to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: feature_view_pb2.MaterializationConfig) -> "MaterializationConfig":
        """
        Create a MaterializationConfig from its protobuf representation.

        Args:
            proto (feature_view_pb2.MaterializationConfig): The protobuf message to convert.

        Returns:
            MaterializationConfig: The created MaterializationConfig object.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return cls(
                feature_start_time=proto.feature_start_time.ToDatetime(),
                schedule=isodate.parse_duration(proto.schedule),
                alerts=list(proto.alerts),
            )
        except Exception as e:
            logger.error(f"Error converting proto to MaterializationConfig: {e}")
            raise ProtoConversionError(proto, "from", str(e))


class FeatureView(BaseModel):
    """
    Represents a feature view in the feature store.

    Attributes:
        metadata (CommonMetadata): Metadata for the feature view.
        entities (List[Union[Entity, EntityRef]]): List of entities associated with this feature view.
        features (List[Feature]): List of features in this feature view.
        materialization (MaterializationConfig): Configuration for materializing this feature view.
        ttl (Optional[timedelta]): Time-to-live for the features in this view.
        feature_dict (Dict[str, FeatureReference]): Dictionary of feature references.
    """

    metadata: CommonMetadata = Field(..., description="Metadata for the feature view")
    entities: List[Union[Entity, EntityRef]] = Field(
        ..., description="List of entities associated with this feature view"
    )
    features: List[Feature] = Field(..., description="List of features in this feature view")
    materialization: MaterializationConfig = Field(..., description="Configuration for materializing this feature view")
    ttl: Optional[timedelta] = Field(None, description="Time-to-live for the features in this view")
    feature_dict: Dict[str, FeatureReference] = Field(
        default_factory=dict, description="Dictionary of feature references"
    )

    def __init__(self, **data):
        super().__init__(**data)
        self.feature_dict = {
            feature.name: FeatureReference.from_feature(feature, self.metadata.namespace, self.metadata.name)
            for feature in self.features
        }

    def __getattr__(self, name):
        if name in self.feature_dict:
            return self.feature_dict[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    # The following comment is to suppress a false positive warning in PyCharm
    # See: https://youtrack.jetbrains.com/issue/PY-34368/
    # noinspection PyNestedDecorators
    @model_validator(mode="before")
    @classmethod
    def convert_entity_to_ref(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if "entities" in values and isinstance(values["entities"], list):
            values["entities"] = [item.to_ref() if isinstance(item, Entity) else item for item in values["entities"]]
        return values

    def to_proto(self) -> feature_view_pb2.FeatureViewSpec:
        """
        Convert the FeatureView to its protobuf representation.

        Returns:
            feature_view_pb2.FeatureViewSpec: The protobuf representation of the feature view.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            proto = feature_view_pb2.FeatureViewSpec(
                metadata=self.metadata.to_proto(),
                entities=[e.to_proto() for e in self.entities],
                features=[f.to_proto() for f in self.features],
                materialization=self.materialization.to_proto(),
            )

            if self.ttl:
                duration = Duration()
                duration.FromTimedelta(self.ttl)
                proto.ttl.CopyFrom(duration)

            return proto
        except Exception as e:
            logger.error(f"Error converting FeatureView to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: feature_view_pb2.FeatureViewSpec) -> "FeatureView":
        """
        Create a FeatureView from its protobuf representation.

        Args:
            proto (feature_view_pb2.FeatureViewSpec): The protobuf message to convert.

        Returns:
            FeatureView: The created FeatureView object.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return cls(
                metadata=CommonMetadata.from_proto(proto.metadata),
                entities=[EntityRef.from_proto(e) for e in proto.entities],
                features=[Feature.from_proto(f) for f in proto.features],
                materialization=MaterializationConfig.from_proto(proto.materialization),
                ttl=proto.ttl.ToTimedelta() if proto.HasField("ttl") else None,
            )
        except Exception as e:
            logger.error(f"Error converting proto to FeatureView: {e}")
            raise ProtoConversionError(proto, "from", str(e))
