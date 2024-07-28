import urllib3
import asyncio
import inspect
import functools
from typing import Any, Self, Callable

from minio import Minio

from core.logging.helpers import create_logger
from core.settings import config

logger = create_logger("minio")


class __AsyncMinio(Minio):
    def build(self) -> Self:
        class a:
            def __init__(self_) -> None:
                for name, method in inspect.getmembers(
                    self, predicate=inspect.ismethod
                ):
                    if name.startswith("_"):
                        continue
                    
                    setattr(self_, name, self_.__make_async(method))

            @staticmethod
            def __make_async(func: Callable[..., Any]) -> Callable[..., Any]:
                async def async_func(*args, **kwargs):
                    loop = asyncio.get_event_loop()
                    pfunc = functools.partial(func, *args, **kwargs)
                    return await loop.run_in_executor(None, pfunc)
                return async_func
            
            make_bucket = self.make_bucket
            list_buckets = self.list_buckets
            bucket_exists = self.bucket_exists
            remove_bucket = self.remove_bucket
            fput_object = self.fput_object
            fget_object = self.fget_object
            put_object = self.put_object
            get_object = self.get_object
            stat_object = self.stat_object
            remove_object = self.remove_object
            list_objects = self.list_objects
            copy_object = self.copy_object
            presigned_get_object= self.presigned_get_object
            presigned_put_object= self.presigned_put_object
            presigned_post_policy= self.presigned_post_policy

        self.a = a()
        return self


__http_client = urllib3.PoolManager(
    timeout=urllib3.Timeout(connect=2.0, read=5.0),
    retries=urllib3.Retry(
        total=5,
        backoff_factor=0.2,
        status_forcelist=[500, 502, 503, 504]
    )
)

client = __AsyncMinio(
    endpoint=config.MINIO_URL,
    access_key=config.MINIO_ROOT_USER,
    secret_key=config.MINIO_ROOT_PASSWORD.get_secret_value(),
    secure=False,
    http_client=__http_client
).build()


async def test_storage_connection():
    buckets_len = len(await client.a.list_buckets())
    return f"MinIO buckets length: {buckets_len}"
