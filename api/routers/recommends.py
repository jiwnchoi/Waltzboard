from random import choices
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.models import *
from api.config import gl
from api.utills import tokenize
from waltzboard import WaltzboardDashboard
from waltzboard.oracle import get_statistics


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
    dashboard = WaltzboardDashboard(
        [gl.get_chart_from_tokens(tokenize(c)) for c in body.chartKeys]
    )
    all_charts = gl.get_all_charts()
    print(len(all_charts))
    if len(all_charts) > 10000:
        all_charts = choices(all_charts, k=10000)
    appended_dashboards = [dashboard.extend([c]) for c in all_charts]
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
