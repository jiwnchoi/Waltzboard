from fastapi import APIRouter
from pydantic import BaseModel
from api.models import *
from api.config import gl


from api.utills import tokenize



class GetChartResponse(BaseModel):
    chart: GleanerChartModel


router = APIRouter(
    prefix="/get_chart",
    tags=["get_chart"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_chart(token: str) -> GetChartResponse:
    chart = gl.get_chart_from_tokens(tokenize(token))
    return GetChartResponse(
        chart=GleanerChartModel.from_gleaner_chart(
            chart, gl.oracle.get_statistics_from_chart(chart)
        )
    )
