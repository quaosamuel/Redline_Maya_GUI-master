import numpy as np
import open3d as o3d

input_path= "C:/Users/DylanSteimel/Desktop/"
output_path= "C:/Users/DylanSteimel/Desktop/"
dataname="text4uNorms.txt"

print('Loading Text as array')
point_cloud= np.loadtxt(input_path+dataname,skiprows=1)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(point_cloud[:,:3])
pcd.colors = o3d.utility.Vector3dVector(point_cloud[:,3:6]/255)
pcd.normals = o3d.utility.Vector3dVector(point_cloud[:,6:9])

#o3d.visualization.draw_geometries([pcd])
print('Calculating distances')
distances = pcd.compute_nearest_neighbor_distance()
avg_dist = np.mean(distances)
radius = 6 * avg_dist

print('Creating Mesh')
bpa_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,o3d.utility.DoubleVector([radius, radius * 2]))

print('Simplifying Mesh')
dec_mesh = bpa_mesh.simplify_quadric_decimation(100000)

print('Cleaning Mesh')
dec_mesh.remove_degenerate_triangles()
dec_mesh.remove_duplicated_triangles()
dec_mesh.remove_duplicated_vertices()
dec_mesh.remove_non_manifold_edges()

#poisson_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8, width=0, scale=1.1, linear_fit=False)[0]

#bbox = pcd.get_axis_aligned_bounding_box()
#p_mesh_crop = poisson_mesh.crop(bbox)
print('Exporting Mesh')
o3d.io.write_triangle_mesh(output_path+"bpa_mesh.ply", dec_mesh)
#o3d.io.write_triangle_mesh(output_path+"p_mesh_c.ply", p_mesh_crop)

def lod_mesh_export(mesh, lods, extension, path):
    mesh_lods={}
    for i in lods:
        mesh_lod = mesh.simplify_quadric_decimation(i)
        o3d.io.write_triangle_mesh(path+"lod_"+str(i)+extension, mesh_lod)
        mesh_lods[i]=mesh_lod
    print("generation of "+str(i)+" LoD successful")
    return mesh_lods

my_lods = lod_mesh_export(bpa_mesh, [100000,50000,10000,1000,100], ".ply", output_path)
my_lods2 = lod_mesh_export(bpa_mesh, [8000,800,300], ".ply", output_path)
o3d.visualization.draw_geometries([my_lods[100000]])
