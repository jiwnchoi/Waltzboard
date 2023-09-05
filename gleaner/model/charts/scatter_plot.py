import altair as alt
from altair import Chart
from altair.utils.schemapi import UndefinedType
from .base_chart import BaseChart


class ScatterPlot(BaseChart):
    def display(self) -> Chart:
        c = alt.Chart(self.df, self.title)
        c: alt.Chart = c.mark_circle()
        c: alt.Chart = c.encode(
            x=alt.X(
                self.altair_token.x,
            )
        )
        c: alt.Chart = c.encode(y=alt.Y(y=self.altair_token.y, aggregate=self.altair_token.agg_y))
        c: alt.Chart = c.encode(
            color=alt.Color(
                self.altair_token.z,
                bin=True if isinstance(self.altair_token.z, str) and self.altair_token.z[-1] == "Q" else False,
            )
        )
        return c
