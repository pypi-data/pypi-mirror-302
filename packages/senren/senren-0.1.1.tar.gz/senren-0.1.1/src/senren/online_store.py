from enum import Enum

from pydantic import BaseModel, Field

from senren.custom_exceptions import ProtoConversionError
from senren.feature_store.v1.specs import online_store_pb2
from senren.logging_config import get_logger
from senren.metadata import CommonMetadata

logger = get_logger(__name__)


class Cloud(str, Enum):
    """
    Enumeration of supported cloud providers.

    Attributes:
        CLOUD_UNSPECIFIED: Unspecified cloud provider.
        AWS: Amazon Web Services.
        GCP: Google Cloud Platform.
    """

    CLOUD_UNSPECIFIED = "CLOUD_UNSPECIFIED"
    AWS = "AWS"
    GCP = "GCP"

    def to_proto(self) -> int:
        """Convert the Cloud enum to its corresponding protobuf enum value."""
        return online_store_pb2.Cloud.Value(self.name)


class Region(str, Enum):
    """
    Enumeration of supported cloud regions.

    Attributes:
        REGION_UNSPECIFIED: Unspecified region.
        AWS_US_EAST_1: AWS US East (N. Virginia) region.
        AWS_US_WEST_2: AWS US West (Oregon) region.
        AWS_EU_CENTRAL_1: AWS Europe (Frankfurt) region.
        AWS_AP_SOUTHEAST_1: AWS Asia Pacific (Singapore) region.
        GCP_US_CENTRAL1: GCP US Central (Iowa) region.
        GCP_EUROPE_WEST1: GCP Europe West (Belgium) region.
        GCP_ASIA_EAST1: GCP Asia East (Taiwan) region.
    """

    REGION_UNSPECIFIED = "REGION_UNSPECIFIED"
    AWS_US_EAST_1 = "AWS_US_EAST_1"
    AWS_US_WEST_2 = "AWS_US_WEST_2"
    AWS_EU_CENTRAL_1 = "AWS_EU_CENTRAL_1"
    AWS_AP_SOUTHEAST_1 = "AWS_AP_SOUTHEAST_1"
    GCP_US_CENTRAL1 = "GCP_US_CENTRAL1"
    GCP_EUROPE_WEST1 = "GCP_EUROPE_WEST1"
    GCP_ASIA_EAST1 = "GCP_ASIA_EAST1"

    def to_proto(self) -> int:
        """Convert the Region enum to its corresponding protobuf enum value."""
        return online_store_pb2.Region.Value(self.name)


class NodeSize(str, Enum):
    """
    Enumeration of supported node sizes for online stores.

    Attributes:
        NODE_SIZE_UNSPECIFIED: Unspecified node size.
        AWS_T3_MICRO: AWS t3.micro instance type.
        AWS_T3_SMALL: AWS t3.small instance type.
        AWS_T3_MEDIUM: AWS t3.medium instance type.
        GCP_E2_MICRO: GCP e2-micro machine type.
        GCP_E2_SMALL: GCP e2-small machine type.
        GCP_E2_MEDIUM: GCP e2-medium machine type.
    """

    NODE_SIZE_UNSPECIFIED = "NODE_SIZE_UNSPECIFIED"
    AWS_T3_MICRO = "AWS_T3_MICRO"
    AWS_T3_SMALL = "AWS_T3_SMALL"
    AWS_T3_MEDIUM = "AWS_T3_MEDIUM"
    GCP_E2_MICRO = "GCP_E2_MICRO"
    GCP_E2_SMALL = "GCP_E2_SMALL"
    GCP_E2_MEDIUM = "GCP_E2_MEDIUM"

    def to_proto(self) -> int:
        """Convert the NodeSize enum to its corresponding protobuf enum value."""
        return online_store_pb2.NodeSize.Value(self.name)


class OnlineStore(BaseModel):
    """
    Represents an online store in the feature store.

    Attributes:
        metadata (CommonMetadata): Common metadata for the online store.
        cloud (Cloud): Cloud provider for the online store.
        node_size (NodeSize): Size of the nodes in the online store.
        num_nodes (int): Number of nodes in the online store cluster.
        region (Region): Region where the online store is deployed.
    """

    metadata: CommonMetadata = Field(..., description="Common metadata for the online store")
    cloud: Cloud = Field(..., description="Cloud provider for the online store")
    node_size: NodeSize = Field(..., description="Size of the nodes in the online store")
    num_nodes: int = Field(..., description="Number of nodes in the online store cluster")
    region: Region = Field(..., description="Region where the online store is deployed")

    def to_proto(self) -> online_store_pb2.OnlineStoreSpec:
        """
        Convert the OnlineStore object to its corresponding protobuf message.

        Returns:
            online_store_pb2.OnlineStoreSpec: The protobuf representation of the online store.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return online_store_pb2.OnlineStoreSpec(
                metadata=self.metadata.to_proto(),
                cloud=self.cloud.to_proto(),
                node_size=self.node_size.to_proto(),
                num_nodes=self.num_nodes,
                region=self.region.to_proto(),
            )
        except Exception as e:
            logger.error(f"Error converting OnlineStore to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: online_store_pb2.OnlineStoreSpec) -> "OnlineStore":
        """
        Create an OnlineStore object from its corresponding protobuf message.

        Args:
            proto (online_store_pb2.OnlineStoreSpec): The protobuf message to convert.

        Returns:
            OnlineStore: The created OnlineStore object.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return cls(
                metadata=CommonMetadata.from_proto(proto.metadata),
                cloud=Cloud(online_store_pb2.Cloud.Name(proto.cloud)),
                node_size=NodeSize(online_store_pb2.NodeSize.Name(proto.node_size)),
                num_nodes=proto.num_nodes,
                region=Region(online_store_pb2.Region.Name(proto.region)),
            )
        except Exception as e:
            logger.error(f"Error converting proto to OnlineStore: {e}")
            raise ProtoConversionError(proto, "from", str(e))


class OnlineStoreRef(BaseModel):
    """
    Represents a reference to an online store.

    Attributes:
        name (str): The name of the online store.
    """

    name: str = Field(..., description="The name of the online store")

    def to_proto(self) -> online_store_pb2.OnlineStoreRef:
        """
        Convert the OnlineStoreRef object to its corresponding protobuf message.

        Returns:
            online_store_pb2.OnlineStoreRef: The protobuf representation of the online store reference.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return online_store_pb2.OnlineStoreRef(name=self.name)
        except Exception as e:
            logger.error(f"Error converting OnlineStoreRef to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: online_store_pb2.OnlineStoreRef) -> "OnlineStoreRef":
        """
        Create an OnlineStoreRef object from its corresponding protobuf message.

        Args:
            proto (online_store_pb2.OnlineStoreRef): The protobuf message to convert.

        Returns:
            OnlineStoreRef: The created OnlineStoreRef object.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return cls(name=proto.name)
        except Exception as e:
            logger.error(f"Error converting proto to OnlineStoreRef: {e}")
            raise ProtoConversionError(proto, "from", str(e))
