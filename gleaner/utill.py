# type: ignore

import pandas as pd
from IPython.display import clear_output, display
import altair as alt


def display_function(epoch, train_results):
    data = pd.DataFrame(
        {
            "epoch": range(epoch + 1),
            "scores": [r.scores.mean() for r in train_results],
            "maxs": [r.scores.max() for r in train_results],
            "specificity": [r.specificity.mean() for r in train_results],
            "interestingness": [r.interestingness.mean() for r in train_results],
            "coverage": [r.coverage.mean() for r in train_results],
            "diversity": [r.diversity.mean() for r in train_results],
            "conciseness": [r.conciseness.mean() for r in train_results],
            "n_charts": [r.n_charts.mean() for r in train_results],
        }
    )
    if epoch % 5 == 0:
        clear_output(wait=True)
        print(f"Epoch {epoch}")
        line = (
            alt.Chart(data)
            .mark_line()
            .encode(
                x="epoch",
            )
            .properties(width=150, height=100)
        )
        display(
            (
                line.encode(y=alt.Y("scores", scale=alt.Scale(zero=False)))
                | line.encode(y=alt.Y("maxs", scale=alt.Scale(zero=False)))
            )
            & (
                line.encode(y=alt.Y("specificity", scale=alt.Scale(zero=False)))
                | line.encode(y=alt.Y("interestingness", scale=alt.Scale(zero=False)))
                | line.encode(y=alt.Y("coverage", scale=alt.Scale(zero=False)))
                | line.encode(y=alt.Y("diversity", scale=alt.Scale(zero=False)))
                | (
                    line.encode(y=alt.Y("conciseness", scale=alt.Scale(zero=False)))
                    + line.encode(
                        y=alt.Y("n_charts", scale=alt.Scale(zero=False))
                    ).mark_line(color="orange")
                ).resolve_scale(y="independent")
            )
        )
