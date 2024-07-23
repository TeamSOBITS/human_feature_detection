cmake_minimum_required(VERSION 3.8)
project(human_feature_detection)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find_package(catkin REQUIRED COMPONENTS REQUIRED
#   roscpp
#   rospy
#   std_msgs
#   # cv_bridge
#   sensor_msgs
#   vision_msgs
#   roslib
#   tf2_ros
#   pcl_ros
#   pcl_conversions
#   message_generation
# )
# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(vision_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)


# add_message_files(
#   FILES
#   Feature.msg
# )
set(msg_files
  "msg/Feature.msg"
)


# add_service_files(
#   FILES
#   Features.srv
#   Feature3d.srv
# )
set(srv_files
  "srv/Features.srv"
  "srv/Feature3d.srv"
)

# generate_messages(
#   DEPENDENCIES
#   std_msgs
#   sensor_msgs
#   vision_msgs
# )
rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  ${srv_files}
  DEPENDENCIES std_msgs geometry_msgs sensor_msgs vision_msgs
)


#--- for C++
# include_directories(include)
# add_executable(service_server_cpp src/service_server_cpp.cpp)
# ament_target_dependencies(service_server_cpp rclcpp std_srvs)
# add_executable(service_client_cpp src/service_client_cpp.cpp)
# ament_target_dependencies(service_client_cpp rclcpp std_srvs)

# install(TARGETS
#   # service_server_cpp
#   # service_client_cpp
#   DESTINATION lib/${PROJECT_NAME}
# )
#--- end C++

#-- for Python
# ament_python_install_package(${PROJECT_NAME})

install(PROGRAMS
  scripts/feature_detect.py
  example/sample_2d.py
  DESTINATION lib/${PROJECT_NAME}
)
#--- end Python



# catkin_package(
#  INCLUDE_DIRS include
#  CATKIN_DEPENDS roscpp rospy std_msgs cv_bridge tf2_ros visualization_msgs pcl_ros pcl_conversions
# )

# include_directories(
#   include
#   ${catkin_INCLUDE_DIRS}
#   ${OpenCV_INCLUDE_DIRS}
# )

# add_executable(feature_detect_3d src/feature_detect_3d.cpp src/point_cloud_processor.cpp)
# target_link_libraries(feature_detect_3d ${catkin_LIBRARIES})
# add_dependencies(feature_detect_3d ${catkin_EXPORTED_TARGETS})
# add_dependencies(feature_detect_3d ${${PROJECT_NAME}_EXPORTED_TARGETS})



if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()