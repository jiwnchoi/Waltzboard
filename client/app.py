import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pynpm import NPMPackage
from vega_datasets import data
import os

from api.config import config
from api.models import *

from gleaner import Gleaner, GleanerChart, GleanerDashboard
from gleaner.model import get_gleaner_chart_from_key

df = data.movies()

gl = Gleaner(df)
app = FastAPI()

package = NPMPackage("./package.json")

if not os.path.exists("node_modules"):
    package.install()

if not os.path.exists("dist"):
    package.run("build")


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.mount("/", StaticFiles(directory="dist", html=True), name="GleanerInterface")


@app.get("/init")
async def init() -> InitResponse:
    return InitResponse(
        chartTypes=list(chart_types.values()),
        taskTypes=list(task_types.values()),
        attributes=[AttributeModel(name=a.name, type=a.type) for a in gl.config.attrs],
    )


@app.post("/train")
async def train(train: TrainBody):
    print(train)
    try:
        gl.config.give_constraints(train.constraints)
        gl.oracle.update(
            specificity=train.weight.specificity,
            interestingness=train.weight.interestingness,
            coverage=train.weight.coverage,
            diversity=train.weight.diversity,
            conciseness=train.weight.conciseness,
        )
        gl.train(train.preferences)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


@app.post("/infer")
async def infer(body: InferBody) -> InferResponse:
    print(body)
    (
        result_n_scores,
        raw_scores,
        normalized_scores,
        specificity,
        interestingness,
        coverage,
        diversity,
        conciseness,
    ) = gl.explorer._infer(gl.generator, gl.oracle, gl.preferences)
    dashboard = result_n_scores[0][1]
    result = result_n_scores[0][0]
    charts = [GleanerChartModel.from_gleaner_chart(c, gl.oracle.get_statistics_from_chart(c)) for c in dashboard.charts]

    return InferResponse(
        charts=charts,
        result=OracleResultModel.from_oracle_result(result),
        scores=list(raw_scores),
        specificity=list(specificity),
        interestingness=list(interestingness),
        coverage=list(coverage),
        diversity=list(diversity),
        conciseness=list(conciseness),
    )


@app.post("/recommend")
async def recommend(body: RecommendBody) -> RecommendResponse:
    charts = [get_gleaner_chart_from_key(c) for c in body.chartKeys]
    results = gl.recommend(GleanerDashboard(charts), body.nResults)
    return RecommendResponse(
        charts=[GleanerChartModel.from_gleaner_chart(c, gl.oracle.get_statistics_from_chart(c)) for c in results]
    )


@app.post("/score")
async def score(body: ScoreBody) -> ScoreResponse:
    dashboard = GleanerDashboard([get_gleaner_chart_from_key(c) for c in body.chartKeys])
    results = gl.oracle.get_result(dashboard, set(gl.preferences))
    return ScoreResponse(
        result=OracleResultModel.from_oracle_result(results),
    )


if __name__ == "__main__":
    uvicorn.run(
        app="app:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=config.DEBUG,
    )
