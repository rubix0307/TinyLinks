import os
import dotenv

dotenv.load_dotenv('.env')

MONGO_DB_SERVER = os.environ['MONGO_DB_SERVER']
MONGODB_ADMINUSERNAME = os.environ['MONGODB_ADMINUSERNAME']
MONGODB_ADMINPASSWORD = os.environ['MONGODB_ADMINPASSWORD']
BOT_TOKEN = os.environ['BOT_TOKEN']