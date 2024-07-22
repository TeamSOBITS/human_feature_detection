#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import roslib
import cv2
from mtcnn.mtcnn import MTCNN
from deepface import DeepFace
import roslib.packages

def bbox(image, bboxes, name_list):
    for bbox, name in zip(bboxes, name_list):
        x, y, w, h = bbox
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, name, (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    path = roslib.packages.get_pkg_dir("human_feature_detection")
    cv2.imwrite(path + '/images/sample_image_result.png', image)

def detect_faces(image):
    detector = MTCNN()
    face_locations = detector.detect_faces(image)
    return face_locations

def analyze_face(image, face_location):
    x, y, w, h = face_location['box']
    detected_face = image[y:y+h, x:x+w]
    result = DeepFace.analyze(detected_face, actions=['age', 'gender', 'emotion'], enforce_detection=False)
    return result

def main():
    path = roslib.packages.get_pkg_dir("human_feature_detection")
    image = cv2.imread(path + "/images/sample_image.png")
    face_locations = detect_faces(image)
    features = []
    box_text = []
    for index, face_location in enumerate(face_locations):
        results = analyze_face(image, face_location)
        for result in results:
            age = int(result['age'])
            emotion = result['dominant_emotion']
            if (result['gender']['Woman'] < result['gender']['Man']):
                sex = "Man"
            else:
                sex = "Woman"
            features += [(face_location['box'][0], face_location['box'][1], face_location['box'][2], face_location['box'][3])]
            box_text += ["Age:" + str(age) + ", Sex:" + str(sex) + ", Emotion:" + str(emotion)]
    bbox(image, features, box_text)


if __name__ == '__main__':
    main()
