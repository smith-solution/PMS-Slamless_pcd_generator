import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from tf2_ros import Buffer, TransformListener
from tf2_py import TransformException
from sensor_msgs_py.point_cloud2 import read_points
import open3d as o3d
import numpy as np
import transforms3d
from pathlib import Path

class PointCloudProcessor(Node):
    def __init__(self, pc_topic):
        super().__init__('pointcloud_processor')

        # 시뮬레이션 시간 사용
        self.set_parameters([
            rclpy.parameter.Parameter('use_sim_time', rclpy.Parameter.Type.BOOL, True)
        ])

        self.tf_buffer = Buffer(cache_time=rclpy.duration.Duration(seconds=60.0))
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.total_pcd = o3d.geometry.PointCloud()
        self.processed_frames = 0
        self.skipped_frames = 0

        # 저장 경로
        self.output_dir = Path.home() / "rosbag" / "pcd_tf_result_parkinglot"
        self.output_dir.mkdir(exist_ok=True)

        # 구독 시작
        self.create_subscription(
            PointCloud2,
            pc_topic,
            self.pc_callback,
            10
        )

    def pc_callback(self, msg):
        self.processed_frames += 1

        frame_id = msg.header.frame_id
        self.get_logger().debug(f"Frame ID: {frame_id}")

        try:
            # 최신 transform 사용
            trans = self.tf_buffer.lookup_transform(
                'map',
                frame_id,
                rclpy.time.Time(),  # 최신 TF
                timeout=rclpy.duration.Duration(seconds=0.5)
            )
        except TransformException as e:
            self.skipped_frames += 1
            self.get_logger().warn(
                f"TF not available for frame {frame_id}, skipping. Reason: {e}"
            )
            return

        tf_mat = self.transform_to_matrix(trans.transform)

        ros_points = read_points(msg, field_names=('x', 'y', 'z'), skip_nans=True)
        points = np.fromiter(ros_points, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
        if len(points) == 0:
            return
        points_xyz = np.stack([points['x'], points['y'], points['z']], axis=1)
        homog_points = np.hstack((points_xyz, np.ones((points_xyz.shape[0], 1))))
        points_tf = (tf_mat @ homog_points.T).T[:, :3]

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points_tf)
        self.total_pcd += pcd

        if self.processed_frames % 20 == 0:
            self.get_logger().info(
                f"Processed {self.processed_frames} frames, skipped {self.skipped_frames}"
            )

    def transform_to_matrix(self, transform):
        t = transform.translation
        q = transform.rotation
        quat = [q.w, q.x, q.y, q.z]
        rot_mat = transforms3d.quaternions.quat2mat(quat)
        tf_mat = np.eye(4)
        tf_mat[:3, :3] = rot_mat
        tf_mat[:3, 3] = [t.x, t.y, t.z]
        return tf_mat

def main():
    rclpy.init()

    pc_topic = "/carla/hero/semantic_lidar"
    node = PointCloudProcessor(pc_topic)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    # 종료 시 pointcloud 저장
    if len(node.total_pcd.points) > 0:
        output_file = node.output_dir / "map_merged.pcd"
        o3d.io.write_point_cloud(str(output_file), node.total_pcd)
        node.get_logger().info(
            f"Saved merged pointcloud to {output_file}. "
            f"Processed frames: {node.processed_frames}, skipped: {node.skipped_frames}"
        )

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

