from ode import Body, Mass, HingeJoint, FixedJoint

body_density = 1
servo_density = 8
battery_density = 10


def fix(world, body1, body2):
    joint = FixedJoint(world)
    joint.attach(body1, body2)


def make_servo(world, position=(0, 0, 0)):
    mass = Mass()
    mass.setBox(servo_density, 40, 20, 35)
    body = Body(world)
    body.setMass(mass)
    body.setPosition(position)
    return body


def make_battery(world, position=(0, 0, 0)):
    mass = Mass()
    mass.setBox(battery_density, 70, 25, 35)
    body = Body(world)
    body.setMass(mass)
    body.setPosition(position)
    return body


def make_body(world):
    mass = Mass()
    mass.setBox(body_density, 240, 27, 150)
    body = Body(world)
    body.setMass(mass)
    fix(world, body, make_battery(world, (0, 27 / 2, -(150 / 2 - 35 / 2))))
    fix(world, body, make_battery(world, (0, 27 / 2, 150 / 2 - 35 / 2)))
    fix(world, body, make_servo(world, (240 / 2 - 30, 0, 150 / 2)))
    fix(world, body, make_servo(world, (240 / 2 - 30, 0, -150 / 2)))
    fix(world, body, make_servo(world, (-(240 / 2 - 30), 0, 150 / 2)))
    fix(world, body, make_servo(world, (-(240 / 2 - 30), 0, -150 / 2)))
    return body


def make_upper_leg(world):
    upper_leg_mass = Mass()
    upper_leg_mass.setBox(body_density, 30, 100, 5)
    upper_leg = Body(world)
    upper_leg.setMass(upper_leg_mass)
    return upper_leg


def make_lower_leg(world):
    lower_leg_mass = Mass()
    lower_leg_mass.setBox(body_density, 30, 100, 5)
    lower_leg = Body(world)
    lower_leg.setMass(lower_leg_mass)
    servo = make_servo(world)
    fix(world, lower_leg, servo)
    return lower_leg


def make_leg(world, offset):
    upper_leg = make_upper_leg(world)
    upper_leg.setPosition((offset[0], offset[1] - 40, offset[2]))
    lower_leg = make_lower_leg(world)
    lower_leg.setPosition((offset[0], offset[1] - 40 - 40, offset[2]))
    knee_joint = HingeJoint(world)
    knee_joint.setAxis((0, 0, 1))
    knee_joint.setAnchor((offset[0], offset[1] - 80, offset[2]))
    knee_joint.attach(upper_leg, lower_leg)
    return upper_leg


def make_dog(world):
    body = make_body(world)

    front_left_leg = make_leg(world, (240 / 2 - 20, 0, -(150 / 2 + 10)))
    front_left_shoulder = HingeJoint(world)
    front_left_shoulder.setAxis((0, 0, -1))
    front_left_shoulder.attach(front_left_leg, body)

    front_right_leg = make_leg(world, (240 / 2 - 20, 0, 150 / 2 + 10))
    front_right_shoulder = HingeJoint(world)
    front_right_shoulder.setAxis((0, 0, 1))
    front_right_shoulder.attach(front_right_leg, body)

    back_right_leg = make_leg(world, (-(240 / 2 - 20), 0, 150 / 2 + 10))
    back_right_shoulder = HingeJoint(world)
    back_right_shoulder.setAxis((0, 0, 1))
    back_right_shoulder.attach(back_right_leg, body)

    back_left_leg = make_leg(world, (-(240 / 2 - 20), 0, -(150 / 2 + 10)))
    back_left_shoulder = HingeJoint(world)
    back_left_shoulder.setAxis((0, 0, -1))
    back_left_shoulder.attach(back_left_leg, body)

    return body

