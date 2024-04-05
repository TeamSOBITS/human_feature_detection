#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import roslib
import cv2
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from mtcnn.mtcnn import MTCNN
from deepface import DeepFace
from human_feature_detect.srv import Features, FeaturesResponse
from human_feature_detect.msg import Feature
import roslib.packages


class FEATURE_SERVER:
    def model_load(self):
        self.detector = MTCNN()
        path = roslib.packages.get_pkg_dir("human_feature_detect")
        image = cv2.imread(path + "/images/sample_image.png")
        face_locations = self.detect_faces(image)
        for index, face_location in enumerate(face_locations):
            self.analyze_face(image, face_location)

    def bbox_plot(self, image, bboxes, name_list):
        copied_image = np.copy(image)
        for bbox, name in zip(bboxes, name_list):
            x = bbox.boundingbox.center.x - bbox.boundingbox.size_x//2
            y = bbox.boundingbox.center.y - bbox.boundingbox.size_y//2
            w = bbox.boundingbox.size_x
            h = bbox.boundingbox.size_y
            cv2.rectangle(copied_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(copied_image, name, (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        path = roslib.packages.get_pkg_dir("human_feature_detect")
        cv2.imwrite(path + '/images/result.png', copied_image)
        bridge = CvBridge()
        return (bridge.cv2_to_imgmsg(copied_image))

    def detect_faces(self, image):
        face_locations = self.detector.detect_faces(image)
        return face_locations

    def analyze_face(self, image, face_location):
        x, y, w, h = face_location['box']
        detected_face = image[y:y+h, x:x+w]
        result = DeepFace.analyze(detected_face, actions=['age', 'gender', 'emotion'], enforce_detection=False)
        return result

    def human_features_callback(self, hfd_srv):
        bridge = CvBridge()
        image = bridge.imgmsg_to_cv2(hfd_srv.input_image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_locations = self.detect_faces(image)

        features = FeaturesResponse()
        box_text = []
        for index, face_location in enumerate(face_locations):
            feature = Feature()
            results = self.analyze_face(image, face_location)

            for result in results:
                feature.age = int(result['age'])
                feature.emotion = result['dominant_emotion']
                feature.boundingbox.center.x = face_location['box'][0] + face_location['box'][2]//2
                feature.boundingbox.center.y = face_location['box'][1] + face_location['box'][3]//2
                feature.boundingbox.center.theta = 0.0
                feature.boundingbox.size_x = face_location['box'][2]
                feature.boundingbox.size_y = face_location['box'][3]
                if (result['gender']['Woman'] < result['gender']['Man']):
                    feature.sex = "Man"
                else:
                    feature.sex = "Woman"
                features.features += [feature]
                box_text += ["Age:" + str(feature.age) + ", Sex:" + str(feature.sex) + ", Emotion:" + str(feature.emotion)]

        features.result_image = self.bbox_plot(image, features.features, box_text)
        return FeaturesResponse(result_image=features.result_image , features=features.features )

    def wait_server(self):
        self.model_load()
        rospy.Service("/human_feature_detect/features", Features, self.human_features_callback)
        rospy.loginfo("Waiting for service...")
        rospy.spin()



if __name__ == '__main__':
    rospy.init_node("feature_detect")
    try:
        feature_server = FEATURE_SERVER()
        feature_server.wait_server()

    except (KeyboardInterrupt, rospy.ROSInterruptException) as e:
        rospy.logfatal("Error occurred! Stopping the caht gpt ros service node...")
