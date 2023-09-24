from api.utills import tokenize
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.models import *
from api.config import gl


class InferBody(BaseModel):
    chartKeys: list[str]


class InferResponse(BaseModel):
    charts: list[WaltzboardChartModel]
    result: OracleResultModel


router = APIRouter(
    prefix="/infer",
    tags=["infer"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def infer(body: InferBody) -> InferResponse:
    fixed_charts = [gl.get_chart_from_tokens(tokenize(key)) for key in body.chartKeys]
    dashboard, result = gl.explorer.search(
        gl.generator, gl.oracle, gl.preferences, fixed_charts
    )
    charts = [
        WaltzboardChartModel.from_waltzboard_chart(
            c, gl.oracle.get_statistics_from_chart(c)
        )
        for c in dashboard.charts
    ]

    return InferResponse(
        charts=charts,
        result=OracleResultModel.from_oracle_result(result),
    )
