#!/usr/bin/env python3
import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from human_feature_detect.srv import ImageToFeatures
from human_feature_detect.srv import PathToFeatures

def main():
    path()
    # img()
    rospy.spin()

def path():
    rospy.init_node('client')
    num = input("number = ")
    path = "/home/sobits/catkin_ws/src/human_feature_detect/img" + num + ".jpg"
    rospy.wait_for_service("/human_feature_detect/imagepath_features")
    service = rospy.ServiceProxy("/human_feature_detect/path_features", PathToFeatures)
    res = PathToFeatures()
    res.path = path
    re = service(res.path)
    print(re)

def img():
    rospy.init_node('client')
    num = input("number = ")
    pic = cv2.imread("/home/sobits/catkin_ws/src/human_feature_detect/img" + num + ".jpg")
    bridge = CvBridge()
    image_msg = bridge.cv2_to_imgmsg(pic, encoding="bgr8")
    rospy.wait_for_service("/human_feature_detect/imagedata_features")
    service = rospy.ServiceProxy("/human_feature_detect/image_features", ImageToFeatures)
    res = ImageToFeatures()
    res.image = image_msg
    re = service(res.image)
    print(re)


if __name__ == '__main__':
    main()