import altair as alt
from altair.utils.schemapi import Undefined
from altair import Chart
from .base_chart import BaseChart
from gleaner.utills import x_to_y, y_to_x


class Heatmap(BaseChart):
    def display(self) -> Chart:
        dict_x = {
            "field": self.altair_token.x.name,
            "type": self.altair_token.x.type,
            "bin": True if self.altair_token.x.type == "quantitative" else False,
            "axis": alt.Axis(format="~s" if self.altair_token.y.type == "quantitative" else Undefined),
        }

        dict_y = {
            "field": self.altair_token.y.name,
            "type": self.altair_token.y.type,
            "bin": True if self.altair_token.y.type == "quantitative" else False,
            "axis": alt.Axis(format="~s" if self.altair_token.y.type == "quantitative" else Undefined),
        }

        color = alt.Color(
            self.altair_token.z.name,
            type=self.altair_token.z.type,
            aggregate=self.altair_token.z.aggregate,
            legend=alt.Legend(format="~s" if self.altair_token.z.type == "quantitative" else Undefined),
        )

        x = alt.X(**dict_x)
        y = alt.Y(**dict_y)

        if self.altair_token.x.type == "nominal" and self.altair_token.y.type == "nominal":
            max_len_x = self.df[self.altair_token.x.name].str.len().max()
            max_len_y = self.df[self.altair_token.y.name].str.len().max()
            if max_len_x > max_len_y:
                x = alt.Y(**dict_x)
                y = alt.X(**dict_y)

        elif self.altair_token.x.type == "nominal":
            x = alt.Y(**dict_x)
            y = alt.X(**dict_y)

        return alt.Chart(self.df, title=self.title).mark_rect().encode(x, y, color)
