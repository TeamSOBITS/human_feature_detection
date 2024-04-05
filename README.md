<a name="readme-top"></a>

[JP](template_readme.md) | [EN](template_readme_en.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
<!-- [![MIT License][license-shield]][license-url] -->

# Human Feature Detect

<!-- 目次 -->
<details>
  <summary>目次</summary>
  <ol>
    <li>
      <a href="#概要">概要</a>
    </li>
    <li>
      <a href="#環境構築">環境構築</a>
      <ul>
        <li><a href="#環境条件">環境条件</a></li>
        <li><a href="#インストール方法">インストール方法</a></li>
      </ul>
    </li>
    <li><a href="#実行・操作方法">実行・操作方法</a></li>
    <li><a href="#マイルストーン">マイルストーン</a></li>
    <li><a href="#変更履歴">変更履歴</a></li>
    <!-- <li><a href="#contributing">Contributing</a></li> -->
    <!-- <li><a href="#license">License</a></li> -->
    <li><a href="#参考文献">参考文献</a></li>
  </ol>
</details>



<!-- レポジトリの概要 -->
## 概要

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

写真から人の特徴を推論するパッケージです．\
APIを使用しないため，ネットワークなしで，オフラインの推論が行えます．/
ROSのService通信を用いて特徴を検出します．\
caffemodelが日本人ではないため，日本人の年齢と性別の推定には精度が低いです．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>



<!-- セットアップ -->
## セットアップ
ここで，本レポジトリのセットアップ方法について説明します．

### 環境条件

以下に正常動作環境を示します．
| System  | Version |
| ------------- | ------------- |
| Ubuntu | 20.04 (Focal Fossa) |
| ROS | Noetic Ninjemys |
| Python | 3.0~ |

### インストール方法

1. ROSの`src`フォルダに移動します．
   ```sh
   $ cd　~/catkin_ws/src/
   ```
2. 本レポジトリをcloneします．
   ```sh
   $ git clone https://github.com/TeamSOBITS/human_feature_detect.git
   ```
3. レポジトリの中へ移動します．
   ```sh
   $ cd human_feature_detect
   ```
4. 依存パッケージをインストールします．
   ```sh
   $ bash install.sh
   ```
5. パッケージをコンパイルします．
   ```sh
   $ cd ~/catkin_ws/
   $ catkin_make
   ```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>



<!-- 実行・操作方法 -->
## 実行・操作方法
### 2次元で行える特徴検出（性別と年齢）
<!-- デモの実行方法やスクリーンショットがあるとわかりやすくなるでしょう -->
1. [human_feature_detect.launch](/launch/human_feature_detect.launch)というlaunchファイルを実行します．
    ```sh
    $ roslaunch human_feature_detect human_feature_detect.launch
    ```
    これによって，画像から推論を行えるROSのService通信のServerが起動します．
2. [任意] imagesフォルダにあるサンプル画像([sample_image.jpg](/images/sample_image.jpg))を使って推論をしてみましょう．
    exampleコードを準備したので，それを使っていきます．
   1. Pythonの場合
        ```sh
        $ rosrun human_feature_detect sample_2d.py
        ```
   2. C++の場合
        ```sh
        $ rosrun human_feature_detect sample_2d
        ```
    人の顔にバウンディングボックスがあてられ，性別と年齢を推定した結果の画像が出力されました．
    出力された画像は，[sample_image_result.jpg](/images/sample_image_result.jpg)として保存されています．

### 3次元で行える特徴検出（身長と服の色）
1. 点群のTopic名を設定します．paramとして[human_feature_detect.launch](/launch/human_feature_detect.launch)ファイルに設定します．
   ```xml
    <param name="topic_name" value="/points2"/>
    ...
   ```
   他のパラメータについて
   ```
    <param name="target_frame" value="base_footprint"/>　　<!-- ロボットの基準フレーム。これによって身長を地面を基準とする頭の高さとできる -->
    <param name="face_range" value="0.20"/>               <!-- 顔の大体の大きさ。服の色を測る際に頭の先からどれだけ下の点群を参照するか -->
    <param name="clothes_range" value="0.35"/>            <!-- 服のおおよその縦幅。服の色を測る際、どれだけ広範囲を参照するか -->
   ```
2. 設定が完了したら，[human_feature_detect.launch](/launch/human_feature_detect.launch)というlaunchファイルを実行します．
    ```sh
    $ roslaunch human_feature_detect human_feature_detect.launch
    ```
    これによって，点群から推論を行えるROSのService通信のServerが起動します．
3. [任意] imagesフォルダにあるサンプル画像([sample_image.jpg](/images/sample_image.jpg))を使って推論をしてみましょう．
    exampleコードを準備したので，それを使っていきます．
   1. Pythonの場合
        ```sh
        $ rosrun human_feature_detect sample_3d.py
        ```
   2. C++の場合
        ```sh
        $ rosrun human_feature_detect sample_3d
        ```
    ターミナルに，身長と服の色が出力されました．

> [!NOTE]
> このexampleコードを使えば，ロボットのカメラから得た画像や点群から，データをServiceのServerに送信することで，人の特徴を推定することができます．\
> [example](/example/)フォルダを確認し，それぞれのサンプルファイルからServiceのクライアント(リクエスト側)について学びましょう．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>



<!-- マイルストーン -->
<!-- ## マイルストーン

- [x] 目標 1
- [ ] 目標 2
- [ ] 目標 3
    - [ ] サブ目標

現時点のバッグや新規機能の依頼を確認するために[Issueページ](https://github.com/github_username/repo_name/issues) をご覧ください．

<p align="right">(<a href="#readme-top">上に</a>)</p> -->



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

<p align="right">(<a href="#readme-top">上に戻る</a>)</p> -->



<!-- LICENSE -->
<!-- ## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">上に戻る</a>)</p> -->



<!-- 参考文献 -->
## 参考文献

* []()

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
<!-- [license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt -->


## Example Code
<details><summary>C++</summary>

## C++
```cpp
#include <stdio.h>
#include <ros/ros.h>
#include <cstdlib>
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>
#include <vector>
#include <string>
#include <iostream>
#include <sensor_msgs/Image.h>
#include <human_feature_detect/Features.h>

int main(int argc, char** argv) {
    ros::init(argc, argv, "human_feature_detect_sample_2d");
    std::string home_path = getenv("HOME"); // ここにターミナルのhomeディレクトリまでのパスが代入  ex) home_path = "/home/sobits"

    // 写真をopencvで読み込む。home_path + catkin_ws以降の写真ホルダーまでのパスを入力
    std::string picture_file_path = home_path + "/catkin_ws/src/human_feature_detect/images/sample_image.jpg";
    cv::Mat picture = cv::imread(picture_file_path);
    ros::spinOnce();
    cv_bridge::CvImage cv_image;

    // 写真の型(BGR型)から、ROSで通信を行える型(sensor_msgs/Image型)に変換する
    cv_image.encoding = sensor_msgs::image_encodings::BGR8;
    cv_image.image = picture;

    // 特徴(年齢と性別)を取得してくれるServiceのサーバーが立ち上がったら接続される定義をする
    ros::NodeHandle nh;
    ros::ServiceClient service = nh.serviceClient<human_feature_detect::Features>("/human_feature_detect/features");

    // サーバーに送信するデータを作成する
    human_feature_detect::Features srv;
    srv.request.input_image = *cv_image.toImageMsg();

    // サーバーが立ち上がったらROSのメッセージにした写真をサーバーに送信
    while (ros::ok()) {
        if (service.call(srv)) break;
        else {
            ros::spinOnce();
            continue;
        }
    }

    // 返答されたデータから、テキストで出力する(例)
    printf("検出された人数は%ld人です。\n\n",srv.response.features.size());
    for (int i=0; i<srv.response.features.size(); i++) {
        printf("%d人目の人は、性別は%sで、\n", (i+1), srv.response.features[i].sex.c_str());
        printf("年齢は%d歳から%d歳くらいです。\n\n", srv.response.features[i].age_lower, srv.response.features[i].age_uper);
    }

    // 返答されたデータから、画像を出力する方法
    // 返答されたROSのメッセージの型(sensor_msgs/Image型)から写真の型(BGR型)に変換する。
    cv_bridge::CvImageConstPtr cv_ptr = cv_bridge::toCvCopy(srv.response.result_image, sensor_msgs::image_encodings::BGR8);
    cv::Mat output_image = cv_ptr->image;
    for (int i=0; i<4; i++) picture_file_path.pop_back();
    cv::imwrite(picture_file_path + "_result.jpg", output_image);
    cv::imshow("result_image", output_image);
    cv::waitKey(100);
    ros::spinOnce();
    ros::spin();
    return 0;
}
```
</details>

<details><summary>Python</summary>

## Python

```python
#!/usr/bin/env python3
import rospy
from os.path import expanduser
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from human_feature_detect.srv import Features

def main():
    rospy.init_node("human_feature_detect_sample_2d")
    home_path = expanduser("~") # ここにターミナルのhomeディレクトリまでのパスが代入  ex) home_path = "/home/sobits"

    # 写真をopencvで読み込む。home_path + catkin_ws以降の写真ホルダーまでのパスを入力
    picture_file_path = home_path + "/catkin_ws/src/human_feature_detect/images/sample_image.jpg"
    picture = cv2.imread(picture_file_path)
    bridge = CvBridge()

    # 写真の型(BGR型)から、ROSで通信を行える型(sensor_msgs/Image型)に変換する
    image_msg = bridge.cv2_to_imgmsg(picture, encoding="bgr8")

    # 特徴(年齢と性別)を取得してくれるServiceのサーバーが立ち上がるまで待つ
    rospy.wait_for_service("/human_feature_detect/features")
    # サーバーが立ち上がったらこちら側でクライアントとして定義する
    service = rospy.ServiceProxy("/human_feature_detect/features", Features)

    # ROSのメッセージにした写真をサーバーに送信。返答結果はresponseに代入される
    response = service(image_msg)

    # 返答されたデータから、テキストで出力する(例)
    print("検出された人数は" + str(len(response.features)) + "人です。\n")
    for i in range(len(response.features)):
        print(str(i+1) + "人目の人は、性別は" + str(response.features[i].sex) + "で、")
        print("年齢は" + str(response.features[i].age_lower) + "歳から" + str(response.features[i].age_uper) + "歳くらいです。\n")
    
    # 返答されたデータから、画像を出力する方法
    # 返答されたROSのメッセージの型(sensor_msgs/Image型)から写真の型(BGR型)に変換する。
    output_image = bridge.imgmsg_to_cv2(response.result_image, desired_encoding="bgr8")
    # 写真が保存されていたところに、バウンディングボックスをつけた返答画像も保存する。
    cv2.imwrite(picture_file_path[:-4] + "_result.jpg", output_image)
    # 画像を表示
    cv2.imshow("result_image", output_image)
    cv2.waitKey(0)
    rospy.spin()

if __name__ == '__main__':
    main()
```
