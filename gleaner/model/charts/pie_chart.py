import altair as alt
from altair import Chart
from .base_chart import BaseChart


class PieChart(BaseChart):
    def display(self) -> Chart:
        c = alt.Chart(self.df, self.title)
        c: alt.Chart = c.mark_arc()
        c: alt.Chart = c.encode(
            color=alt.Color(self.altair_token.x),
            theta=alt.Theta(
                self.altair_token.y,
                aggregate=self.altair_token.agg_y,
            ),
        )
        c: alt.Chart = c.encode(y=alt.Y(y=self.altair_token.y, aggregate=self.altair_token.agg_y))
        c: alt.Chart = c.encode(color=alt.Color(self.altair_token.z))

        return c
