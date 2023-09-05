from dataclasses import dataclass
from altair import Chart, Undefined
from abc import ABCMeta, abstractmethod
import pandas as pd
from gleaner.model import AllTokenTypes, ChartTokens, AggTypes, AggXTypes
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from gleaner.model.attribute import Attribute


class BaseChart(metaclass=ABCMeta):
    tokens: ChartTokens
    df: pd.DataFrame
    attrs: list["Attribute"]
    num_attrs: int
    agg_types: list[AggXTypes | AggTypes]
    num_aggs: int

    def __init__(self, result: list, df: pd.DataFrame) -> None:
        mark, x, y, z, tx, ty, tz = result
        self.tokens: ChartTokens = (
            mark,
            x.name if x else None,
            y.name if y else None,
            z.name if z else None,
            tx,
            ty,
            tz,
        )
        self.df = df
        self.attrs = [x, y, z]
        self.num_attrs = len([a.name for a in self.attrs if a.name])
        self.agg_types = [a for a in [self.tokens[4], self.tokens[5], self.tokens[6]]]
        self.num_aggs = len([a for a in self.agg_types if a])
        self.title, self.title_tokens = self.get_title()
        self.altair_token = self.get_altair_token()

    def get_title(self) -> tuple[str, list[str]]:
        value_field = self.attrs[-1].name
        value_agg = self.agg_types[-1] if self.num_aggs else None

        tokens: list[str] = [
            [f"{value_agg[0].upper()}{value_agg[1:]}"] if value_agg else [],
            ["of"] if value_agg else [],
            [f"{value_field}"],
            ["by", self.attrs[0].name, "and", self.attrs[1].name] if self.num_attrs == 3 else [],
            ["by", self.attrs[0].name] if self.num_attrs == 2 else [],
        ]
        tokens = [token for token_list in tokens for token in token_list]
        return " ".join(tokens), tokens

    def get_coverage(self) -> dict[str, float]:
        coverage = {a.name: 1.0 for a in self.attrs if a.name}
        if self.tokens[4]:
            coverage[self.tokens[1]] *= 0.25
        if self.tokens[5]:
            coverage[self.tokens[2]] *= 0.25
        if self.tokens[6]:
            coverage[self.tokens[3]] *= 0.25
        return coverage

    def get_vegalite(self) -> str:
        chart = self.display()
        chart.configure_legend(title=None)
        return chart.to_json()

    def get_bov(self) -> set[str]:
        bot = set([self.tokens[0]])
        bot.update([a.name for a in self.attrs if a.name])
        if self.tokens[4]:
            bot.update([f"aggx_{self.tokens[4]}"])
        if self.tokens[5]:
            bot.update([f"aggy_{self.tokens[5]}"])
        if self.tokens[6]:
            bot.update([f"aggz_{self.tokens[6]}"])
        return bot

    def get_altair_token(self):
        return AltairToken(
            self.tokens[0],
            f"{self.attrs[0].name}:{self.attrs[0].type}",
            f"{self.attrs[1].name}:{self.attrs[1].type}" if self.attrs[1] else Undefined,
            f"{self.attrs[2].name}:{self.attrs[2].type}" if self.attrs[2] else Undefined,
            self.tokens[4] if self.tokens[4] else Undefined,
            self.tokens[5] if self.tokens[5] else Undefined,
            self.tokens[6] if self.tokens[6] else Undefined,
        )

    @abstractmethod
    def display(self) -> Chart:
        raise NotImplementedError


@dataclass
class AltairToken:
    mark: str
    x: str
    y: str | Undefined
    z: str | Undefined
    agg_x: str | Undefined
    agg_y: str | Undefined
    agg_z: str | Undefined
