from typing import Dict

from pydantic import BaseModel, Field

from senren.custom_exceptions import ProtoConversionError
from senren.data_source import DataSource
from senren.entity import Entity
from senren.feature_service import FeatureService
from senren.feature_view import FeatureView
from senren.logging_config import get_logger
from senren.online_store import OnlineStore

logger = get_logger(__name__)


class RepoSpec(BaseModel):
    """
    Represents the complete specification of a feature store repository.

    Attributes:
        entities (Dict[str, Entity]): Dictionary of entities in the repository.
        data_sources (Dict[str, DataSource]): Dictionary of data sources in the repository.
        feature_views (Dict[str, FeatureView]): Dictionary of feature views in the repository.
        feature_services (Dict[str, FeatureService]): Dictionary of feature services in the repository.
        online_stores (Dict[str, OnlineStore]): Dictionary of online stores in the repository.
    """

    entities: Dict[str, Entity] = Field(..., description="Dictionary of entities in the repository")
    data_sources: Dict[str, DataSource] = Field(..., description="Dictionary of data sources in the repository")
    feature_views: Dict[str, FeatureView] = Field(..., description="Dictionary of feature views in the repository")
    feature_services: Dict[str, FeatureService] = Field(
        ..., description="Dictionary of feature services in the repository"
    )
    online_stores: Dict[str, OnlineStore] = Field(..., description="Dictionary of online stores in the repository")

    def to_proto(self):
        """
        Convert the RepoSpec object to its corresponding protobuf message.

        Returns:
            repo_pb2.RepoSpec: The protobuf representation of the repository specification.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            from senren.feature_store.v1.specs import repo_pb2

            return repo_pb2.RepoSpec(
                entities={k: v.to_proto() for k, v in self.entities.items()},
                data_sources={k: v.to_proto() for k, v in self.data_sources.items()},
                feature_views={k: v.to_proto() for k, v in self.feature_views.items()},
                feature_services={k: v.to_proto() for k, v in self.feature_services.items()},
                online_stores={k: v.to_proto() for k, v in self.online_stores.items()},
            )
        except Exception as e:
            logger.error(f"Error converting RepoSpec to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto):
        """
        Create a RepoSpec object from its corresponding protobuf message.

        Args:
            proto (repo_pb2.RepoSpec): The protobuf message to convert.

        Returns:
            RepoSpec: The created RepoSpec object.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return cls(
                entities={k: Entity.from_proto(v) for k, v in proto.entities.items()},
                data_sources={k: DataSource.from_proto(v) for k, v in proto.data_sources.items()},
                feature_views={k: FeatureView.from_proto(v) for k, v in proto.feature_views.items()},
                feature_services={k: FeatureService.from_proto(v) for k, v in proto.feature_services.items()},
                online_stores={k: OnlineStore.from_proto(v) for k, v in proto.online_stores.items()},
            )
        except Exception as e:
            logger.error(f"Error converting proto to RepoSpec: {e}")
            raise ProtoConversionError(proto, "from", str(e))
