import pandas as pd
from pydantic_settings import BaseSettings

from waltzboard import Waltzboard


class Config(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 3000
    DEBUG: bool = False
    ALLOWED_HOSTS: list[str] = ["*"]
    USER_ID: str = "test"


config = Config()


datasets = {
    "Birdstrikes": pd.read_csv("data/birdstrikes.csv").sample(5000),
    "Movies": pd.read_csv("data/movies.csv"),
    "Student Performance": pd.read_csv("data/student_performance.csv"),
}

df = datasets["Birdstrikes"]
gl = Waltzboard(df)
