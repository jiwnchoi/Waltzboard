from fastapi import APIRouter
from pydantic import BaseModel
from api.models import *
from api.config import gl


from api.utills import tokenize


class IsValidResponse(BaseModel):
    isValid: bool


router = APIRouter(
    prefix="/is_valid",
    tags=["is_valid"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def init(token: str) -> IsValidResponse:
    return IsValidResponse(isValid=gl.is_valid_tokens(tokenize(token)))

