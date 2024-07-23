#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import rospy
import rclpy
from rclpy.node import Node
from time import sleep
# from os.path import expanduser
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from human_feature_detection.srv import Features


srv_img = Features.Request()
start_ok = False
def callback_img(msg):
    global srv_img, start_ok
    srv_img.input_image = msg
    start_ok = True


def main():
    global srv_img, start_ok
    # rospy.init_node("human_feature_detect_sample_2d_ros")
    # rospy.Subscriber("/rgb/image_raw", Image, callback_img)  ## Topic名をsensor_msgs/Image型の画像にする
    rclpy.init()
    nd = Node("human_feature_detect_sample_2d_ros")
    sub = nd.create_subscription(Image, "/rgb/image_raw", callback_img, qos_profile_sensor_data)  ## Topic名をsensor_msgs/Image型の画像にする

    while rclpy.ok():
        if start_ok:
            break      # 画像がコールバックされたら抜け出す
    
    if start_ok:
        print("撮影まで...\n3")
        sleep(1)
        print("2")
        sleep(1)
        print("1")
        sleep(1)

        # サーバーが立ち上がったらこちら側でクライアントとして定義する
        client = nd.create_client(Features, "/human_feature_detection/features")
        # # 特徴(年齢と性別)を取得してくれるServiceのサーバーが立ち上がるまで待つ
        client.wait_for_service()
        # # 特徴(年齢と性別)を取得してくれるServiceのサーバーが立ち上がるまで待つ
        # rospy.wait_for_service("/human_feature_detection/features")
        # # サーバーが立ち上がったらこちら側でクライアントとして定義する
        # service = rospy.ServiceProxy("/human_feature_detection/features", Features)

        # ROSのメッセージにした写真をサーバーに送信。返答結果はresponseに代入される
        f = client.call_async(srv_img)
        rclpy.spin_until_future_complete(nd, f)
        response = f.result()

        # 返答されたデータから、テキストで出力する(例)
        print("検出された人数は" + str(len(response.features)) + "人です。\n")
        for i in range(len(response.features)):
            print(str(i+1) + "人目の人は、性別は" + str(response.features[i].sex) + "で、")
            print("年齢は" + str(response.features[i].age) + "歳くらいです。")
            print("表情は" + str(response.features[i].emotion) + "です。\n")

if __name__ == '__main__':
    main()
