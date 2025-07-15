# PMS-Slamless_pcd_generator
Generate PCD map files from ROS bags containing LiDAR point cloud topics and TF topics without requiring any SLAM. This tool extracts point cloud data, applies TF transformations to reconstruct the global map, and exports it as PCD files. It is compatible with any ROS2 bag that includes LiDAR and TF data, not limited to Carla simulations. 
