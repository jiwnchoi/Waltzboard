import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from vega_datasets import data

from api.config import config
from api.models import *

from gleaner import Gleaner, GleanerChart, GleanerDashboard
from gleaner.model import get_gleaner_chart_from_key

df = data.movies()

gl = Gleaner(df)
gl.config.n_epoch = 10
app = FastAPI()


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
    gl.__init__(df)
    return InitResponse(
        chartTypes=list(chart_types.values()),
        aggregations=list(agg_types.values()),
        taskTypes=list(task_types.values()),
        attributes=[AttributeModel(name=a.name, type=a.type) for a in gl.config.attrs],
    )


@app.post("/train")
async def train(train: TrainBody) -> TrainResponse:
    gl.__init__(df)
    gl.config.give_constraints(train.constraints)
    gl.oracle.update(
        specificity=train.weight.specificity,
        interestingness=train.weight.interestingness,
        coverage=train.weight.coverage,
        diversity=train.weight.diversity,
        parsimony=train.weight.parsimony,
    )
    print(train.constraints, train.preferences)
    train_result = gl.train(train.preferences)
    attrs, cts, ags = gl.generator.prior.export()
    return TrainResponse(
        attribute=[AttributeDistModel.model_validate(attr) for attr in attrs],
        chartType=[ChartTypeDistModel.model_validate(ct) for ct in cts],
        aggregation=[AggregationDistModel.model_validate(ag) for ag in ags],
    )


@app.post("/infer")
async def infer(body: InferBody) -> InferResponse:
    (
        result_n_scores,
        raw_scores,
        normalized_scores,
        specificity,
        interestingness,
        coverage,
        diversity,
        parsimony,
    ) = gl.explorer._infer(gl.generator, gl.oracle, gl.preferences)
    dashboard = result_n_scores[0][1]
    result = result_n_scores[0][0]
    charts = [GleanerChartModel.from_gleaner_chart(c, gl.oracle.get_statistics_from_chart(c)) for c in dashboard.charts]

    return InferResponse(
        charts=charts,
        result=OracleResultModel.from_oracle_result(result),
        dist=ScoreDistModel(
            score=list(raw_scores),
            specificity=list(specificity),
            interestingness=list(interestingness),
            coverage=list(coverage),
            diversity=list(diversity),
            parsimony=list(parsimony),
        ),
    )


@app.post("/recommend")
async def recommend(body: RecommendBody) -> RecommendResponse:
    print(body)
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
