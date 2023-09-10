import re
import secrets
import string
from jose import JWTError, jwt
from typing import Optional
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Request, status

from config import settings
from models.auth import User, DBUser, TokenData

# Password
def CreateSalt():
    salt = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(settings.SALT_SIZE))
    return salt

def SaltPassword(pword: str, salt:str):
    return pword + salt

def CreatePasswordHash(pword: str):
    return settings.PWD_CONTEXT.hash(pword)

def VerifyPassword(user:User, plain:str):
    salted = SaltPassword(plain, user.Salt)
    return settings.PWD_CONTEXT.verify(salted, user.HashedPassword)

def VerifyPasswordComplexity(plain: str):
    if re.match(settings.PASSWORD_COMPLEXITY_PATTERN, plain):
        return True
    return False

def ValidateEmail(email:str):
    if(re.match(settings.EMAIL_VALIDATE_PATTERN, email)):
        return True
    return False

def GetUser(uid: str):
    cypher = f"MATCH (user:User) WHERE user.UUID = '{uid}' RETURN user"
    with settings.DB.session() as session:
        user = session.run(query=cypher)
        data = user.data()
        if len(data) > 0:
            user_data = data[0]['user']
            return DBUser(**user_data)
    return None

def GetUserByEmail(email: str):
    cypher = f"MATCH (user:User) WHERE user.Email = '{email}' RETURN user"
    with settings.DB.session() as session:
        user = session.run(query=cypher)
        data = user.data()
        if len(data) > 0:
            user_data = data[0]['user']
            return DBUser(**user_data)
    return None

def EmailInUse(email: str):
    cypher = f"""MATCH (u:User) WHERE u.Email = '{email}' RETURN COUNT(u) > 0 AS u"""
    with settings.DB.session() as session:
        res = session.run(query=cypher)
        return {"response":res.data()[0]['u']}

def AuthenticateUser(email: str, pword: str):
    user = GetUserByEmail(email)
    print(user)
    if user:
        return user if VerifyPassword(user, pword) else False
    return False

def CreateAccessToken(data:dict, expires: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(settings.TIMEZONE)
    if expires:
        expire += expires
    else:
        expire += timedelta(minutes=settings.TOKEN_LIFETIME_MINUTES)
    to_encode["expires"]=str(expire)
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def ReadToken(token: str):
    cred_except = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate", "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        uid: str = payload.get('UUID')
        ip: str = payload.get("IP")
        if uid is None or ip is None:
            raise cred_except
        token_data = TokenData(UUID=uid,IP=ip)
    except JWTError as e:
        raise cred_except from e
    return token_data, cred_except

async def GetCurrentUser(token:str=Depends(settings.OAUTH2_SCHEME)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token_data, cred_except = ReadToken(token=token)
    user = GetUser(token_data.UUID)
    if user is None:
        raise cred_except
    return user

async def GetCookieUser(request: Request):
    if "JWT" in request.cookies:
        return await GetCurrentUser(token=request.cookies["JWT"])
    return None

async def GetCookieUserAllowGuest(request: Request):
    if "JWT" in request.cookies:
        try:
            return await GetCurrentUser(token=request.cookies["JWT"])
        except HTTPException as e:
            return None
    return None