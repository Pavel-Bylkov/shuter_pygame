import random
class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    @staticmethod
    def random():
        return (random.randint(50, 250), random.randint(50, 250), random.randint(50, 250))
