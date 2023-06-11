#include <stdio.h>
#include <ros/ros.h>
// #include <geometry_msgs/Twist.h>
// #include <geometry_msgs/Vector3.h>
// #include <nav_msgs/Odometry.h>
// #include <sensor_msgs/LaserScan.h>
// #include <std_msgs/Bool.h>
#include <vector>
#include <string>
// #include <iostream>
#include <limits>
// #include <cmath>
#include <math.h>
// #include <typeinfo>
// #include <sys/time.h>
// #include <matplotlib-cpp/matplotlibcpp.h>
// #include <active_slam/Plot.h>
// #include <active_slam/MapInformation.h>
#include <cstdlib>
#include <opencv2/opencv.hpp>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/Image.h>



// class GRIDDING
// {
//     public:
//         float size = 0.05;
//         float arg_size = 1/size;
//         float float_to_grid(float s, bool f=true)  // 適当な値をgrid幅に矯正する関数
//         {
//             float r = s - (((float)(s/size) - (int)(s/size))*size);
//             if ((s<0) && (f))
//             {
//                 r-=size;
//             }
//             r += (size/2);
//             return r;
//         }
//         int float_to_int(float s, bool f=true)  // grid幅の値を0を基準にした格納番号(int型)に変換する関数
//         {
//             int r = s*arg_size;
//             if ((s<0) && (f))
//             {
//                 r--;
//             }
//             return r;
//         }
//         float int_to_grid(int s)  // float_to_intの逆をする
//         {
//             return (float)((s/arg_size) + (1/(2*arg_size)));
//         }
// };


class FEATURE_SERVER
{
    private:
        std::string path;
        ros::NodeHandle nh;
    public:
        FEATURE_SERVER()
        {
            nh.getParam("/foo/bar", path);
        }
        void wait_for_call()
        {}
        void human_feature_detect()
        {}
};


