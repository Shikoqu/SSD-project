from abc import ABC, abstractmethod
import numpy as np
import pickle


class BaseModel(ABC):
    def __init__(
        self,
        size: tuple[int, int],
        start: tuple[int, int],
        background_value=0,
        start_value=1,
    ):
        self.shroom_matrix = np.full(size, background_value, dtype=np.int8)
        self.shroom_matrix[start] = start_value

    def roll_chances(self) -> np.ndarray:
        # mean = 127.5
        # std = 40
        # size = self.shroom_matrix.shape
        # samples = np.random.normal(mean, std, size)

        # # Reject values outside the valid range
        # while np.any(samples < 0) or np.any(samples > 255):
        #     invalid_indices = (samples < 0) | (samples > 255)
        #     samples[invalid_indices] = np.random.normal(
        #         mean, std, np.count_nonzero(invalid_indices)
        #     )
        # return samples.astype(np.uint8)
        return np.random.random(self.shroom_matrix.shape)

    def get_neighbours(self, x: int, y: int) -> np.ndarray:
        return self.shroom_matrix[x - 1 : x + 2, y - 1 : y + 2]

    def get_neighbour_count(self, x: int, y: int, stage: int = 0) -> int:
        return np.count_nonzero(self.get_neighbours(x, y) > stage)

    def get_borders(self):
        return [
            self.shroom_matrix[1, :],
            self.shroom_matrix[-2, :],
            self.shroom_matrix[:, 1],
            self.shroom_matrix[:, -2],
        ]

    def get_corners(self):
        return [
            self.shroom_matrix[1:4, 1:4],
            self.shroom_matrix[-4:-1, 1:4],
            self.shroom_matrix[1:4, -4:-1],
            self.shroom_matrix[-4:-1, -4:-1],
        ]

    def save_state(self, file):
        pickle.dump(self.shroom_matrix, file)

    def grow(self, gen):
        chances = self.roll_chances()
        new_shroom_matrix = self.shroom_matrix.copy()

        for x in range(1, self.shroom_matrix.shape[0] - 1):
            for y in range(1, self.shroom_matrix.shape[1] - 1):
                new_shroom = self.get_new_shroom_cell(x, y, chances[x, y], gen)
                if new_shroom is not None:
                    new_shroom_matrix[x, y] = new_shroom

        if np.all(new_shroom_matrix == self.shroom_matrix):
            return False

        self.shroom_matrix = new_shroom_matrix
        return True

    @abstractmethod
    def get_new_shroom_cell(
        self, x: int, y: int, chance: float, gen: int
    ) -> np.int8 | None:
        pass
