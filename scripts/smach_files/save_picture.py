#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
from picture_saver.srv import picture_cmd

# filepath = "/home/sobits/catkin_ws/src/picture_saver/imgs/"
filepath = "/home/sobits/catkin_ws/src/amazon_recognition_for_fmm/imgs/"

def save_result(img_name):
    global filepath
    rospy.wait_for_service('/picture_cmd')
    try:
        pic_save = rospy.ServiceProxy("/picture_cmd", picture_cmd)
        res = pic_save(1, filepath , img_name)
    except rospy.ServiceException as e:
	    print ("Service call failed: %s"%e)

if __name__ == "__main__":
    # 出力ファイル名を指定
    image_name = "example.jpg"
    save_result(image_name)

