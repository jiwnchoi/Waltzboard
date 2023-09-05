import altair as alt
from altair import Chart
from .base_chart import BaseChart


class SingleBarChart(BaseChart):
    def display(self) -> Chart:
        c = alt.Chart(self.df, self.title)
        c: alt.Chart = c.mark_bar()
        c: alt.Chart = c.encode(
            x=alt.X(
                self.altair_token.x,
                timeUnit=self.altair_token.agg_x,
            )
        )
        c: alt.Chart = c.encode(y=alt.Y(y=self.altair_token.y, aggregate=self.altair_token.agg_y))
        return c


class MultipleBarChart(BaseChart):
    def display(self) -> Chart:
        c = alt.Chart(self.df, self.title)
        c: alt.Chart = c.mark_bar()
        c: alt.Chart = c.encode(
            x=alt.X(
                self.altair_token.x,
                timeUnit=self.altair_token.agg_x,
            )
        )

        c: alt.Chart = c.encode(
            y=alt.Y(
                self.altair_token.y,
                aggregate=self.altair_token.agg_y,
            )
        )

        if self.self.altair_token[5] == "sum":
            c: alt.Chart = c.encode(color=alt.Color(self.altair_token.z))
        else:
            c: alt.Chart = c.encode(color=alt.Color(self.altair_token.z))
            c: alt.Chart = c.encode(xOffset=alt.XOffset(self.altair_token.z))

        return c
