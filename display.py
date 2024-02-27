import lzma
import pickle
import numpy as np
import pygame
import sys


class Display:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.frames = self.load_frames()
        self.num_frames = len(self.frames)
        self.current_frame = 0
        self.paused = False
        self.clock = pygame.time.Clock()
        self.clock_tick = 15
        self.shape = np.array(self.frames[0].shape) * 10
        self.screen = pygame.display.set_mode(self.shape)
        pygame.display.set_caption("Fungal Growth Simulation")

    def load_frames(self):
        frames = []
        with lzma.open(self.file_name, "rb") as file:
            while True:
                try:
                    frame = pickle.load(file)
                    frames.append(frame)
                except EOFError:
                    break
        return frames

    def recolor_array(self, frame):
        color_palette = {
            # -5: (0, 43, 51),
            # -4: (0, 34, 51),
            # -3: (0, 26, 51),
            # -2: (0, 17, 51),
            # -1: (0, 0, 51),
            -5: (100, 100, 100),
            -4: (75, 75, 75),
            -3: (50, 50, 50),
            -2: (25, 25, 25),
            -1: (0, 0, 0),
            0: (0, 0, 0),
            1: (255, 255, 128),
            2: (255, 170, 0),
            3: (230, 38, 0),
            4: (179, 0, 89),
            5: (102, 0, 153),
        }

        colored_frame = np.zeros(frame.shape + (3,), dtype=np.uint8)

        for value, color in color_palette.items():
            colored_frame[frame == value] = color

        return colored_frame

    def exit(self):
        pygame.quit()
        sys.exit()

    def pause(self, toggle: bool = False):
        if toggle:
            self.paused = not self.paused
        else:
            self.paused = True

    def next_frame(self):
        self.current_frame = (self.current_frame + 1) % self.num_frames

    def prev_frame(self):
        self.current_frame = max(self.current_frame - 1, 0)

    def increase_speed(self):
        self.clock_tick = min(self.clock_tick * 1.1, 240)
        self.clock.tick(self.clock_tick)

    def decrease_speed(self):
        self.clock_tick = max(self.clock_tick / 1.1, 1)
        self.clock.tick(self.clock_tick)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        self.exit()
                    elif event.key == pygame.K_SPACE:
                        self.pause(toggle=True)
                    elif event.key == pygame.K_RIGHT:
                        self.next_frame()
                    elif event.key == pygame.K_LEFT:
                        self.prev_frame()
                    elif event.key == pygame.K_UP:
                        self.increase_speed()
                    elif event.key == pygame.K_DOWN:
                        self.decrease_speed()

            if not self.paused:
                self.next_frame()

            # Automatically pause at the end of frames
            if self.current_frame == self.num_frames - 1:
                self.pause()

            frame = self.frames[self.current_frame]

            # Color the frame
            colored_frame = self.recolor_array(frame)

            # Create a Pygame surface from the colored frame
            surface = pygame.surfarray.make_surface(colored_frame)

            # Resize the surface to fit the screen
            surface = pygame.transform.scale(surface, self.shape)

            # Display the surface
            self.screen.blit(surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.clock_tick)



FILENAME = "model_3a"

def main():
    Display(f"log/{FILENAME}.pkl").run()


if __name__ == "__main__":
    main()
