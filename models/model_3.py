import numpy as np
from abc import ABC, abstractmethod

from .baese_model import BaseModel


class Model3(BaseModel, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.directions = {
            0: (0, 0),
            1: (0, 1),
            2: (0, 2),
            3: (1, 2),
            4: (2, 2),
            5: (2, 1),
            6: (2, 0),
            7: (1, 0),
        }

    def get_new_shroom_cell(
        self, x: int, y: int, chance: float, gen: int
    ) -> np.int8 | None:
        if self.shroom_matrix[x, y] > 0:
            return None
        
        neighbour_count = self.get_neighbour_count(x, y)
        if neighbour_count == 0:
            return None
        
        if self.get_neighbours(x, y)[self.directions[gen % 8]] <= 0:
            return None
        
        if self.get_local_growth_probability(neighbour_count) >= chance:
            return np.int8(1)
        
        return None

    @abstractmethod
    def get_local_growth_probability(self, neighbour_count: int):
        pass


class Model3A(Model3):
    def get_local_growth_probability(self, neighbour_count: int):
        match neighbour_count:
            case 1:
                return 0.5
            case _:
                return 0.0


class Model3B(Model3):
    def get_local_growth_probability(self, neighbour_count: int):
        match neighbour_count:
            case 1:
                return 0.5
            case 2:
                return 0.25
            case 3:
                return 0.125
            case _:
                return 0.0
