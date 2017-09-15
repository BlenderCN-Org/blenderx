import bpy


def render_animation(out_path, frame_start, frame_end, engine = 'BLENDER_RENDER'):
    scene = bpy.context.scene

    scene.render.filepath = out_path + '/'
    scene.render.engine = engine
    scene.frame_start = frame_start
    scene.frame_end = frame_end

    if engine == 'CYCLES':
        scene.render.tile_x = 256
        scene.render.tile_y = 256
        scene.cycles.device = 'GPU'
        bpy.context.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'

    bpy.ops.render.render(animation = True)
