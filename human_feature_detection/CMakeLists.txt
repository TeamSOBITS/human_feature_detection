cmake_minimum_required(VERSION 3.8)
project(human_feature_detection)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(vision_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_eigen REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(pcl_ros REQUIRED)
find_package(pcl_conversions REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(rosidl_typesupport_cpp REQUIRED)
find_package(human_feature_detection_msgs REQUIRED)


#--- for C++
add_executable(feature_detect_3d src/feature_detect_3d.cpp src/point_cloud_processor.cpp)
ament_target_dependencies(feature_detect_3d rclcpp std_msgs sensor_msgs pcl_conversions pcl_ros tf2_ros tf2_eigen tf2_geometry_msgs human_feature_detection_msgs rosidl_default_runtime)

include_directories(include ${PCL_INCLUDE_DIRS} ${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_CURRENT_BINARY_DIR}/rosidl_generator_cpp ${ament_index_build_prefix}/${PROJECT_NAME}/include)

install(TARGETS
  feature_detect_3d
  DESTINATION lib/${PROJECT_NAME}
)
#--- end C++

#-- for Python
install(PROGRAMS
  scripts/feature_detect.py
  example/sample_2d.py
  example/sample_3d.py
  DESTINATION lib/${PROJECT_NAME}
)
#--- end Python

#-- for Launch
install(DIRECTORY launch/
        DESTINATION share/${PROJECT_NAME}/launch)
#--- end Launch


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