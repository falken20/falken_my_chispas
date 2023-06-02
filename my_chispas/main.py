# by Richi Rod AKA @richionline / falken20
# ./my_chispas/main.py

from .logger import Log
from . import settings

Log.info(f"Some value from .env: {settings.ENV_PRO}")
