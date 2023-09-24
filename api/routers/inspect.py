from fastapi import APIRouter
from pydantic import BaseModel
from api.models import *
from api.config import gl


from api.utills import tokenize
from waltzboard import WaltzboardDashboard
from waltzboard.model import get_chart_from_tokens


class InspectBody(BaseModel):
    chartKeys: list[str]
    target: int


class InspectResponse(BaseModel):
    result: OracleSingleResultModel


router = APIRouter(
    prefix="/inspect",
    tags=["inspect"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def init(body: InspectBody) -> InspectResponse:
    return InspectResponse(
        result=OracleSingleResultModel.from_oracle_result(
            gl.oracle.get_single_chart_results(
                WaltzboardDashboard(
                    [
                        get_chart_from_tokens(tokenize(key), gl.config)
                        for key in body.chartKeys
                    ]
                ),
                body.target,
                set(gl.preferences),
            )
        )
    )
