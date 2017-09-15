import bpy
import numpy as np


def add_constraint(obj, type, name = None):
    scene = bpy.context.scene
    scene.objects.active = obj

    if name is None:
        name = '{0}-{1}-{2}'.format(obj.name, type, np.random.random())

    bpy.ops.object.constraint_add(type = type)
    if type == 'RIGID_BODY_JOINT':
        con = obj.constraints['Rigid Body Joint']
    else:
        raise NotImplementedError

    con.name = name
    return con


def add_fixed_constraint(source, target):
    name = 'fixed-{0}-{1}-{2}'.format(source.name, target.name, np.random.random())

    con = add_constraint(source, type = 'RIGID_BODY_JOINT', name = name)
    con.target = target

    con.pivot_type = 'GENERIC_6_DOF'
    con.use_linked_collision = True
    con.use_limit_x = con.use_angular_limit_x = True
    con.use_limit_y = con.use_angular_limit_y = True
    con.use_limit_z = con.use_angular_limit_z = True
    return con
