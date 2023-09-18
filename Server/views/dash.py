from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from config import settings
from models.auth import User
from drivers.auth import utils
router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def dash(request:Request, user:User=Depends(utils.GetCookieUser)):
    return settings.TEMPLATES.TemplateResponse("dashboard.html", {"request":request, "user":user})