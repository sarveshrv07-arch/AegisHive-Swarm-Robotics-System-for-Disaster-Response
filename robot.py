import random
import math

class RescueRobot:

    def __init__(self, robot_id, x, y):

        self.robot_id = robot_id

        self.x = x
        self.y = y

        self.battery = 100

        self.detected_survivors = []

    def move(self):

        direction = random.choice([
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ])

        self.x += direction[0]
        self.y += direction[1]

        self.battery -= 0.1

    def detect_survivor(self, environment):

        for survivor in environment.survivors:

            distance = math.dist(
                (self.x, self.y),
                survivor
            )

            if distance < 3:

                self.detected_survivors.append(survivor)

                return survivor

        return None
