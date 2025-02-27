#!/bin/bash

echo "╔══╣ Install: Human Feature Detect (STARTING) ╠══╗"

sudo apt-get update

sudo apt-get install -y \
    ros-${ROS_DISTRO}-cv-bridge \
    ros-${ROS_DISTRO}-geometry-msgs \
    ros-${ROS_DISTRO}-message-filters \
    ros-${ROS_DISTRO}-pcl-ros \
    ros-${ROS_DISTRO}-pcl-conversions \
    ros-${ROS_DISTRO}-tf2 \
    ros-${ROS_DISTRO}-tf2-ros \
    ros-${ROS_DISTRO}-tf2-geometry-msgs \
    ros-${ROS_DISTRO}-sensor-msgs \
    ros-${ROS_DISTRO}-std-msgs \
    ros-${ROS_DISTRO}-pluginlib \
    ros-${ROS_DISTRO}-sensor-msgs \
    ros-${ROS_DISTRO}-std-msgs

python3 -m pip install -U pip

python3 -m pip install \
    tensorflow[and-cuda] \
    tf-keras

python3 -m pip install \
    mtcnn \
    deepface

git clone -b feature/human_feature_detection https://github.com/TeamSOBITS/sobits_msgs.git

python3 model_setup.py

echo "╚══╣ Install: Human Feature Detect (FINISHED) ╠══╝"