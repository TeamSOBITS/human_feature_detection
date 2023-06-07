#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import rospy
from sobit_common_msg.srv import RunCtrl

def processing(msg):
    rospy.wait_for_service('/ulfg_face_detect/detect_ctrl')

    try:
        service = rospy.ServiceProxy('/ulfg_face_detect/detect_ctrl', RunCtrl)
        result = service(msg)

        print(result)


    except rospy.ServiceException as e:
        print("Service call failed: %s" % (e))


if __name__ == '__main__':
    rospy.init_node("ulfg_face_detect_controll", anonymous = True)
    processing()
