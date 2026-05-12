import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():

    database_path = LaunchConfiguration('database_path')
    imu_topic = LaunchConfiguration('imu_topic')

    parameters=[{
          'frame_id':'camera_link',
          'subscribe_depth':False,
          'subscribe_rgbd':True,
          'subscribe_odom_info':True,
          'approx_sync':True,
          'qos_imu':2}] # False: exac sync, True: approx sync (if your camera is not publishing synchronized RGB and depth images)
    rtabmap_parameters = parameters + [{'database_path': database_path}]

    remappings = [
        ('rgb/image', '/camera/camera/color/image_raw'),
        ('rgb/camera_info', '/camera/camera/color/camera_info'),
        ('depth/image', '/camera/camera/aligned_depth_to_color/image_raw')
    ]

    return LaunchDescription([

        DeclareLaunchArgument(
            'database_path',
            default_value=os.path.expanduser('~/.ros/rtabmap_offline.db')
        ),
        DeclareLaunchArgument(
            'imu_topic',
            default_value='/camera/camera/imu'
        ),

        Node(
            package='rtabmap_sync',
            executable='rgbd_sync',
            output='screen',
            parameters=[{
                'approx_sync': True,
                'sync_queue_size': 20,
                'topic_queue_size': 20
            }],
            remappings=remappings
        ),

        Node(
            package='rtabmap_odom',
            executable='rgbd_odometry',
            output='screen',
            parameters=parameters,
            remappings=[('imu', imu_topic)]
        ),

        Node(
            package='rtabmap_slam',
            executable='rtabmap',
            output='screen',
            parameters=rtabmap_parameters,
            arguments=['-d']
        ),

        Node(
            package='rtabmap_viz',
            executable='rtabmap_viz',
            output='screen',
            parameters=parameters
        ),
    ])
