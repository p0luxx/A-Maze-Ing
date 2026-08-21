from .grid import Grid


class MazeGnerator():
    def __init__(self, width: int, height: int, seed: int, entry: tuple[int, int], end: tuple[int, int], output_file: str, perfect: bool = False):
        self.width = width
        self.height = height
        self.seed = seed
        self.entry = entry
        self.end = end
        self.output_file = output_file
        self.perfect = perfect

    def check_parameters(self):
        pass

    def chose_algorithm(self):
        if self.perfect == True:
            #seleccionar algoritmo para perfect
        else:
            #seleccionar algoritmo para no_perfect
