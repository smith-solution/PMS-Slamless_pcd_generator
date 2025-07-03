import open3d as o3d

# Load binary PCD
pcd = o3d.io.read_point_cloud("/home/ddokkon/rosbag/pcd_tf_result/map_merged.pcd")

# Save as ASCII
o3d.io.write_point_cloud(
    "/home/ddokkon/rosbag/pcd_tf_result/map_merged_ascii.pcd",
    pcd,
    write_ascii=True
)

