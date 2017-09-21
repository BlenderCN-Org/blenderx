import bpy


def deselect_all_objects():
    scene = bpy.context.scene

    for obj in bpy.data.objects:
        scene.objects.active = obj

        # switch to object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # deselect object
        obj.select = False


def render_animation(out_path, frames, resolution = (256, 256), tile = (64, 64), engine = 'BLENDER_RENDER'):
    scene = bpy.context.scene

    # set up frames for rendering
    if len(frames) == 1:
        frames = (0, frames[0], 1)
    elif len(frames) == 2:
        frames = (frames[0], frames[1], 1)

    scene.frame_start = frames[0]
    scene.frame_end = frames[1]
    scene.frame_step = frames[2]

    # set up resolution for rendering
    scene.render.resolution_x = resolution[0]
    scene.render.resolution_y = resolution[1]
    scene.render.resolution_percentage = 100

    # set up tile size for rendering
    scene.render.tile_x = tile[0]
    scene.render.tile_y = tile[1]

    # set up engine for rendering
    assert engine in ['BLENDER_RENDER', 'CYCLES'], 'engine "%s" is not supported' % engine
    scene.render.engine = engine

    if engine == 'CYCLES':
        scene.cycles.device = 'GPU'
        bpy.context.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'

    # rendering animation
    scene.render.filepath = out_path + '/'
    bpy.ops.render.render(animation = True)
