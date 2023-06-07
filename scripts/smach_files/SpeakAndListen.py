#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
import random
from web_speech_recognition.srv import SpeechRecognition
from text_to_speech.srv import TextToSpeech

def speak(msg):
    rospy.wait_for_service('/speech_word')

    try:
        service = rospy.ServiceProxy('/speech_word', TextToSpeech)
        result = service(msg)
        print(result)

    except rospy.ServiceException as e:
        print("Service call failed: %s" % (e))

# 音声を聞き取る(google_speech_recognitionを用いる)
def listen(timeout_sec):
    rospy.loginfo('waiting service')
    rospy.wait_for_service('/speech_recognition')

    while True:
        try:
            service = rospy.ServiceProxy('/speech_recognition', SpeechRecognition)
            response = service(timeout_sec)
            print(response.transcript)
            break

        except rospy.ServiceException as e:
            print ("Service call failed: %s" % (e))

    return response.transcript

def conversation():
    Guestname = None
    speak("Answer after the buzzer.")
    for h in range(10):
        answer_flag = False
        name_flag = False
        speak("what is your name?")
        rospy.sleep(1)
        listen1 = listen(8)
        name_number = 0
        name_list = ["Amelia", "Angel", "Ava", "Charlie", "Charlotte", "Hunter", "Jack", "Max", "Mia", "Noah", "Oliver", "Olivia", "Parker", "Sam", "Thomas", "William"]
        replace_lists = [
        ["Amelia", "America", "American", "ameria", "americium", "ameri", "ameriga", "amerio", "amidia", "ameridia", "media"],
        ["Angel", "Angela", "angel", "banjo", "Ender", "inverse", "there", "enter", "engineer", "engine", "angels", "Angelo", "angelle", "Andrew"],
        ["Ava", "favor", "Eva", "neighbor", "fever", "ever", "awful", "April", "evil", "Avila"],
        ["Charlie", "cherry", "sorry", "Charly", "Chari", "charity", "Sherry", "showering", "Shari", "sharing", "Sharon", "charity", "Tony", "tell"],
        ["Charlotte", "shut", "Cheryl", "charot", "charlott", "cherot", "Cheroke", "cherub", "Cherokee", "cherube", "charitable", "Charleston", "Charlotte", "shuttle"],
        ["Hunter", "hunta", "Hanta", "Honda", "control", "Honkers", "Horner", "portal", "honka", "hunt"],
        ["Jack", "Chuck", "Jak", "check", "joke", "Jac", "jock", "check", "Jeff", "duck"],
        ["Max", "maps", "mark", "knock", "nap", "marks", "Maxx", "Knox", "Mox"],
        ["Mia", "mere", "Mira", "mirror", "near", "Mir", "yeah", "Mya", "Mayer", "Maya", "Maia", "Myer"],
        ["Noah", "law", "North", "know", "Moa", "Norah", "knock", "more", "Roar", "Noel", "Noir", "Laura"],
        ["Oliver", "horrible", "River", "River", "river", "oribur", "Rivera", "Boulevard", "oriber", "Oriole", "Oregon", "origin", "Audible"],
        ["Olivia", "arubia", "Arabian", "Arabia", "aravian", "aravia", "Bolivia", "oruvia", "rubia", "Aruba", "arubia"],
        ["Parker", "Papa", "purple", "Popeye", "Poppa", "parka", "parkour", "Peppa", "Paka", "Paca", "poker", "packer"],
        ["Sam", "sum", "salmon", "Summit", "summer", "Simon", "timer", "samet", "sama", "summon", "Samuel", "Samer"],
        ["Thomas", "poems", "poem", "Pumas", "Tomas", "Toma", "Tomah", "comma", "troma", "trauma", "Tomah", "Tom"],
        ["William", "Miriam", "video", "radiant", "Radian", "medium", "radium", "reading", "ridiam", "media", "Lydia"]
        ]
        for i in range(len(listen1)):
            split_lis = listen1[i].lower().split()
            print(split_lis)
            for j in range(len(split_lis)):
                for k, replace in enumerate(replace_lists):
                    if split_lis[j] in replace:
                        name_number = k
                        name_flag = True
                        print("true")
                        break
                    elif split_lis[j] not in replace:
                        print("false")
                        
                    elif split_lis[j] == []:#何も聞き取れないとき
                        print("Nothing")

                if name_flag == True:
                    break
            if name_flag == True:
                break
        if  name_flag == False:
            if h == 4:
                Guestname = random.choice(name_list)
            else:
                speak("Sorry.")
                #rospy.sleep(0.5)
        elif name_flag == True:
            speak("Are you ")
            speak(name_list[name_number] + "?")
            Guestname = name_list[name_number]
            listen2 = listen(5)
            answer_list = ["yes"]
            for i in range(len(listen2)):
                split_lis = listen2[i].lower().split()
                print(split_lis)
                for j in range(len(split_lis)):
                    for k in range(len(answer_list)):
                        if not split_lis[j] == "no":
                            print("true")
                            answer_flag = True
                            break
                        else:
                            print("false")
                    if answer_flag == True:
                        break
                if answer_flag == True:
                    break
            if answer_flag == True:
                break
            elif answer_flag == False:
                speak("Sorry")
    
    print("guest is {}".format(Guestname))
    speak("Got it")

    return Guestname


if __name__ == '__main__':
    rospy.init_node("speak_and_listen", anonymous = True)
    # conversation()
    listen_res = listen(10)
    print(listen_res)
