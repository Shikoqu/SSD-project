from cell_automa import CellAutoma

from models import Model1A, Model1B, Model1C, Model2A, Model3A, Model3B, Model4A, Model4B
from display import Display


MODEL = Model3A
SHAPE = (100, 100)
FILENAME = "model_3a"

def print_params():
    print("-"*40)
    print(f"MODEL: {MODEL}")
    print(f"SHAPE: {SHAPE}")
    print(f"FILENAME: {FILENAME}")
    print("-"*40)


def main():
    print_params()
    automa = CellAutoma(MODEL, SHAPE)
    automa.run(f"log/{FILENAME}.pkl", stop_condition="all_c", max_generations=None)
    
    Display(f"log/{FILENAME}.pkl").run()


if __name__ == "__main__":
    main()
