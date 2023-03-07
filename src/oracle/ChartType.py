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



chart_types: dict[str, ChartType] = {
    "bar": ChartType("Bar Chart", "bar"),
    "line": ChartType("Line Chart", "line"),
    "pie": ChartType("Pie Chart", "arc"),
    "scatter": ChartType("Scatterplot", "point"),
    "area": ChartType("Area Chart", "area"),
    "heatmap": ChartType("Heatmap", "rect"),
    "boxplot": ChartType("Boxplot", "boxplot"),
    "stripplot": ChartType("Strip Plot", "tick"),
}
