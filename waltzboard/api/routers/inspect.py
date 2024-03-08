from fastapi import APIRouter
from pydantic import BaseModel

from waltzboard import WaltzboardDashboard
from waltzboard.api.config import gl
from waltzboard.api.utills import tokenize
from waltzboard.model import get_chart_from_tokens

from ..models import OracleResultModel


class InspectBody(BaseModel):
    chartKeys: list[str]
    target: int


class InspectResponse(BaseModel):
    result: OracleResultModel


router = APIRouter(
    prefix="/inspect",
    tags=["inspect"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def init(body: InspectBody) -> InspectResponse:
    return InspectResponse(
        result=OracleResultModel.from_oracle_result(
            gl.oracle.get_result(
                WaltzboardDashboard(
                    [
                        get_chart_from_tokens(tokenize(key), gl.config)
                        for key in [
                            k for i, k in enumerate(body.chartKeys) if i != body.target
                        ]
                    ]
                ),
                set(gl.preferences),
            )
        )
    )
