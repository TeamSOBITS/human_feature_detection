#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import rospy
from text_to_speech.srv import TextToSpeech

def processing(msg):
    rospy.wait_for_service('/speech_word')

    try:
        service = rospy.ServiceProxy('/speech_word', TextToSpeech)
        result = service(msg)

        #print(result)


    except rospy.ServiceException as e:
        print("Service call failed: %s" % (e))


if __name__ == '__main__':
    rospy.init_node("speech", anonymous = True)
    processing()
