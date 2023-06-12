# human_feature_detect

写真から人の特徴を推論するパッケージです\
\
APIを使用しないため、ネットワークなしで、オフラインの推論が行えます。
service通信を用いて特徴を検出します。

## インストール方法

```python
$ cd ~/catkin_ws/src/
$ git clone https://github.com/TeamSOBITS/human_feature_detect
$ cd ~/catkin_ws/
$ catkin_make
```

## 使用方法
```python
$ roslaunch human_feature_detect human_feature_detect.launch
```
## Example Code
<details><summary>C++</summary>

## C++
```cpp
#include <ros/ros.h>
#include <human_feature_detect/>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "test_human_feature_detect");
    ros::NodeHandle nh;
    ros::spin();
}
```
</details>

<details><summary>Python</summary>

## Python

```python
#!/usr/bin/env python3
import rospy
from human_feature_detect.srv import ImageToFeatures
from human_feature_detect.srv import PathToFeatures


def main():
    rospy.init_node('test_human_feature_detect')
    
    # ここに特徴を検出したい人が映った画像のパスを書く
    image = cv2.imread("/home/sobits/catkin_ws/src/human_feature_detect/image.jpg")

    bridge = CvBridge()
    image_msg = bridge.cv2_to_imgmsg(image, encoding="bgr8")
    rospy.wait_for_service("/human_feature_detect/imagedata_features")  # 画像を送る場合はこのService名を指定
    # rospy.wait_for_service("/human_feature_detect/imagepath_features")  # 画像のパスを送る場合はこのService名を指定
    service = rospy.ServiceProxy("/human_feature_detect/image_features", ImageToFeatures)
    req = ImageToFeatures()
    req.image = image_msg
    res = service(req.image)
    print(res)
    rospy.spin()


if __name__ == '__main__':
    main()
```
