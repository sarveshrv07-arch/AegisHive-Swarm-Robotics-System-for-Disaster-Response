import pygame

from config import *
from environment import DisasterEnvironment
from robot import RescueRobot

pygame.init()

screen = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)

pygame.display.set_caption("AegisHive")

clock = pygame.time.Clock()

environment = DisasterEnvironment(
    MAP_WIDTH,
    MAP_HEIGHT
)

environment.generate_obstacles(100)
environment.generate_survivors(SURVIVOR_COUNT)

robots = []

for i in range(ROBOT_COUNT):

    robot = RescueRobot(i, 50, 50)

    robots.append(robot)

running = True

while running:

    screen.fill((20, 20, 20))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    for obstacle in environment.obstacles:

        pygame.draw.circle(
            screen,
            (100, 100, 100),
            (obstacle[0] * 10, obstacle[1] * 7),
            5
        )

    for survivor in environment.survivors:

        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (survivor[0] * 10, survivor[1] * 7),
            5
        )

    for robot in robots:

        robot.move()

        pygame.draw.circle(
            screen,
            (0, 255, 255),
            (robot.x * 10, robot.y * 7),
            8
        )

        detected = robot.detect_survivor(environment)

        if detected:

            print(
                f"Robot {robot.robot_id} detected survivor at {detected}"
            )

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
