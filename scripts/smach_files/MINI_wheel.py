#!/usr/bin/env python3
import rospy
from sobit_mini_module import SobitTurtlebotController
import sys

def fixed_wheel(wheel):
    args = sys.argv
    mini_wheel_ctr = SobitTurtlebotController(args[0]) # args[0] : C++上でros::init()を行うための引数

    # タイヤ車輪をを動かす 
    rospy.loginfo("wheel : {}".format(wheel))
    mini_wheel_ctr.controlWheelLinear(wheel)
    print("wwwwwwwwwwwwwwwwwwwwwww")

if __name__ == '__main__':
    try:
        rospy.init_node('MINI_wheel')
        fixed_wheel()
    except rospy.ROSInitException: pass
