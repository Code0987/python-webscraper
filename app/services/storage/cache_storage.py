from redis import from_url
from typing import Any, Dict, Optional
from config import settings

from . import Storage


class CacheStorage(Storage):
    '''
    This class is used to store data in Redis, in the form of JSON strings.
    It provides methods to put, get, delete, and clear data from Redis.
    '''

    def __init__(self):
        self.redis_client = from_url(settings.REDIS_URL)

    def put(self, key: str, data: Any) -> None:
        self.redis_client.set(key, data)

    def get(self, key: str) -> Optional[Any]:
        return self.redis_client.get(key)

    def clear(self) -> None:
        # TODO: Implement
        pass
