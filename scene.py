import os
from time import time

import bpy


def deselect_all_objects():
    scene = bpy.context.scene

    for obj in bpy.data.objects:
        scene.objects.active = obj

        # switch to the object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # deselect the object
        obj.select = False


def render_depth(out_path = None):
    # # Validate and standardize error-prone inputs
    # if hide is not None:
    #     if not isinstance(hide, list):
    #         # A single object
    #         hide = [hide]
    #     for element in hide:
    #         assert isinstance(element, str), \
    #             "'hide' should contain object names (i.e., strings), not objects themselves"

    if out_path is None:
        outpath = '/tmp/%s_zbuffer' % time()
    elif out_path.endswith('.png'):
        outpath = out_path[:-4]

    # Duplicate scene to avoid touching the original scene
    bpy.ops.scene.new(type = 'LINK_OBJECTS')

    scene = bpy.context.scene
    # scene.camera = cam
    scene.use_nodes = True
    node_tree = scene.node_tree
    nodes = node_tree.nodes

    # Remove all nodes
    for node in nodes:
        nodes.remove(node)

    # Set up nodes for z pass
    nodes.new('CompositorNodeRLayers')
    nodes.new('CompositorNodeOutputFile')
    node_tree.links.new(nodes['Render Layers'].outputs[2], nodes['File Output'].inputs[0])
    nodes['File Output'].format.file_format = 'OPEN_EXR'
    nodes['File Output'].format.color_mode = 'RGB'
    nodes['File Output'].format.color_depth = '32'  # full float
    nodes['File Output'].base_path = os.path.dirname(outpath)
    nodes['File Output'].file_slots[0].path = os.path.basename(outpath)

    # Render
    scene.cycles.samples = 1
    scene.render.filepath = '/tmp/%s_rgb.png' % time()  # redirect RGB rendering to avoid overwritting
    bpy.ops.render.render(write_still = True)

    # Delete this new scene
    bpy.ops.scene.delete()

    # Load z-buffer as array
    exr_path = outpath + '.png'
    # im = scipy.misc.imread(exr_path)
    # im = cv2.imread(exr_path, cv2.IMREAD_UNCHANGED)
    # assert (np.array_equal(im[:, :, 0], im[:, :, 1]) and np.array_equal(im[:, :, 0], im[:, :, 2])), \
    #     "BGR channels of the z-buffer should be all the same, but they are not"
    # zbuffer = im[:, :, 0]

    # Delete or move the .exr as user wants
    if out_path is None:
        # User doesn't want it -- delete
        os.remove(exr_path)
    else:
        # User wants it -- rename
        os.rename(exr_path, outpath + '.exr')


        # return zbuffer


def render_animation(out_path, frames, resolution = (256, 256), tile = (64, 64), engine = 'BLENDER_RENDER'):
    scene = bpy.context.scene

    # set up the frames for rendering
    if len(frames) == 1:
        frames = (0, frames[0], 1)
    elif len(frames) == 2:
        frames = (frames[0], frames[1], 1)

    scene.frame_start = frames[0]
    scene.frame_end = frames[1]
    scene.frame_step = frames[2]

    # set up the resolution for rendering
    scene.render.resolution_x = resolution[0]
    scene.render.resolution_y = resolution[1]
    scene.render.resolution_percentage = 100

    # set up the tile size for rendering
    scene.render.tile_x = tile[0]
    scene.render.tile_y = tile[1]

    # set up the engine for rendering
    assert engine in ['BLENDER_RENDER', 'CYCLES'], 'engine "%s" is not supported' % engine
    scene.render.engine = engine

    if engine == 'CYCLES':
        scene.cycles.device = 'GPU'
        bpy.context.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'

    # render the animation
    scene.render.filepath = out_path + '/'
    bpy.ops.render.render(animation = True)
