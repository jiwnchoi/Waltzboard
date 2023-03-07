from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src import Columbus, ColumbusOracle, ColumbusCofnig, OracleWeight
from src.oracle import chart_types, task_types, ChartType, TaskType
from vega_datasets import data


df = data.movies()

# name attributes
name_attrs = [
    col
    for col in df.columns
    if (df[col].dtype == "object" and df[col].nunique() < 10)
    or df[col].dtype != "object"
]
df = df[name_attrs]


class InitItem(BaseModel):
    chartTypes: list[dict]
    taskTypes: list[dict]
    attributes: list[dict[str, str]]
    result: dict


class Result(BaseModel):
    result: dict


class CreateDashboardBody(BaseModel):
    numVis: int
    numSample: int
    numFilter: int
    weight: OracleWeight
    chartTypes: list[str]
    wildcard: list[str]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


config = ColumbusCofnig()

columbus = Columbus(df, config)


@app.get("/5001/init")
async def init(num_vis: int = 12) -> InitItem:
    return InitItem(
        chartTypes=[c.to_dict() for c in chart_types.values()],
        taskTypes=[t.to_dict() for t in task_types.values()],
        attributes=columbus.get_attributes(),
        result=columbus.sample(
            ColumbusOracle(OracleWeight()),
            num_vis,
            100,
            [],
            [c.mark for c in chart_types.values()],
        ).to_dict(),
    )


@app.post("/5001/create_dashboard")
async def create_dashboard(body: CreateDashboardBody) -> Result:
    return Result(
        result=columbus.sample(
            ColumbusOracle(body.weight),
            body.numVis,
            body.numSample,
            body.wildcard,
            body.chartTypes,
        ).to_dict()
    )
