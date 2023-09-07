import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from vega_datasets import data

from api.config import config
from api.models import *

from gleaner import Gleaner, GleanerDashboard
from gleaner.model import get_chart_from_tokens

df = data.movies()

gl = Gleaner(df)
gl.config.n_epoch = 5
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
    gl.config.n_epoch = 5
    gl.update_config()
    return InitResponse(
        chartTypes=list(chart_types.values()),
        transformations=list(trs_types.values()),
        taskTypes=list(task_types.values()),
        attributes=[AttributeModel(name=a.name, type=a.type) for a in gl.config.attrs[1:]],  # type: ignore
    )


@app.post("/train")
async def train(train: TrainBody) -> TrainResponse:
    print(train)
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
        transformation=[TransformationDistModel.model_validate(ag) for ag in ags],
        result=ScoreDistModel.model_validate(train_result.to_dict()),
    )


@app.post("/infer")
async def infer(body: InferBody) -> InferResponse:
    print(f"infer: {body}")
    dashboard, result = gl.explorer.search(gl.generator, gl.oracle, gl.preferences)
    charts = [GleanerChartModel.from_gleaner_chart(c, gl.oracle.get_statistics_from_chart(c)) for c in dashboard.charts]

    return InferResponse(
        charts=charts,
        result=OracleResultModel.from_oracle_result(result),
    )


@app.post("/recommend")
async def recommend(body: RecommendBody) -> RecommendResponse:
    charts = [get_chart_from_tokens(c, df) for c in [tuple(c) for c in body.chartKeys]]  # type: ignore
    results = gl.recommend(GleanerDashboard(charts), body.nResults)
    return RecommendResponse(
        charts=[GleanerChartModel.from_gleaner_chart(c, gl.oracle.get_statistics_from_chart(c)) for c in results]
    )


@app.post("/score")
async def score(body: ScoreBody) -> ScoreResponse:
    dashboard = GleanerDashboard([get_chart_from_tokens(c, df) for c in [tuple(c) for c in body.chartKeys]])  # type: ignore
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
