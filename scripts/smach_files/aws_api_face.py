#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import boto3
# import json
# iniファイルを使用するためのライブラリを読み込む
import configparser
# 認識結果を表示するためのライブラリを読み込む
from matplotlib import pyplot as plt
from PIL import Image as im
import random
import rospy
from picture_saver.srv import picture_cmd
from std_msgs.msg import Bool

# 画像の保存場所
filepath = "/home/sobits/catkin_ws/src/amazon_recognition_for_fmm/imgs/"

ini_path = "/home/sobits/catkin_ws/src/amazon_recognition_for_fmm/config.ini"
# 使用するバケットを指定する
bucket = "rcjpfmm"
# 使用するリージョンを指定する
region = "ap-northeast-1"

person_flag = False

def save_picture(img_name):
    global filepath
    rospy.wait_for_service('/picture_cmd')
    try:
        pic_save = rospy.ServiceProxy("/picture_cmd", picture_cmd)
        res = pic_save(1, filepath , img_name)
    except rospy.ServiceException as e:
	    print ("Service call failed: %s"%e)

def image_pose(input_filename, output_filename):
    global filepath, ini_path, person_flag
    #configparserのインスタンスを作る
    ini = configparser.ConfigParser()
    #あらかじめ作ったiniファイルを読み込む
    ini.read(ini_path, "UTF-8")
    # 認識させるファイルを指定する

    #画像を開いて、サイズを取得する
    img = im.open(filepath + input_filename).convert("RGB")
    # img = CvBridge.imgmsg_to_cv2(img,"rgb8")
    img_width = img.size[0]
    img_height = img.size[1]

    # サービスを利用するための識別情報(iniファイルの中身）を読み込む
    access_key = ini["AWS_KEY"]["awsaccesskeyid"]
    secret_key = ini["AWS_KEY"]["awssecretkey"]
    # サービスへの接続情報を取得する
    session = boto3.Session(
        aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region
    )

    # S3サービスに接続する
    s3 = session.client("s3")
    # Recognitionサービスに接続する
    recognition = session.client("recognition")

    # ファイルを読み込む
    with open(filepath + input_filename, "rb") as f:
        # 読み込んだファイルをS3サービスにアップロード
        s3.put_object(Bucket=bucket, Key=input_filename, Body=f)

    # S3に置いたファイルをRecognitionに認識させる
    res = recognition.detect_labels(
        Image={"S3Object": {"Bucket": bucket, "Name": input_filename}})
    rospy.sleep(10)

    # Recognitionの認識結果を表示する
    # print("Detected labels for " + filename)
    target_size = 0
    for label in res["Labels"]:
        
        if "Person" in label["Name"]:
            person_flag = True
            # print("Label: " + label["Name"])
            # print("Confidence: " + str(label["Confidence"]))
            # print("Instances:")
            for instance in label["Instances"]:
                print("  Bounding box")
                print("    Top: " + str(instance["BoundingBox"]["Top"]))
                print("    Left: " + str(instance["BoundingBox"]["Left"]))
                print("    Width: " + str(instance["BoundingBox"]["Width"]))
                print("    Height: " + str(instance["BoundingBox"]["Height"]))
                print("  Confidence: " + str(instance["Confidence"]))

                bb_size = instance["BoundingBox"]["Height"] * instance["BoundingBox"]["Width"]
                if bb_size > target_size and instance["Confidence"] > 0.9:
                    target_size = bb_size
                    top     = instance["BoundingBox"]["Top"] \
                        if instance["BoundingBox"]["Top"] >= 0 else 0
                    bottom  = instance["BoundingBox"]["Top"] + instance["BoundingBox"]["Height"] \
                        if instance["BoundingBox"]["Top"] + instance["BoundingBox"]["Height"] <= 1 else 1
                    left    = instance["BoundingBox"]["Left"] \
                        if instance["BoundingBox"]["Left"] >= 0 else 0
                    right   = instance["BoundingBox"]["Left"] + instance["BoundingBox"]["Width"] \
                        if instance["BoundingBox"]["Left"] + instance["BoundingBox"]["Width"] <= 1 else 1
    
    s3.delete_object(Bucket=bucket, Key=input_filename)

    if person_flag == True:
        #保存
        target_area_img = img.crop((left * img_width, top * img_height, right * img_width, bottom * img_height))
        target_area_img.save(filepath + output_filename)
        person_flag = False
        return "successed"

    return "failed"
    # Boundingbox有りの画像を表示させる（target:赤 person:緑）
    # colors = {'target': (1,0,0), 'Person': (0,1,0)}
    # for label in res["Labels"]:
    #     if "Person" in label["Name"]:
    #         label_name = label["Name"]
    #         if label_name not in colors:
    #             colors[label_name] = (random.random(), random.random(), random.random())
    #         for instance in label["Instances"]:
    #             bb = instance["BoundingBox"]
    #             if left is bb["Left"] and top is bb["Top"]:
    #                 label_name = 'target'
    #             else :
    #                 label_name = "Person"

    #             rect = plt.Rectangle(
    #                 (bb["Left"] * img_width, bb["Top"] * img_height),
    #                 bb["Width"] * img_width,
    #                 bb["Height"] * img_height,
    #                 fill=False,
    #                 edgecolor=colors[label_name],
    #             )
    #             plt.gca().add_patch(rect)

    # plt.imshow(img)
    # plt.show()

    # S3サービスにアップロードしたファイルを削除する



