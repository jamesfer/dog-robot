import math
from ode import HingeJoint, FixedJoint, ParamLoStop, ParamHiStop, ParamBounce, ParamVel

from shapes import Box

body_density = 1
servo_density = 8
battery_density = 10


def fix(shape1, shape2):
    joint = FixedJoint(shape1.scene.world)
    joint.attach(shape1.body, shape2.body)
    joint.setFixed()


def hinge(shape1, shape2, axis=None, anchor=None):
    joint = HingeJoint(shape1.scene.world)
    joint.attach(shape1.body, shape2.body)
    if anchor is not None:
        joint.setAxis(axis)
    if anchor is not None:
        joint.setAnchor(anchor)
    return joint


def make_servo(scene, position=(0, 0, 0)):
    return Box(scene, servo_density, dimensions=(.04, .02, .035), position=position, color=(0.2, 0.2, 0.2))


def make_battery(scene, position=(0, 0, 0)):
    return Box(scene, battery_density, dimensions=(.07, .025, .035), position=position, color=(0, 0, 0.8))


def make_body(scene):
    body = Box(scene, body_density, dimensions=(.24, .027, .15), color=(0.63, 0.23, 0.78))
    # fix(body, make_battery(scene, (0, .027 / 2 + .02 / 2, -(.15 / 2 - .035 / 2))))
    # fix(body, make_battery(scene, (0, .027 / 2 + .02 / 2, .15 / 2 - .035 / 2)))
    # fix(body, make_servo(scene, (.24 / 2 - .03, 0, .15 / 2)))
    # fix(body, make_servo(scene, (.24 / 2 - .03, 0, -.15 / 2)))
    # fix(body, make_servo(scene, (-(.24 / 2 - .03), 0, .15 / 2)))
    # fix(body, make_servo(scene, (-(.24 / 2 - .03), 0, -.15 / 2)))
    return body


def make_upper_leg(scene):
    return Box(scene, body_density, dimensions=(.03, .10, .01), color=(0.63, 0.83, 0.78))


def make_lower_leg(scene):
    # servo = make_servo(scene)
    lower_leg = Box(scene, body_density, dimensions=(.03, .10, .01), color=(0.63, 0.23, 0.78))
    # fix(lower_leg, servo)
    return lower_leg


def knee_joint(upper_leg, lower_leg, axis, offset):
    joint = hinge(upper_leg, lower_leg, axis, offset)
    joint.setParam(ParamLoStop, -math.pi / 3)
    joint.setParam(ParamHiStop, math.pi / 3)
    joint.setParam(ParamBounce, 0.001)


def make_leg(scene, offset):
    upper_leg = make_upper_leg(scene)
    upper_leg.set_position((offset[0], offset[1] - .04, offset[2]))
    lower_leg = make_lower_leg(scene)
    lower_leg.set_position((offset[0], offset[1] - .04 - .09, offset[2] + (.015 if offset[2] >= 0 else -0.015)))
    knee_joint(upper_leg, lower_leg, (0, 0, 1), (offset[0], offset[1] - 0.08, offset[2]))
    return upper_leg


def make_dog(scene):
    body = make_body(scene)

    front_left_leg = make_leg(scene, (.24 / 2 - .02, 0, -(.15 / 2 + 0.01 + .035)))
    knee_joint(front_left_leg, body, (0, 0, -1), (.24 / 2 - .02, 0, -(.15 / 2 + 0.01 + .035)))

    front_right_leg = make_leg(scene, (.24 / 2 - .02, 0, .15 / 2 + .01 + .035))
    knee_joint(front_right_leg, body, (0, 0, 1), (.24 / 2 - .02, 0, .15 / 2 + .01 + .035))

    back_right_leg = make_leg(scene, (-(.24 / 2 - .02), 0, .15 / 2 + .01 + .035))
    knee_joint(back_right_leg, body, (0, 0, 1), (-(.24 / 2 - .02), 0, .15 / 2 + .01 + .035))

    back_left_leg = make_leg(scene, (-(.24 / 2 - .02), 0, -(.15 / 2 + .01 + .035)))
    knee_joint(back_left_leg, body, (0, 0, -1), (-(.24 / 2 - .02), 0, -(.15 / 2 + .01 + .035)))

    return body

