from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.models import *
from api.config import gl, datasets


class InitResponse(BaseModel):
    datasets: list[str]
    chartTypes: list[ChartTypeModel]
    transformations: list[TrsTypeModel]
    attributes: list[AttributeModel]


router = APIRouter(
    prefix="/init", tags=["init"], responses={404: {"description": "Not found"}}
)


@router.get("/")
async def init(name: str = "Movies") -> InitResponse:
    gl.__init__(datasets[name])
    gl.config.n_epoch = 5
    gl.update_config()
    return InitResponse(
        datasets=list(datasets.keys()),
        chartTypes=list(chart_types.values()),
        transformations=list(trs_types.values()),
        attributes=[AttributeModel(name=a.name, type=a.type) for a in gl.config.attrs[1:]],  # type: ignore
    )
