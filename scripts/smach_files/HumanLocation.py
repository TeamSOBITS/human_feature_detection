#!/usr/bin/env python3
import rospy
import tf
import yaml
import numpy as np


def main(Guest):
    # with open('/home/sobits/catkin_ws/src/edu_fmm/script/smach_files/move_and_location2.yaml') as file:
    with open('/home/sobits/catkin_ws/src/edu_fmm/script/smach_files/location_rcjp_2023_shiga.yaml') as file:
        config = yaml.safe_load(file)

    rate = rospy.Rate(10.0)
  
    Guest_x = Guest[0]
    Guest_y = Guest[1]

    location1_x = config['location_pose'][0]['translation_x']
    location1_y = config['location_pose'][0]['translation_y']

    location2_x = config['location_pose'][1]['translation_x']
    location2_y = config['location_pose'][1]['translation_y']

    location3_x = config['location_pose'][2]['translation_x']
    location3_y = config['location_pose'][2]['translation_y']

    location4_x = config['location_pose'][3]['translation_x']
    location4_y = config['location_pose'][3]['translation_y']

    location5_x = config['location_pose'][4]['translation_x']
    location5_y = config['location_pose'][4]['translation_y']


    Face = np.array((Guest_x, Guest_y))
    location1 = np.array((location1_x, location1_y))
    location2 = np.array((location2_x, location2_y))
    location3 = np.array((location3_x, location3_y))
    location4 = np.array((location4_x, location4_y))
    location5 = np.array((location5_x, location5_y))

    dist1 = np.linalg.norm(Face - location1)
    dist2 = np.linalg.norm(Face - location2)
    dist3 = np.linalg.norm(Face - location3)
    dist4 = np.linalg.norm(Face - location4)
    dist5 = np.linalg.norm(Face - location5)

    list_location = [dist1,dist2,dist3,dist4,dist5]

    Guest_Location = None

    if (min(list_location) == dist1):
        print("Talltableの近くにいます")
        Guest_Location = 'Tall table'
    elif (min(list_location) == dist2):
        print("Longtableの近くにいます")
        Guest_Location = 'Long table'
    elif (min(list_location) == dist3):
        print("Drawerの近くにいます")
        Guest_Location = 'Drawer'
    elif (min(list_location) == dist4):
        print("Whitetableの近くにいます")
        Guest_Location = 'White table'
    elif (min(list_location) == dist5):
        print("Binの近くにいます")
        Guest_Location = 'Bin'

        #except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            #continue

    rate.sleep()

    return Guest_Location

if __name__ == '__main__':
    rospy.init_node('tf')
    main()
