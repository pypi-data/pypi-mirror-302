# cnpjData/__init__.py

from .client import CNPJAPIClient, APIException, RateLimitException

__all__ = ["CNPJAPIClient", "APIException", "RateLimitException"]
