import dataclasses
from typing import Callable, Optional


@dataclasses.dataclass
class Function:
    function: Callable
    representation: str
    weight: Optional[Callable] = None
    integral: Optional[Callable] = None
    derivative: Optional[Callable] = None
