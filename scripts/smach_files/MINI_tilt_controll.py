#!/usr/bin/env python3
import rospy
from sobit_mini_module import SobitMiniController
from sobit_mini_module import Joint
import sys
import numpy as np

def Tilt(tiltdegree):
    r = rospy.Rate(1) # 10hz
    ang = np.deg2rad(tiltdegree)
    args = sys.argv
    mini_pantilt_ctr = SobitMiniController(args[0]) # args[0] : C++上でros::init()を行うための引数

        # カメラチルトを動かす
    mini_pantilt_ctr.moveJoint( Joint.HEAD_TILT_JOINT, ang, 3.0, False )
    r.sleep()

if __name__ == '__main__':
    rospy.init_node('head_move')
    Tilt(0)
