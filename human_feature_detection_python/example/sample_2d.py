import rclpy  
from rclpy.node import Node  
import cv2  
from cv_bridge import CvBridge  
from sensor_msgs.msg import Image  
from sobits_interfaces.srv import Features 
import threading  
import os  

srv_img = Features.Request()  # Instance of the service request
start_ok = False  # Flag to check if the image has been received
bridge = CvBridge()  # Instance of CvBridge

def callback_img(msg):  # Callback function for image messages
    global srv_img, start_ok
    srv_img.input_image = msg
    start_ok = True

def countdown_timer(seconds, callback):  # Countdown timer function
    if seconds >= 0:
        print(f"Time until capture... {seconds}")
        threading.Timer(1, countdown_timer, [seconds - 1, callback]).start()
    else:
        callback()  # Call the send_image_to_server function

def main():  # Main function
    global srv_img, start_ok
    rclpy.init()
    node = Node("human_feature_detect_sample_2d_ros")  # Create node
    logger = node.get_logger()
    sub = node.create_subscription(Image, "/image_raw", callback_img, 10)  # Subscribe to image topic
    
    while rclpy.ok():  # Wait until the image is received in the callback
        rclpy.spin_once(node, timeout_sec=0.1)
        if start_ok:
            break
    
    if start_ok:
        countdown_thread = threading.Thread(target=countdown_timer, args=(3, lambda: send_image_to_server(node, logger)))  # Start a 3-second countdown in a separate thread
        countdown_thread.start()

        while countdown_thread.is_alive():  # Continue subscribing to images in the main thread
            rclpy.spin_once(node, timeout_sec=0.1)

def send_image_to_server(node, logger):  # Function to send the image to the server
    global srv_img
    rclpy.spin_once(node)
    client = node.create_client(Features, "/human_feature_detection_python/features")  # Create client
    client.wait_for_service()  # Wait for the service server to start
    f = client.call_async(srv_img)  # Send the image to the server
    rclpy.spin_until_future_complete(node, f)
    response = f.result()

    logger.info("The number of detected people is " + str(len(response.features)) + ".\n")  # Log the detection results
    for i in range(len(response.features)):
        logger.info("Person " + str(i+1) + " is " + str(response.features[i].sex) + ",")
        logger.info("approximately " + str(response.features[i].age) + " years old.")
        logger.info("Their emotion is " + str(response.features[i].emotion) + ".\n")

    cv_image = bridge.imgmsg_to_cv2(response.result_image, desired_encoding='passthrough')  # Convert the image to OpenCV format
    display_image(cv_image, logger)  # Save and display the image

def display_image(cv_image, logger):  # Function to save and display the image
    cv2.imshow("Result Image", cv_image)  # Display the image
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main() 