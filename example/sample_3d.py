#!/usr/bin/env python3
import rospy
from human_feature_detect.srv import Feature3d

def main():
    rospy.init_node("human_feature_detect_sample_3d")

    # 特徴(身長と服の色)を取得してくれるServiceのサーバーが立ち上がるまで待つ
    rospy.wait_for_service("/human_feature_detect/feature3d")
    # サーバーが立ち上がったらこちら側でクライアントとして定義する
    service = rospy.ServiceProxy("/human_feature_detect/feature3d", Feature3d)

    # ロボット(カメラ)の前方何メートルから何メートルまでの範囲にいる点群を検出するかをサーバーに送信
    # 返答結果はresponseに代入される
    # 以下の例では0.2メートルから1.2メートルの範囲の点群で検出する
    response = service(0.2, 1.2)

    # 返答されたデータから、テキストで出力する(例)
    print("身長は、およそ" + str(response.height) + "センチメートルです。")
    if (response.color_success):
        print("服の色は、" + str(response.color) + "でした。")
    else:
        print("服の色がよくわかりませんでした。")
    rospy.spin()

if __name__ == '__main__':
    main()