from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from config import settings
from models.auth import User
from drivers.auth import utils
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
@router.post("/", response_class=HTMLResponse)
async def home(request:Request, user:User=Depends(utils.GetCookieUserAllowGuest)):
    return settings.TEMPLATES.TemplateResponse("index.html", {"request":request, "user":user})