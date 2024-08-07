#!/bin/bash

echo "╔══╣ Install: Human Feature Detect (STARTING) ╠══╗"

sudo apt-get update

sudo apt-get install -y \
    ros-${ROS_DISTRO}-vision-msgs

pip3 install --upgrade pip
pip3 install mtcnn
pip3 install deepface
pip3 install --upgrade pip

python3 model_setup.py

echo "╚══╣ Install: Human Feature Detect (FINISHED) ╠══╝"
