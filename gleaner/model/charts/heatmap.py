import altair as alt
from altair import Chart
from .base_chart import BaseChart


class Heatmap(BaseChart):
    def display(self) -> Chart:
        c = alt.Chart(self.df, self.title)
        c: alt.Chart = c.mark_rect()
        c: alt.Chart = c.encode(
            x=alt.X(self.altair_token.x, bin=True if self.altair_token.x[-1] == "Q" else False),
            y=alt.Y(
                self.altair_token.y,
                bin=True if isinstance(self.altair_token.y, str) and self.altair_token.y[-1] == "Q" else False,
            ),
            color=alt.Color(self.altair_token.z, aggregate=self.altair_token.agg_z),
        )
        return c
