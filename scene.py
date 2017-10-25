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


def render_depth(out_path, engine = 'CYCLES'):
    # duplicate a new scene
    bpy.ops.scene.new(type = 'LINK_OBJECTS')
    scene = bpy.context.scene
    scene.use_nodes = True

    # set up the nodes for scene
    node_tree = scene.node_tree
    nodes = node_tree.nodes

    # remove all of the nodes
    for node in nodes:
        nodes.remove(node)

    # set up the nodes for z pass
    nodes.new('CompositorNodeRLayers')
    nodes.new('CompositorNodeOutputFile')
    node_tree.links.new(nodes['Render Layers'].outputs[2], nodes['File Output'].inputs[0])

    # set up the file output
    nodes['File Output'].format.file_format = 'OPEN_EXR'
    nodes['File Output'].format.color_mode = 'RGB'
    nodes['File Output'].format.color_depth = '32'
    nodes['File Output'].base_path = os.path.dirname(out_path)
    nodes['File Output'].file_slots[0].path = os.path.basename(out_path[:-4])

    # set up the engine for rendering
    assert engine in ['BLENDER_RENDER', 'CYCLES'], 'engine "%s" is not supported' % engine
    scene.render.engine = engine

    if engine == 'CYCLES':
        scene.cycles.samples = 1

    # render the depth map
    scene.render.filepath = '/tmp/{0}_rgb.png'.format(time())
    bpy.ops.render.render(write_still = True)
    os.rename('{0}{1:04d}.exr'.format(out_path[:-4], scene.frame_current), out_path)

    # remove this new scene
    bpy.ops.scene.delete()
