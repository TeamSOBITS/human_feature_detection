#!/usr/bin/env python3
import rospy
from os.path import expanduser
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from human_feature_detect.srv import Features

def main():
    rospy.init_node("human_feature_detect_sample_2d")
    home_path = expanduser("~") # ここにターミナルのhomeディレクトリまでのパスが代入  ex) home_path = "/home/sobits"

    # 写真をopencvで読み込む。home_path + catkin_ws以降の写真ホルダーまでのパスを入力
    picture_file_path = home_path + "/catkin_ws/src/human_feature_detect/images/sample_image.png"
    picture = cv2.imread(picture_file_path)
    picture_rgb = cv2.cvtColor(picture, cv2.COLOR_BGR2RGB)
    bridge = CvBridge()

    # 写真の型(BGR型)から、ROSで通信を行える型(sensor_msgs/Image型)に変換する
    image_msg = bridge.cv2_to_imgmsg(picture_rgb)

    # 特徴(年齢と性別)を取得してくれるServiceのサーバーが立ち上がるまで待つ
    rospy.wait_for_service("/human_feature_detect/features")
    # サーバーが立ち上がったらこちら側でクライアントとして定義する
    service = rospy.ServiceProxy("/human_feature_detect/features", Features)

    # ROSのメッセージにした写真をサーバーに送信。返答結果はresponseに代入される
    response = service(image_msg)

    # 返答されたデータから、テキストで出力する(例)
    print("検出された人数は" + str(len(response.features)) + "人です。\n")
    for i in range(len(response.features)):
        print(str(i+1) + "人目の人は、性別は" + str(response.features[i].sex) + "で、")
        print("年齢は" + str(response.features[i].age) + "歳くらいです。\n")

if __name__ == '__main__':
    main()
