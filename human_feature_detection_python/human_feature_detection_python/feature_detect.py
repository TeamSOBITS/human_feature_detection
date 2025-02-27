import rclpy
from rclpy.node import Node
import cv2
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from deepface import DeepFace
from sobits_interfaces.msg import Feature
from sobits_interfaces.srv import Features
from ament_index_python.packages import get_package_share_directory
import os

class FEATURE_SERVER:
    def __init__(self, node):
        self.node = node

    def model_load(self):
        from mtcnn.mtcnn import MTCNN  # Load MTCNN model
        self.detector = MTCNN()
        package_share_directory = get_package_share_directory('human_feature_detection_python')  # Set relative path from package share directory
        image_path = os.path.join(package_share_directory, 'images', 'sample_image.png')
        if not os.path.exists(image_path):
            self.node.get_logger().error(f"File not found: {image_path}")
            return  # Exit method if image not found
        else:
            image = cv2.imread(image_path)
            self.node.get_logger().info(f"Image loaded: {image_path}")
        face_locations = self.detect_faces(image)  # Detect faces
        for index, face_location in enumerate(face_locations):
            self.analyze_face(image, face_location)  # Analyze each detected face

    def bbox_plot(self, image, bboxes, name_list):
        copied_image = np.copy(image)  # Draw bounding boxes
        for bbox, name in zip(bboxes, name_list):
            x = bbox.boundingbox.center.position.x - bbox.boundingbox.size_x // 2  # Calculate bounding box coordinates
            y = bbox.boundingbox.center.position.y - bbox.boundingbox.size_y // 2
            w = bbox.boundingbox.size_x
            h = bbox.boundingbox.size_y
            cv2.rectangle(copied_image, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0), 2)  # Draw bounding box
            cv2.putText(copied_image, name, (int(x), int(y) - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # Draw name
        relative_path = '../images/result.png'  # Relative path to save image
        script_dir = os.path.dirname(__file__)  # Get current script directory
        abs_path = os.path.join(script_dir, relative_path)  # Convert relative path to absolute path
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)  # Create directory if it does not exist
        cv2.imwrite(abs_path, copied_image)  # Save image
        self.node.get_logger().info(f"Image saved: {abs_path}")
        bridge = CvBridge()  # Convert image to ROS message
        return bridge.cv2_to_imgmsg(copied_image)

    def detect_faces(self, image):
        face_locations = self.detector.detect_faces(image)  # Detect faces
        return face_locations

    def analyze_face(self, image, face_location):
        x, y, w, h = face_location['box']  # Analyze face
        detected_face = image[y:y + h, x:x + w]
        result = DeepFace.analyze(detected_face, actions=['age', 'gender', 'emotion'], enforce_detection=False)  # Analyze face features using DeepFace
        return result

    def human_features_callback(self, request, response):
        bridge = CvBridge()  # Service callback
        image = bridge.imgmsg_to_cv2(request.input_image)  # Convert image message to OpenCV image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert image to RGB
        face_locations = self.detect_faces(image)  # Detect faces

        box_text = []
        for index, face_location in enumerate(face_locations):
            feature = Feature()
            results = self.analyze_face(image, face_location)  # Analyze face features

            for result in results:
                feature.age = int(result['age'])  # Set features
                feature.emotion = result['dominant_emotion']
                feature.boundingbox.center.position.x = float(face_location['box'][0] + face_location['box'][2] // 2)
                feature.boundingbox.center.position.y = float(face_location['box'][1] + face_location['box'][3] // 2)
                feature.boundingbox.center.theta = 0.0
                feature.boundingbox.size_x = float(face_location['box'][2])
                feature.boundingbox.size_y = float(face_location['box'][3])
                feature.sex = "Man" if result['gender']['Woman'] < result['gender']['Man'] else "Woman"
                response.features += [feature]  # Add features to response
                box_text += ["Age:" + str(feature.age) + ", Sex:" + str(feature.sex) + ", Emotion:" + str(feature.emotion)]  # Add bounding box text

        response.result_image = self.bbox_plot(image, response.features, box_text)  # Set result image
        return response

    def wait_server(self, node):
        try:
            self.model_load()  # Wait for server
            srv = node.create_service(Features, "/human_feature_detection_python/features", self.human_features_callback)  # Create service
            node.get_logger().info('Waiting for service...')
            rclpy.spin(node)  # Spin node
        except KeyboardInterrupt:
            node.get_logger().info('Keyboard Interrupt (Ctrl+C) detected. Shutting down...')
        finally:
            node.destroy_node()  # Destroy node
            if rclpy.ok():
                rclpy.shutdown()

def main():
    try:
        rclpy.init()  # Main function
        node = Node("feature_detect")  # Create node
        feature_server = FEATURE_SERVER(node)  # Create server
        feature_server.wait_server(node)
    except KeyboardInterrupt:
        print('Keyboard Interrupt (Ctrl+C) detected. Exiting...')
    finally:
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()