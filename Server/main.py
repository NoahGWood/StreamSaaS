from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from config import settings
from config.routes import ImportRoutes

app = FastAPI(
    title = settings.APP_NAME,
    description = settings.DESCRIPTION,
    version = settings.VERSION,
    docs_url = settings.DOCS_URL,
    redoc_url = settings.REDOC_URL,
    debug = settings.DEBUG
)

app.mount(settings.STATIC_ROUTE, 
            StaticFiles(directory=settings.STATIC_DIR),
            name="static")

# Include Routes
ImportRoutes(app)