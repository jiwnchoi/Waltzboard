from time import time

from fastapi import APIRouter
from pydantic import BaseModel

from waltzboard.api.config import gl
from waltzboard.api.utills import printLog

from ..models import (
    AttributeDistModel,
    ChartTypeDistModel,
    OracleWeightModel,
    ScoreDistModel,
    TransformationDistModel,
)


class TrainBody(BaseModel):
    weight: OracleWeightModel
    preferences: list[str]
    constraints: list[str]


class TrainResponse(BaseModel):
    attribute: list[AttributeDistModel]
    chartType: list[ChartTypeDistModel]
    transformation: list[TransformationDistModel]
    result: ScoreDistModel


router = APIRouter(
    prefix="/train",
    tags=["train"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def train(train: TrainBody) -> TrainResponse:
    printLog(
        "REQ",
        "/train",
        {
            "weight": train.weight.model_dump(),
            "preferences": train.preferences,
            "constraints": train.constraints,
        },
    )
    gl.update_preferences(train.preferences)
    gl.update_constraints(train.constraints)
    gl.update_weight(
        specificity=train.weight.specificity,
        interestingness=train.weight.interestingness,
        coverage=train.weight.coverage,
        diversity=train.weight.diversity,
        parsimony=train.weight.parsimony,
    )
    time()
    train_results = gl.train()
    train_result = (
        {
            "score": [0, 0, 0, 0, 0],
            "coverage": [0, 0, 0, 0, 0],
            "diversity": [0, 0, 0, 0, 0],
            "specificity": [0, 0, 0, 0, 0],
            "interestingness": [0, 0, 0, 0, 0],
            "parsimony": [0, 0, 0, 0, 0],
        }
        if len(train_results) == 0
        else train_results[-1].to_dict()
    )

    if len(train_results) != 0:
        printLog(
            "RES",
            "/train",
            {
                "weight": train.weight.model_dump(),
                "preferences": train.preferences,
                "constraints": train.constraints,
            },
        )
    attrs, cts, ags = gl.generator.prior.export()
    last_body = TrainResponse(
        attribute=[AttributeDistModel.model_validate(attr) for attr in attrs],
        chartType=[ChartTypeDistModel.model_validate(ct) for ct in cts],
        transformation=[TransformationDistModel.model_validate(ag) for ag in ags],
        result=ScoreDistModel.model_validate(train_result),
    )

    return last_body
