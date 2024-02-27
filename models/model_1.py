import numpy as np
from abc import ABC, abstractmethod

from .baese_model import BaseModel


class Model1(BaseModel, ABC):
    def get_new_shroom_cell(
        self, x: int, y: int, chance: float, gen: int
    ) -> np.int8 | None:
        if self.shroom_matrix[x, y] > 0:
            return None
        
        neighbour_count = self.get_neighbour_count(x, y)
        if neighbour_count == 0:
            return None
        
        if self.get_local_growth_probability(neighbour_count) >= chance:
            return np.int8(1)
    
        return None

    @abstractmethod
    def get_local_growth_probability(self, neighbour_count: int):
        pass


class Model1A(Model1):
    def get_local_growth_probability(self, neighbour_count: int):
        match neighbour_count:
            case 1:
                return 0.125
            case 2:
                return 0.25
            case 3:
                return 0.5
            case _:
                return 0.0


class Model1B(Model1):
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


class Model1C(Model1):
    def get_local_growth_probability(self, neighbour_count: int):
        match neighbour_count:
            case 1:
                return 0.125
            case _:
                return 0.0
