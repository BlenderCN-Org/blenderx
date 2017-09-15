import bpy


def render_animation(out_path, frame_start, frame_end, engine = 'BLENDER_RENDER'):
    bpy.context.scene.render.filepath = out_path + '/'
    bpy.context.scene.render.engine = engine
    bpy.context.scene.frame_start = frame_start
    bpy.context.scene.frame_end = frame_end

    if engine == 'CYCLES':
        bpy.context.scene.render.tile_x = 256
        bpy.context.scene.render.tile_y = 256
        bpy.context.scene.cycles.device = 'GPU'
        bpy.context.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'

    bpy.ops.render.render(animation = True)
