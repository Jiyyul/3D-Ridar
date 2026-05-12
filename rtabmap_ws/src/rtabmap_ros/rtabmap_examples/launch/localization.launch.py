import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    database_path = LaunchConfiguration('database_path')
    use_sim_time = LaunchConfiguration('use_sim_time')
    imu_topic = LaunchConfiguration('imu_topic')

    common_parameters = [{
        'frame_id': 'camera_link',
        'use_sim_time': use_sim_time,
        'approx_sync': True,
        'approx_sync_max_interval': 0.02,
        'wait_for_transform': 0.2,
        'sync_queue_size': 20,
        'topic_queue_size': 20,
        'subscribe_depth': False,
        'subscribe_rgbd': True,
        'subscribe_odom_info': True,
        'qos_imu': 2,
        'Vis/MinInliers': '10',
        'Vis/MinDepth': '0.3',
        'Vis/MaxDepth': '4.0',
        'Odom/ResetCountdown': '10'
    }]

    localization_parameters = [{
        'database_path': database_path,
        'Mem/IncrementalMemory': 'False',
        'Mem/InitWMWithAllNodes': 'True'
    }]

    rgbd_sync_parameters = [{
        'use_sim_time': use_sim_time,
        'approx_sync': True,
        'approx_sync_max_interval': 0.02,
        'topic_queue_size': 20,
        'sync_queue_size': 20
    }]

    rgbd_remappings = [
        ('rgb/image', '/camera/camera/color/image_raw'),
        ('rgb/camera_info', '/camera/camera/color/camera_info'),
        ('depth/image', '/camera/camera/aligned_depth_to_color/image_raw')
    ]

    localization_remappings = [
        ('rgbd_image', 'rgbd_image')
    ]

    return LaunchDescription([
        
        DeclareLaunchArgument(
            'database_path',
            default_value=os.path.expanduser('~/.ros/rtabmap_offline.db'),
            description='RTAB-Map database created during mapping. This is the map used for localization.'
        ),

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Set to true when replaying a rosbag with --clock.'
        ),
        DeclareLaunchArgument(
            'imu_topic',
            default_value='/camera/camera/imu',
            description='IMU topic remapped to rgbd_odometry input imu.'
        ),

        Node(
            package='rtabmap_sync',
            executable='rgbd_sync',
            output='screen',
            parameters=rgbd_sync_parameters,
            remappings=rgbd_remappings
        ),

        Node(
            package='rtabmap_odom',
            executable='rgbd_odometry',
            output='screen',
            parameters=common_parameters,
            remappings=localization_remappings + [('imu', imu_topic)]
        ),

        Node(
            package='rtabmap_slam',
            executable='rtabmap',
            output='screen',
            parameters=common_parameters + localization_parameters,
            remappings=localization_remappings
        ),

        Node(
            package='rtabmap_viz',
            executable='rtabmap_viz',
            output='screen',
            parameters=common_parameters + localization_parameters,
            remappings=localization_remappings
        ),
    ])
