#include <stdio.h>
#include <rclcpp/rclcpp.hpp>
// #include <ros/ros.h>
#include <vector>
#include <string>
#include <iostream>
#include <limits>
#include <math.h>
#include <cmath>
#include <string>
#include <cstring>
#include <cstdlib>
// #include <opencv2/opencv.hpp>
// #include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/msg/image.hpp>

#include "human_feature_detection/point_cloud_processor.hpp"
// #include "human_feature_detection/srv/feature3d.hpp"
// #include "sobits_msgs/srv/feature3d.hpp"
#include "human_feature_detection_msgs/srv/feature3d.hpp"


struct RGB {
    uint r, g, b;
};


class HUMAN_FEATURE_DETECT_3D {
    private:
        rclcpp::Node::SharedPtr nd_;
        rclcpp::Subscription<sensor_msgs::msg::PointCloud2>::SharedPtr sub_points_;
        rclcpp::Service<human_feature_detection_msgs::srv::Feature3d>::SharedPtr server_feature_3d;
        // ros::NodeHandle nh_;
        // ros::NodeHandle pnh_;
        // ros::Subscriber sub_points_;
        // ros::Publisher pub_cloud_;
        std::string topic_name;
        human_feature_detection::PointCloudProcessor pcp_;
        std::string target_frame_;
        PointCloud::Ptr cloud_;
        RGB set_rgb;
        std::vector<int> r;
        std::vector<int> g;
        std::vector<int> b;
        bool flag = false;
        double height = 0.0;
        float face_range;
        float clothes_range;
        float min_range;
        float max_range;
        int bightness_value;

