#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
from os.path import expanduser
from sensor_msgs.msg import Image
from human_feature_detect.srv import Features


srv_img = Image()
start_ok = False
def callback_img(msg):
    global srv_img, start_ok
    srv_img = msg
    start_ok = True


def main():
    global srv_img, start_ok
    rospy.init_node("human_feature_detect_sample_2d_ros")
    rospy.Subscriber("/camera/rgb/image_raw", Image, callback_img)  ## Topic名をsensor_msgs/Image型の画像にする

    while not rospy.is_shutdown():
        if start_ok:
            break      # 画像がコールバックされたら抜け出す
    
    if start_ok:
        print("撮影まで...\n3")
        rospy.sleep(1)
        print("2")
        rospy.sleep(1)
        print("1")
        rospy.sleep(1)

        # 特徴(年齢と性別)を取得してくれるServiceのサーバーが立ち上がるまで待つ
        rospy.wait_for_service("/human_feature_detect/features")
        # サーバーが立ち上がったらこちら側でクライアントとして定義する
        service = rospy.ServiceProxy("/human_feature_detect/features", Features)

        # ROSのメッセージにした写真をサーバーに送信。返答結果はresponseに代入される
        response = service(srv_img)

        # 返答されたデータから、テキストで出力する(例)
        print("検出された人数は" + str(len(response.features)) + "人です。\n")
        for i in range(len(response.features)):
            print(str(i+1) + "人目の人は、性別は" + str(response.features[i].sex) + "で、")
            print("年齢は" + str(response.features[i].age) + "歳くらいです。")
            print("表情は" + str(response.features[i].emotion) + "です。\n")

if __name__ == '__main__':
    main()