def detect_faces(input_filename):
    global filepath, ini_path
    #configparserのインスタンスを作る
    ini = configparser.ConfigParser()
    #あらかじめ作ったiniファイルを読み込む
    ini.read(ini_path, "UTF-8")

    #画像を開いて、サイズを取得する
    img = im.open(filepath + input_filename).convert("RGB")
    img_width = img.size[0]
    img_height = img.size[1]

    # サービスを利用するための識別情報(iniファイルの中身）を読み込む
    access_key = ini["AWS_KEY"]["awsaccesskeyid"]
    secret_key = ini["AWS_KEY"]["awssecretkey"]
    # サービスへの接続情報を取得する
    session = boto3.Session(
        aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region
    )
    # S3サービスに接続する
    s3 = session.client("s3")
    # Recognitionサービスに接続する
    recognition = session.client("recognition")

    # ファイルを読み込む
    with open(filepath + input_filename, "rb") as f:
        # 読み込んだファイルをS3サービスにアップロード
        s3.put_object(Bucket=bucket, Key=input_filename, Body=f)

    res = recognition.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':input_filename}},Attributes=['ALL'])

    # Recognitionの認識結果を表示する
    print('Detected faces for ' + input_filename)
    i = 0
    for faceDetail in res['FaceDetails']:
        # print('The detected face is between ' + str(faceDetail['AgeRange']['Low']) 
        #       + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')

        # print('Here are the other attributes:')
        # print(json.dumps(faceDetail, indent=4, sort_keys=True))

		# # Access predictions for individual face details and print them
        # print("Gender: " + str(faceDetail['Gender']))
        # print("Smile: " + str(faceDetail['Smile']))
        #[AgeRange, Beard, BoundingBox, Emotions, Eyeglasses, Gender, Landmarks, Mustache, Smile, Sunglasses]
        i = i + 1
        # print("Data : " + str(i))
        # print("    AgeRange     : " + str(faceDetail['AgeRange']['Low']) + '~' + str(faceDetail['AgeRange']['High']))
        # print("    Beard        : " + str(faceDetail['Beard']['Value']))
        # # print("    Emotions     : " + str(faceDetail['Emotions'][0]['Type']))
        # print("    Eyeglasses   : " + str(faceDetail['Eyeglasses']['Value']))
        # print("    Gender       : " + str(faceDetail['Gender']['Value']))
        # print("    Mustache     : " + str(faceDetail['Mustache']['Value']))
        # # print("    Smile        : " + str(faceDetail['Smile']['Value']))
        # # print("    Sunglasses   : " + str(faceDetail['Sunglasses']['Value']))

    # S3サービスにアップロードしたファイルを削除する
    s3.delete_object(Bucket=bucket, Key=input_filename)

    return int(len(res['FaceDetails'])) ,int((faceDetail['AgeRange']['Low'] + faceDetail['AgeRange']['High'])/2)  , str(faceDetail['Beard']['Value']),\
      str(faceDetail['Eyeglasses']['Value']), str(faceDetail['Gender']['Value']), str(faceDetail['Mustache']['Value'])

def main():
    # 認識させるファイルを指定
    image_name = "kani_check_image.jpg"
    # 出力ファイル名を指定
    target_image_name = "target_image.jpg"
    # save_picture(image_name)
    image_pose(image_name,target_image_name)
    face_count, age, beard, eyeglasses, gender, mustache= detect_faces(target_image_name)
    print("    AgeRange     : " + age)
    print("    Beard        : " + beard)
    print("    Eyeglasses   : " + eyeglasses)
    print("    Gender       : " + gender)
    print("    Mustache     : " + mustache)
    print("Faces detected: " + str(face_count))

if __name__ == "__main__":
    main()

