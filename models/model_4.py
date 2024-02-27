import numpy as np
from abc import ABC, abstractmethod

from .baese_model import BaseModel


class Model4(BaseModel, ABC):
    def __init__(self, size: tuple[int, int], start: tuple[int, int]):
        super().__init__(size, start, -4, 5)

    def get_new_shroom_cell(
        self, x: int, y: int, chance: float, gen: int
    ) -> np.int8 | None:
        if self.shroom_matrix[x, y] == 0:
            return None

        neighbour_count = self.get_neighbour_count(x, y)
        if neighbour_count == 0:
            return None

        if self.shroom_matrix[x, y] > 0:
            if self.get_local_age_probability(x, y) >= chance:
                return min(5, self.shroom_matrix[x, y] + 1)
        else:
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

    @abstractmethod
    def get_local_age_probability(self, x: int, y: int):
        pass


class Model4A(Model4):
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

    def get_local_age_probability(self, x: int, y: int):
        if self.get_neighbour_count(x, y) > 2:
            return 0.125
        return 0.0


class Model4B(Model4A):
    def get_local_age_probability(self, x: int, y: int):
        neighbours = self.get_neighbours(x, y)
        cell = self.shroom_matrix[x, y]
        # any cell that is > 0 and < cell is younger so we can't age
        if np.any((0 < neighbours) & (neighbours < cell)):
            return 0.0

        match np.count_nonzero(neighbours > cell):
            case 0:
                if np.count_nonzero(neighbours >= cell) > 3:
                    return 1 / 32
                return 0.0
            case 1:
                return 1 / 16
            case 2:
                return 1 / 8
            case _:
                return 1 / 4
