from motor.motor_asyncio import AsyncIOMotorClient
from pg_common import SingletonBase, RuntimeException
from pg_environment import config
from pg_mongodb.define import *



__all__ = ("MongoManager", )

class _MongoManager(SingletonBase):

    def __init__(self):
        self._mongo_client = {}
        _cfg_mongodb = config.get_conf(KEY_MONGODB)
        for _k, _v in _cfg_mongodb.items():
            self._mongo_client[_k] = AsyncIOMotorClient(_v[KEY_MONGODB_URI])

    def get_mongodb(self, svr_name=KEY_MONGODB_DEFAULT_KEY):
        if svr_name in self._mongo_client:
            return self._mongo_client[svr_name]
        elif KEY_MONGODB_DEFAULT_KEY in self._mongo_client:
            return self._mongo_client[KEY_MONGODB_DEFAULT_KEY]
        else:
            raise RuntimeException("getMongodbClient", f"Can't find mongodb config for {svr_name}")


MongoManager = _MongoManager()