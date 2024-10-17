from fastapi import Request

from modelhub_server.types.auth import AuthParams
from modelhub_server.config import get_config
from modelhub_server.lib.db import get_mongo_db
from modelhub_server.lib.utils import hash_password
from loguru import logger


def get_auth_params(request: Request):
    """Get auth params"""
    auth = request.headers.get("Authorization") or request.headers.get("authorization")
    if not auth:
        return None
    if auth.startswith("Bearer "):
        auth = auth[len("Bearer ") :]
    if len(auth.split(":", 1)) != 2:
        return AuthParams(user_name=auth, user_password="")
    user_name, user_password = auth.split(":", 1)
    return AuthParams(user_name=user_name, user_password=user_password)


def check_user_auth(params: AuthParams | None):
    """Check user authentication"""
    if not get_config().app.check_auth:
        return True
    if not params:
        return False
    try:
        users_collection = get_mongo_db()[get_config().db.users_collection]
        hashed_password = hash_password(params.user_password)
        user = users_collection.find_one({"_id": params.user_name})
        if not user:
            return False
        return user["password"] == hashed_password
    except Exception as e:
        logger.error(f"Failed to authenticate user: {e}")
        return False


def create_user(user: str, password: str):
    try:
        users_collection = get_mongo_db()[get_config().db.users_collection]
        hashed_password = hash_password(password)
        users_collection.update_one(
            {"_id": user},
            {"$set": {"user_name": user, "password": hashed_password}},
            upsert=True,
        )
        logger.info(f"User {user} created")
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