int main(int argc, char **argv)
{
    ros::init(argc, argv, "human_feature_detect");
    std::string path;
    std::string user_name = std::getenv("USER");
    path = "/home/" + user_name + "/catkin_ws/src/human_feature_detect/filter/";
    
    std::string cascade_filename, age_net_model, age_net_weight, sex_net_model, sex_net_weight;
    cascade_filename = path + "haarcascade_frontalface_alt.xml";
    age_net_model = path + "deploy_age.prototxt";
    age_net_weight = path + "age_net.caffemodel";
    sex_net_model = path + "deploy_gender.prototxt";
    sex_net_weight = path + "gender_net.caffemodel";

    cv::CascadeClassifier cascade;
    if (!cascade.load(cascade_filename)) {
        std::cerr << "Failed to load cascade classifier." << std::endl;
        printf("NO!!\n");
        return -1;
    }

    std::vector<float> MODEL_MEAN_VALUES = {78.4263377603, 87.7689143744, 114.895847746};

    cv::dnn::Net age_net, sex_net;
    age_net = cv::dnn::readNetFromCaffe(age_net_model, age_net_weight);
    sex_net = cv::dnn::readNetFromCaffe(sex_net_model, sex_net_weight);

    std::vector<std::string> age_list = {"0 ~ 2","4 ~ 6","8 ~ 12","15 ~ 20","25 ~ 32","38 ~ 43","48 ~ 53","60 ~ 100"};
    std::vector<std::string> sex_list = {"Male", "Female"};


    // std::cout << "okay!" << std::endl;
    // set up END

    // sensor_msgs::Image::ConstPtr image_msg;  // 元の画像
    // cv_bridge::CvImagePtr bridge;   // opencvに変換する先
    // try
    // {
    //     bridge = cv_bridge::toCvCopy(image_msg, sensor_msgs::image_encodings::BGR8);
    // }
    // catch (cv_bridge::Exception& e)
    // {
    //     printf("err\n");
    //     ROS_ERROR("cv_bridge exception: %s", e.what());
    //     return -1;
    // }
    // cv::Mat image = bridge->image;
    cv::Mat image = cv::imread("/home/" + user_name + "/catkin_ws/src/human_feature_detect/img1.jpg");
    if (image.empty())
    {
        std::cout << "画像の読み込みに失敗しました" << std::endl;
        return -1;
    }
    cv::Mat gray;
    cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);
    std::vector<cv::Rect> results;
    cascade.detectMultiScale(image, results, 1.1, 5, 0, cv::Size(20,20));


    // std::vector<float> index_in(2,0);
    // std::vector<std::vector<float>> index(results.size(),index_in);
    // std::cout << results.size() << std::endl;
    int i = 0;
    for (const cv::Rect& rect : results)
    {
        cv::rectangle(image, rect, cv::Scalar(0, 255, 0), 2);
        // 切り出す範囲を指定
        cv::Rect roi(rect.x, rect.y, rect.width, rect.height);  // (x, y, width, height)

        // 指定した範囲で切り出す
        cv::Mat face = image(roi);

        // 入力画像を指定したサイズにリサイズ
        cv::Mat resiz_face;
        cv::resize(face, resiz_face, cv::Size(227, 227));

        // 入力画像をBLOB形式に変換
        cv::Scalar mean_values(MODEL_MEAN_VALUES[0], MODEL_MEAN_VALUES[1], MODEL_MEAN_VALUES[2]);
        cv::Mat blob = cv::dnn::blobFromImage(resiz_face, 1.0, cv::Size(227, 227), mean_values, false, false);
        
         // ブロブデータをネットワークに入力
        age_net.setInput(blob);
        sex_net.setInput(blob);

        // ネットワークの順伝播を実行し、予測結果を取得
        cv::Mat age_preds = age_net.forward();
        cv::Mat sex_preds = sex_net.forward();

        
        int max_index;
        float max_value;
        // 予測結果から最も高い確率のインデックスを取得
        max_index = 0;
        max_value = age_preds.at<float>(0);
        for (int i = 1; i < age_preds.rows; i++) {
            float value = age_preds.at<float>(i);
            if (value > max_value) {
                max_index = i;
                max_value = value;
            }
        }
        // 最大値のインデックスをgenderに代入
        int age_index = max_index;


        // 予測結果から最も高い確率のインデックスを取得
        max_index = 0;
        max_value = sex_preds.at<float>(0);
        for (int i = 1; i < sex_preds.rows; i++) {
            float value = sex_preds.at<float>(i);
            if (value > max_value) {
                max_index = i;
                max_value = value;
            }
        }
        // 最大値のインデックスをgenderに代入
        int sex_index = max_index;

        // // 最も高い確率のインデックスを取得
        // int age_index = max_loc_age.x;
        // int sex_index = max_loc_sex.x;
        std::cout << "age = " << age_list[age_index] << ", sex = " << sex_list[sex_index] << std::endl;
        // std::cout << "age = " << age_list[max_loc_age.y] << ", sex = " << sex_list[max_loc_sex.y] << std::endl;
        // std::cout << "age = " << age_list[max_loc_age] << ", sex = " << sex_list[max_loc_sex] << std::endl;
        // printf("\n");
        // cv::rectangle(image, rect, cv::Scalar(0, 255, 0), 2);
        // std::cout << "Detection result: x = " << rect.x << ", y = " << rect.y << ", width = " << rect.width << ", height = " << rect.height << std::endl;
    }
    cv::Mat resizedImage;
    cv::resize(image, resizedImage, cv::Size(500, 700));
    // cv::imshow("Image", image);
    cv::imshow("Image", resizedImage);
    cv::waitKey(0);
    return 0;
}

// int main() {
//     std::string user_name = std::getenv("USER");
//     std::string cascade_filename;
//     cascade_filename = "/home/" + user_name + "/catkin_ws/src/human_feature_detect/filter/haarcascade_frontalface_alt.xml";
//     cv::CascadeClassifier cascade;
//     // std::string cascade_filename = "/home/sobits/catkin_ws/src/sample_py/filter/haarcascade_frontalface_alt.xml";
//     // cv::CascadeClassifier cascade;
    
//     // カスケード分類器の読み込み
//     if (!cascade.load(cascade_filename)) {
//         std::cerr << "Failed to load cascade classifier." << std::endl;
//         return -1;
//     }

//     // 画像の読み込み
//     cv::Mat image = cv::imread("/home/" +user_name + "/catkin_ws/src/human_feature_detect/img1.jpg");
    
//     // グレースケールに変換
//     cv::Mat gray;
//     cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);
    
//     // 顔検出
//     std::vector<cv::Rect> faces;
//     cascade.detectMultiScale(gray, faces, 1.1, 2, 0 | cv::CASCADE_SCALE_IMAGE, cv::Size(30, 30));
    
//     // 検出された顔の描画
//     for (const auto& face : faces) {
//         cv::rectangle(image, face, cv::Scalar(0, 255, 0), 2);
//     }
    
//     // 画像の表示
//     cv::imshow("Image", image);
//     cv::waitKey(0);
    
//     return 0;
// }
