from fastapi import FastAPI
from views import routes as WebRoutes
from api import routes as ApiRoutes

ROUTES = []
ROUTES.extend(WebRoutes.ROUTES)
ROUTES.extend(ApiRoutes.ROUTES)

def ImportRoutes(app: FastAPI):
    for route in ROUTES:
        if "APIRouter" in str(type(route)):
            app.include_router(route)
        elif 'list' in str(type(route["router"])):
            for each in route["router"]:
                app.include_router(
                    each,
                    prefix=route["prefix"],
                    tags=route["tags"]
                )
        else:
            app.include_router(
                route["router"],
                prefix=route["prefix"] or None,
                tags=route["tags"] or None
            )
