import pathlib

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .api.config import config
from .api.routers import (
    get_chart,
    infer,
    init,
    inspect,
    is_valid,
    recommends,
    score,
    train,
    variants,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/waltzboard",
    StaticFiles(directory=f"{pathlib.Path(__file__).parent}/api/static"),
    name="waltzboard",
)
app.include_router(train.router)
app.include_router(init.router)
app.include_router(infer.router)
app.include_router(score.router)
app.include_router(variants.router)
app.include_router(is_valid.router)
app.include_router(inspect.router)
app.include_router(recommends.router)
app.include_router(get_chart.router)


@app.get("/")
async def index() -> RedirectResponse:
    return RedirectResponse(url="/waltzboard/index.html")


def run_app(host=config.APP_HOST, port=config.APP_PORT):
    uvicorn.run(
        app,
        host=host,
        port=port,
    )
