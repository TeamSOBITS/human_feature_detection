#ifndef POINT_CLOUD_PROCESSOR_HPP
#define POINT_CLOUD_PROCESSOR_HPP

#include <rclcpp/rclcpp.hpp>
#include <tf2_ros/transform_listener.h>
#include <tf2_ros/buffer.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <sensor_msgs/msg/point_cloud2.hpp>
// #include <pcl_ros/point_cloud.h>
#include <pcl_ros/transforms.hpp>
#include <pcl_conversions/pcl_conversions.h>

#include <pcl/point_types.h>
#include <pcl/common/common.h>
#include <pcl/search/kdtree.h>
// #include <pcl/kdtree/kdtree.h>
#include <pcl/filters/statistical_outlier_removal.h>

// #include <pcl/point_cloud.h>


typedef pcl::PointXYZRGB PointT;
typedef pcl::PointCloud<PointT> PointCloud;

namespace human_feature_detection {
    class PointCloudProcessor {
        protected:
            rclcpp::Node::SharedPtr nd_;
            tf2_ros::Buffer tfBuffer_;
            tf2_ros::TransformListener tf_listener_;
            pcl::search::KdTree<PointT>::Ptr tree_;

        public:
            PointCloudProcessor(std::shared_ptr<rclcpp::Node> nd);
            bool transformFramePointCloud ( const std::string &target_frame, const sensor_msgs::msg::PointCloud2::SharedPtr& input_cloud, PointCloud::Ptr output_cloud );
    };
}

#endif