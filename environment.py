import random

class DisasterEnvironment:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.obstacles = []
        self.survivors = []

    def generate_obstacles(self, count):

        for _ in range(count):

            x = random.randint(0, self.width)
            y = random.randint(0, self.height)

            self.obstacles.append((x, y))

    def generate_survivors(self, count):

        for _ in range(count):

            x = random.randint(0, self.width)
            y = random.randint(0, self.height)

            self.survivors.append((x, y))
