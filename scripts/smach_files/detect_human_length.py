#!/usr/bin/env python3
import rospy
from sobit_common_msg.msg import BoundingBoxes
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge
import cv2
import math


bottom_to_camera = 1014.1055#830 #mm     地面からカメラの高さ                    ////////
distance_from_human = 1000#1300 #mm      カメラから人の距離                ////////
degree_camera = 25#30 #deg                  カメラの角度                ////////


#camera_information
Camera_cols = 1280  #画面の大きさ横
Camera_rows = 720   #画面の大きさ縦
focal_length = 0.1961647#0.1185 #mm / from 130cm        焦点距離      ////////
image_sensor_cols = 0.27288 #mm カメラセンサの大きさ横（ここは固定）
image_sensor_rows = 0.15498 #mm カメラセンサの大きさ縦

human_length = 0

bounding_box_flag = True

def length_callback(msg):
    global human_length,bounding_box_flag
    area = []
    xmax_2 = []
    xmin_2 = []
    ymax_2 = []
    ymin_2 = []
    # xmax = msg.bounding_boxes[0].xmax
    # xmin = msg.bounding_boxes[0].xmin
    # ymax = msg.bounding_boxes[0].ymax
    # ymin = msg.bounding_boxes[0].ymin
    # face_y = (ymax + ymin) / 2

    # print(len(msg.bounding_boxes))
    number_of_bounding_box = len(msg.bounding_boxes)
    print("number_of_bounding_box:",number_of_bounding_box)
    print(number_of_bounding_box,"人を検出")

    if number_of_bounding_box < 1:
        bounding_box_flag = False
        # print("yyyyyyyyyyyyyyyyyyyyyyyyyyy")
        # print("human_length:",human_length)
        # return human_length


    if number_of_bounding_box > 1:
        bounding_box_flag = True
        for i in range(0,number_of_bounding_box):
            xmax_2.append(msg.bounding_boxes[i].xmax)
            xmin_2.append(msg.bounding_boxes[i].xmin)
            ymax_2.append(msg.bounding_boxes[i].ymax)
            ymin_2.append(msg.bounding_boxes[i].ymin)
    
        for j in range(0,number_of_bounding_box):
            area.append((xmax_2[j]-xmin_2[j])*(ymax_2[j]-ymin_2[j]))
            area.sort(reverse=True)
            if (xmax_2[j]-xmin_2[j])*(ymax_2[j]-ymin_2[j]) == area[0]:
                xmax = xmax_2[j]
                xmin = xmin_2[j]
                ymax = ymax_2[j]
                ymin = ymin_2[j]

    if number_of_bounding_box == 1:
        bounding_box_flag = True
        xmax = msg.bounding_boxes[0].xmax
        xmin = msg.bounding_boxes[0].xmin
        ymax = msg.bounding_boxes[0].ymax
        ymin = msg.bounding_boxes[0].ymin


    # print("-------------------")
    # print(xmax)
    # print(xmin)
    # print(ymax)
    # print(ymin)
    # print("-------------------")
    # print(area[0])
    # print(area[1])
    # print("-----------------")
    if bounding_box_flag:
        face_y = (ymax + ymin) / 2

    # print(xmax_2)
    # print(xmin_2)
    # print(ymax_2)
    # print(ymin_2)


    
    length_from_image_pixel = ((focal_length * distance_from_human) / image_sensor_rows) / Camera_rows
    distace_light_wheel_to_face_y = Camera_rows/2 - face_y   
    human_length = (bottom_to_camera + (math.tan(math.pi * (degree_camera / 180)) * distance_from_human) + (length_from_image_pixel * distace_light_wheel_to_face_y))*1/10

    #print(math.tan(math.pi * (degree_camera / 180)))
    
    # print(math.floor(human_length))
    # print("--------------------------\n")
    # print(round(human_length,3))

def bounding_box_judge():
    global bounding_box_flag
    rospy.Subscriber("/ssd_face_detect/object_rect", BoundingBoxes ,length_callback)
    return bounding_box_flag

def human_length_result():
    global human_length,bounding_box_flag
    # rospy.loginfo('img_proc node started')
    rospy.Subscriber("/ssd_face_detect/object_rect", BoundingBoxes ,length_callback)
    while not human_length > 0:
        if bounding_box_flag == False:
            break
        continue
    return round(human_length),bounding_box_flag
    # rospy.spin()

if __name__ == '__main__':
    try:
        rospy.init_node('img_proc')
        result = human_length_result()
        print(result)
        # rospy.spin()
        
    except rospy.ROSInterruptException: pass