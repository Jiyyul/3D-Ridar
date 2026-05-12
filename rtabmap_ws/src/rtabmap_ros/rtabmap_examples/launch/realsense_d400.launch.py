# Requirements:
#   A realsense D400 series
#   Install realsense2 ros2 package (make sure you have this patch: https://github.com/IntelRealSense/realsense-ros/issues/2564#issuecomment-1336288238)
# Example:
#   $ ros2 launch rtabmap_examples realsense_d400.launch.py

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node, SetParameter
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    parameters=[{
          'frame_id':'camera_link',
          'subscribe_depth':True,
          'subscribe_odom_info':True,
          'approx_sync':True}] # False: exac sync, True: approx sync (if your camera is not publishing synchronized RGB and depth images)

    remappings=[
          ('rgb/image', '/camera/camera/color/image_raw'),
          ('rgb/camera_info', '/camera/camera/color/camera_info'),
          ('depth/image', '/camera/camera/aligned_depth_to_color/image_raw')]

    return LaunchDescription([

        # Make sure IR emitter is enabled
        # D455 depth는 stereo 기반으로, IR emitter가 켜져있어야 depth가 제대로 나온다.
        SetParameter(name='depth_module.emitter_enabled', value=1),

        # Launch camera driver
        # width x height x fps
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('realsense2_camera'), 'launch'),
                '/rs_launch.py']),
                launch_arguments={'align_depth.enable': 'true',
                                  'rgb_camera.color_profile': '640,360,30',
                                  'enable_gyro': 'true',
                                  'enable_accel': 'true',
                                  'unite_imu_method': '2'},
                                  .items(),
        ),
        # odometry 계산하는 노드
        Node(
            package='rtabmap_odom', executable='rgbd_odometry', output='screen',
            parameters=parameters,
            remappings=remappings),
        # map과 pose graph 관리하는 SLAM back-end 노드
        Node(
            package='rtabmap_slam', executable='rtabmap', output='screen',
            parameters=parameters,
            remappings=remappings,
            arguments=['-d']),
        # map visualization 노드
        Node(
            package='rtabmap_viz', executable='rtabmap_viz', output='screen',
            parameters=parameters,
            remappings=remappings),
    ])
