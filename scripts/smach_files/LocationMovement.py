#!/usr/bin/env python3
import rospy
from sobit_navigation_module import SOBITNavigationLibraryPython
import sys

def LocationMove(DecidedMove):
    r = rospy.Rate(10) # 10hz
    args = sys.argv
    nav_lib = SOBITNavigationLibraryPython(args[0]) # args[0] : C++上でros::init()を行うための引数

    nav_lib.move2Location( DecidedMove, True )
    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        #rospy.loginfo("move2Location")
        if ( nav_lib.exist_goal_ == False ) : break
        r.sleep()
    rospy.sleep(2)

if __name__ == '__main__':
    rospy.init_node("move", anonymous = True)
    LocationMove()
