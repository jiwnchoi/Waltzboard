from fastapi import APIRouter, Depends
from pydantic import BaseModel
from api.models import (
    OracleWeightModel,
    AttributeDistModel,
    ChartTypeDistModel,
    TransformationDistModel,
    ScoreDistModel,
)
from api.config import gl


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
    gl.preferences = train.preferences
    gl.config.update_constraints(train.constraints)
    gl.config.update_weight(
        specificity=train.weight.specificity,
        interestingness=train.weight.interestingness,
        coverage=train.weight.coverage,
        diversity=train.weight.diversity,
        parsimony=train.weight.parsimony,
    )
    gl.update_config()
    train_result = gl.train(train.preferences)[-1]
    attrs, cts, ags = gl.generator.prior.export()
    return TrainResponse(
        attribute=[AttributeDistModel.model_validate(attr) for attr in attrs],
        chartType=[ChartTypeDistModel.model_validate(ct) for ct in cts],
        transformation=[
            TransformationDistModel.model_validate(ag) for ag in ags
        ],
        result=ScoreDistModel.model_validate(train_result.to_dict()),
    )
