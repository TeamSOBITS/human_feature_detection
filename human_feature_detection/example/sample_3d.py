#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import rospy
import rclpy
from rclpy.node import Node
from time import sleep
from human_feature_detection_msgs.srv import Feature3d

def main():
    # rospy.init_node("human_feature_detect_sample_3d")
    rclpy.init()
    nd = Node("human_feature_detect_sample_2d_ros")

    # サーバーが立ち上がったらこちら側でクライアントとして定義する
    # service = rospy.ServiceProxy("/human_feature_detection/feature3d", Feature3d)
    client = nd.create_client(Feature3d, "/human_feature_detection/feature3d")

    # 特徴(身長と服の色)を取得してくれるServiceのサーバーが立ち上がるまで待つ
    client.wait_for_service()
    # rospy.wait_for_service("/human_feature_detection/feature3d")

    # ロボット(カメラ)の前方何メートルから何メートルまでの範囲にある点群を検出するかをサーバーに送信
    # 返答結果はresponseに代入される
    # 以下の例では0.2メートルから1.2メートルの範囲の点群で検出する
    req = Feature3d.Request()
    req.min_range = 0.2
    req.max_range = 1.2
    f = client.call_async(req)
    rclpy.spin_until_future_complete(nd, f)
    response = f.result()
    # response = service(0.2, 1.2)

    # 返答されたデータから、テキストで出力する(例)
    print("身長は、およそ" + str(response.height) + "センチメートルです。")
    if (response.color_success):
        print("服の色は、" + str(response.color) + "です。")
    else:
        print("服の色がよくわかりません。")

if __name__ == '__main__':
    main()