from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.models import *
from api.config import gl
from api.utills import tokenize
from gleaner import GleanerDashboard


class VariantsBody(BaseModel):
    chartKeys: list[str]
    targetIndex: int


class VariantsResponse(BaseModel):
    variants: list[GleanerChartModel]


router = APIRouter(
    prefix="/variants",
    tags=["variants"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def variants(body: VariantsBody) -> VariantsResponse:
    charts = [gl.get_chart_from_tokens(tokenize(key)) for key in body.chartKeys]
    targetChart = charts[body.targetIndex]
    variants = gl.get_variants_from_chart(targetChart)
    variant_charts = [
        charts[0 : body.targetIndex] + [v] + charts[body.targetIndex :]
        for v in variants
    ]
    variant_dashboards = [GleanerDashboard(c) for c in variant_charts]
    variant_results = [
        gl.oracle.get_result(d, set(gl.preferences)) for d in variant_dashboards
    ]
    variant_scores = [r.get_score() for r in variant_results]
    top_five_dashboard_index = sorted(
        range(len(variant_scores)),
        key=lambda i: variant_scores[i],
        reverse=True,
    )[:5]
    top_five_charts = [variants[i] for i in top_five_dashboard_index]

    return VariantsResponse(
        variants=[
            GleanerChartModel.from_gleaner_chart(c, gl.oracle.get_statistics_from_chart(c)) for c in top_five_charts
        ]
    )
