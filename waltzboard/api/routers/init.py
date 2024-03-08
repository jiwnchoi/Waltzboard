from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from waltzboard.api.config import config, datasets, gl
from waltzboard.api.models import (
    AttributeModel,
    ChartTypeModel,
    TrsTypeModel,
    chart_types,
    trs_types,
)
from waltzboard.api.utills import printLog


class InitBody(BaseModel):
    userId: str
    dataset: str = "Birdstrikes"
    n_epoch: int = 10
    n_candidates: int = 100
    n_search_space: int = 50
    n_beam: int = 10
    robustness: int = 10
    n_min_charts: int = 3
    acceleration: float = 1.0


class InitResponse(BaseModel):
    n_epoch: int
    robustness: int
    datasets: list[str]
    chartTypes: list[ChartTypeModel]
    transformations: list[TrsTypeModel]
    attributes: list[AttributeModel]
    configs: dict[str, int | str]


router = APIRouter(
    prefix="/init", tags=["init"], responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=None)
async def init(body: InitBody):
    if body.userId != config.USER_ID:
        printLog("ERR", "/init", {"id": body.userId, "dataset": body.dataset})
        return HTTPException(status_code=401, detail="Unauthorized")
    printLog("REQ", "/init", {"id": body.userId, "dataset": body.dataset})
    gl.__init__(datasets[body.dataset])
    gl.config.n_epoch = body.n_epoch
    gl.config.n_candidates = body.n_candidates
    gl.config.n_search_space = body.n_search_space
    gl.config.n_beam = body.n_beam
    gl.config.robustness = body.robustness
    gl.config.n_min_charts = body.n_min_charts
    gl.config.acceleration = body.acceleration
    gl.update_config()
    return InitResponse(
        n_epoch=gl.config.n_epoch,
        robustness=gl.config.robustness,
        datasets=list(datasets.keys()),
        chartTypes=list(chart_types.values()),
        transformations=list(trs_types.values()),
        attributes=[
            AttributeModel(name=a.name, type=a.type) for a in gl.config.attrs[1:]
        ],  # type: ignore
        configs=body.model_dump(),
    )
