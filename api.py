from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src import Columbus, ColumbusOracle, ColumbusCofnig, OracleWeight
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





task_types = [
    
]


class InitItem(BaseModel):
    chartTypes: list[dict[str, str]]
    attributes: list[dict[str, str]]
    result: dict


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
        chartTypes=chart_types,
        attributes=columbus.get_attributes(),
        result=columbus.sample(
            ColumbusOracle(OracleWeight()), num_vis, 100, []
        ).to_dict(),
    )

