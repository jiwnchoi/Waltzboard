from dataclasses import dataclass


# chart_types = [
#     {"name": "Bar Chart", "mark": "bar"},
#     {"name": "Line Chart", "mark": "line"},
#     {"name": "Pie Chart", "mark": "pie"},
#     {"name": "Scatterplot", "mark": "point"},
#     {"name": "Area Chart", "mark": "area"},
#     {"name": "Heatmap", "mark": "rect"},
#     {"name": "Boxplot", "mark": "boxplot"},
#     {"name": "Strip Plot", "mark": "tick"},
# ]


@dataclass
class ChartType:
    name: str
    mark: str

    def to_dict(self):
        return {"name": self.name, "mark": self.mark}


chart_types: list[ChartType] = [
    ChartType("Bar Chart", "bar"),
    ChartType("Line Chart", "line"),
    ChartType("Pie Chart", "pie"),
    ChartType("Scatterplot", "point"),
    ChartType("Area Chart", "area"),
    ChartType("Heatmap", "rect"),
    ChartType("Boxplot", "boxplot"),
    ChartType("Strip Plot", "tick"),
    ChartType("Histogram", "bar"),
]
