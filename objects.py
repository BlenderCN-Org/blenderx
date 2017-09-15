import bpy
import numpy as np
from mathutils import Matrix

def add_object(model_path, rot_mat = ((1, 0, 0), (0, 1, 0), (0, 0, 1)), trans_vec = (0, 0, 0), scale = 1, name = None):
    bpy.ops.import_scene.obj(filepath = model_path)

    obj_list = []
    for i, obj in enumerate(bpy.context.selected_objects):
        if name is not None:
            if len(bpy.context.selected_objects) == 1:
                obj.name = name
            else:
                obj.name = name + '-' + str(i)

        trans_4x4 = Matrix.Translation(trans_vec)
        rot_4x4 = Matrix(rot_mat).to_4x4()
        scale_4x4 = Matrix(np.eye(4))
        obj.matrix_world = trans_4x4 * rot_4x4 * scale_4x4

        obj.scale = (scale, scale, scale)
        obj_list.append(obj)
    return obj_list


def set_material(obj, material):
    scene = bpy.context.scene
    scene.objects.active = obj

    while len(obj.material_slots) > 0:
        bpy.ops.object.material_slot_remove()
    obj.active_material = material
