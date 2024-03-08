import altair as alt
from altair import Chart
from altair.utils.schemapi import Undefined

from .base_chart import BaseChart


class SingleBarChart(BaseChart):
    def display(self) -> Chart:
        dict_x = {
            "field": self.altair_token.x.name,
            "type": self.altair_token.x.type,
            "timeUnit": self.altair_token.x.aggregate
            if self.altair_token.x.aggregate != "bin"
            else Undefined,
            "bin": True if self.altair_token.x.aggregate == "bin" else False,
        }

        dict_y = {
            "field": self.altair_token.y.name,
            "type": self.altair_token.y.type,
            "aggregate": self.altair_token.y.aggregate,
            "axis": alt.Axis(
                format="~s" if self.altair_token.y.type == "quantitative" else Undefined
            ),
        }

        x = alt.X(**dict_x)
        y = alt.Y(**dict_y)

        if (
            self.altair_token.x.type == "nominal"
            and self.altair_token.y.type == "nominal"
        ):
            max_len_x = self.df[self.altair_token.x.name].str.len().max()
            max_len_y = self.df[self.altair_token.y.name].str.len().max()
            if max_len_x > max_len_y:
                x = alt.Y(**dict_x)
                y = alt.X(**dict_y)

        elif self.altair_token.x.type == "nominal":
            x = alt.Y(**dict_x)
            y = alt.X(**dict_y)

        return alt.Chart(self.df, title=self.title).mark_bar().encode(x, y)


class MultipleBarChart(BaseChart):
    def display(self) -> Chart:
        dict_x = {
            "field": self.altair_token.x.name,
            "type": self.altair_token.x.type,
            "timeUnit": self.altair_token.x.aggregate
            if self.altair_token.x.aggregate != "bin"
            else Undefined,
            "bin": True if self.altair_token.x.aggregate == "bin" else False,
        }

        dict_y = {
            "field": self.altair_token.y.name,
            "type": self.altair_token.y.type,
            "aggregate": self.altair_token.y.aggregate,
            "axis": alt.Axis(
                format="~s" if self.altair_token.y.type == "quantitative" else Undefined
            ),
        }

        x = alt.X(**dict_x)
        y = alt.Y(**dict_y)
        xOffset = None
        color = None

        if self.altair_token.y.aggregate == "sum":
            color = alt.Color(
                self.altair_token.z.name,
                type=self.altair_token.z.type,
            )

        else:
            xOffset = alt.XOffset(
                self.altair_token.z.name,
                type=self.altair_token.z.type,
            )
            color = alt.Color(
                self.altair_token.z.name,
                type=self.altair_token.z.type,
            )

        if (
            self.altair_token.x.type == "nominal"
            and self.altair_token.y.type == "nominal"
        ):
            max_len_x = self.df[self.altair_token.x.name].str.len().max()
            max_len_y = self.df[self.altair_token.y.name].str.len().max()
            if max_len_x > max_len_y:
                x = alt.Y(**dict_x)
                y = alt.X(**dict_y)

        elif self.altair_token.x.type == "nominal":
            x = alt.Y(**dict_x)
            y = alt.X(**dict_y)

        chart = alt.Chart(self.df, title=self.title).mark_bar().encode(x, y)

        if xOffset:
            chart = chart.encode(xOffset)

        if color:
            chart = chart.encode(color)

        return chart
