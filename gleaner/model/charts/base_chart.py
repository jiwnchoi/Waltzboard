from dataclasses import dataclass
from altair import Chart
from altair.utils.schemapi import UndefinedType, Undefined
from abc import abstractmethod
import pandas as pd

from typing import TYPE_CHECKING

from gleaner.model import ChartTokens, AggTypes, AggXTypes, ChartSampled

if TYPE_CHECKING:
    from gleaner.model.attribute import Attribute


class BaseChart:
    tokens: ChartTokens
    df: pd.DataFrame
    sub_df: pd.DataFrame
    attrs: list["Attribute"]
    num_attrs: int
    agg_types: list[AggXTypes | AggTypes]
    num_aggs: int

    def __init__(self, result: ChartSampled, df: pd.DataFrame) -> None:
        mark, x, y, z, tx, ty, tz = result
        self.tokens: ChartTokens = (
            mark,
            x.name,  # type: ignore
            y.name,
            z.name,
            tx,
            ty,
            tz,
        )
        self.df = df
        self.attrs = [x, y, z]
        self.sub_df = df[[a.name for a in self.attrs if a.name]]
        self.num_attrs = len([a.name for a in self.attrs if a.name])
        self.agg_types = [tx, ty, tz]
        self.num_aggs = len([a for a in self.agg_types if a])
        self.title, self.title_tokens = self.get_title()
        self.altair_token = self.get_altair_token()

    def get_title(self) -> tuple[str, list[str]]:
        value_field_name = self.attrs[self.num_attrs - 1].name if self.num_attrs else None
        value_agg = self.agg_types[self.num_aggs - 1] if self.num_aggs else None

        tokens: list[list[str | None]] = [
            [f"{value_agg[0].upper()}{value_agg[1:]}"] if value_agg else [],
            ["of"] if value_agg else [],
            [f"{value_field_name}"],
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

    def get_bot(self) -> set[str]:
        bot = set([t for t in self.tokens if t])
        # if self.tokens[4]:
        #     bot.update([f"aggx_{self.tokens[4]}"])
        # if self.tokens[5]:
        #     bot.update([f"aggy_{self.tokens[5]}"])
        # if self.tokens[6]:
        #     bot.update([f"aggz_{self.tokens[6]}"])
        return bot

    def get_altair_token(self):
        return AltairToken(
            mark=self.tokens[0],
            x=AltairAttribute(self.attrs[0].name, self.attrs[0].long_type(), self.tokens[4]),
            y=AltairAttribute(self.attrs[1].name, self.attrs[1].long_type(), self.tokens[5]),
            z=AltairAttribute(self.attrs[2].name, self.attrs[2].long_type(), self.tokens[6]),
        )

    @abstractmethod
    def display(self) -> Chart:
        raise NotImplementedError


class AltairAttribute:
    name: str | UndefinedType
    type: str | UndefinedType
    aggregate: str | UndefinedType

    def __init__(self, name, type, aggregate) -> None:
        self.name = name if name else Undefined
        self.type = type if type else Undefined
        self.aggregate = aggregate if aggregate else Undefined

    def __repr__(self) -> str:
        return f"{self.name} {self.type} {self.aggregate}"


@dataclass
class AltairToken:
    mark: str
    x: AltairAttribute
    y: AltairAttribute
    z: AltairAttribute
