import pygame
import json
import random
import os



from config import *
from environment import DisasterEnvironment
from robot import RescueRobot

pygame.init()

screen = pygame.display.set_mode(
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)

pygame.display.set_caption("AegisHive")

font = pygame.font.SysFont(None, 24)

clock = pygame.time.Clock()

mission_start = pygame.time.get_ticks()

start_ticks = pygame.time.get_ticks()

font = pygame.font.Font(None, 24)

environment = DisasterEnvironment(
    MAP_WIDTH,
    MAP_HEIGHT
)

environment.generate_obstacles(350)
environment.generate_survivors(SURVIVOR_COUNT)

robots = []
global_explored = set()

for i in range(ROBOT_COUNT):

    robot = RescueRobot(i, 50, 50)

    robots.append(robot)

running = True
shared_target = None
last_dashboard_update = 0

while running:
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000

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
            (obstacle[0] * 4, obstacle[1] * 4),
            5
        )

    # Survivors
    for survivor in environment.survivors:

        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (survivor[0] * 4, survivor[1] *4),
            5
        )

    # Robots
    for robot in robots:

        for other_robot in robots:

             if other_robot != robot:

                  distance = abs(robot.x - other_robot.x) + abs(robot.y - other_robot.y)

                  # Push robots apart

                  if distance < 25:

                       if robot.x < other_robot.x:
                          robot.x -= 3
                       else:
                          robot.x += 3

                       if robot.y < other_robot.y:
                          robot.y -= 3
                       else:
                          robot.y += 3

        robot.move(environment, global_explored)

        battery_level = robot.battery
        
        if robot.x < 15 and robot.y < 15:

                      robot.battery += 0.2

        if robot.battery > 100:
                      robot.battery = 100

        if battery_level < 20:

            robot_color = (255, 0, 0)
            status = "Returning"

        else:

            robot_color = (0, 255, 255)
            status = "Active"

        for point in robot.path:

              pygame.draw.circle(
              screen,
              (50, 50, 50),
              (point[0] * 4, point[1] * 4),
              2
              )

        pygame.draw.circle(
            screen,
            robot_color,
            (robot.x * 4, robot.y * 4),
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
            (robot.x * 4 + 10, robot.y * 4)
        )

        detected = robot.detect_survivor(environment)
        
        if detected in environment.survivors:

            environment.survivors.remove(detected)
            shared_target = None

        if detected:
            #shared_target = detected

            print(
                f"Robot {robot.robot_id} detected survivor at {detected}"
            )
    timer_text = font.render(
    f"Mission Time: {seconds}s",
    True,
    (255, 255, 255)
    )

    screen.blit(timer_text, (650, 20))

    # Coverage Display
    coverage = int(
      (
        len(global_explored)
        / TOTAL_GRID_CELLS
      ) * 100
    )

    coverage_text = font.render(
       f"Area Explored: {coverage}%",
       True,
       (255, 255, 255)
    )

    screen.blit(coverage_text, (650, 50))

    mission_time = pygame.time.get_ticks() // 1000

    overall_explored = int(
       (
         len(global_explored)
         / TOTAL_GRID_CELLS
       ) * 100
    )

    current_time = pygame.time.get_ticks()

    if current_time - last_dashboard_update > 1000:

      dashboard_data = {

        "mission_time": mission_time,

        "overall_explored": overall_explored,

        "survivors_detected": sum(
            len(robot.detected_survivors)
            for robot in robots
        ),

        "robots": []
      }

      for robot in robots:

        robot_explored = int(
            (
                len(robot.unique_explored)
                / TOTAL_GRID_CELLS
            ) * 100
        )

        dashboard_data["robots"].append({

            "id": robot.robot_id,

            "battery": int(robot.battery),

            "status": (
                "Charging"
                if robot.charging
                else "Active"
            ),

            "explored": robot_explored,

            "survivors": len(
                robot.detected_survivors
            )
        })

      with open("dashboard_data.json", "w") as file:

        json.dump(dashboard_data, file)

      last_dashboard_update = current_time

    

    

    # LIVE DASHBOARD

    dashboard_x = WINDOW_WIDTH - 260

    pygame.draw.rect(
      screen,
     (30, 30, 30),
     (dashboard_x, 0, 260, WINDOW_HEIGHT)
    )

    # Mission timer

    mission_time = (
      pygame.time.get_ticks() - mission_start
    ) // 1000

    timer_text = font.render(
      f"Mission Time: {mission_time}s",
      True,
      (255, 255, 255)
    )

    screen.blit(timer_text, (dashboard_x + 10, 20))

    # Overall explored %
    overall_text = font.render(
      f"Overall Explored: {overall_explored}%",
      True,
      (0, 255, 0)
    )

    screen.blit(overall_text, (dashboard_x + 10, 60))

    # Robot stats

    y_offset = 120

    for robot in robots:

      robot_area = int(
        (
            len(robot.unique_explored)
            / TOTAL_GRID_CELLS
        ) * 100
      )


      status = "Charging" if robot.charging else "Active"

      robot_text = font.render(
        f"R{robot.robot_id} | "
        f"{robot_area}% | "
        f"Battery: {int(robot.battery)} | "
        f"{status}",
        True,
        (255, 255, 255)
      )

      screen.blit(robot_text, (dashboard_x + 10, y_offset))

      survivor_text = font.render(
        f"Survivors: {len(robot.detected_survivors)}",
        True,
        (255, 100, 100)
      )

      screen.blit(
        survivor_text,
        (dashboard_x + 20, y_offset + 25)
      )

      y_offset += 70

    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
