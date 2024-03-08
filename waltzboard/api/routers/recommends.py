from random import choices

from fastapi import APIRouter
from pydantic import BaseModel

from waltzboard import WaltzboardDashboard
from waltzboard.api.config import gl
from waltzboard.api.utills import printLog, tokenize
from waltzboard.oracle import get_statistics

from ..models import WaltzboardChartModel


class RecommendBody(BaseModel):
    chartKeys: list[str]


class RecommendResponse(BaseModel):
    recommends: list[WaltzboardChartModel]


router = APIRouter(
    prefix="/recommends",
    tags=["recommends"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def recommends(body: RecommendBody) -> RecommendResponse:
    printLog(
        "REQ",
        "/recommends",
        {},
    )
    keys = [tokenize(key) for key in body.chartKeys]
    dashboard = WaltzboardDashboard([gl.get_chart_from_tokens(key) for key in keys])
    all_charts = gl.config.all_charts
    if len(all_charts) > 10000:
        all_charts = choices(all_charts, k=10000)
    appended_dashboards = [
        dashboard.extend([c]) for c in all_charts if c.tokens not in keys
    ]
    scores = [
        gl.oracle.get_result(d, set(gl.preferences)).get_score()
        for d in appended_dashboards
    ]
    top_scoreed_indices = sorted(
        range(len(scores)), key=lambda i: scores[i], reverse=True
    )[:10]
    return RecommendResponse(
        recommends=[
            WaltzboardChartModel.from_waltzboard_chart(
                all_charts[i], get_statistics(all_charts[i])
            )
            for i in top_scoreed_indices
        ]
    )
