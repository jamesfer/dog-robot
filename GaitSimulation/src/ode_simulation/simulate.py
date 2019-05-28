import ode
from dog_model import make_dog


# Create the world
world = ode.World()
world.setGravity((0, -9.8, 0))

dog = make_dog(world)

# Simulate
time = 0.0
delta = 0.04
while time < 2.0:
    x, y, z = dog.getPosition()
    u, v, w = dog.getLinearVel()
    print "%1.2f, %6.3f, %6.3f, %6.3f, %6.3f, %6.3f, %6.3f" % (time, x, y, z, u, v, w)
    world.step(delta)
    time += delta



