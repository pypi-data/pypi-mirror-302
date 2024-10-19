"""Init file for the Layer SDK."""

from .auth import AuthProvider, OIDCClientCredentials
from .client import Client
from .schemas import SessionActionKind
from .exceptions import (
    LayerAuthError,
    LayerHTTPError,
    LayerRequestError,
    LayerSDKException,
    LayerAlreadyInitializedError,
    LayerRequestPreparationError,
    LayerMissingRequiredConfigurationError,
)

layer = Client()

__all__ = [
    "layer",
    "AuthProvider",
    "SessionActionKind",
    "OIDCClientCredentials",
    "LayerAuthError",
    "LayerHTTPError",
    "LayerSDKException",
    "LayerMissingRequiredConfigurationError",
    "LayerAlreadyInitializedError",
    "LayerRequestPreparationError",
    "LayerRequestError",
]
