#!/usr/bin/env python3
import rospy
from sobit_mini_module import SobitTurtlebotController
import sys

def fixed_rotation(rotate):
    args = sys.argv
    mini_wheel_ctr = SobitTurtlebotController(args[0]) # args[0] : C++上でros::init()を行うための引数
    
    mini_wheel_ctr.controlWheelRotateDeg(rotate)

if __name__ == '__main__':
    rospy.init_node('MINI_rotate')
    fixed_rotation()
