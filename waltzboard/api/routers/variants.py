from fastapi import APIRouter
from pydantic import BaseModel

from waltzboard import WaltzboardDashboard
from waltzboard.api.config import gl
from waltzboard.api.utills import printLog, tokenize

from ..models import WaltzboardChartModel


class VariantsBody(BaseModel):
    chartKeys: list[str]
    targetIndex: int


class VariantsResponse(BaseModel):
    variants: list[WaltzboardChartModel]


router = APIRouter(
    prefix="/variants",
    tags=["variants"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def variants(body: VariantsBody) -> VariantsResponse:
    printLog("REQ", "/variants", {"targetChartKey": body.targetIndex})
    charts = [gl.get_chart_from_tokens(tokenize(key)) for key in body.chartKeys]
    targetChart = charts[body.targetIndex]
    variants = gl.get_variants_from_chart(targetChart)
    variant_charts = [
        charts[0 : body.targetIndex] + [v] + charts[body.targetIndex :]
        for v in variants
    ]
    variant_dashboards = [WaltzboardDashboard(c) for c in variant_charts]
    variant_results = [
        gl.oracle.get_result(d, set(gl.preferences)) for d in variant_dashboards
    ]
    variant_scores = [r.get_score() for r in variant_results]
    top_dashboard_indices = sorted(
        range(len(variant_scores)),
        key=lambda i: variant_scores[i],
        reverse=True,
    )[:10]
    top_five_charts = [variants[i] for i in top_dashboard_indices]

    return VariantsResponse(
        variants=[
            WaltzboardChartModel.from_waltzboard_chart(
                c, gl.oracle.get_statistics_from_chart(c)
            )
            for c in top_five_charts
        ]
    )
