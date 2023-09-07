import altair as alt
from altair import Chart
from altair.utils.schemapi import Undefined
from .base_chart import BaseChart


class SingleBarChart(BaseChart):
    def display(self) -> Chart:
        x = alt.X(
            self.altair_token.x.name,
            type=self.altair_token.x.type,
            timeUnit=self.altair_token.x.trsregate if self.altair_token.x.trsregate != "bin" else Undefined,
            bin=True if self.altair_token.x.trsregate == "bin" else False,
        )
        y = alt.Y(
            self.altair_token.y.name,
            type=self.altair_token.y.type,
            trsregate=self.altair_token.y.trsregate,
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
                    timeUnit=self.altair_token.x.trsregate,
                    bin=True if self.altair_token.x.trsregate == "bin" else False,
                ),
                alt.Y(
                    self.altair_token.y.name,
                    type=self.altair_token.y.type,
                    trsregate=self.altair_token.y.trsregate,
                ),
                alt.Color(self.altair_token.z.name, type=self.altair_token.z.type),
            )
        )

        if self.altair_token.y.trsregate != "sum":
            c = c.encode(alt.XOffset(self.altair_token.z.name, type=self.altair_token.z.type))

        return c
