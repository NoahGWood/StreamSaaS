"""models/auth.py

This file contains the database models needed to implement authentication.
"""

from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from config import settings

class Token(BaseModel):
    """Token represents a bearer token used to authenticate
    a user to the Presently SaaS application.
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """TokenData contains information about the token
    used to authenticate a user to the Presently SaaS app.
    """
    UUID: Optional[str] = None
    IP: Optional[str] = None
    # Add other stuff for browser fingerprinting and security stuff

class User(BaseModel):
    """User class"""
    UUID: str
    Email: str
    Phone: Optional[str] = None

    # Metadata
    JoinDate: Optional[datetime] = datetime.now(settings.TIMEZONE)
    LastAccess: Optional[datetime] = None
    Logins: Optional[List[str]] = None # Stores the user IP address

class RegisterUser(BaseModel):
    """Helper class for registration forms"""
    Email: str
    Password: str
    Phone: Optional[str] = None

class DBUser(User):
    HashedPassword: str
    Salt: str