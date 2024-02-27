import numpy as np
from abc import ABC, abstractmethod

from .baese_model import BaseModel


class Model2(BaseModel, ABC):
    def __init__(self, size: tuple[int, int], start: tuple[int, int]):
        super().__init__(size, start, -5)

    def get_new_shroom_cell(
        self, x: int, y: int, chance: float, gen: int
    ) -> np.int8 | None:
        if self.shroom_matrix[x, y] >= 0:
            return None

        neighbour_count = self.get_neighbour_count(x, y)
        if neighbour_count == 0:
            return None

        if self.get_local_growth_probability(neighbour_count) >= chance:
            return np.int8(1)

        if self.get_local_eat_probability(neighbour_count) >= chance:
            return self.shroom_matrix[x, y] + 1

        return None

    @abstractmethod
    def get_local_growth_probability(self, neighbour_count: int):
        pass

    @abstractmethod
    def get_local_eat_probability(self, neighbour_count: int):
        pass


class Model2A(Model2):
    def get_local_growth_probability(self, neighbour_count: int):
        match neighbour_count:
            case 1:
                return 0.125
            case _:
                return 0.0

    def get_local_eat_probability(self, neighbour_count: int):
        match neighbour_count:
            case 0:
                return 0.0
            case 1:
                return 0.5
            case 2:
                return 0.75
            case _:
                return 1.0
