#!/usr/bin/env python3
import numpy as np

guest_point = np.zeros((3,3))
# guest_point = []
b = []
c = []

def test_numpy():
    global guest_point
    a = [[1.5,-0.2,0.9],[-2.3,5.9,6.2],[0.3,9.0,0.5]]
    # a=guest_point
    # for i in range(0,len(a)):
    #     b.append(a[i])
    # print(a[0])
    # b.append(a[0])
    # b.append(a[1])
    # c.append(b)
    print("guest_point:\n",guest_point)
    print("a:",a)
    # guest_point = a
    # print("guest_point_2:",guest_point[0])
    # print("b_1:",b)
    for i in range(0,len(a)):
        if a[i][0] < 0:
            print("ロボットより後ろにいます")
            continue
        b.append(a[i])
    print("b_1:",b)
    # print("c:",c)
    if 0 < guest_point[2][0] < 0.9:
        print("ok")
    guest_point = b
    print("guest_point_4",guest_point)
    print("guest_point_5",guest_point[0][0])
    for i in guest_point:
        print("result:\n",i)
    print("debug",guest_point)
    # if 0 < guest_point[2][0] < 0.9:
    #     print("ok")
    # if guest_point[0][0] > 1.0:
    #     print("ok_2")
    # guest_point_2 = np.append(guest_point,a,axis=1)
    # print(guest_point_2)
    # print(np.degrees(np.arctan2(-0.03424632549285889, 1.98520827293396)))
    # print(np.degrees(np.arctan2(-0.8705790042877197, 3.033323049545288)))

if __name__ == '__main__':
    test_numpy()