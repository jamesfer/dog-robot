from open3d import create_mesh_sphere, create_mesh_cylinder, create_mesh_coordinate_frame, draw_geometries

mesh_sphere = create_mesh_sphere(radius=1.0)
mesh_sphere.compute_vertex_normals()
mesh_sphere.paint_uniform_color([0.1, 0.1, 0.7])
mesh_cylinder = create_mesh_cylinder(radius=0.3, height=4.0)
mesh_cylinder.compute_vertex_normals()
mesh_cylinder.paint_uniform_color([0.1, 0.9, 0.1])
mesh_frame = create_mesh_coordinate_frame(size=0.6, origin=[-2, -2, -2])

print("We draw a few primitives using collection.")
draw_geometries([mesh_sphere, mesh_cylinder, mesh_frame])
