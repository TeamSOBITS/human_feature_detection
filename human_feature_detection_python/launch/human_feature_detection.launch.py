import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='human_feature_detection_python',   # Specify the package name
            executable='feature_detect',                # Entry point name
            name='feature_detect',                      # Node name
            output='screen'                             # Output destination
        )
    ])