        void cbPoints(const std::shared_ptr<sensor_msgs::msg::PointCloud2> cloud_msg) {
        // void cbPoints(const sensor_msgs::PointCloud2ConstPtr &cloud_msg) {
            pcp_.transformFramePointCloud( target_frame_, cloud_msg, cloud_ );
            r.clear();
            g.clear();
            b.clear();
            double height_temp = (std::numeric_limits<double>::max())*(-1);
            for (std::size_t i=0; i<cloud_->points.size(); i++)
            {
                if ((min_range < cloud_->points[i].x) && (cloud_->points[i].x < max_range) && (-0.3 < cloud_->points[i].y) && (cloud_->points[i].y < 0.3) && (0.0 < cloud_->points[i].z) && (cloud_->points[i].z < 2.0))
                {
                    if (height_temp < cloud_->points[i].z)
                    {
                        height_temp = cloud_->points[i].z;
                    }
                }
            }
            if (height_temp != (std::numeric_limits<double>::max())*(-1))
            {
                height = height_temp;
                for (std::size_t i=0; i<cloud_->points.size(); i++)
                {
                    if ((min_range < cloud_->points[i].x) && (cloud_->points[i].x < max_range) && ((height - face_range - clothes_range) < cloud_->points[i].z ) && (cloud_->points[i].z < (height - face_range)))
                    {
                        r.push_back(cloud_->points[i].r);
                        g.push_back(cloud_->points[i].g);
                        b.push_back(cloud_->points[i].b);
                    }
                }
                std::sort(r.begin(), r.end());
                std::sort(g.begin(), g.end());
                std::sort(b.begin(), b.end());
                set_rgb.r = r[r.size()/2];
                set_rgb.g = g[g.size()/2];
                set_rgb.b = b[b.size()/2];
                flag = true;
            }
            // rclcpp::spin_some(nd_);
        }
        void human_feature_3d(const std::shared_ptr<human_feature_detection_msgs::srv::Feature3d::Request> req, std::shared_ptr<human_feature_detection_msgs::srv::Feature3d::Response> res)
        // void human_feature_3d(const std::shared_ptr<sobits_msgs::srv::Feature3d::Request> req, std::shared_ptr<sobits_msgs::srv::Feature3d::Response> res)
        // void human_feature_3d(const std::shared_ptr<human_feature_detection::srv::Feature3d::Request> req, std::shared_ptr<human_feature_detection::srv::Feature3d::Response> res)
        // bool human_feature_3d(human_feature_detection::Feature3d::Request &req, human_feature_detection::Feature3d::Response &res)
        {
            min_range = req->min_range;
            max_range = req->max_range;
            flag = false;
            // CALL_BACK Start
            rclcpp::Node::SharedPtr nd_pc = std::make_shared<rclcpp::Node>("human_feature_detection_3d_point_cloud");
            sub_points_ = nd_pc->create_subscription<sensor_msgs::msg::PointCloud2>(topic_name, 5, std::bind(&HUMAN_FEATURE_DETECT_3D::cbPoints, this, std::placeholders::_1));
            // sub_points_ = nh_.subscribe(topic_name, 5, &HUMAN_FEATURE_DETECT_3D::cbPoints, this);
            cloud_.reset(new PointCloud());
            rclcpp::Rate loop_rate(10);
            sleep(2.0);
            while (rclcpp::ok()) {
                if (flag) break;
                loop_rate.sleep();
                rclcpp::spin_some(nd_pc);
            }
            // CALL_BACK End
            res->color = decideColor(set_rgb);
            res->height = height*100;
            RCLCPP_INFO(nd_->get_logger(), "R = %d, G = %d, B = %d",set_rgb.r + bightness_value, set_rgb.g + bightness_value, set_rgb.b + bightness_value);
            RCLCPP_INFO(nd_->get_logger(), "color = %s",res->color.c_str());
            RCLCPP_INFO(nd_->get_logger(), "height = %.1f\n", height*100);
            // ROS_INFO("R = %d, G = %d, B = %d\n",set_rgb.r + bightness_value, set_rgb.g + bightness_value, set_rgb.b + bightness_value);
            // ROS_INFO("color = %s\n",res->color.c_str());
            // ROS_INFO("height = %.1f\n\n", height*100);
            if (res->color.compare("Unknown") == 0)
            {
                res->color_success = false;
                res->color = "";
            }
            else
            {
                res->color_success = true;
            }
            // sub_points_.shutdown(nd_);
            sub_points_ = nullptr;
        }
        void wait_for_call()
        {
            server_feature_3d = nd_->create_service<human_feature_detection_msgs::srv::Feature3d>("/human_feature_detection/feature3d", std::bind(&HUMAN_FEATURE_DETECT_3D::human_feature_3d, this, std::placeholders::_1, std::placeholders::_2));
            RCLCPP_INFO(nd_->get_logger(), "WAIT FOR SERVER");
            // rclcpp::spin(nd_);
            // ros::ServiceServer server_feature_3d = nh_.advertiseService("/human_feature_detection/feature3d", &HUMAN_FEATURE_DETECT_3D::human_feature_3d, this);
            // ros::spinOnce();
            // ros::spin();
        }
        std::string decideColor(RGB rgb)
        {
            float R = (float)((rgb.r + bightness_value) / 256.0);
            float G = (float)((rgb.g + bightness_value) / 256.0);
            float B = (float)((rgb.b + bightness_value) / 256.0);
            double Max = std::max({ R, G, B });
            double Min = std::min({ R, G, B });

            double h = Max - Min;
            if (h == 0) {
                h = 1;
            }
            if (Max == 0) {
                Max = 1;
            }

            double S = (h / Max) * 100;
            double V = Max * 100;
            double H;

            if (Max == R) {
                H = 60 * ((G - B) / h);
                if (H < 0) {
                    H = 360 - std::abs(H);
                }
            }
            else if (Max == G) {
                H = 60 * ((B - R) / h) + 120;
            }
            else if (Max == B) {
                H = 60 * ((R - G) / h) + 240;
            }
            else if (R == G && G == B) {
                H = 0;
            }
            else {
                // Should not reach this point
                return "Unknown";
            }

            if ((H >= 0 && H < 30) || (H >= 340 && H <= 360)) {
                if (S <= 10 && V > 85) {
                    return "White";
                }
                else if (S <= 10 && V > 15 && V <= 85) {
                    return "Gray";
                }
                else if (V <= 15) {
                    return "Black";
                }
                else {
                    return "Red";
                }
            }
            else if (H >= 30 && H < 40) {
                if (S <= 10 && V > 85) {
                    return "White";
                }
                else if (S <= 10 && V > 15 && V <= 85) {
                    return "Gray";
                }
                else if (V <= 15) {
                    return "Black";
                }
                else if (S >= 50 && V <= 80 && V > 15) {
                    return "Brown";
                }
                else {
                    return "Orange";
                }
            }
            else if (H >= 40 && H < 65) {
                if (S <= 10 && V > 85) {
                    return "White";
                }
                else if (S <= 10 && V > 15 && V <= 85) {
                    return "Gray";
                }
                else if (V <= 15) {
                    return "Black";
                }
                else {
                    return "Yellow";
                }
            }
            else if (H >= 65 && H < 165) {
                if (S <= 10 && V > 85) {
                    return "White";
                }
                else if (S <= 10 && V > 15 && V <= 85) {
                    return "Gray";
                }
                else if (V <= 15) {
                    return "Black";
                }
                else {
                    return "Green";
                }
            }
            else if (H >= 165 && H < 265) {
                if (S <= 10 && V > 85) {
                    return "White";
                }
                else if (S <= 10 && V > 15 && V <= 85) {
                    return "Gray";
                }
                else if (V <= 15) {
                    return "Black";
                }
                else {
                    return "Blue";
                }
            }
            else if (H >= 265 && H < 340) {
                if (S <= 10 && V > 85) {
                    return "White";
                }
                else if (S <= 10 && V > 15 && V <= 85) {
                    return "Gray";
                }
                else if (V <= 15) {
                    return "Black";
                }
                else if (H >= 300 && S > 5 && V >= 80) {
                    return "Pink";
                }
                else {
                    return "Purple";
                }
            }
            else {
                return "Unknown";
            }
        }
    public:
        HUMAN_FEATURE_DETECT_3D(std::shared_ptr<rclcpp::Node> nd): nd_(nd), pcp_(nd) {
            // topic_name = nd_.param<std::string>( "topic_name", "/points2" );
            // face_range = nd_.param<float>( "face_range", 0.20 );
            // clothes_range = nd_.param<float>( "clothes_range", 0.50 );
            // target_frame_ = nd_.param<std::string>( "target_frame", "base_footprint" );
            // bightness_value = nd_.param<int>( "bightness_value", 0 );
            topic_name = "/camera/camera/depth/color/points";
            face_range = 0.20;
            clothes_range = 0.50;
            target_frame_ = "camera_link";
            bightness_value = 0;
            wait_for_call();
        }
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    rclcpp::Node::SharedPtr nd = std::make_shared<rclcpp::Node>("human_feature_detection_3d");
    // ros::init(argc, argv, "human_feature_detection_3d");
    // HUMAN_FEATURE_DETECT_3D human_feature_detect_3d;
    auto human_feature_detect_3d = std::make_shared<HUMAN_FEATURE_DETECT_3D>(nd);
    rclcpp::executors::SingleThreadedExecutor exec;
    exec.add_node(nd);
    exec.spin();
    rclcpp::shutdown();
    return 0;
}