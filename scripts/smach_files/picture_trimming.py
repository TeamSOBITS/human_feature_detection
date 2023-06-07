#!/usr/bin/env python3
import rospy
import cv2
from sobit_common_msg.msg import BoundingBoxes
# from sensor_msgs.msg import Images



# trimming = False

x_max = 0
x_min = 0
y_max = 0
y_min = 0
x_max_flag = False


def ssd_callback(ssd_picture):
    global x_max,x_min,y_max,y_min,x_max_flag
    area = []
    xmax_2 = []
    xmin_2 = []
    ymax_2 = []
    ymin_2 = []

    number_of_bounding_box = len(ssd_picture.bounding_boxes)

    if number_of_bounding_box > 1:
        for i in range(0,number_of_bounding_box):
            xmax_2.append(ssd_picture.bounding_boxes[i].xmax)
            xmin_2.append(ssd_picture.bounding_boxes[i].xmin)
            ymax_2.append(ssd_picture.bounding_boxes[i].ymax)
            ymin_2.append(ssd_picture.bounding_boxes[i].ymin)

        for j in range(0,number_of_bounding_box):
            area.append((xmax_2[j]-xmin_2[j])*(ymax_2[j]-ymin_2[j]))
            area.sort(reverse=True)
            if (xmax_2[j]-xmin_2[j])*(ymax_2[j]-ymin_2[j]) == area[0]:
                x_max = xmax_2[j]
                x_min = xmin_2[j]
                y_max = ymax_2[j]
                y_min = ymin_2[j]
    
    if number_of_bounding_box == 1:
        x_max = ssd_picture.bounding_boxes[0].xmax
        x_min = ssd_picture.bounding_boxes[0].xmin
        y_max = ssd_picture.bounding_boxes[0].ymax
        y_min = ssd_picture.bounding_boxes[0].ymin

    # x_max = ssd_picture.bounding_boxes[0].xmax 
    # x_min = ssd_picture.bounding_boxes[0].xmin 
    # y_max = ssd_picture.bounding_boxes[0].ymax
    # y_min = ssd_picture.bounding_boxes[0].ymin

    # img = img[y_min:y_max,x_min:x_max]#[top:bottom,left:right]
    if x_max != 0:
        x_max_flag = True

    # 画像の保存
    # cv2.imwrite( '/home/sobits/catkin_ws/src/amazon_recognition_for_fmm/imgs/test.jpg' ,img)
    # if x_max > 0:
    #     trimming = True
    # else:
    #     trimming = False

def picture_result(trimming_path):
    global x_max,x_min,y_max,y_min,x_max_flag
    # 画像の読込
    img = cv2.imread(trimming_path)
    rospy.Subscriber("/ssd_object_detect/object_rect",BoundingBoxes,ssd_callback)
    while not x_max_flag:
        continue
    # print("x_max_2:",x_max)
    top = y_min
    bottom = y_max
    left = x_min
    right = x_max
    print("top:"+str(top)+"\n"+"bottom:"+str(bottom)+"\n"+"left:"+str(left)+"\n"+"right:"+str(right))
    # img = img[y_min-10:y_max,x_min-10:x_max+10]#[top:bottom,left:right]
    img_2 = img[top : bottom, left: right]#[top:bottom,left:right]
    # print(img_2)
    # 画像の保存
    cv2.imwrite( '/home/sobits/catkin_ws/src/amazon_recognition_for_fmm/imgs/trimming.jpg' ,img_2)
    # while not trimming:
    #     continue
   

if __name__ == '__main__':
    try:
        rospy.init_node('picture_trimming')
        picture_result()


    except rospy.ROSInitException: pass

