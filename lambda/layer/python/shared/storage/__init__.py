"""Storage abstraction layer for data persistence"""
from .base import StorageBackend
from .dynamodb import DynamoDBBackend

__all__ = ['StorageBackend', 'DynamoDBBackend']
