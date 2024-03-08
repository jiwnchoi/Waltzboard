from fastapi import APIRouter
from pydantic import BaseModel

from waltzboard.api.config import gl
from waltzboard.api.utills import printLog, tokenize


class IsValidResponse(BaseModel):
    isValid: bool


router = APIRouter(
    prefix="/is_valid",
    tags=["is_valid"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def init(token: str) -> IsValidResponse:
    isValid = gl.is_valid_tokens(tokenize(token))
    if isValid:
        printLog(
            "REQ",
            "/is_valid",
            {
                "token": token,
                "isValid": isValid,
            },
        )
    return IsValidResponse(isValid=isValid)
