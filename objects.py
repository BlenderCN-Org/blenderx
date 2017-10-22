import bpy
import numpy as np
from mathutils import Matrix

from .scene import deselect_all_objects


def add_object(model_path, scale = 1, trans_vec = (0, 0, 0), rot_mat = ((1, 0, 0), (0, 1, 0), (0, 0, 1)), name = None):
    # import the object
    if model_path.endswith('.obj'):
        bpy.ops.import_scene.obj(filepath = model_path)
    elif model_path.endswith('.dae'):
        bpy.ops.wm.collada_import(filepath = model_path)

    objs = []
    for k, obj in enumerate(bpy.context.selected_objects):
        if obj.type != 'MESH':
            continue

        # rename the objects
        if name is not None:
            if len(bpy.context.selected_objects) == 1:
                obj.name = name
            else:
                obj.name = name + '-' + str(k + 1)

        # compute the world matrix
        trans_4x4 = Matrix.Translation(trans_vec)
        rot_4x4 = Matrix(rot_mat).to_4x4()
        obj.matrix_world = trans_4x4 * rot_4x4

        # scale
        obj.scale = (scale, scale, scale)
        objs.append(obj)

    # update the scene
    bpy.context.scene.update()
    return objs


def add_plane(scale = 1, trans_vec = (0, 0, 0), rot_mat = ((1, 0, 0), (0, 1, 0), (0, 0, 1)), name = None):
    scene = bpy.context.scene

    # add the plane
    bpy.ops.mesh.primitive_plane_add()
    obj = scene.objects.active

    # rename the object
    if name is not None:
        obj.name = name

    # compute the world matrix
    trans_4x4 = Matrix.Translation(trans_vec)
    rot_4x4 = Matrix(rot_mat).to_4x4()
    scale_4x4 = Matrix(np.eye(4))
    obj.matrix_world = trans_4x4 * rot_4x4 * scale_4x4

    # scale
    obj.scale = (scale, scale, scale)

    # update the scene
    bpy.context.scene.update()
    return obj


def add_sphere(scale = 1, trans_vec = (0, 0, 0), rot_mat = ((1, 0, 0), (0, 1, 0), (0, 0, 1)), name = None):
    scene = bpy.context.scene

    # add the sphere
    bpy.ops.mesh.primitive_uv_sphere_add()
    obj = scene.objects.active

    # rename the object
    if name is not None:
        obj.name = name

    # compute the world matrix
    trans_4x4 = Matrix.Translation(trans_vec)
    rot_4x4 = Matrix(rot_mat).to_4x4()
    scale_4x4 = Matrix(np.eye(4))
    obj.matrix_world = trans_4x4 * rot_4x4 * scale_4x4

    # scale
    obj.scale = (scale, scale, scale)

    # update the scene
    bpy.context.scene.update()
    return obj


def join_objects(objs, name = None):
    scene = bpy.context.scene

    # deselect all objects
    deselect_all_objects()

    # select the object
    for obj in objs:
        obj.select = True

    # join the object
    scene.objects.active = objs[0]
    bpy.ops.object.join()
    obj = scene.objects.active

    # deselect all objects
    deselect_all_objects()

    # recenter the object
    obj.select = True
    bpy.ops.object.origin_set(type = 'ORIGIN_GEOMETRY', center = 'BOUNDS')

    # rename the object
    if name is not None:
        obj.name = name

    # update the scene
    bpy.context.scene.update()
    return obj


def separate_object(obj, mode = 'LOOSE'):
    # deselect all objects
    deselect_all_objects()

    # seperate the object
    obj.select = True
    bpy.ops.mesh.separate(type = mode)

    objs = []
    for i, obj in enumerate(bpy.context.selected_objects):
        objs.append(obj)

    # update the scene
    bpy.context.scene.update()
    return objs


def clean_object(obj):
    scene = bpy.context.scene

    for ops, argv in [
        # delete loose
        (bpy.ops.mesh.delete_loose, {}),

        # remove doubles
        (bpy.ops.mesh.remove_doubles, {}),

        # fill holes
        (bpy.ops.mesh.fill_holes, {}),

        # recalculate normals
        (bpy.ops.mesh.normals_make_consistent, {'inside': False})
    ]:
        # deselect all objects
        deselect_all_objects()

        # select the object in the edit mode
        obj.select = True
        scene.objects.active = obj
        bpy.ops.object.mode_set(mode = 'EDIT')

        # select all faces, edges and vertices
        bpy.ops.mesh.select_mode(type = 'FACE')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.select_mode(type = 'EDGE')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.select_mode(type = 'VERT')
        bpy.ops.mesh.select_all(action = 'SELECT')

        # perform the operator on the object
        ops(**argv)


def remesh_object(obj, mode = 'SMOOTH', depth = 8, remove_disconnected = False):
    scene = bpy.context.scene

    # add the remesh modifier
    scene.objects.active = obj
    bpy.ops.object.modifier_add(type = 'REMESH')
    obj.modifiers['Remesh'].mode = mode
    obj.modifiers['Remesh'].octree_depth = depth
    obj.modifiers['Remesh'].use_remove_disconnected = remove_disconnected

    # apply the remesh modifier
    scene.objects.active = obj
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.modifier_apply(apply_as = 'DATA', modifier = 'Remesh')
