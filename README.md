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
    <!-- <li><a href="#変更履歴">変更履歴</a></li> -->
    <!-- <li><a href="#contributing">Contributing</a></li> -->
    <!-- <li><a href="#license">License</a></li> -->
    <li><a href="#参考文献">参考文献</a></li>
  </ol>
</details>



<!-- レポジトリの概要 -->
## 概要

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

画像や点群から人の特徴を推論するパッケージです．\
APIなどのネットワークを使用しないため，ネットワークなしで，オフラインの推論が行えます．\
画像や点群を入力値として推定返り値とするため，ROSのService通信を用いて特徴を検出します．

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
1. なんらかのカメラを起動する\
    Topicとしてsensor_msgs/Image型が出ればどのカメラでも構いません．\
    例として，PCに付いているカメラを起動させてみる方法を以下に記述する．
    ```sh
    $ roslaunch usb_cam usb_cam-test.launch
    ```
    これが上手く行かない場合は，カメラが存在しないPCかubuntu上でカメラが使えないPCの可能性が高いので，USB接続でROS通信ができるカメラを起動する．
2. [human_feature_detect.launch](/launch/human_feature_detect.launch)というlaunchファイルを実行します．
    ```sh
    $ roslaunch human_feature_detect human_feature_detect.launch
    ```
    これによって，画像から推論を行えるROSのService通信のServerが起動します．
3. [任意]TopicにPublishされているImageを送ってみる\
    exampleコードを準備したのでそれを使っていきます．\
    [example/sample_2d.py](example/sample_2d.py)にある19行目のTopic名を「1.」で起動したカメラのTopic名に変更する．\
    そのままでは，「/camera/rgb/image_raw」になっていて，主にxtionなどのカメラのTopic名となっている．\
    以下のコマンドを実行すると，3秒のカウントダウンの後に写っていた画像についての推論を行う．（カウントダウンが開始されない場合，カメラが起動していないかTopic名が間違えている可能性があります）
    ```sh
    $ rosrun human_feature_detect sample_2d.py
    ```
    ターミナルに，検出した人数と，それぞれの年齢と性別，表情が出力されました．\
    ちなみにこの結果を反映させた画像は，[result.png](/images/result.png)としてimagesフォルダの中に保存されていますので確認してみてください．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

### 3次元で行える特徴検出（身長と服の色）
1. 点群をPublishすることのできるカメラを起動する\
  depthカメラを起動してください．
2. 点群のTopic名を設定する\
  paramとして[human_feature_detect.launch](/launch/human_feature_detect.launch)ファイルの6行目に，「1.」のTopic名に設定します．\
  例として，azure kinectの点群名である/points2に設定しています．
  ```xml
    <param name="topic_name" value="/points2"/>
  ```
  他のパラメータについて
  ```
    <param name="target_frame" value="base_footprint"/>　 <!-- ロボットの基準フレーム。これによって身長を地面を基準とする頭の高さとできる -->
    <param name="face_range" value="0.20"/>               <!-- 顔の大体の大きさ。服の色を測る際に頭の先からどれだけ下の点群を参照するか -->
    <param name="clothes_range" value="0.35"/>            <!-- 服のおおよその縦幅。服の色を測る際、どれだけ広範囲を参照するか -->
  ```
3. 設定が完了したら，[human_feature_detect.launch](/launch/human_feature_detect.launch)というlaunchファイルを実行します．
  ```sh
   $ roslaunch human_feature_detect human_feature_detect.launch
  ```
  これによって，点群から推論を行えるROSのService通信のServerが起動します．
4. [任意]指定した点群をリクエストしてみる\
  exampleコードを準備したので，それを使っていきます．\
  3次元での推論をする場合は，カメラの前方1メートルあたりに立ってください．
  ```sh
   $ rosrun human_feature_detect sample_3d.py
  ```
  ターミナルに，身長と服の色が出力されました．\
  出力されない場合，「2.」で設定した点群名(topic_name)や基準のフレーム名(target_frame)が間違っている可能性が高いです．

> [!NOTE]
> このexampleコードを使えば，ロボットのカメラから得た画像や点群から，データをServiceのServerに送信することで，人の特徴を推定することができます．\
> [example](/example/)フォルダを確認し，それぞれのサンプルファイルからServiceのクライアント(リクエスト側)について学びましょう．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>



<!-- マイルストーン -->
## マイルストーン

- [x] OSS化
- [ ] README(英語版)の作成

現時点のバッグや新規機能の依頼を確認するために[Issueページ](issues-url) をご覧ください．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>


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

* [Joint Face Detection and Alignment using Multi-task Cascaded Convolutional Networks](https://arxiv.org/abs/1604.02878)
* [DeepFace: Closing the Gap to Human-Level Performance in Face Verification](https://www.cs.toronto.edu/~ranzato/publications/taigman_cvpr14.pdf)

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TeamSOBITS/human_feature_detect.svg?style=for-the-badge
[contributors-url]: https://github.com/TeamSOBITS/human_feature_detect/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TeamSOBITS/human_feature_detect.svg?style=for-the-badge
[forks-url]: https://github.com/TeamSOBITS/human_feature_detect/network/members
[stars-shield]: https://img.shields.io/github/stars/TeamSOBITS/human_feature_detect.svg?style=for-the-badge
[stars-url]: https://github.com/TeamSOBITS/human_feature_detect/stargazers
[issues-shield]: https://img.shields.io/github/issues/TeamSOBITS/human_feature_detect.svg?style=for-the-badge
[issues-url]: https://github.com/TeamSOBITS/human_feature_detect/issues
[license-shield]: https://img.shields.io/github/license/TeamSOBITS/human_feature_detect.svg?style=for-the-badge
[license-url]: LICENSE

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

</details>
