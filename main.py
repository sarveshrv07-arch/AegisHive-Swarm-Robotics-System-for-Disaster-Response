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

font = pygame.font.Font(None, 24)

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

    # Base Station
    pygame.draw.rect(
        screen,
        (0, 0, 255),
        (40, 40, 120, 80)
    )

    base_text = font.render(
        "Base Station",
        True,
        (255, 255, 255)
    )

    screen.blit(base_text, (50, 70))

    # Obstacles
    for obstacle in environment.obstacles:

        pygame.draw.circle(
            screen,
            (100, 100, 100),
            (obstacle[0] * 10, obstacle[1] * 7),
            5
        )

    # Survivors
    for survivor in environment.survivors:

        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (survivor[0] * 10, survivor[1] * 7),
            5
        )

    # Robots
    for robot in robots:

        robot.move()

        battery_level = 100 - (robot.x % 100)

        if battery_level < 20:

            robot_color = (255, 0, 0)
            status = "Returning"

        else:

            robot_color = (0, 255, 255)
            status = "Active"

        pygame.draw.circle(
            screen,
            robot_color,
            (robot.x * 10, robot.y * 7),
            8
        )

        # Robot Label
        robot_label = font.render(
            f"R{robot.robot_id}",
            True,
            (255, 255, 255)
        )

        screen.blit(
            robot_label,
            (robot.x * 10 + 10, robot.y * 7)
        )

        detected = robot.detect_survivor(environment)

        if detected:

            print(
                f"Robot {robot.robot_id} detected survivor at {detected}"
            )

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
