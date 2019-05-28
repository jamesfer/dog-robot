from ode import FixedJoint, environment
from shapes import Scene, Box
from dog_model import make_dog

scene = Scene()
dog = make_dog(scene)
# box = Box(scene, density=1, dimensions=(.05, .05, .05), position=(0, -.15, 0.1), color=(1, 0.2, 0.2))

floor = Box(scene, density=1, dimensions=(1, .2, 1), position=(0, -.30, 0), color=(0.7, 0.7, 0.7))
joint = FixedJoint(scene.world)
joint.attach(floor.body, environment)
joint.setFixed()

scene.visualize(duration=10.0, delta=0.005)
