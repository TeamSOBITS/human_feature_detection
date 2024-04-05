#include <human_feature_detect/point_cloud_processor.hpp>

using namespace human_feature_detect;

PointCloudProcessor::PointCloudProcessor() : tfBuffer_(), tf_listener_(tfBuffer_) {
    tree_ .reset ( new pcl::search::KdTree<PointT>() );
}
bool PointCloudProcessor::transformFramePointCloud(const std::string& target_frame, const sensor_msgs::PointCloud2ConstPtr& input_cloud, PointCloud::Ptr output_cloud) {
    PointCloud cloud_src;
    pcl::fromROSMsg(*input_cloud, cloud_src);
    if (!target_frame.empty()) {
        try {
            while (ros::ok()) {
                if (tfBuffer_.canTransform(target_frame, cloud_src.header.frame_id, ros::Time(0), ros::Duration(1.0))) {
                    break;
                } else {
                    ros::Duration(1.0).sleep();
                }
            }
            pcl_ros::transformPointCloud(target_frame, ros::Time(0), cloud_src, cloud_src.header.frame_id, *output_cloud, tfBuffer_);
            output_cloud->header.frame_id = target_frame;
        } catch (tf2::TransformException& ex) {
            ROS_ERROR("%s", ex.what());
            return false;
        }
    } else {
        ROS_ERROR("Please set the target frame.");
        return false;
    }
    return true;
}