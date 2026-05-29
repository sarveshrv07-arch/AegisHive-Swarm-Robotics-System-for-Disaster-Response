import random
import math
from config import MAP_WIDTH, MAP_HEIGHT, GRID_SIZE, TOTAL_GRID_CELLS

class RescueRobot:

    def __init__(self, robot_id, x, y):

        self.target_zone = random.choice([
          "top",
          "bottom",
          "left",
          "right"
        ])

        self.robot_id = robot_id

        self.x = x
        self.y = y

        self.battery = 100

        self.drain_rate = random.uniform(0.05, 0.15)

        self.charging = False

        self.path = []

        self.detected_survivors = []
        self.unique_explored = set()

        self.exploration_bias = random.choice([
           (1, 0),
           (-1, 0),
           (0, 1),
           (0, -1)
        ])

    def move(self, environment, global_explored):

        # Actual charging mode

        if self.battery < 20:
                       self.charging = True

        # Charging behavior

        if self.charging:

            # Biased movement toward base

           move_x = 0
           move_y = 0

        # Direct fast return to base

           if self.x > 5:
               move_x = random.choice([-2, -1, 0])

           elif self.x < 5:
               move_x = random.choice([0, 1, 2])

           if self.y > 5:
               move_y = random.choice([-2, -1, 0])

           elif self.y < 5:
               move_y = random.choice([0, 1, 2])

           self.x += move_x
           self.y += move_y

        # Recharge at base

           if abs(self.x - 5) < 3 and abs(self.y - 5) < 3:

              self.battery += 0.5

              if self.battery >= 80:

                  self.charging = False

           return
        # battery drain

        self.battery -= self.drain_rate

        # store path

        

        possible_moves = []

        possible_moves = [

         (5, 0),
         (-5, 0),
         (0, 5),
         (0, -5),

         (5, 5),
         (-5, -5),
         (5, -5),
         (-5, 5),

         (8, 0),
         (-8, 0),
         (0, 8),
         (0, -8),

         (10, 5),
         (-10, 5),
         (10, -5),
         (-10, -5),

         (5, 10),
         (-5, 10),
         (5, -10),
         (-5, -10)
        ]
        best_move = None
        lowest_visit = float('inf')

        random.shuffle(possible_moves)

        for move in possible_moves:

              new_x = self.x + move[0]
              new_y = self.y + move[1]

              visit_score = 0

              # Normal exploration memory

              if self.battery > 35:

                 if (new_x, new_y) in global_explored:

                        visit_score += 1
              # Random exploration factor

              visit_score += random.uniform(0, 2)


              # Prioritize obstacle-heavy area

              obstacle_bonus = 0

              for obstacle in environment.obstacles:

                  distance = abs(new_x - obstacle[0]) + abs(new_y - obstacle[1])

                  if distance < 15:

                      obstacle_bonus -= 0.2

              visit_score += obstacle_bonus

              # Encourage large-distance exploration

              distance_bonus = abs(move[0]) + abs(move[1])

              visit_score -= distance_bonus * 0.05

              # Edge penalty

              if new_x < 10 or new_x > MAP_WIDTH - 10:
                                         visit_score += 3

              if new_y < 10 or new_y > MAP_HEIGHT - 10:
                                         visit_score += 3
                                         
              # Avoid staying too close to current position

              distance_from_current = abs(move[0]) + abs(move[1])

              if distance_from_current <= 1:

                  visit_score += 0.5

              if visit_score < lowest_visit:

                  lowest_visit = visit_score
                  best_move = move

        self.x += best_move[0]
        self.y += best_move[1]

        self.x = max(0, min(self.x, MAP_WIDTH))
        self.y = max(0, min(self.y, MAP_HEIGHT))

        trail_x = self.x
        trail_y = self.y
        
        grid_x = int(self.x // GRID_SIZE)
        grid_y = int(self.y // GRID_SIZE)

        cell = (grid_x, grid_y)

        if cell not in global_explored:

            global_explored.add(cell)

            self.unique_explored.add(cell)

            self.path.append((trail_x, trail_y))

    
        # Keep robots inside map boundaries

        # Boundary handling

        if self.x <= 0:
               self.x += 2

        if self.y <= 0:
               self.y += 2

        if self.x >= MAP_WIDTH:
               self.x -= 2

        if self.y >= MAP_HEIGHT:
               self.y -= 2
        self.x = int(self.x)
        self.y = int(self.y)

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
