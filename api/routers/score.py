from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.models import *
from api.config import gl
from api.utills import tokenize
from gleaner import GleanerDashboard


class ScoreBody(BaseModel):
    chartKeys: list[str]


class ScoreResponse(BaseModel):
    result: OracleResultModel
    chartResults: list[OracleResultModel]


router = APIRouter(prefix="/score", tags=["score"], responses={404: {"description": "Not found"}})


@router.post("/")
async def score(body: ScoreBody) -> ScoreResponse:
    dashboard = GleanerDashboard([gl.get_chart_from_tokens(c) for c in [tokenize(c) for c in body.chartKeys]])  # type: ignore
    results = gl.oracle.get_result(dashboard, set(gl.preferences))
    ablated_dashboard = [
        GleanerDashboard([c for j, c in enumerate(dashboard.charts) if i != j]) for i in range((len(dashboard)))
    ]
    ablated_result = [gl.oracle.get_result(d, set(gl.preferences)) for d in ablated_dashboard]
    return ScoreResponse(
        result=OracleResultModel.from_oracle_result(results),
        chartResults=[OracleResultModel.from_oracle_result(r) for r in ablated_result],
    )
