from dataclasses import dataclass
from src.oracle import OracleWeight


@dataclass
class Task:
    name: str
    weight: OracleWeight
    chartTypes: list
