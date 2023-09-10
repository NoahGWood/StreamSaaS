"""views/user.py

holds all user-related views
"""
from fastapi import APIRouter, Request, Depends
from fastapi import HTTPException, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse

from config import settings
from drivers.auth import utils
from models.auth import User, RegisterUser

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
async def get_login(request:Request, user:User = Depends(utils.GetCookieUserAllowGuest)):
    if user:
        return RedirectResponse("/")
    return settings.TEMPLATES.TemplateResponse("login.html",{"request":request, "user":user})

@router.post("/login")
async def post_login(request: Request, email:str = Form(), password:str = Form()):
    user = utils.AuthenticateUser(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password."
        )
    token = utils.CreateAccessToken(data={"UUID":user.UUID, "IP":request.client.host})
    response = RedirectResponse("/")
    response.set_cookie(key="JWT", value=token, httponly=True, samesite="lax")
    return response

@router.get("/logout")
async def get_logout(request:Request):
    response =RedirectResponse("/")
    response.delete_cookie("JWT")
    return response