from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.models import *
from api.config import gl, datasets


class InitBody(BaseModel):
    dataset: str = 'Movies'
    n_epoch: int = 5
    robustness: int = 50
    

class InitResponse(BaseModel):
    n_epoch: int
    robustness: int 
    datasets: list[str]
    chartTypes: list[ChartTypeModel]
    transformations: list[TrsTypeModel]
    attributes: list[AttributeModel]


router = APIRouter(
    prefix="/init", tags=["init"], responses={404: {"description": "Not found"}}
)


@router.post("/")
async def init(body: InitBody) -> InitResponse:
    gl.__init__(datasets[body.dataset])
    gl.config.n_epoch = body.n_epoch
    gl.config.robustness = body.robustness
    gl.update_config()
    return InitResponse(
        n_epoch=gl.config.n_epoch,
        robustness=gl.config.robustness,
        datasets=list(datasets.keys()),
        chartTypes=list(chart_types.values()),
        transformations=list(trs_types.values()),
        attributes=[AttributeModel(name=a.name, type=a.type) for a in gl.config.attrs[1:]],  # type: ignore
    )
