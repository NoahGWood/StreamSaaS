import os
from datetime import timezone
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from neo4j import GraphDatabase
from passlib.context import CryptContext

# Main App Settings
APP_NAME = "Presently"
DESCRIPTION = "Open-Source SaaS Presentation Generator"
VERSION = "1.0.0"
DOCS_URL = "/docs"
REDOC_URL = "/redoc"
DEBUG = True
HOST = "0.0.0.0"
PORT = 8000
TIMEZONE = timezone.utc
LOG_LEVEL = "info"
# Templating
TEMPLATE_DIR = "templates"
TEMPLATES = Jinja2Templates(directory=TEMPLATE_DIR)
# Static Files
STATIC_ROUTE = "/static"
STATIC_DIR = "static"

# Security Settings
FORCE_SSL = False # MUST BE ON IN PRODUCTION! Disable in development
SECRET_KEY = os.environ.get("SECRET_KEY", "oWbIsc67Cx0ZVOxAJICDuebJXcPAr7bM1ELhpZKOaKQ")
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# Auth Settings
AUTH_ENDPOINT = "/auth"
TOKEN_URL = "/token"
TOKEN_ENDPOINT = AUTH_ENDPOINT + TOKEN_URL 
JWT_ALGORITHM = "HS256"
TOKEN_LIFETIME_MINUTES=15
ENABLE_BEARER_AUTH=True
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl=TOKEN_ENDPOINT, auto_error=False)
# Password Settings
FORCE_COMPLEX = False # SHOULD be on in production
# Password complexity
# Must have:
#   8 chars, 1 Uppercase, 1 Lowercase, 1 Number, 1 Special Char
PASSWORD_COMPLEXITY_PATTERN = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
# RFC 5322 Regex Email Pattern
EMAIL_VALIDATE_PATTERN = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"

PASSWORD_SCHEMES = ["bcrypt"]
PASSWORD_SCHEMES_DEPRECATED = "auto"
SALT_SIZE = 32 # Random salt, pre-bcrypt
PWD_CONTEXT = CryptContext(schemes=PASSWORD_SCHEMES,
                            deprecated=PASSWORD_SCHEMES_DEPRECATED)

# Database
DATABASE_URL = os.environ.get("DATABASE_URL", "neo4j://localhost:7687")
DATABASE_USER = os.environ.get("DATABASE_USER", "neo4j")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "password") 

DB = GraphDatabase.driver(DATABASE_URL, auth=(DATABASE_USER, DATABASE_PASSWORD))

# Redirection Rules
ON_LOGIN_REDIRECT = "/"
ON_REGISTER_REDIRECT = "/"