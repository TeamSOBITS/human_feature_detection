#include <human_feature_detection/point_cloud_processor.hpp>

using namespace human_feature_detection;

PointCloudProcessor::PointCloudProcessor(std::shared_ptr<rclcpp::Node> nd) : nd_(nd), tfBuffer_(std::make_shared<rclcpp::Clock>(RCL_ROS_TIME)), tf_listener_(tfBuffer_) {
    tree_.reset ( new pcl::search::KdTree<PointT>() );
}
bool PointCloudProcessor::transformFramePointCloud(const std::string& target_frame, const sensor_msgs::msg::PointCloud2::SharedPtr& input_cloud, PointCloud::Ptr output_cloud) {
    PointCloud::Ptr cloud_src(new PointCloud);
    pcl::fromROSMsg(*input_cloud, *cloud_src);
    if (!target_frame.empty()) {
        try {
            while (rclcpp::ok()) {
                if (tfBuffer_.canTransform(target_frame, input_cloud->header.frame_id, tf2::TimePointZero, tf2::durationFromSec(1.0))) {
                // if (tfBuffer_.canTransform(target_frame, cloud_src.header.frame_id, ros::Time(0), ros::Duration(1.0))) {
                    break;
                } else {
                    rclcpp::sleep_for(std::chrono::seconds(1));
                    // ros::Duration(1).sleep();
                }
            }
            geometry_msgs::msg::TransformStamped transform_stamped = tfBuffer_.lookupTransform(target_frame, input_cloud->header.frame_id, tf2::TimePointZero, tf2::durationFromSec(1.0));
            pcl_ros::transformPointCloud(*cloud_src, *output_cloud, transform_stamped);
            // pcl_ros::transformPointCloud(target_frame, tf2::TimePointZero, *cloud_src, input_cloud->header.frame_id, *output_cloud, tfBuffer_);
            // pcl_ros::transformPointCloud(target_frame, ros::Time(0), cloud_src, cloud_src.header.frame_id, *output_cloud, tfBuffer_);
            output_cloud->header.frame_id = target_frame;
        } catch (tf2::TransformException& ex) {
            RCLCPP_ERROR(nd_->get_logger(), "%s", ex.what());
            // ROS_ERROR("%s", ex.what());
            return false;
        }
    } else {
        RCLCPP_ERROR(nd_->get_logger(), "Please set the target frame.");
        // ROS_ERROR("Please set the target frame.");
        return false;
    }
    return true;
}