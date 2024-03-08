from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from waltzboard.api.config import gl
from waltzboard.api.utills import tokenize

from ..models import WaltzboardChartModel


class GetChartResponse(BaseModel):
    chart: WaltzboardChartModel | None


router = APIRouter(
    prefix="/get_chart",
    tags=["get_chart"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_chart(token: str) -> GetChartResponse:
    is_valid = gl.is_valid_tokens(tokenize(token))
    if not is_valid:
        return GetChartResponse(chart=None)

    chart = gl.get_chart_from_tokens(tokenize(token))
    return GetChartResponse(
        chart=WaltzboardChartModel.from_waltzboard_chart(
            chart, gl.oracle.get_statistics_from_chart(chart)
        )
    )
