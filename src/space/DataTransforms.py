from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Union
from .DataModel import Attribute
from .DataTransformsModel import Aggregation, Filter, Sort, Binning
from copy import deepcopy
from config import AggregationType

if TYPE_CHECKING:
    from .Node import VISNode


def apply_aggregation(
    node: "VISNode", by: list[str], type: AggregationType
) -> "VISNode":
    new_node = deepcopy(node)
    new_node.transforms.append(Aggregation(by, type))
    if type == "count":
        new_node.dim += 1
        new_node.attrs.append(Attribute(f"count", "Q", True))

    for i in range(len(new_node.attrs)):
        if new_node.attrs[i].name in by:
            new_node.attrs[i].immutable = True
        else:
            new_node.attrs[i].immutable = True
            # new_node.attrs[i] = Attribute(f"{new_node.attrs[i].name}_{type}", "Q", True)
    return new_node


def apply_filtering(
    node: "VISNode", by: str, value: Union[int, float, str], type: Literal["eq", "neq"]
) -> "VISNode":
    node = node.get_copy()
    node.transforms.append(Filter(by, value, type))

    if type == "eq":
        node.attrs = list(filter(lambda attr: attr.name != by, node.attrs))
        node.dim -= 1

    return node


def apply_sorting(node: "VISNode", by: str, type: Literal["asc", "desc"]) -> "VISNode":
    node = node.get_copy()
    node.transforms.append(Sort(by, type))
    return node


def apply_binning(node: "VISNode", by: str) -> "VISNode":
    node = node.get_copy()
    node.transforms.append(Binning(by))

    for attr in node.attrs:
        if attr.name == by:
            attr.immutable = True
            attr.type = "O"
            break

    return node
