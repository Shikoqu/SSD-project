import numpy as np
import lzma
import time


class CellAutoma:
    def __init__(
        self, Model: type, size: tuple[int, int], start: tuple[int, int] = None
    ):
        start = start or (int(size[0] // 2), int(size[1] // 2))
        self.shroom_matrix = Model(size, start)
        self.stop_conditions = {
            "one_border": self.one_border,
            "one_corner": self.one_corner,
            "all_borders": self.all_borders,
            "all_corners": self.all_corners,
            "one_b": self.one_border,
            "one_c": self.one_corner,
            "all_b": self.all_borders,
            "all_c": self.all_corners,
        }

    def one_border(self):
        return any(
            any(cell > 0 for cell in border)
            for border in self.shroom_matrix.get_borders()
        )

    def all_borders(self):
        return all(
            any(cell > 0 for cell in border)
            for border in self.shroom_matrix.get_borders()
        )

    def one_corner(self):
        return any(
            any(cell > 0 for cell in corner.flatten())
            for corner in self.shroom_matrix.get_corners()
        )

    def all_corners(self):
        return all(
            any(cell > 0 for cell in corner.flatten())
            for corner in self.shroom_matrix.get_corners()
        )

    def run(
        self,
        file_name: str,
        stop_condition: str = "one_border",
        max_generations: int = None,
    ):
        i = 0
        check_stop = self.stop_conditions[stop_condition]
        with lzma.open(file_name, "wb") as file:
            self.shroom_matrix.save_state(file)
            
            max_fail_counter = 10
            fail_counter = 0
            while True:
                start = time.time()
                if not self.shroom_matrix.grow(i):
                    fail_counter += 1
                    if fail_counter >= max_fail_counter:
                        print(f"No changes for {max_fail_counter} generations. Stopping...")
                        break

                self.shroom_matrix.save_state(file)
                print(f"Gen {i}   \t- {format(time.time() - start, '.4f')} s")

                if check_stop():
                    break
                if max_generations is not None and i >= max_generations:
                    break
                i -= -1
