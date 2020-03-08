from os import environ

SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")

GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
