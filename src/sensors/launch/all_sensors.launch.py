from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='sensors',
            executable='camera_node',
            name='camera_node',
            output='screen',
            parameters=[
                {'frame_id': 'camera_frame'},
                {'width': 640},
                {'height': 480},
                {'framerate': 15.0}
            ]
        ),
        Node(
            package='sensors',
            executable='imu_node',
            name='imu_node',
            output='screen',
            parameters=[
                {'frame_id': 'imu_frame'},
                {'update_rate': 50.0}
            ]
        ),
        Node(
            package='sensors',
            executable='temp_humidity_node',
            name='temp_humidity_node',
            output='screen',
            parameters=[
                {'frame_id': 'temp_humidity_frame'},
                {'update_rate': 1.0}
            ]
        )
    ])