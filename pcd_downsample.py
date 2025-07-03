import open3d as o3d

# 원본 PCD 읽기
pcd = o3d.io.read_point_cloud("map_merged.pcd")
print("Original point cloud has", len(pcd.points), "points")

# 과감하게 다운샘플링
voxel_size = 0.4  # 40cm voxel
downsampled_pcd = pcd.voxel_down_sample(voxel_size)

print("Downsampled point cloud has", len(downsampled_pcd.points), "points")

# 저장
o3d.io.write_point_cloud("downsampled_map_merged.pcd", downsampled_pcd)
