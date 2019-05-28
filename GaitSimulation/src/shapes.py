import math
from ode import World, Body, Mass, Space, GeomBox, JointGroup, ContactJoint, collide
from open3d import Visualizer, Geometry, Vector3dVector, TriangleMesh, create_mesh_cylinder
import numpy as np

identity = (1, 0, 0, 0, 1, 0, 0, 0, 1)


class VisualizationUpdater:
    def __init__(self, visualization, callback=None):
        self.visualization = visualization
        self.callback = callback

    def __call__(self, *args, **kwargs):
        self.visualization.update_geometry()
        self.visualization.poll_events()
        self.visualization.update_renderer()
        if self.callback is not None:
            self.callback(*args, **kwargs)


class Scene:
    def __init__(self):
        self.geometries = []
        self.world = World()
        self.world.setGravity((0, -9.8, 0))
        self.world.setERP(0.4)
        self.world.setCFM(1E-5)
        self.space = Space()
        self.contact_group = JointGroup()
        self.update_callbacks = []

    def add_geometry(self, geometry):
        self.geometries.append(geometry)

    def simulate(self, delta=0.04, duration=2.0, callback=None):
        time = 0.0
        collision_iterations = 4
        while time < duration:
            for i in range(collision_iterations):
                # Detect collisions and create contact joints
                self.space.collide((), self.near_callback)

                # Simulate the world
                self.world.step(delta / collision_iterations)

                # Remove contact joints
                self.contact_group.empty()
            time += delta

            for update_callback in self.update_callbacks:
                update_callback(time)
            if callback is not None:
                callback(time)

    def near_callback(self, _, geom1, geom2):
        # Check if the objects do collide
        contacts = collide(geom1, geom2)

        # Create contact joints
        for contact in contacts:
            contact.setBounce(0.01)
            contact.setMu(2000)
            joint = ContactJoint(self.world, self.contact_group, contact)
            joint.attach(geom1.getBody(), geom2.getBody())

    def visualize(self, delta=0.04, duration=2.0, callback=None):
        visualizer = Visualizer()
        visualizer.create_window()
        for geometry in self.geometries:
            visualizer.add_geometry(geometry)
        self.simulate(delta, duration, callback=VisualizationUpdater(visualizer, callback))
        visualizer.destroy_window()

    def on_update(self, callback):
        self.update_callbacks.append(callback)


class Shape:
    def __init__(self, scene):
        self.scene = scene
        self.body = Body(scene.world)
        self.scene.on_update(self.update)

    def update(self, time):
        pass


class Box(Shape):
    def __init__(self, scene, density=1, dimensions=(1, 1, 1), position=(0, 0, 0), color=(1, 0, 0)):
        Shape.__init__(self, scene)

        self.body.setMass(self.create_mass(density, dimensions))
        self.body.setPosition(position)

        self.collision = GeomBox(scene.space, lengths=dimensions)
        self.collision.setBody(self.body)

        self.geometries = self.create_geometry(dimensions, position, color)
        self.geometries.add_geometry_to(scene)

    def create_mass(self, density, dimensions):
        width, height, depth = dimensions
        mass = Mass()
        mass.setBox(density, width, height, depth)
        return mass

    def create_geometry(self, dimensions, position, color):
        geometries = approximate_mesh_box(dimensions)
        geometries.compute_vertex_normals()
        geometries.paint_uniform_color(color)
        geometries.set_transform(position)
        return geometries

    def update(self, time):

        self.update_transform_from_body()
        # print (self.body.getRotation(), self.body.getQuaternion())

    def set_position(self, position):
        self.body.setPosition(position)
        self.update_transform_from_body()

    def update_transform_from_body(self):
        self.geometries.set_transform(self.body.getPosition(), self.body.getRotation())


class GeometryWrapper:
    def __init__(self, offset, geometry):
        self.offset = offset
        # self.position = (0, 0, 0)
        self.original_geometry = geometry
        self.geometry = TriangleMesh()
        self.geometry += self.original_geometry

        # Correctly apply the offset of the geometry, only needs to be done once
        self.set_transform()

    def add_to(self, scene):
        scene.add_geometry(self.geometry)

    def set_transform(self, position=(0, 0, 0), rotation=identity):
        self.geometry.clear()
        self.geometry += self.original_geometry

        matrix = np.dot(make_matrix(position, rotation), make_matrix(self.offset, identity))
        self.geometry.transform(matrix)
        # position_diff = np.ma.subtract(position, self.position)
        # rotation_diff =
        # self.transform_geometry(position_diff)
        # self.position = position

    def transform_geometry(self, position):
        self.geometry.transform(make_matrix(position))

    def compute_vertex_normals(self):
        self.original_geometry.compute_vertex_normals()
        self.geometry.compute_vertex_normals()

    def paint_uniform_color(self, color):
        self.original_geometry.paint_uniform_color(color)
        self.geometry.paint_uniform_color(color)


class GeometryCollection:
    def __init__(self):
        self.geometries = []

    def add_geometry(self, offset, geometry):
        self.geometries.append(GeometryWrapper(offset, geometry))

    def add_geometry_to(self, scene):
        for geometry in self.geometries:
            geometry.add_to(scene)

    def set_transform(self, position=(0, 0, 0), rotation=identity):
        for geometry in self.geometries:
            geometry.set_transform(position, rotation)
        pass

    def compute_vertex_normals(self):
        for geometry in self.geometries:
            geometry.compute_vertex_normals()

    def paint_uniform_color(self, color):
        for geometry in self.geometries:
            geometry.paint_uniform_color(color)


def make_matrix(position, rotation):
    return [
        [rotation[0], rotation[1], rotation[2], position[0]],
        [rotation[3], rotation[4], rotation[5], position[1]],
        [rotation[6], rotation[7], rotation[8], position[2]],
        [0.0, 0.0, 0.0, 1.0]
        # [rotation[0], rotation[3], rotation[6], position[0]],
        # [rotation[1], rotation[4], rotation[7], position[1]],
        # [rotation[2], rotation[5], rotation[8], position[2]],
        # [0.0, 0.0, 0.0, 1.0]
    ]


def make_offset_position(axis, offset):
    if axis == 0:
        return offset, 0, 0
    if axis == 1:
        return 0, offset, 0
    if axis == 2:
        return 0, 0, offset


def approximate_mesh_box(dimensions):
    width, height, depth = dimensions
    length = depth
    collection = GeometryCollection()
    radius = min(width, height) / 2.0
    fill_distance = max(width, height) / 2.0
    cylinder_count = int(math.ceil(fill_distance / radius))
    cylinder_spacing = fill_distance / cylinder_count
    spacing_axis = 0 if width > height else 1

    # Add an initial cylinder right in the middle
    collection.add_geometry((0, 0, 0), create_mesh_cylinder(height=length, radius=radius))

    # Add extra cylinders, filling upwards
    for i in range(1, cylinder_count):
        collection.add_geometry(
            make_offset_position(spacing_axis, i * cylinder_spacing),
            create_mesh_cylinder(height=length, radius=radius)
        )

    # Add extra cylinders, filling downwards
    for i in range(1, cylinder_count):
        collection.add_geometry(
            make_offset_position(spacing_axis, -i * cylinder_spacing),
            create_mesh_cylinder(height=length, radius=radius)
        )

    return collection
