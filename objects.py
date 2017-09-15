import bpy
import numpy as np
from mathutils import Matrix

from .scene import deselect_all_objects


def add_object(model_path, scale = 1, trans_vec = (0, 0, 0), rot_mat = ((1, 0, 0), (0, 1, 0), (0, 0, 1)), name = None):
    # import object
    bpy.ops.import_scene.obj(filepath = model_path)

    objs = []
    for k, obj in enumerate(bpy.context.selected_objects):
        # rename objects
        if name is not None:
            if len(bpy.context.selected_objects) == 1:
                obj.name = name
            else:
                obj.name = name + '-' + str(k + 1)

        # compute world matrix
        trans_4x4 = Matrix.Translation(trans_vec)
        rot_4x4 = Matrix(rot_mat).to_4x4()
        scale_4x4 = Matrix(np.eye(4))
        obj.matrix_world = trans_4x4 * rot_4x4 * scale_4x4

        # scale
        obj.scale = (scale, scale, scale)
        objs.append(obj)

    # update scene
    bpy.context.scene.update()
    return objs


def add_plane(scale = 1, trans_vec = (0, 0, 0), rot_mat = ((1, 0, 0), (0, 1, 0), (0, 0, 1)), name = None):
    scene = bpy.context.scene

    # add plane
    bpy.ops.mesh.primitive_plane_add()
    obj = scene.objects.active

    # rename object
    if name is not None:
        obj.name = name

    # compute world matrix
    trans_4x4 = Matrix.Translation(trans_vec)
    rot_4x4 = Matrix(rot_mat).to_4x4()
    scale_4x4 = Matrix(np.eye(4))
    obj.matrix_world = trans_4x4 * rot_4x4 * scale_4x4

    # scale
    obj.scale = (scale, scale, scale)

    # update scene
    bpy.context.scene.update()
    return obj


def add_sphere(scale = 1, trans_vec = (0, 0, 0), rot_mat = ((1, 0, 0), (0, 1, 0), (0, 0, 1)), name = None):
    scene = bpy.context.scene

    # add sphere
    bpy.ops.mesh.primitive_uv_sphere_add()
    obj = scene.objects.active

    # rename object
    if name is not None:
        obj.name = name

    # compute world matrix
    trans_4x4 = Matrix.Translation(trans_vec)
    rot_4x4 = Matrix(rot_mat).to_4x4()
    scale_4x4 = Matrix(np.eye(4))
    obj.matrix_world = trans_4x4 * rot_4x4 * scale_4x4

    # scale
    obj.scale = (scale, scale, scale)

    # update scene
    bpy.context.scene.update()
    return obj


def join_objects(objs, name = None):
    scene = bpy.context.scene

    # join objects
    scene.objects.active = objs[0]
    bpy.ops.object.join()
    obj = scene.objects.active

    # deselect all objects
    deselect_all_objects()

    # recenter object
    obj.select = True
    bpy.ops.object.origin_set(type = 'ORIGIN_GEOMETRY')

    # rename object
    if name is not None:
        obj.name = name
    return obj


def set_material(obj, material):
    scene = bpy.context.scene
    scene.objects.active = obj

    while len(obj.material_slots) > 0:
        bpy.ops.object.material_slot_remove()
    obj.active_material = material
