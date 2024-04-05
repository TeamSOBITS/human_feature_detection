cmake_minimum_required(VERSION 3.10.2)
project(human_feature_detect)

add_compile_options(-std=c++14)

find_package(catkin REQUIRED COMPONENTS REQUIRED
  roscpp
  rospy
  std_msgs
  # cv_bridge
  sensor_msgs
  vision_msgs
  roslib
  tf2_ros
  pcl_ros
  pcl_conversions
  message_generation
)

add_message_files(
  FILES
  Feature.msg
)

add_service_files(
  FILES
  Features.srv
  Feature3d.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
  sensor_msgs
  vision_msgs
)

catkin_package(
 INCLUDE_DIRS include
 CATKIN_DEPENDS roscpp rospy std_msgs cv_bridge tf2_ros visualization_msgs pcl_ros pcl_conversions
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
)

add_executable(feature_detect_3d src/feature_detect_3d.cpp src/point_cloud_processor.cpp)
target_link_libraries(feature_detect_3d ${catkin_LIBRARIES})
add_dependencies(feature_detect_3d ${catkin_EXPORTED_TARGETS})
add_dependencies(feature_detect_3d ${${PROJECT_NAME}_EXPORTED_TARGETS})
