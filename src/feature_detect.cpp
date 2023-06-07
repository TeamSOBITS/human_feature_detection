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
    // FEATURE_SERVER feature_server;
    // ros::spin();
    std::string cascade_filename;
    std::string user_name = std::getenv("USER");
    cascade_filename = "/home/" + user_name + "/catkin_ws/src/human_feature_detect/filter/haarcascade_frontalface_alt.xml";
    // std::cout << "USER: " << user_name << std::endl;
    std::cout << "PATH : " << cascade_filename << std::endl;
}