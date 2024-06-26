from abc import ABC, abstractmethod
from typing import Dict

from praatio.textgrid import Textgrid

# Base metric interface


class Metric(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def __call__(self, target: Dict[str, Textgrid], align: Dict[str, Textgrid]) -> float:
        pass
