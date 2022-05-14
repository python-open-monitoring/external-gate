import os

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from starlette.datastructures import Secret

config = Config(".env")
DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URI_GATE = config("DATABASE_URI_GATE", cast=str)
DATABASE_URI_API = config("DATABASE_URI_API", cast=str)
AMQP_URI = config("AMQP_URI")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=CommaSeparatedStrings)
JWT_SECRET_KEY = config("JWT_SECRET_KEY", cast=Secret)
JWT_PREFIX = config("JWT_PREFIX", cast=str)
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str)
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
FRONTEND_URL = config("FRONTEND_URL", cast=str)
TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN", cast=str, default="")

# MAILJET
MAILJET_API_KEY = config("MAILJET_API_KEY", cast=str, default="")
MAILJET_API_SECRET = config("MAILJET_API_SECRET", cast=str, default="")
PROJECT_MAIL = config("PROJECT_MAIL", cast=str, default="")
