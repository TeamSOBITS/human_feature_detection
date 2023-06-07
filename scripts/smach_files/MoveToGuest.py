#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import rospy
import tf
import numpy as np
import math
from sobit_mini_module import SobitTurtlebotController
from sobit_mini_module import SobitMiniController
from sobit_mini_module import Joint
import sys
from geometry_msgs.msg import Vector3
from sobit_common_msg.srv import RunCtrl

facenumber_global = None
Guest_pose = None
Guest_map_pose = []
Guest_Pose_Map = None
Guest_Pose_Robot = []
onetime = False
listener = None
Guest_point = np.zeros((1,3))
Guest_point_flag = False
is_second = False
is_third = False
is_third_flag = True


def processing(msg):
    rospy.wait_for_service('/ulfg_face_detect/detect_ctrl')
    try:
        service = rospy.ServiceProxy('/ulfg_face_detect/detect_ctrl', RunCtrl)
        result = service(msg)
        print("\n\nresult:")
        print(result)
        print("\n\n")

    except rospy.ServiceException as e:
        print("Service call failed: %s" % (e))


def tf_face(mft1,rft1,deg_decided,is_first = True):
    global facenumber_global
    global listener
    global Guest_point
    global Guest_point_flag
    global is_second
    global is_third
    global is_third_flag

    args = sys.argv
    mini_wheel_ctr = SobitTurtlebotController(args[0]) # args[0] : C++上でros::init()を行うための引数
    listener = tf.TransformListener()
    
    while True:
        while not rospy.is_shutdown():
            rospy.sleep(10)
            if listener.frameExists("face_0") == False :
                rospy.sleep(1)
                processing(False)#ulfg_detect_controllをoff
                rospy.sleep(1)
                mini_wheel_ctr.controlWheelRotateDeg(deg_decided)#向いている方向にいなかったら回転
                print("deg :")
                print(deg_decided)
                deg_decided = deg_decided * -1
                rospy.sleep(0.5)
                processing(True)#ulfg_detect_controllをon

            else:
                break

        Map_guestface_trans = []
        Robot_guestface_trans = []
        guest_face = []
        
        listener.waitForTransform("/map", "/base_footprint", rospy.Time(0), rospy.Duration(2.0))
        (trans_map_robot, rot_map_robot) = listener.lookupTransform("/map", "/base_footprint", rospy.Time(0))#map基準のbasefootprint
        print("--------------------------------")
        print("trans_map_robot, rot_map_robot:")
        print(trans_map_robot, rot_map_robot)
        print("--------------------------------")
        RobotBase_x = trans_map_robot[0]#x座標
        RobotBase_y = trans_map_robot[1]#y座標
        RobotBase_z = trans_map_robot[2]#z座標
        RobotBase_qx = rot_map_robot[0]#qx座標
        RobotBase_qy = rot_map_robot[1]#qy座標
        RobotBase_qz = rot_map_robot[2]#qz座標
        RobotBase_qw = rot_map_robot[3]#qw座標

        robot_euler = tf.transformations.euler_from_quaternion((RobotBase_qx, RobotBase_qy, RobotBase_qz, RobotBase_qw))
        Bf_rot_Z = robot_euler[2]#map基準のbasefootprintのZ軸
        detect_flag1 = False

        print("robot_euler:",robot_euler)

        linear1 = 0.1
        while not detect_flag1:#xtionで取れた人数分のそれぞれの座標を取得（map基準から見たface）
            for k in range(100):
                if listener.frameExists("face_{}".format(k)):
                    try:
                        listener.waitForTransform('/map', "face_{}".format(k) , rospy.Time(0), rospy.Duration(2.0))
                        (map_guestface_trans, map_guestface_rot) = listener.lookupTransform('/map', "face_{}".format(k) , rospy.Time(0))
                    except:
                        print("mistake_tf")#死んでないtfを確認&確実に映っているtfのみを取得できるように
                        break
                    print("\n\nmap_guestface_trans\n\n",map_guestface_trans,"\n\n")
                    Map_guestface_trans.append(map_guestface_trans)
                    detect_flag1 = True
                elif k == 0:
                    print("failed!!", "face_{}".format(k))
                    mini_wheel_ctr.controlWheelLinear(linear1)
                    rospy.sleep(3)
                    linear1 *= -0.5
                    break
                else:
                    break
        print("Map_guestface_trans_1 : ",Map_guestface_trans)

        detect_flag2 = False
        linear2 = 0.1
        while not detect_flag2:#xtionで取れた人数分のそれぞれの座標を取得（base_footprint基準から見たface）
            for j in range(100):
                if listener.frameExists("face_{}".format(j)):
                    print("j:",j)
                    try:
                        listener.waitForTransform('/base_footprint', "face_{}".format(j) , rospy.Time(0), rospy.Duration(2.0))
                        (robot_guestface_trans, robot_guestface_rot) = listener.lookupTransform('/base_footprint', "face_{}".format(j) , rospy.Time(0))
                    except:
                        print("mistake_tf")
                        break
                    if robot_guestface_trans[0] < 0:
                        print("\n\nロボットより後ろにいます\n\n")
                        continue
                    print("\n\nrobot_guestface_trans",robot_guestface_trans,"\n\n")
                    Robot_guestface_trans.append(robot_guestface_trans)
                    detect_flag2 = True
                elif j == 0:
                    print("failed!!", "face_{}".format(j))
                    mini_wheel_ctr.controlWheelLinear(linear2)
                    rospy.sleep(3)
                    linear2 *= -0.5
                    break
                else:
                    break
        print("Robot_guestface_trans_1 :", Robot_guestface_trans)

        #map外判定
        # map_xmin = -1.0016393661 #競技用map
        # map_xmax = 1.80836481094
        # map_ymin = -4.2087244606
        # map_ymax = -1.70619080067

        # map_xmin = -2.9718446731 #e301map
        # map_xmax = 1.33827233314
        # map_ymin = -1.25119900703
        # map_ymax = 4.358048439025

        # map_xmin = -3.45233535766 #choi labo
        # map_xmax = 9.09232330322
        # map_ymin = -6.68825721740
        # map_ymax = 3.00499439239
       
        # map_xmin = -1.60016393661#競技用map
        # map_xmax = 2.15836481094
        # map_ymin = -4.3087244606
        # map_ymax = -1.95619080067

        # map_xmin = -2.517955303192 #e301map_4月模擬競技
        # map_xmax = 2.1429677009582
        # map_ymin = -1.094612240791
        # map_ymax = 4.6707000732421
    
        map_xmin = 0.733097136020 #rcjp_2023_shiga
        map_xmax = 4.551927566528
        map_ymin = -3.23575973510
        map_ymax = 1.025874614715

        for m in range(len(Map_guestface_trans)):#mapの内外判定
            if map_xmin <= Map_guestface_trans[m][0] and Map_guestface_trans[m][0] <= map_xmax and map_ymin <= Map_guestface_trans[m][1] and Map_guestface_trans[m][1] <= map_ymax:
                print("mapにいます")
                
                guest_face.append(Map_guestface_trans[m])
                print("guest_face:",guest_face)
            else:
                print("mapの外にいます")
                # Robot_guestface_trans[m][0] = 100
                # Robot_guestface_trans[m][1] = 100

        if len(guest_face) == 0:#ゲストがいない場合最初の処理に戻る
            processing(False)#ulfg_detect_controllをoff
            rospy.sleep(1)
            mini_wheel_ctr.controlWheelRotateDeg(deg_decided)#向いている方向にいなかったら回転
            print("deg :")
            print(deg_decided)
            deg_decided = deg_decided * -1
            rospy.sleep(0.5)
            processing(True)#ulfg_detect_controllをon
            rospy.sleep(5)
            continue
        # print(guest_face)

        distance_face_robot = []#ロボットとゲストそれぞれの間の距離
        for n in range(len(Robot_guestface_trans)):
            Robot_face = np.array((Robot_guestface_trans[n][0], Robot_guestface_trans[n][1]))
            print("Robot_face :")
            print(Robot_face)
            robot_base = np.array((0,0))
            print("robot_base:")
            print(robot_base)
            dist = np.linalg.norm(Robot_face - robot_base)
            print("dist :")
            print(dist)
            distance_face_robot.append(dist)
        print(distance_face_robot)
        print("Robot_guestface_trans_3:"+ str(distance_face_robot))

        zip_lists = list(zip(distance_face_robot, Robot_guestface_trans))#ロボットから一番近い人の座標順にソートしている
        print("zip_lists:",zip_lists)
        zip_sort = sorted(zip_lists)
        print("zip_sort",zip_sort)
        print("Robot_guestface_trans_4:"+str(len(Robot_guestface_trans)))
        distance_face_robot, Robot_guestface_trans = zip(*zip_sort)
        print("Robot_guestface_trans_5:"+str(len(Robot_guestface_trans)))
        is_checked = True

        for o in range(0,len(Robot_guestface_trans)):
            print("number_o:",o)

            for p in range(0,len(guest_face)):
                print("number_p:",p)
                
                # if abs(guest_face[p][0] - RobotBase_x - Robot_guestface_trans[o][0]*np.cos(Bf_rot_Z) - Robot_guestface_trans[o][1]*np.sin(Bf_rot_Z)) <= 0.5 and abs(guest_face[p][1] - RobotBase_y - Robot_guestface_trans[o][0]*np.sin(Bf_rot_Z) - Robot_guestface_trans[o][1]*np.cos(Bf_rot_Z)) <= 0.5 :#比較した座標が指定範囲内かつmap内だったらゲストとして登録
            
                is_checked = False
                # Guest_point_flag = False           
                print("Robot_guestface_trans_6 :",Robot_guestface_trans[o])
                print("guest_face1 :", guest_face[p])
                
                if is_checked == False:
                    # Guest_point = np.zeros((3,3))
                    # if 0 < abs(Guest_point[0][0] - guest_face[0][0]) < 0.5 and 0 < abs(Guest_point[0][1] - guest_face[0][1]) < 0.5 and Guest_point_flag == True:
                    #     mini_wheel_ctr.controlWheelRotateDeg(-50)
                    #     Guest_point_flag = False

                    if is_third == True:
                        mft1.append(guest_face[p])
                        rft1.append(Robot_guestface_trans[o])
                        is_third = False
                        # is_third_flag = False
                        print("mft1_3",mft1)
                        print("rft1_3",rft1)
                        return mft1,rft1

                    if is_first == True:
                        # Guest_point = np.array((0,0,0))
                        mft1.append(guest_face[p])#一人目の値が入る
                        rft1.append(Robot_guestface_trans[o])
                        is_first = False
                        
                        Guest_point = mft1
                        Guest_point_flag = True
                        print("\n\n")
                        print("Guest_point:")
                        print(Guest_point)
                        print("\n\n")
                        print("mft1a : " , mft1[0][0])
                        print("guest_face" ,guest_face[p][0])
                        
                    
                    # if 0 < abs(mft1[0][0]-guest_face[p][0]) < 0.5 and 0 < abs(mft1[0][1]-guest_face[p][1]) < 0.5 and Guest_point_flag == True:
                    #     mini_wheel_ctr.controlWheelRotateDeg(-50)
                    
                    # if 0 < abs(mft1[0][0]-guest_face[p][0]) <0.5 and 0 < abs(mft1[0][1]-guest_face[p][1]) <0.5:
                    #     mini_wheel_ctr.controlWheelRotateDeg(-50)
    
                    if abs(mft1[0][0]-guest_face[p][0]) < 0.5 and abs(mft1[0][1]-guest_face[p][1]) < 0.5:
                        print("ゲスト１探索済み")
                        print("mft1_x:",mft1[0][0])
                        print("guest_face_x:",guest_face[p][0])
                        print("guest_face_y:",guest_face[p][1])
                        # mini_wheel_ctr.controlWheelRotateDeg(-50)

                    else:
                    # elif is_second == True:
                        print("二人目です")
                        print("mft1_x:",mft1[0][0])
                        print("guest_face_x:",guest_face[p][0])
                        print("guest_face_y:",guest_face[p][1])                            
                        mft1.append(guest_face[p])
                        rft1.append(Robot_guestface_trans[o])
                        is_third = True
                        
                        print("mft1 :")
                        print(mft1)
                        return mft1,rft1
                # else:
                #     print("pokrr")
                # if is_third_flag == False:
                #     break
        return mft1,rft1          

                            
