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
// #include <limits>
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
    std::cout << "OpenCV version : " << CV_MAJOR_VERSION << "." << CV_MINOR_VERSION << std::endl;
    return 0;
    // FEATURE_SERVER feature_server;
    // ros::spin();
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

    cv::dnn::Net age_net, sex_net;
    age_net = cv::dnn::readNetFromCaffe(age_net_model, age_net_weight);
    sex_net = cv::dnn::readNetFromCaffe(sex_net_model, sex_net_weight);

    // printf("ok\n");
    // std::cout << age_net << std::endl;
    // std::cout << sex_net << std::endl;
    // std::cout << path << std::endl;




    sensor_msgs::Image::ConstPtr image_msg;  // 元の画像
    cv_bridge::CvImagePtr bridge;   // opencvに変換する先
    try
    {
        bridge = cv_bridge::toCvCopy(image_msg, sensor_msgs::image_encodings::BGR8);
    }
    catch (cv_bridge::Exception& e)
    {
        printf("err\n");
        ROS_ERROR("cv_bridge exception: %s", e.what());
        return -1;
    }
    cv::Mat orig = bridge->image;


    // cascade.detectMultiScale( orig, scaleFactor= 1.1, minNeighbors=5, minSize=(20,20) );
    // cascade.detectMultiScale(orig, cv::Size(20,20), 1.1, 5, 0, cv::Size());

    printf("ok!\n");

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
//     cv::Mat image = cv::imread("/home/" +user_name + "/catkin_ws/src/image1.jpg");
    
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
