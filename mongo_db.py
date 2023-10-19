import motor.motor_asyncio

from config import MONGO_DB_SERVER, MONGODB_ADMINUSERNAME, MONGODB_ADMINPASSWORD

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
    f'mongodb://{MONGODB_ADMINUSERNAME}:{MONGODB_ADMINPASSWORD}@{MONGO_DB_SERVER}:27017')
db = mongo_client.tiny_link