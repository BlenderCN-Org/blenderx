import bpy
import numpy as np


def set_physics(obj, physics_type = 'RIGID_BODY', collision_type = None, mass = 1.):
    obj.game.physics_type = physics_type
    if collision_type is not None:
        obj.game.use_collision_bounds = True
        obj.game.collision_bounds_type = collision_type
        obj.game.collision_margin = 0.
        obj.game.use_collision_compound = True
    obj.game.mass = mass


def apply_impulse(obj, point, impulse, time = 0, local = False):
    scene = bpy.context.scene
    scene.objects.active = obj

    name = '{0}-{1}-{2}'.format(obj.name, time, np.random.random())

    stream = bpy.data.texts.new(name + '.py')
    print('from bge import logic', file = stream)
    print('controller = logic.getCurrentController()', file = stream)
    print('controller.owner.applyImpulse({0}, {1}, {2})'.format(point, impulse, local), file = stream)

    bpy.ops.logic.sensor_add(type = 'DELAY', name = name + '-s')
    obj.game.sensors[name + '-s'].delay = time
    bpy.ops.logic.controller_add(type = 'PYTHON', name = name + '-c')
    obj.game.controllers[name + '-c'].text = stream
    obj.game.controllers[name + '-c'].link(sensor = obj.game.sensors[name + '-s'])


def simulate(nframes):
    key = np.random.choice(bpy.data.objects.keys())
    obj = bpy.data.objects[key]

    scene = bpy.context.scene
    scene.objects.active = obj

    name = 'simulation-timer-{0}'.format(np.random.random())

    bpy.ops.logic.sensor_add(type = 'DELAY', name = name + '-s')
    obj.game.sensors[name + '-s'].delay = nframes
    bpy.ops.logic.actuator_add(type = 'GAME', name = name + '-a')
    obj.game.actuators[name + '-a'].mode = 'QUIT'
    bpy.ops.logic.controller_add(type = 'LOGIC_AND', name = name + '-c')
    obj.game.controllers[name + '-c'].link(
        sensor = obj.game.sensors[name + '-s'],
        actuator = obj.game.actuators[name + '-a']
    )

    bpy.context.scene.render.engine = 'BLENDER_GAME'
    bpy.context.scene.game_settings.physics_step_max = 1
    bpy.context.scene.game_settings.physics_step_sub = 50
    bpy.context.scene.game_settings.use_animation_record = True
    bpy.ops.view3d.game_start()
