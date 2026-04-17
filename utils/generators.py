import random
from typing import List, Union, Callable

class Generator:
    """Base class for time interval generators."""
    def __next__(self) -> float:
        raise NotImplementedError

    def get_desc(self, _t) -> str:
        return ""

    def __iter__(self):
        return self

class ConstantGenerator(Generator):
    """Generates a constant value."""
    def __init__(self, value: float):
        self.value = value

    def __next__(self) -> float:
        return self.value

    def get_desc(self, _t) -> str:
        return f"({self.value})"

class ListGenerator(Generator):
    """Generates values from a list, then can repeat the last or return 0."""
    def __init__(self, values: List[float], repeat_last: bool = True):
        self.values = values
        self.index = 0
        self.repeat_last = repeat_last

    def __next__(self) -> float:
        if self.index < len(self.values):
            val = self.values[self.index]
            self.index += 1
            return val
        if self.repeat_last and self.values:
            return self.values[-1]
        return 0.0

    def get_desc(self, _t) -> str:
        return f"({_t('gen_list_type')})"

class ExponentialGenerator(Generator):
    """Generates values following an exponential distribution (not used in tables but common)."""
    def __init__(self, mean: float):
        self.mean = mean

    def __next__(self) -> float:
        return random.expovariate(1.0 / self.mean)

    def get_desc(self, _t) -> str:
        return f"(Exp={self.mean})"
