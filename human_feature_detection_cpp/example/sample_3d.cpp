#include <rclcpp/rclcpp.hpp>
#include <sobits_interfaces/srv/feature3d.hpp>
#include <iostream>

class HumanFeatureDetectClient : public rclcpp::Node {
public:
    HumanFeatureDetectClient() : Node("sample_3d") {
        client_ = this->create_client<sobits_interfaces::srv::Feature3d>("/human_feature_detection_cpp/feature3d");


        // サービスが利用可能になるまで待つ
        while (!client_->wait_for_service(std::chrono::seconds(1))) {
            RCLCPP_INFO(this->get_logger(), "サービスの待機中...");
        }

        // リクエストを作成
        auto request = std::make_shared<sobits_interfaces::srv::Feature3d::Request>();
        request->min_range = 0.2;
        request->max_range = 1.2;

        // 非同期でサービスを呼び出す
        auto future = client_->async_send_request(request);

        // レスポンスを待つ
        if (rclcpp::spin_until_future_complete(this->get_node_base_interface(), future) == rclcpp::FutureReturnCode::SUCCESS) {
            auto response = future.get();
            std::cout << "身長は、およそ " << response->height << " センチメートルです。" << std::endl;
            if (response->color_success) {
                std::cout << "服の色は、" << response->color << " です。" << std::endl;
            } else {
                std::cout << "服の色がよくわかりません。" << std::endl;
            }
        } else {
            RCLCPP_ERROR(this->get_logger(), "サービス呼び出しに失敗しました");
        }
    }

private:
    rclcpp::Client<sobits_interfaces::srv::Feature3d>::SharedPtr client_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<HumanFeatureDetectClient>();
    rclcpp::shutdown();
    return 0;
}
