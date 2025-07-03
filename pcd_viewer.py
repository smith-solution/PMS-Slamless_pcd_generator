import open3d as o3d

# 저장한 pcd 경로
pcd = o3d.io.read_point_cloud("/home/ddokkon/rosbag/pcd_tf_result/map_merged.pcd")

print(pcd)  # 점 개수 정보

# 보기
o3d.visualization.draw_geometries([pcd])

