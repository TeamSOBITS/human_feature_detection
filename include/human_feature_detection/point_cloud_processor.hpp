#ifndef POINT_CLOUD_PROCESSOR_HPP
#define POINT_CLOUD_PROCESSOR_HPP

#include <tf2_ros/transform_listener.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_ros/point_cloud.h>
#include <pcl_ros/transforms.h>
#include <pcl/point_types.h>
#include <pcl/common/common.h>
#include <pcl/kdtree/kdtree.h>
#include <pcl/filters/statistical_outlier_removal.h>

typedef pcl::PointXYZRGB PointT;
typedef pcl::PointCloud<PointT> PointCloud;

namespace human_feature_detection {
    class PointCloudProcessor {
        protected:
            tf2_ros::Buffer tfBuffer_;
            tf2_ros::TransformListener tf_listener_;
            pcl::search::KdTree<PointT>::Ptr tree_;

        public:
            PointCloudProcessor();
            bool transformFramePointCloud ( const std::string &target_frame, const sensor_msgs::PointCloud2ConstPtr &input_cloud, PointCloud::Ptr output_cloud );
    };
}

#endif