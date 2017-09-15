def set_physics(obj, physics_type = 'RIGID_BODY', collision_type = None, mass = 1.):
    obj.game.physics_type = physics_type
    if collision_type is not None:
        obj.game.use_collision_bounds = True
        obj.game.collision_bounds_type = collision_type
        obj.game.collision_margin = 0.
        obj.game.use_collision_compound = True
    obj.game.mass = mass
