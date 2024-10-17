import pymongo

from modelhub_server.config import get_config

_mongo_db = None


def get_mongo_db():
    global _mongo_db
    if _mongo_db is None:
        config = get_config()
        mongo_client = pymongo.MongoClient(config.db.mongo_url)
        _mongo_db = mongo_client[config.db.mongo_db]
    return _mongo_db
