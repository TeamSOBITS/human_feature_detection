#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from std_msgs.msg       import Float64
from std_msgs.msg import String
from cv_bridge import CvBridge
from geometry_msgs.msg import Point
#from ulfg_face_detector.msg import BoundingBoxesStamp#追加

cascade_filename = '/home/sobits/catkin_ws/src/sample_py/filter/haarcascade_frontalface_alt.xml'
cascade = cv2.CascadeClassifier(cascade_filename)

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

age_net = cv2.dnn.readNetFromCaffe(
	'/home/sobits/catkin_ws/src/sample_py/filter/deploy_age.prototxt',
	'/home/sobits/catkin_ws/src/sample_py/filter/age_net.caffemodel')

gender_net = cv2.dnn.readNetFromCaffe(
	'/home/sobits/catkin_ws/src/sample_py/filter/deploy_gender.prototxt',
	'/home/sobits/catkin_ws/src/sample_py/filter/gender_net.caffemodel')

age_list = ['(0 ~ 2)','(4 ~ 6)','(8 ~ 12)','(15 ~ 20)',
            '(25 ~ 32)','(38 ~ 43)','(48 ~ 53)','(60 ~ 100)']
gender_list = ['Male', 'Female']

result_age = None
result_gender = None

result_flag = False

def imgDetector(img,cascade,age_net,gender_net,MODEL_MEAN_VALUES,age_list,gender_list):
    global result_age, result_gender,result_flag
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    pub_gender = rospy.Publisher('gender', String, queue_size=10)
    pub_age = rospy.Publisher('age', String, queue_size=10)
    pub_coordinates = rospy.Publisher('coordinates_face', Point, queue_size=10)

    results = cascade.detectMultiScale(img,            
                                        scaleFactor= 1.1,
                                        minNeighbors=5,  
                                        minSize=(20,20)  
                                        )
    
    gender = None
    age = None
    position = Point(None,None,None)

    for box in results:

        x, y, w, h = box
        face = img[int(y):int(y+h),int(x):int(x+h)].copy()
        blob = cv2.dnn.blobFromImage(face, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        
        # gender detection
        gender_net.setInput(blob)
        gender_preds = gender_net.forward()
        gender = gender_preds.argmax()
        # Predict age
        age_net.setInput(blob)
        age_preds = age_net.forward()
        age = age_preds.argmax()
        info = gender_list[gender] +' '+ age_list[age]
        result_age = age_list[age]
        result_gender = gender_list[gender]
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,255,255), thickness=2)
        cv2.putText(img, info, (x,y),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
        position = Point(x,y,0)

        # rospy.loginfo(info)
    # print(result_age)

    pub_gender.publish(gender)
    pub_age.publish(age)
    pub_coordinates.publish(position)

    result_flag = True

    # cv2.imshow('facenet',img)  
    # cv2.waitKey(1)

def age_gender_callback(msg):
    try:
        bridge = CvBridge()
        orig = bridge.imgmsg_to_cv2(msg, "bgr8")
        #img = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
        imgDetector(orig,cascade,age_net,gender_net,MODEL_MEAN_VALUES,age_list,gender_list )

    except Exception as err:
        print(err)

def result_age_gender():
    global result_age, result_gender,result_flag
    # print(info)
    # rospy.loginfo('img_proc node started')
    # rospy.Subscriber("/usb_cam/image_raw", Image, process_image)
    # rospy.Subscriber("/camera/color/image_raw", Image, process_image)
    rospy.Subscriber("/image_topic", Image, age_gender_callback)
    # rospy.Subscriber("/result_image_correction", Image, age_gender_callback)
    # rospy.Subscriber("/ulfg_face_detect/faces_rect_stamp", BoundingBoxesStamp, process_image)
    # rospy.spin()
    # while not result_age != None:
    #     continue
    while result_flag == False:
        continue
    result_flag = False
    return result_age, result_gender

if __name__ == '__main__':
    try:
        rospy.init_node('img_proc')
        a = result_age_gender()
        print(a)
    except rospy.ROSInterruptException:
        pass
