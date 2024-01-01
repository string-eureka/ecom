from .settings import *
import os
import environ

env = environ.Env()
environ.Env.read_env()
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False
SECRET_KEY = env("SECRET_KEY")


hostname = env("DBHOST")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DBNAME"),
        "HOST": hostname + ".postgres.database.azure.com",
        "USER": env("DBUSER"),
        "PASSWORD": env("DBPASS"),
    }
}

ALLOWED_HOSTS = (
    [os.environ["WEBSITE_HOSTNAME"]] if "WEBSITE_HOSTNAME" in os.environ else []
)
CSRF_TRUSTED_ORIGINS = (
    ["https://" + os.environ["WEBSITE_HOSTNAME"]]
    if "WEBSITE_HOSTNAME" in os.environ
    else []
)
