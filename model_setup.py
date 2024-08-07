# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
from deepface import DeepFace
import getpass

def bbox(image, bboxes, name_list):
    for bbox, name in zip(bboxes, name_list):
        x, y, w, h = bbox
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, name, (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    path = "/home/" + str(getpass.getuser()) + "/colcon_ws/src/human_feature_detection/human_feature_detection"
    cv2.imwrite(path + "/images/sample_image_result.png", image)

def detect_faces(image):
    from mtcnn.mtcnn import MTCNN
    detector = MTCNN()
    face_locations = detector.detect_faces(image)
    return face_locations

def analyze_face(image, bbox):
    x, y, w, h = bbox
    detected_face = image[y:y+h, x:x+w].copy()
    result = DeepFace.analyze(detected_face, actions=["age", "gender", "emotion"], enforce_detection=False)
    return result


def main():
    path = "/home/" + str(getpass.getuser()) + "/colcon_ws/src/human_feature_detection/human_feature_detection"
    image = cv2.imread(path + "/images/sample_image.png")
    face_locations = detect_faces(image)
    print("\033[41m", face_locations, "\033[0m")
    features = []
    box_text = []
    for index, face_location in enumerate(face_locations):
        results = analyze_face(image, face_location["box"])
        for result in results:
            age = int(result["age"])
            emotion = result["dominant_emotion"]
            if (result["gender"]["Woman"] < result["gender"]["Man"]):
                sex = "Man"
            else:
                sex = "Woman"
            features += [(face_location["box"][0], face_location["box"][1], face_location["box"][2], face_location["box"][3])]
            box_text += ["Age:" + str(age) + ", Sex:" + str(sex) + ", Emotion:" + str(emotion)]
    bbox(image, features, box_text)


if __name__ == "__main__":
    main()