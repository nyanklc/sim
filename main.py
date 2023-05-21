import math
import numpy as np
import pygame
import time

from car import Car, getDistance
from game_window import GameWindow


# path = [(200, y) for y in range(200, 3001, 30)]
# path += [(x, 3000) for x in range(201, 6001, 30)]

path =[
    (466+30+30+30+30+30+30+30,31),
    (466+30+30+30+30+30+30,31),
    (466+30+30+30+30+30,31),
    (466+30+30+30+30,31),
    (466+30+30+30,31),
    (466+30+30,31),
    (466+30,31),
    (436,31),
    (466,31),
    (448,28),
    (429,25),
    (411,24),
    (391,22),
    (372,23),
    (351,23),
    (330,25),
    (309,27),
    (289,31),
    (271,36),
    (253,44),
    (240,52),
    (229,62),
    (223,72),
    (221,83),
    (224,95),
    (232,108),
    (243,122),
    (260,136),
    (278,151),
    (302,167),
    (323,183),
    (351,201),
    (371,217),
    (396,236),
    (410,251),
    (426,270),
    (430,283),
    (435,299),
    (426,311),
    (417,323),
    (396,331),
    (376,339),
    (345,343),
    (317,347),
    (281,349),
    (249,350),
    (212,350),
    (177,350),
    ]

path = [(x[0], 2*x[1]) for x in path]

goal_radius = 180

meters_per_pixel = 0.001
fps = 5000
sim_step = 1 * meters_per_pixel

master = Car((0,255,0), x=466+30+30+30+30+30+30+30, y=2*31, yaw=math.pi, goal_rad=goal_radius)
# linear speed controller
p = 0.4
i = 0.04
d = 0.00001
car_vel = 0
pid_params = (p, i, d, car_vel)
master.setController('pid', pid_params)
# angular speed controller
p = 0.4
i = 0.04
d = 0.00001
car_angular_vel = 0
pid_params = (p, i, d, car_angular_vel)
master.setAngularController('pid', pid_params)

window = GameWindow((640, 480))

clock = pygame.time.Clock()
curr_time = time.time()
prev_time = curr_time

tim = 0
iteration_count = 0
time_arr = []
lin_speed_arr = []
ang_speed_arr = []
sample_period = 400
pos_arr_x = []
pos_arr_y = []
while True:
    iteration_count += 1

    clock.tick(fps)

    master.get_goal(path)

    master.calculate_goal_yaw(path)

    master.update(sim_step, (path[master.goal_index][0], path[master.goal_index][1]), master.goal_yaw)

    # master.print_speeds()

    # record values
    tim += clock.get_time()
    if iteration_count % sample_period == 0:
        print(f"tim: {tim}")
        print(f"x: {master.x}, y: {master.y}")
        time_arr.append(tim)
        lin_speed_arr.append(master.speed * meters_per_pixel)
        ang_speed_arr.append(master.angular_speed)
        pos_arr_x.append(master.x)
        pos_arr_y.append(master.y)

    window.set_info_text("ALSJDKLAJSDLK", (255, 0, 0))
    window.draw([master], path)

    if master.goal_index == len(path) - 1:
        break
time_arr_np = np.array(time_arr)
lin_speed_arr_np = np.array(lin_speed_arr)
ang_speed_arr_np = np.array(ang_speed_arr)

print(f"lin: {lin_speed_arr}")
print(f"ang: {ang_speed_arr}")
print(f"time: {time_arr}")

np.save("./time_arr.npy", time_arr_np)
np.save("./lin_speed_arr.npy", lin_speed_arr_np)
np.save("./ang_speed_arr.npy", ang_speed_arr_np)
np.save("./pos_arr_x.npy", pos_arr_x)
np.save("./pos_arr_y.npy", pos_arr_y)