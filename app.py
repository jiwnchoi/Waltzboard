import warnings
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import config
from api.routers import *


warnings.filterwarnings("ignore")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(train.router)
app.include_router(init.router)
app.include_router(infer.router)
app.include_router(score.router)
app.include_router(variants.router)
app.include_router(is_valid.router)
app.include_router(inspect.router)

if __name__ == "__main__":
    uvicorn.run(
        app="app:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=config.DEBUG,
    )
