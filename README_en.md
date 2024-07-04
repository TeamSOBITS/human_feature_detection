<a name="readme-top"></a>

[JP](README.md) | [EN](README_en.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
<!-- [![MIT License][license-shield]][license-url] -->

# Human Feature Detect

<!-- 目次 -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#Introduction">Introduction</a>
    </li>
    <li>
      <a href="#Getting Started">Getting Started</a>
      <ul>
        <li><a href="#Requirements">Requirements</a></li>
        <li><a href="#Installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#Launch and Usage">Launch and Usage</a></li>
    <li><a href="#Milestone">Milestone</a></li>
    <li><a href="#Acknowledgements">Acknowledgements</a></li>
  </ol>
</details>


<!-- レポジトリの概要 -->
## Introduction

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

This package infers human features from images and point clouds.\
The package does not use networks such as APIs, so offline inference can be performed without networks.\
Detects features using ROS Service communication, using images or point clouds as input values and the estimated results as return values.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- セットアップ -->
## Getting Started

This section describes how to set up this repository.

### Requirements


| System  | Version |
| ------------- | ------------- |
| Ubuntu | 20.04 (Focal Fossa) |
| ROS | Noetic Ninjemys |
| Python | 3.0~ |

### Installation

1. Change directory
   ```sh
   $ cd ~/catkin_ws/src
   ```
2. clone TeamSOBITS/human_feature_detection
   ```sh
   $ git clone https://github.com/TeamSOBITS/human_feature_detection.git
   ```
3. Change directory
   ```sh
   $ cd human_feature_detection/
   ```
4. Install dependent packages
   ```sh
   $ bash install.sh
   ```
5. compile
   ```sh
   $ cd ~/catkin_ws/
   $ catkin_make
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- 実行・操作方法 -->
## Launch and Usage
### Feature detection possible in 2D（Sex and Age）
<!-- デモの実行方法やスクリーンショットがあるとわかりやすくなるでしょう -->
1. Launch the RGB camera\

    As an example, we describe below how to activate the camera attached to a PC.
    ```sh
    $ roslaunch usb_cam usb_cam-test.launch
    ```
    If this does not work, it is most likely that the PC does not have a camera or the camera is not available on ubuntu, so start a camera that can communicate with ROS via USB connection.
2. Launch the [human_feature_detection.launch](/launch/human_feature_detection.launch)
    ```sh
    $ roslaunch human_feature_detection human_feature_detection.launch
    ```
    This activates the Server for ROS Service communication, which allows inference from images.
3. [Optional]Let's try to send an Image that has been Published to Topic.\
    run the example.\
    Match the Topic name in line 19 in [example/sample_2d.py](example/sample_2d.py) to the Topic name of the camera.\
    As it is, it is “/camera/rgb/image_raw”, which is mainly an example of an xtion camera.\
    The following commands will cause an inference to be made about the image that was captured after the 3-second countdown. (If the countdown does not start, the camera may not be activated or the Topic name may be incorrect.)
    ```sh
    $ rosrun human_feature_detection sample_2d.py
    ```
    The terminal outputs the number of people detected, their age, sex, and facial expressions.\
    The resulting images are stored at the [result.png](/images/result.png).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Feature detection possible in 3D（height and clothing color）
1. Launch the RGB-D camera\
  Please activate the depth camera.
2. Set the Topic name of the point cloud\
  In the sixth line of the [human_feature_detection.launch](/launch/human_feature_detection.launch) file, as a “param”, match the Topic name.\
  The following example is for /points2, the azure kinect point cloud name.
  ```xml
    <param name="topic_name" value="/points2"/>
  ```
  About other parameters
  ```
    <param name="target_frame" value="base_footprint"/>　 <!-- The reference frame of the robot. This allows the height to be the head height with respect to the ground -->
    <param name="face_range" value="0.20"/>               <!-- The approximate size of the face. How far down the point cloud from the tip of the head is referenced when measuring clothing color. -->
    <param name="clothes_range" value="0.35"/>            <!-- The approximate length of the clothing. How wide an area is referenced when measuring the color of a garment. -->
  ```
3. Launch the [human_feature_detection.launch](/launch/human_feature_detection.launch)
  ```sh
   $ roslaunch human_feature_detection human_feature_detection.launch
  ```
  This activates the Server for Service communication in ROS, which allows inference from point clouds.
4. [Optional]Let's request a specified point cloud\
  run the example.\
  For 3D inference, stand 1 meter in front of the camera.
  ```sh
   $ rosrun human_feature_detection sample_3d.py
  ```
  The terminal outputs height and clothing color.\
  If it is not output, it is most likely that the point cloud name (topic_name) or reference frame name (target_frame) is incorrect.

> [!NOTE]
> With this example code, human features can be estimated from images and point clouds obtained from the robot's camera by sending the data to the Service's Server.\
> Check the [example](/example/) folder to become familiar with how SOBIT PRO works, and learn the working functions from each sample file.


### Service Server
- When reasoning with 2D images(Sex and Age)
```
/human_feature_detection/features (human_feature_detection/Features)
```
- When reasoning with 3D images(height and clothing color)
```
/human_feature_detection/feature3d (human_feature_detection/Feature3d)
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- マイルストーン -->
## Milestone

See the [open issues](issues-url) for a full list of proposed features (and known issues).


<!-- 変更履歴 -->
<!-- ## 変更履歴

- 2.0: 代表的なタイトル
  - 詳細 1
  - 詳細 2
  - 詳細 3
- 1.1: 代表的なタイトル
  - 詳細 1
  - 詳細 2
  - 詳細 3
- 1.0: 代表的なタイトル
  - 詳細 1
  - 詳細 2
  - 詳細 3 -->

<!-- CONTRIBUTING -->
<!-- ## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- LICENSE -->
<!-- ## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- 参考文献 -->
## Acknowledgements

* [Joint Face Detection and Alignment using Multi-task Cascaded Convolutional Networks](https://arxiv.org/abs/1604.02878)
* [DeepFace: Closing the Gap to Human-Level Performance in Face Verification](https://www.cs.toronto.edu/~ranzato/publications/taigman_cvpr14.pdf)

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

<p align="right">(<a href="#readme-top">back to top</a>)</p>

</details>
