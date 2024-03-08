from fastapi import APIRouter
from pydantic import BaseModel

from waltzboard.api.config import gl
from waltzboard.api.utills import printLog, tokenize

from ..models import OracleResultModel, WaltzboardChartModel


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
    printLog(
        "REQ",
        "/infer",
        {
            "chartKeys": body.chartKeys,
        },
    )
    fixed_charts = [gl.get_chart_from_tokens(tokenize(key)) for key in body.chartKeys]
    if len(gl.config.all_charts) < gl.config.n_beam:
        return InferResponse(
            charts=gl.config.all_charts,
            result=OracleResultModel.from_oracle_result(
                gl.oracle.get_statistics_from_chart(gl.config.all_charts)  # type: ignore
            ),
        )
    else:
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
