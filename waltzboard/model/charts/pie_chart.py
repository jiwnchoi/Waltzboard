import altair as alt
from altair import Chart

from .base_chart import BaseChart


class PieChart(BaseChart):
    def display(self) -> Chart:
        return (
            alt.Chart(self.df, title=self.title)
            .mark_arc()
            .encode(
                alt.Color(
                    self.altair_token.x.name,
                    type=self.altair_token.x.type,
                    aggregate=self.altair_token.x.aggregate,
                ),
                alt.Theta(
                    self.altair_token.y.name,
                    type=self.altair_token.y.type,
                    aggregate=self.altair_token.y.aggregate,
                ),
            )
        )
