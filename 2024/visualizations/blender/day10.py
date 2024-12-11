# Jeff Standen
# https://phpc.social/@jeff
# https://bsky.app/profile/jstanden.bsky.social

import bpy
from itertools import count
from collections import defaultdict, deque

data = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""".strip()

# Generate a grayscale palette
colors = [(*((0.25 * 0.05 * i) for _ in range(0, 3)), 1.0) for i in range(0, 10)]

# Add red and green
colors.append((1.0, 0.0, 0.0, 1.0))
colors.append((0.0, 1.0, 0.0, 1.0))

materials = []

# Generate materials for every defined color with the same index
for color in colors:
    mat = bpy.data.materials.new(str(color))
    mat.diffuse_color = color
    materials.append(mat)


# Move the anchor point of the active object to the bottom for easier z-axis math
def anchor_bottom():
    for z, co in [(o.bound_box[0][2], v.co) for o in bpy.context.selected_objects for v in o.data.vertices]:
        co.z -= z


# Add our prefab for cubes
bpy.ops.mesh.primitive_cube_add(scale=(0.5, 0.5, 0.25))
ref_cube = bpy.context.object
ref_cube.name = 'Reference Cube'
anchor_bottom()

# Add our prefab for flags
bpy.ops.mesh.primitive_cone_add(scale=(0.25, 0.25, 0.25))
ref_flag = bpy.context.object
ref_flag.name = 'Flag'
anchor_bottom()

# Add the player
bpy.ops.mesh.primitive_ico_sphere_add()
player = bpy.context.object
player.name = 'Player'
player.active_material = materials[11]  # Green
player.keyframe_insert('location', frame=1)
anchor_bottom()

# Cardinal direction vectors
directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

# Grid hashed with (y,x) coords and symbol values
grid = defaultdict(None, {(y, x): int(symbol)
                          for y, row in enumerate(data.splitlines())
                          for x, symbol in enumerate(list(row))})

# Dictionaries of cubes and flags hashed by (y,x)
cubes = {}
flags = {}


def find_in_grid(value):
    return set(filter(lambda item: item[1] == value, grid.items()))


def get_neighbors(loc: tuple):
    neighbors = []
    for d in directions:
        at = vector_add(loc, d)
        if grid.get(at): neighbors.append((at, grid[at]))
    return neighbors


def vector_add(v1, v2):
    return tuple([v1[i] + v2[i] for i in range(len(v1))])


for coord, z in grid.items():
    x, y = coord
    # Clone cubes for performance vs bpy.ops instantiation
    cube = ref_cube.copy()
    cube.data = ref_cube.data.copy()
    cube.name = f'Cube {x} {y} {z}'
    cube.location = (x, y, 0)
    cube.scale.z = z + 1
    cube.active_material = materials[z]
    bpy.context.collection.objects.link(cube)
    cubes[(x, y)] = cube

    # If this is a summit, clone a flag and hide it at this location
    if z == 9:
        # Clone flags for performance
        flag = ref_flag.copy()
        flag.data = ref_flag.data.copy()
        flag.location = (x, y, 5)
        flag.active_material = materials[10]  # Red
        flag.hide_viewport = True
        flag.hide_render = True
        flag.keyframe_insert('hide_viewport', frame=1)
        bpy.context.collection.objects.link(flag)
        flags[(x, y)] = flag

# We update the scene once after cloning our objects
bpy.context.view_layer.update()

# Find the trailheads
trailheads = find_in_grid(0)

part1, part2 = 0, 0
frame_counter = count()

# DFS
for trailhead in trailheads:
    stack = deque()
    goals = set()
    stack.append(trailhead)

    while stack:
        node = stack.pop()
        f = next(frame_counter)

        # Keyframe the player location every move
        x, y = node[0]
        player.location = (x, y, (node[1] + 1) / 2)
        player.keyframe_insert('location', frame=f)

        if node[1] == 9:
            goals.add(node[0])
            part2 += 1

            # Keyframe flag visibility when we reach a peak
            flags[node[0]].hide_viewport = False
            flags[node[0]].keyframe_insert('hide_viewport', frame=f)

        for n_at, n in get_neighbors(node[0]):
            if n == node[1] + 1:
                stack.append((n_at, n))

    part1 += len(goals)