# human_feature_detect

写真から人の特徴を推論するパッケージです\
\
APIを使用しないため、ネットワークなしで、オフラインの推論が行えます。
service通信を用いて特徴を検出します。\

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
