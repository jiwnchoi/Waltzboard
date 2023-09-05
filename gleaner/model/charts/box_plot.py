import altair as alt
from altair import Chart
from .base_chart import BaseChart


class BoxPlot(BaseChart):
    def display(self) -> Chart:
        c = alt.Chart(self.df, self.title)
        c: alt.Chart = c.mark_boxplot()
        c: alt.Chart = c.encode(
            x=alt.X(
                self.altair_token.x,
            )
        )
        c: alt.Chart = c.encode(y=alt.Y(y=self.altair_token.y))
        c: alt.Chart = c.encode(color=alt.Color(self.altair_token.y))

        return c