def main(mft1,rft1,delta,is_first = True): 
    global Guest_pose
    global listener
    global Guest_Pose_Map
    global Guest_Pose_Robot
    global onetime
    args = sys.argv
    mini_wheel_ctr = SobitTurtlebotController(args[0]) # args[0] : C++上でros::init()を行うための引数
    print("delta:",delta)
    if delta == 0:
        deg_decided = -50
    if delta == 1:
        deg_decided = 50
    num = len(Guest_Pose_Robot)
    print("-------------------------------")
    print("num:"+str(num))
    # print("tf_num :"+str(len(Guest_Pose_Robot)))
    print("Guest_Pose_Robot :"+str(len(Guest_Pose_Robot)))
    print("-------------------------------")
    # print(len(Guest_Pose_Robot))
    print("mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
    while num == len(Guest_Pose_Robot):
        Guest_Pose_Map,Guest_Pose_Robot = tf_face(mft1,rft1,deg_decided,is_first)
    print(onetime, is_first)
    processing(False)#ulfg_detect_controllをoffにした

    for i in Guest_Pose_Map:
        print("Guest_Pose_Map:",i)

    for j in Guest_Pose_Robot:
        print("Guest_Pose_Robot:",j)

    if (onetime == False):
        print(Guest_Pose_Robot[0][1], Guest_Pose_Robot[0][0])
        deg = np.degrees(np.arctan2(Guest_Pose_Robot[0][1], Guest_Pose_Robot[0][0]))
        rospy.loginfo("\n\ndeg_decided : {}\n\n".format(deg))
        mini_wheel_ctr.controlWheelRotateDeg(deg)
        rospy.sleep(2)
        mini_wheel_ctr.controlWheelLinear(Guest_Pose_Robot[0][0] - space_human)
        a = Guest_Pose_Robot[0][0] - space_human
        print(Guest_Pose_Robot[0][0])
        print(space_human)
        print("\n\nMoveToGuest_result:"+str(a)+"\n\n")
        rospy.sleep(0.5)
        onetime = True

    return Guest_Pose_Map,Guest_Pose_Robot
    
    
def get(space):
    global space_human
    space_human = space


if __name__ == '__main__':
    rospy.init_node('move_to_guest1')

    main()