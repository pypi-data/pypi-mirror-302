from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from senren.custom_exceptions import ProtoConversionError
from senren.feature_store.v1.specs import data_source_pb2
from senren.logging_config import get_logger
from senren.metadata import CommonMetadata

logger = get_logger(__name__)


class FileFormat(str, Enum):
    """
    Enumeration of supported file formats for data sources.

    Attributes:
        PARQUET: Apache Parquet file format.
        CSV: Comma-Separated Values file format.
        JSON: JavaScript Object Notation file format.
    """

    PARQUET = "PARQUET"
    CSV = "CSV"
    JSON = "JSON"

    def to_proto(self) -> int:
        """Convert the FileFormat enum to its corresponding protobuf enum value."""
        return data_source_pb2.FileFormat.Value(self.name)


class S3File(BaseModel):
    """
    Represents a file stored in Amazon S3.

    Attributes:
        bucket (str): The name of the S3 bucket containing the file.
        key (str): The object key (path) of the file within the S3 bucket.
    """

    bucket: str = Field(..., description="The name of the S3 bucket containing the file")
    key: str = Field(..., description="The object key (path) of the file within the S3 bucket")

    def to_proto(self) -> data_source_pb2.S3File:
        """
        Convert the S3File object to its corresponding protobuf message.

        Returns:
            data_source_pb2.S3File: The protobuf representation of the S3 file.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return data_source_pb2.S3File(bucket=self.bucket, key=self.key)
        except Exception as e:
            logger.error(f"Error converting S3File to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: data_source_pb2.S3File) -> "S3File":
        """
        Create an S3File object from its corresponding protobuf message.

        Args:
            proto (data_source_pb2.S3File): The protobuf message to convert.

        Returns:
            S3File: The created S3File object.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return cls(bucket=proto.bucket, key=proto.key)
        except Exception as e:
            logger.error(f"Error converting proto to S3File: {e}")
            raise ProtoConversionError(proto, "from", str(e))


class FileBatchConfig(BaseModel):
    """
    Configuration for a batch data source using a file.

    Attributes:
        file (S3File): The S3 file containing the batch data.
        file_format (FileFormat): The format of the file (e.g., PARQUET, CSV, JSON).
        timestamp_column (str): The name of the column containing timestamp information.
        region_partitioning_column (Optional[str]): The name of the column used for region-based partitioning, if any.
    """

    file: S3File = Field(..., description="The S3 file containing the batch data")
    file_format: FileFormat = Field(..., description="The format of the file (e.g., PARQUET, CSV, JSON)")
    timestamp_column: str = Field(..., description="The name of the column containing timestamp information")
    region_partitioning_column: Optional[str] = Field(
        None,
        description="The name of the column used for region-based partitioning, if any",
    )

    def to_proto(self) -> data_source_pb2.FileBatchConfig:
        """
        Convert the FileBatchConfig object to its corresponding protobuf message.

        Returns:
            data_source_pb2.FileBatchConfig: The protobuf representation of the file batch configuration.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return data_source_pb2.FileBatchConfig(
                file=self.file.to_proto(),
                file_format=self.file_format.to_proto(),
                timestamp_column=self.timestamp_column,
                region_partitioning_column=self.region_partitioning_column,
            )
        except Exception as e:
            logger.error(f"Error converting FileBatchConfig to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: data_source_pb2.FileBatchConfig) -> "FileBatchConfig":
        """
        Create a FileBatchConfig object from its corresponding protobuf message.

        Args:
            proto (data_source_pb2.FileBatchConfig): The protobuf message to convert.

        Returns:
            FileBatchConfig: The created FileBatchConfig object.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return cls(
                file=S3File.from_proto(proto.file),
                file_format=FileFormat(data_source_pb2.FileFormat.Name(proto.file_format)),
                timestamp_column=proto.timestamp_column,
                region_partitioning_column=proto.region_partitioning_column,
            )
        except Exception as e:
            logger.error(f"Error converting proto to FileBatchConfig: {e}")
            raise ProtoConversionError(proto, "from", str(e))


class DataSource(BaseModel):
    """
    Represents a data source in the feature store.

    Attributes:
        metadata (CommonMetadata): Common metadata for the data source.
        source_config (FileBatchConfig): Configuration for the batch file data source.
    """

    metadata: CommonMetadata = Field(..., description="Common metadata for the data source")
    source_config: FileBatchConfig = Field(..., description="Configuration for the batch file data source")

    def to_proto(self) -> data_source_pb2.DataSourceSpec:
        """
        Convert the DataSource object to its corresponding protobuf message.

        Returns:
            data_source_pb2.DataSourceSpec: The protobuf representation of the data source.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return data_source_pb2.DataSourceSpec(
                metadata=self.metadata.to_proto(),
                source_config=self.source_config.to_proto(),
            )
        except Exception as e:
            logger.error(f"Error converting DataSource to proto: {e}")
            raise ProtoConversionError(self, "to", str(e))

    @classmethod
    def from_proto(cls, proto: data_source_pb2.DataSourceSpec) -> "DataSource":
        """
        Create a DataSource object from its corresponding protobuf message.

        Args:
            proto (data_source_pb2.DataSourceSpec): The protobuf message to convert.

        Returns:
            DataSource: The created DataSource object.

        Raises:
            ProtoConversionError: If there's an error during the conversion process.
        """
        try:
            return cls(
                metadata=CommonMetadata.from_proto(proto.metadata),
                source_config=FileBatchConfig.from_proto(proto.source_config),
            )
        except Exception as e:
            logger.error(f"Error converting proto to DataSource: {e}")
            raise ProtoConversionError(proto, "from", str(e))
