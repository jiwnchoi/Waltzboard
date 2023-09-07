import altair as alt
from altair import Chart
from .base_chart import BaseChart


class Heatmap(BaseChart):
    def display(self) -> Chart:
        return (
            alt.Chart(self.df, title=self.title)
            .mark_rect()
            .encode(
                alt.X(
                    self.altair_token.x.name,
                    type=self.altair_token.x.type,
                    bin=True if self.altair_token.x.type == "quantitative" else False,
                ),
                alt.Y(
                    self.altair_token.y.name,
                    type=self.altair_token.y.type,
                    bin=True if self.altair_token.y.type == "quantitative" else False,
                ),
                alt.Color(
                    self.altair_token.z.name,
                    type=self.altair_token.z.type,
                    trsregate=self.altair_token.z.trsregate,
                ),
            )
        )
