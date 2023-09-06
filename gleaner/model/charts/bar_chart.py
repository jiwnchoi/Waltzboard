import altair as alt
from altair import Chart
from altair.utils.schemapi import Undefined
from .base_chart import BaseChart


class SingleBarChart(BaseChart):
    def display(self) -> Chart:
        x = alt.X(
            self.altair_token.x.name,
            type=self.altair_token.x.type,
            timeUnit=self.altair_token.x.aggregate if self.altair_token.x.aggregate != "bin" else Undefined,
            bin=True if self.altair_token.x.aggregate == "bin" else False,
        )
        y = alt.Y(
            self.altair_token.y.name,
            type=self.altair_token.y.type,
            aggregate=self.altair_token.y.aggregate,
        )
        return alt.Chart(self.df, title=self.title).mark_bar().encode(x, y)


class MultipleBarChart(BaseChart):
    def display(self) -> Chart:
        c = (
            alt.Chart(self.df, title=self.title)
            .mark_bar()
            .encode(
                alt.X(
                    self.altair_token.x.name,
                    type=self.altair_token.x.type,
                    timeUnit=self.altair_token.x.aggregate,
                    bin=True if self.altair_token.x.aggregate == "bin" else False,
                ),
                alt.Y(
                    self.altair_token.y.name,
                    type=self.altair_token.y.type,
                    aggregate=self.altair_token.y.aggregate,
                ),
                alt.Color(self.altair_token.z.name, type=self.altair_token.z.type),
            )
        )

        if self.altair_token.y.aggregate != "sum":
            c = c.encode(alt.XOffset(self.altair_token.z.name, type=self.altair_token.z.type))

        return c
