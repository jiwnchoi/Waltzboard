from gleaner import Gleaner
import pandas as pd
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = True
    ALLOWED_HOSTS: list[str] = ["*"]


config = Config()


datasets = {
    "Birdstrikes": pd.read_csv("data/birdstrikes.csv").sample(1000),
    "Movies": pd.read_json("data/movies.json"),
    "Student Performance": pd.read_csv("data/student_performance.csv"),
}

df = datasets["Movies"]
gl = Gleaner(df)
