# Jeff Standen
# https://phpc.social/@jeff
# https://bsky.app/profile/jstanden.bsky.social

import bpy
from itertools import cycle, count, islice, chain, repeat
import math
from copy import deepcopy

data = "2333133121414131402"
# data = data[:54] # When using full data

WALL_WIDTH = 16
FRAME_STEP = 15

materials = [
    bpy.data.materials.new(""),
    bpy.data.materials.new(""),
    bpy.data.materials.new(""),
    bpy.data.materials.new(""),
]

# Shades of green to alternate in contiguous blocks
materials[0].diffuse_color = (0, 0.2, 0, 1)
materials[1].diffuse_color = (0, 0.4, 0, 1)
materials[2].diffuse_color = (0, 0.6, 0, 1)
materials[3].diffuse_color = (0, 0.8, 0, 1)

blocks = []
modes = cycle(('file', 'free'))
file_ids = chain.from_iterable((i, i) for i in count())

# Decompress (2333133121414131402 -> 00...111...2...333.44.5555.6666.777.888899)
for digit, mode, file_id in zip(data, islice(modes, len(data)), islice(file_ids, len(data))):
    blocks.append(list(repeat(str(file_id), int(digit)) if mode == 'file' else repeat('.', int(digit))))

part1_blocks = list(chain(*blocks))
left, right = 0, len(part1_blocks) - 1

# Wrap our chain of blocks into a wall
for i, block in enumerate(part1_blocks):
    z = WALL_WIDTH - math.floor(i // WALL_WIDTH)
    y = (i % WALL_WIDTH)

    # Create a cube
    bpy.ops.mesh.primitive_cube_add(location=(0, y, z), scale=(0.5, 0.5, 0.5))
    cube = bpy.context.selected_objects[0]

    # If this isn't free space, use our next green material in the cycle
    if block != '.':
        cube.active_material = materials[int(block) % len(materials)]

# Use a generator for frame counts
counter = count(start=FRAME_STEP + 1, step=FRAME_STEP)

# Iterate from both ends simultaneously until the pointers cross
while True:
    while left < len(part1_blocks) and part1_blocks[left] != '.': left += 1
    while right >= 0 and part1_blocks[right] == '.': right -= 1
    if left > right: break

    # Swap our leftmost free space with rightmost file
    part1_blocks[right], part1_blocks[left] = part1_blocks[left], part1_blocks[right]

    # Clone locations before we swap them
    left_loc = deepcopy(bpy.data.objects[left].location)
    right_loc = deepcopy(bpy.data.objects[right].location)

    # Get the next frame increment from the generator
    f = next(counter)

    # Keyframe the blocks beginning positions
    bpy.data.objects[left].keyframe_insert('location', frame=f)
    bpy.data.objects[right].keyframe_insert('location', frame=f)

    # Move our matched pair forward on x
    bpy.data.objects[left].location = (left_loc.x + 1, left_loc.y, left_loc.z)
    bpy.data.objects[right].location = (right_loc.x + 2, right_loc.y, right_loc.z)

    bpy.data.objects[left].keyframe_insert('location', frame=f + math.floor(0.25 * FRAME_STEP))
    bpy.data.objects[right].keyframe_insert('location', frame=f + math.floor(0.25 * FRAME_STEP))

    # Swap our matched pair
    bpy.data.objects[left].location = (right_loc.x + 1, right_loc.y, right_loc.z)
    bpy.data.objects[right].location = (left_loc.x + 2, left_loc.y, left_loc.z)

    bpy.data.objects[left].keyframe_insert('location', frame=f + math.floor(0.75 * FRAME_STEP))
    bpy.data.objects[right].keyframe_insert('location', frame=f + math.floor(0.75 * FRAME_STEP))

    # Move our matched pair back into the wall on -x
    bpy.data.objects[left].location = (right_loc.x, right_loc.y, right_loc.z)
    bpy.data.objects[right].location = (left_loc.x, left_loc.y, left_loc.z)

    bpy.data.objects[left].keyframe_insert('location', frame=f + math.floor(0.95 * FRAME_STEP))
    bpy.data.objects[right].keyframe_insert('location', frame=f + math.floor(0.95 * FRAME_STEP))
