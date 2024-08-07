#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rclpy
from rclpy.node import Node
import cv2
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
# from mtcnn.mtcnn import MTCNN
from deepface import DeepFace
from human_feature_detection_msgs.srv import Features
from human_feature_detection_msgs.msg import Feature
import getpass


class FEATURE_SERVER:
    def model_load(self):
        from mtcnn.mtcnn import MTCNN
        self.detector = MTCNN()
        path = "/home/" + str(getpass.getuser()) + "/colcon_ws/src/human_feature_detection/human_feature_detection"
        image = cv2.imread(path + "/images/sample_image.png")
        face_locations = self.detect_faces(image)
        for index, face_location in enumerate(face_locations):
            self.analyze_face(image, face_location)

    def bbox_plot(self, image, bboxes, name_list):
        copied_image = np.copy(image)
        for bbox, name in zip(bboxes, name_list):
            x = bbox.boundingbox.center.position.x - bbox.boundingbox.size_x//2
            y = bbox.boundingbox.center.position.y - bbox.boundingbox.size_y//2
            w = bbox.boundingbox.size_x
            h = bbox.boundingbox.size_y
            cv2.rectangle(copied_image, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0), 2)
            cv2.putText(copied_image, name, (int(x), int(y) - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        path = "/home/" + str(getpass.getuser()) + "/colcon_ws/src/human_feature_detection/human_feature_detection"
        cv2.imwrite(path + '/images/result.png', copied_image)
        bridge = CvBridge()
        return (bridge.cv2_to_imgmsg(copied_image))

    def detect_faces(self, image):
        face_locations = self.detector.detect_faces(image)
        return face_locations

    def analyze_face(self, image, face_location):
        # from deepface import DeepFace
        x, y, w, h = face_location['box']
        detected_face = image[y:y+h, x:x+w]
        result = DeepFace.analyze(detected_face, actions=['age', 'gender', 'emotion'], enforce_detection=False)
        return result

    def human_features_callback(self, request, response):
        bridge = CvBridge()
        image = bridge.imgmsg_to_cv2(request.input_image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_locations = self.detect_faces(image)


        box_text = []
        for index, face_location in enumerate(face_locations):
            feature = Feature()
            results = self.analyze_face(image, face_location)

            for result in results:
                feature.age = int(result['age'])
                feature.emotion = result['dominant_emotion']
                feature.boundingbox.center.position.x = float(face_location['box'][0] + face_location['box'][2]//2)
                feature.boundingbox.center.position.y = float(face_location['box'][1] + face_location['box'][3]//2)
                feature.boundingbox.center.theta = 0.0
                feature.boundingbox.size_x = float(face_location['box'][2])
                feature.boundingbox.size_y = float(face_location['box'][3])
                if (result['gender']['Woman'] < result['gender']['Man']):
                    feature.sex = "Man"
                else:
                    feature.sex = "Woman"
                response.features += [feature]
                box_text += ["Age:" + str(feature.age) + ", Sex:" + str(feature.sex) + ", Emotion:" + str(feature.emotion)]

        response.result_image = self.bbox_plot(image, response.features, box_text)
        return response

    def wait_server(self, nd):
        self.model_load()
        srv = nd.create_service(Features, "/human_feature_detection/features", self.human_features_callback)
        nd.get_logger().info('Waiting for service...')
        rclpy.spin(nd)



if __name__ == '__main__':
    rclpy.init()
    nd = Node("feature_detect")
    feature_server = FEATURE_SERVER()
    feature_server.wait_server(nd)