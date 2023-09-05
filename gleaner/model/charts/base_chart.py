from dataclasses import dataclass
from altair import Chart
from altair.utils.schemapi import UndefinedType, Undefined
from abc import ABCMeta, abstractmethod
import pandas as pd
from gleaner.model import ChartTokens, AggTypes, AggXTypes, ChartSampled
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from gleaner.model.attribute import Attribute, AttributeNotNull


class BaseChart:
    tokens: ChartTokens
    df: pd.DataFrame
    attrs: list["Attribute | AttributeNotNull"]
    num_attrs: int
    agg_types: list[AggXTypes | AggTypes]
    num_aggs: int

    def __init__(self, result: ChartSampled, df: pd.DataFrame) -> None:
        mark, x, y, z, tx, ty, tz = result
        self.tokens: ChartTokens = (
            mark,
            x.name,
            y.name,
            z.name,
            tx,
            ty,
            tz,
        )
        self.df = df
        self.attrs = [x, y, z]
        self.num_attrs = len([a.name for a in self.attrs if a.name])
        self.agg_types = [tx, ty, tz]
        self.num_aggs = len([a for a in self.agg_types if a])
        self.title, self.title_tokens = self.get_title()
        self.altair_token = self.get_altair_token()

    def get_title(self) -> tuple[str, list[str]]:
        value_field = self.attrs[-1].name
        value_agg = self.agg_types[-1] if self.num_aggs else None

        tokens: list[list[str | None]] = [
            [f"{value_agg[0].upper()}{value_agg[1:]}"] if value_agg else [],
            ["of"] if value_agg else [],
            [f"{value_field}"],
            ["by", self.attrs[0].name, "and", self.attrs[1].name] if self.num_attrs == 3 else [],
            ["by", self.attrs[0].name] if self.num_attrs == 2 else [],
        ]
        tokens_words = [str(w) for t in tokens for w in t]
        return " ".join(tokens_words), tokens_words

    def get_coverage(self) -> dict[str, float]:
        coverage = {a.name: 1.0 for a in self.attrs if a.name}
        if self.tokens[4]:
            coverage[self.tokens[1]] *= 0.25
        if self.tokens[2] and self.tokens[5]:
            coverage[self.tokens[2]] *= 0.25
        if self.tokens[3] and self.tokens[6]:
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
    y: str | UndefinedType
    z: str | UndefinedType
    agg_x: str | UndefinedType
    agg_y: str | UndefinedType
    agg_z: str | UndefinedType
