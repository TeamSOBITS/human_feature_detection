<a name="readme-top"></a>

[JP](README.md) | [EN](README_en.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

# Human Feature Detection

<!-- Table of Contents -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#introduction">Introduction</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#launch-and-usage">Launch and Usage</a>
      <ul>
        <li><a href="#2d-feature-detection-gender-and-age">2D Feature Detection (Gender and Age)</a></li>
        <li><a href="#3d-feature-detection-height-and-clothes-color">3D Feature Detection (Height and Clothes Color)
</a></li>
      </ul>
    </li>
    <li><a href="#service-server">Service Server</a></li>
    <li><a href="#milestone">Milestone</a></li>
    <li><a href="#references">References</a></li>
  </ol>
</details>


<!-- Introduction -->
## Introduction

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

This package infers human features from images and point clouds.\
Since it does not use APIs or other networks, offline inference can be performed without a network connection.\
It uses ROS Service communication to detect features, taking images and point clouds as input and returning the estimation results.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Getting Started -->
## Getting Started

This section describes how to set up this repository.

### Prerequisites

The following shows the normal operating environment.

| System  | Version |
| ------------- | ------------- |
| Ubuntu | 22.04 |
| ROS2 | humble |
| Python | 3.0~ |

### Installation

1. Navigate to your ROS `src` folder.
  ```sh
   $ cd　
   $ cd colcon_ws/src/
  ```
2. Clone this repository.
  ```sh
   $ git clone -b humble-devel https://github.com/TeamSOBITS/human_feature_detection.git
  ```
3. Move into the repository directory.
  ```sh
   $ cd human_feature_detection
  ```
4. Move into the human_feature_detection_python package.
  ```sh
   $ cd human_feature_detection_python
  ```
5. Install dependencies．
  ```sh
   $ bash install.sh
  ```

6. Compile the package．
  ```sh
   $ cd ~/colcon_ws/
   $ colcon build --symlink-install
   $ source ~/colcon_ws/install/setup.sh
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!--Launch and Usage -->
## Launch and Usage
### 2D Feature Detection (Gender and Age)
<!-- デモの実行方法やスクリーンショットがあるとわかりやすくなるでしょう -->
1. Launch any camera.\
   Any camera is fine as long as it publishes sensor_msgs/Image topics.\
   As an example, here's how to launch the camera attached to your PC:
   
    Install the v4l2_camera package:
    ```sh
    $ sudo apt-get install ros-humble-v4l2-camera
    ```
    ```sh
    $ ros2 run v4l2_camera v4l2_camera_node
    ```
    If this doesn't work, it's likely because your PC doesn't have a camera, the camera can't be used on Ubuntu, or permissions haven't been granted.

   In such cases, launch a camera that can communicate with ROS via USB.

2. Run the human_feature_detection.launch.py launch file to start the server that performs inference from images.

   Note that it will take some time for the first run.

   If "Waiting for service..." is displayed, the launch was successful.
    ```sh
    $ ros2 launch human_feature_detection_python human_feature_detection.launch.py
    ```
3. [Optional]ry sending an Image published on a Topic.
    We have prepared example code, so let's use that.\

   Change the Topic name on line 31 of [example/sample_2d.py](/human_feature_detection_python/example/sample_2d.py) to the Topic name of the camera launched in "1.".

   By default, it is "/image_raw", which is mainly the Topic name for cameras like xtion.

   Running the following command will perform inference on the captured image after a 3-second countdown. (If the countdown does not start, the camera may not be running or the Topic name may be incorrect.)
   ```sh
    $ ros2 run human_feature_detection_python sample_2d
    ```
   The number of detected people, their respective ages, genders, and expressions will be output to the terminal.

   By the way, the image reflecting these results is saved as [result.png](/images/result.png) in the images folder, so please check it.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### 3D Feature Detection (Height and Clothes Color)

1. Launch a camera that can publish point clouds.\
Please launch a depth camera.
2. Set the Point Cloud Topic Name.\
   Set the **topic_name** parameter in the [human_feature_detection3d.launch.py](human_feature_detection_cpp/launch/human_feature_detection3d.launch.py) file to the point cloud Topic name of the camera you are using.

  As an example, it is set to /points2, which is the point cloud name for Azure Kinect.
  ```python
  parameters = [{
                  'topic_name':'/points2', #点群名をここにセットする
                  'target_frame':'base_footprint', #ロボットの基準フレーム
                  'face_range':0.20, #顔の大体の大きさ
                  'clothes_range':0.35, #服のおおよその縦幅
                  'brightness_value':0 
                  }]
  ```
3. Once the settings are complete, run the [human_feature_detection3d.launch.py](human_feature_detection_cpp/launch/human_feature_detection3d.launch.py) launch file.
  ```sh
   $ ros2 launch human_feature_detection_cpp human_feature_detection3d.launch.py
  ```
  This will start the ROS Service communication Server that can perform inference from point clouds.
4. [Optional] Try requesting a specified point cloud.\
    We have prepared example code, so we will use that.\
    For 3D inference, please stand about 1 meter in front of the camera.
  ```sh
   $ ros2 run human_feature_detection_cpp sample_3d
  ```
  Height and clothes color were output to the terminal.\
  If there is no output, it is highly likely that the point cloud name (topic_name) or the reference frame name (target_frame) set in "2." is incorrect.

> [!NOTE]
> By using this example code, you can estimate human features by sending data (images and point clouds) obtained from the robot's camera to the Service Server.\
> Check the [example](/example/) folder and learn about the Service client (request side) from each sample file.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Service Server
- For 2D image inference (age and gender):
```
/human_feature_detection/features (human_feature_detection/Features)
```
- For 3D point cloud inference (height and clothes color):
```
/human_feature_detection_cpp/feature3d (human_feature_detection/Feature3d)
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Milestone -->
## Milestone
See the [Issues page](issues-url) for current bugs and feature requests.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- References -->
## References

* [Joint Face Detection and Alignment using Multi-task Cascaded Convolutional Networks](https://arxiv.org/abs/1604.02878)
* [DeepFace: Closing the Gap to Human-Level Performance in Face Verification](https://www.cs.toronto.edu/~ranzato/publications/taigman_cvpr14.pdf)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TeamSOBITS/human_feature_detection.svg?style=for-the-badge
[contributors-url]: https://github.com/TeamSOBITS/human_feature_detection/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TeamSOBITS/human_feature_detection.svg?style=for-the-badge
[forks-url]: https://github.com/TeamSOBITS/human_feature_detection/network/members
[stars-shield]: https://img.shields.io/github/stars/TeamSOBITS/human_feature_detection.svg?style=for-the-badge
[stars-url]: https://github.com/TeamSOBITS/human_feature_detection/stargazers
[issues-shield]: https://img.shields.io/github/issues/TeamSOBITS/human_feature_detection.svg?style=for-the-badge
[issues-url]: https://github.com/TeamSOBITS/human_feature_detection/issues
[license-shield]: https://img.shields.io/github/license/TeamSOBITS/human_feature_detection.svg?style=for-the-badge
[license-url]: LICENSE

</details>
