"""views/user.py

holds all user-related views
"""
from fastapi import APIRouter, Request, Depends
from fastapi import HTTPException, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional

from config import settings
from drivers.auth import utils
from models.auth import User, RegisterUser
from api.auth import register_user
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
    token = utils.GenToken(user, request)
    response = RedirectResponse(settings.ON_LOGIN_REDIRECT)
    response.set_cookie(key="JWT", value=token, httponly=True, samesite="lax")
    return response

@router.get("/logout")
async def get_logout(request:Request):
    response = RedirectResponse("/")
    response.delete_cookie("JWT")
    return response

@router.get("/register", response_class=HTMLResponse)
async def get_login(request:Request, user:User = Depends(utils.GetCookieUserAllowGuest)):
    if user:
        return RedirectResponse("/")
    return settings.TEMPLATES.TemplateResponse("register.html",{"request":request, "user":user})

@router.post("/register")
async def post_login(request: Request, email:str = Form(), password:str = Form()):
    async with request.form() as form:
        phone = form["phone"]
    newUser = RegisterUser(Email=email, Password=password, Phone=phone)
    user = await register_user(request, newUser)
    token = utils.GenToken(user, request)
    response = RedirectResponse(settings.ON_REGISTER_REDIRECT)
    response.set_cookie(key="JWT", value=token, httponly=True, samesite="lax")
    return response