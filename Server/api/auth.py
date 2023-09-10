
import uuid
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional

from config import settings
from drivers.auth import utils
from models.auth import Token, TokenData, User, RegisterUser
from datetime import datetime, timedelta

router = APIRouter()
ROUTE = {
    "router":router,
    "prefix":settings.AUTH_ENDPOINT,
    "tags":["AUTH"]
}

@router.post("/register")
async def register_user(request:Request, user:RegisterUser):
    if not utils.ValidateEmail(user.Email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {user.Email} is not a valid email address."
        )

    if settings.FORCE_COMPLEX and not utils.VerifyPasswordComplexity(user.Password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Password {user.Password} must have a minimum of 8 characters, 1 upper case, 1 lower case, 1 number, and 1 special char.",
        )
    # Create a salt
    salt = utils.CreateSalt()
    # Salt password
    salted = user.Password + salt
    # Hash password
    phash = utils.CreatePasswordHash(salted)
    attributes = {
        "UUID":str(uuid.uuid4()),
        "Email":user.Email,
        "Phone":user.Phone,
        "JoinDate": str(datetime.now(settings.TIMEZONE)),
        "LastAccess": str(datetime.now(settings.TIMEZONE)),
        "Logins": [request.client.host],
        "HashedPassword":phash,
        "Salt":salt
    }
    cypher = "CREATE (user:User $params) RETURN user"
    with settings.DB.session() as session:
        if utils.GetUserByEmail(user.Email):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Operation not permitted, user with email: {user.Email} already exists.",
            )
        response = session.run(query=cypher, parameters={'params':attributes})
        user_data = response.data()[0]['user']
    
    return User(**user_data)

@router.post(settings.TOKEN_URL, response_model=Token)
async def login_access_token(request:Request, form_data: OAuth2PasswordRequestForm = Depends(), expires: Optional[timedelta]=None):
    if not settings.ENABLE_BEARER_AUTH:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Token Authentication Disabled.")
    user = utils.AuthenticateUser(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password."
        )
    if expires:
        token = utils.CreateAccessToken(data={"UUID":user.UUID, "IP":request.client.host}, expires=expires)
    else:
        token = utils.CreateAccessToken(data={"UUID":user.UUID, "IP":request.client.host})
    return {"access_token": token, "token_type":"bearer"}
