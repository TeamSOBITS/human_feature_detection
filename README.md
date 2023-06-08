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
from human_feature_detect import 


def main():
    rospy.init_node('test_human_feature_detect')
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass
```
