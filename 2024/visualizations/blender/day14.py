import bpy
import re
from math import floor
import random

data = bpy.data.texts["day14.txt"].as_string()

grid_height, grid_width = 103, 101
grid_mid_y, grid_mid_x = floor(grid_height / 2), floor(grid_width / 2)


# Move the anchor point of the active object to the bottom for easier z-axis math
def anchor_bottom():
    for z, co in [(o.bound_box[0][2], v.co) for o in bpy.context.selected_objects for v in o.data.vertices]:
        co.z -= z


bpy.ops.mesh.primitive_ico_sphere_add()
prefab_robot = bpy.context.object
anchor_bottom()


# Use modulo to advance robots to positions at (t) time
def robots_at_t(t: int) -> list:
    for r in robots:
        nx = (r.initial_x + t * r.vx) % grid_width
        ny = (r.initial_y + t * r.vy) % grid_height
        r.x = nx
        r.y = ny
    return robots


class Robot():
    def __init__(self, x, y, vx, vy):
        self.initial_x = x
        self.initial_y = y
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

        self.bot = prefab_robot.copy()
        self.bot.data = prefab_robot.data.copy()
        self.bot.name = f'Robot'
        self.bot.color = (1.0, 1.0, 1.0, 1.0)
        self.bot.keyframe_insert('color', frame=1)
        self.bot.active_material = bpy.data.materials['Material']
        bpy.context.collection.objects.link(self.bot)


target_t = 6377

pattern = re.compile(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)')
robots = [Robot(*map(int, re.match(pattern, specs).groups()))
          for specs in data.split('\n')]

frame = 1

for t in range(target_t - 10, target_t + 10):
    if t == 6377:
        frame += 20

    for robot in robots_at_t(t):
        robot.bot.location = (robot.x, robot.y, 0)
        robot.bot.keyframe_insert('location', frame=frame)

        if t == 6377:
            robot.bot.keyframe_insert('location', frame=frame + 20)
            robot.bot.keyframe_insert('color', frame=frame - 40)
            robot.bot.color = random.choice([(1.0, 0, 0, 1.0), (0, 1.0, 0, 1.0)])
            robot.bot.keyframe_insert('color', frame=frame + 20)
            robot.bot.color = (1.0, 1.0, 1.0, 1.0)
            robot.bot.keyframe_insert('color', frame=frame + 45)

    if t == 6377:
        frame += 40

    frame += 10