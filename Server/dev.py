import uvicorn
from config import settings

if __name__ in '__main__':
    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT,
        reload=settings.DEBUG, log_level=settings.LOG_LEVEL)