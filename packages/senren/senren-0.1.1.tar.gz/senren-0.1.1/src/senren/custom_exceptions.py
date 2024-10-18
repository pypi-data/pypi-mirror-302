from typing import Any


class SenrenException(Exception):
    """Base exception for all Senren-related errors."""


class ValidationError(SenrenException):
    """Raised when data validation fails."""


class ConfigurationError(SenrenException):
    """Raised when there's an issue with configuration."""


class RegistryError(SenrenException):
    """Raised when there's an error communicating with the registry service."""


class DataSourceError(SenrenException):
    """Raised when there's an issue with a data source."""


class FeatureViewError(SenrenException):
    """Raised when there's an issue with a feature view."""


class FeatureServiceError(SenrenException):
    """Raised when there's an issue with a feature service."""


class OnlineStoreError(SenrenException):
    """Raised when there's an issue with an online store."""


class ProtoConversionError(SenrenException):
    """Raised when there's an error converting to or from protobuf."""

    def __init__(self, obj: Any, direction: str, *args: object) -> None:
        super().__init__(*args)
        self.obj = obj
        self.direction = direction

    def __str__(self) -> str:
        return f"Error converting {self.obj.__class__.__name__} {self.direction} protobuf"
