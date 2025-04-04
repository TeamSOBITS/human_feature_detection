from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package = 'human_feature_detection_cpp', 
            executable = 'feature_detect_3d',
            name = 'feature_detect_3d',
            output = 'screen',
            parameters = [{
                'topic_name':'/points2', #点群名をここにセットする
                'target_frame':'base_footprint', #ロボットの基準フレーム
                'face_range':0.20, #顔の大体の大きさ
                'clothes_range':0.35, #服のおおよその縦幅
                'brightness_value':0 
                }]
            )
    ])

