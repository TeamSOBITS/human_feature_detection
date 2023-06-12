#include <stdio.h>
#include <ros/ros.h>
#include <vector>
#include <string>
#include <iostream>
#include <limits>
#include <math.h>
#include <cstdlib>
#include <opencv2/opencv.hpp>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/Image.h>

#include <human_feature_detect/ImageToFeature.h>
#include <human_feature_detect/ImageToFeatures.h>
#include <human_feature_detect/PathToFeature.h>
#include <human_feature_detect/PathToFeatures.h>
#include <human_feature_detect/Feature.h>



class FEATURE_SERVER
{
    private:
        std::string path, user_name, cascade_filename, age_net_model, age_net_weight, sex_net_model, sex_net_weight;
        cv::CascadeClassifier cascade;
        std::vector<float> MODEL_MEAN_VALUES{3};
        cv::dnn::Net age_net, sex_net;
        ros::NodeHandle nh;
        std::vector<std::vector<int>> age_list = {{0,2},{4,6},{8,12},{15,20},{25,32},{38,43},{48,53},{60,100}};
        std::vector<std::string> sex_list = {"Male", "Female"};
    public:
        FEATURE_SERVER()
        {
            user_name = std::getenv("USER");
            path = "/home/" + user_name + "/catkin_ws/src/human_feature_detect/filter/";
            cascade_filename = path + "haarcascade_frontalface_alt.xml";
            age_net_model = path + "deploy_age.prototxt";
            age_net_weight = path + "age_net.caffemodel";
            sex_net_model = path + "deploy_gender.prototxt";
            sex_net_weight = path + "gender_net.caffemodel";

            nh.getParam("/MODEL_MEAN_VALUES_0", MODEL_MEAN_VALUES[0]);
            nh.getParam("/MODEL_MEAN_VALUES_1", MODEL_MEAN_VALUES[1]);
            nh.getParam("/MODEL_MEAN_VALUES_2", MODEL_MEAN_VALUES[2]);
            // MODEL_MEAN_VALUES[0] = 78.4263377603;
            // MODEL_MEAN_VALUES[1] = 87.7689143744;
            // MODEL_MEAN_VALUES[2] = 114.895847746;

            age_net = cv::dnn::readNetFromCaffe(age_net_model, age_net_weight);
            sex_net = cv::dnn::readNetFromCaffe(sex_net_model, sex_net_weight);
            bool start_flag = init_checker(cascade_filename);
            if (start_flag)
            {
                wait_for_call();
            }
            // nh.getParam("/foo/bar", path);
        }
        bool init_checker(std::string filename)
        {
            if (!cascade.load(filename))
            {
                std::cerr << "Failed to load cascade classifier." << std::endl;
                printf("NO!!\n");
                return false;
            }
            return true;
        }
        void wait_for_call()
        {
            ros::ServiceServer server_features_image = nh.advertiseService("/human_feature_detect/imagedata_features", &FEATURE_SERVER::human_features_callback_from_image, this);
            ros::ServiceServer server_features_path = nh.advertiseService("/human_feature_detect/imagepath_features", &FEATURE_SERVER::human_features_callback_from_path, this);
            ros::ServiceServer server_feature_image = nh.advertiseService("/human_feature_detect/imagedata_feature", &FEATURE_SERVER::human_feature_callback_from_image, this);
            ros::ServiceServer server_feature_path = nh.advertiseService("/human_feature_detect/imagepath_feature", &FEATURE_SERVER::human_feature_callback_from_path, this);
            ros::spin();
        }
        bool human_feature_callback_from_image(human_feature_detect::ImageToFeature::Request &req, human_feature_detect::ImageToFeature::Response &res)
        {
            res.detect_flag = false;
            res.feature.sex = "";
            res.feature.age_lower = 0;
            res.feature.age_uper = 0;
            res.feature.boundingbox.xmin = 0;
            res.feature.boundingbox.xmax = 0;
            res.feature.boundingbox.ymin = 0;
            res.feature.boundingbox.ymax = 0;


            cv_bridge::CvImagePtr cv_ptr;
            try
            {
                cv_ptr = cv_bridge::toCvCopy(req.image, sensor_msgs::image_encodings::BGR8);
            }
            catch (cv_bridge::Exception& e)
            {
                ROS_ERROR("cv_bridge exception: %s", e.what());
                return true;
            }
            cv::Mat image = cv_ptr->image;
            if (image.empty())
            {
                ROS_ERROR("NO IMAGE");
                return true;
            }

            cv::Mat gray;
            cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);




            cv::Rect rect;
            rect.x = req.boundingbox.xmin;
            rect.y = req.boundingbox.ymin;
            rect.width = req.boundingbox.xmax - req.boundingbox.xmin;
            rect.height = req.boundingbox.ymax - req.boundingbox.ymin;
            cv::rectangle(image, rect, cv::Scalar(0, 255, 0), 2);
            // 切り出す範囲を指定
            cv::Rect roi(req.boundingbox.xmin, req.boundingbox.ymin, req.boundingbox.xmax - req.boundingbox.xmin, req.boundingbox.ymax - req.boundingbox.ymin);

            // 指定した範囲で切り出す
            cv::Mat cut_pic = image(roi);

            // 入力画像を指定したサイズにリサイズ
            cv::Mat resiz_face;
            cv::resize(cut_pic, resiz_face, cv::Size(227, 227));



            std::vector<cv::Rect> results;
            cascade.detectMultiScale(cut_pic, results, 1.1, 5, 0, cv::Size(20,20));

            if (results.size()!=1)
            {
                ROS_ERROR("NO COMPLETE");
                return true;
            }


            // 入力画像をBLOB形式に変換
            cv::Scalar mean_values(MODEL_MEAN_VALUES[0], MODEL_MEAN_VALUES[1], MODEL_MEAN_VALUES[2]);
            cv::Mat blob = cv::dnn::blobFromImage(resiz_face, 1.0, cv::Size(227, 227), mean_values, false, false);
            
            // ブロブデータをネットワークに入力
            age_net.setInput(blob);
            sex_net.setInput(blob);

            // ネットワークの順伝播を実行し、予測結果を取得
            cv::Mat age_preds = age_net.forward();
            cv::Mat sex_preds = sex_net.forward();

            // 予測結果の最大値となるindexを取得
            cv::Point max_loc_age, max_loc_sex;
            cv::minMaxLoc(age_preds, nullptr, nullptr, nullptr, &max_loc_age);
            cv::minMaxLoc(sex_preds, nullptr, nullptr, nullptr, &max_loc_sex);
            int age_index, sex_index;
            age_index = max_loc_age.x;
            sex_index = max_loc_sex.x;

            // 推論結果を出力
            std::cout << "age = " << age_list[age_index][0] << " ~ " << age_list[age_index][1] << ", sex = " << sex_list[sex_index] << std::endl;
            // std::cout << "Detection result: x = " << rect.x << ", y = " << rect.y << ", width = " << rect.width << ", height = " << rect.height << std::endl;



            res.detect_flag = true;
            res.feature.sex = sex_list[sex_index];
            res.feature.age_lower = age_list[age_index][0];
            res.feature.age_uper = age_list[age_index][1];
            res.feature.boundingbox.xmin = req.boundingbox.xmin;
            res.feature.boundingbox.xmax = req.boundingbox.xmax;
            res.feature.boundingbox.ymin = req.boundingbox.ymin;
            res.feature.boundingbox.ymax = req.boundingbox.ymax;



            return true;
        }
        bool human_feature_callback_from_path(human_feature_detect::PathToFeature::Request &req, human_feature_detect::PathToFeature::Response &res)
        {
            res.detect_flag = false;
            res.feature.sex = "";
            res.feature.age_lower = 0;
            res.feature.age_uper = 0;
            res.feature.boundingbox.xmin = 0;
            res.feature.boundingbox.xmax = 0;
            res.feature.boundingbox.ymin = 0;
            res.feature.boundingbox.ymax = 0;
            
            cv::Mat image = cv::imread(req.path);
            if (image.empty())
            {
                ROS_ERROR("NO IMAGE");
                return true;
            }

            cv::Mat gray;
            cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);




            cv::Rect rect;
            rect.x = req.boundingbox.xmin;
            rect.y = req.boundingbox.ymin;
            rect.width = req.boundingbox.xmax - req.boundingbox.xmin;
            rect.height = req.boundingbox.ymax - req.boundingbox.ymin;
            cv::rectangle(image, rect, cv::Scalar(0, 255, 0), 2);
            // 切り出す範囲を指定
            cv::Rect roi(req.boundingbox.xmin, req.boundingbox.ymin, req.boundingbox.xmax - req.boundingbox.xmin, req.boundingbox.ymax - req.boundingbox.ymin);

            // 指定した範囲で切り出す
            cv::Mat cut_pic = image(roi);

            // 入力画像を指定したサイズにリサイズ
            cv::Mat resiz_face;
            cv::resize(cut_pic, resiz_face, cv::Size(227, 227));



            std::vector<cv::Rect> results;
            cascade.detectMultiScale(cut_pic, results, 1.1, 5, 0, cv::Size(20,20));

            if (results.size()!=1)
            {
                ROS_ERROR("NO COMPLETE");
                return true;
            }


            // 入力画像をBLOB形式に変換
            cv::Scalar mean_values(MODEL_MEAN_VALUES[0], MODEL_MEAN_VALUES[1], MODEL_MEAN_VALUES[2]);
            cv::Mat blob = cv::dnn::blobFromImage(resiz_face, 1.0, cv::Size(227, 227), mean_values, false, false);
            
            // ブロブデータをネットワークに入力
            age_net.setInput(blob);
            sex_net.setInput(blob);

            // ネットワークの順伝播を実行し、予測結果を取得
            cv::Mat age_preds = age_net.forward();
            cv::Mat sex_preds = sex_net.forward();

            // 予測結果の最大値となるindexを取得
            cv::Point max_loc_age, max_loc_sex;
            cv::minMaxLoc(age_preds, nullptr, nullptr, nullptr, &max_loc_age);
            cv::minMaxLoc(sex_preds, nullptr, nullptr, nullptr, &max_loc_sex);
            int age_index, sex_index;
            age_index = max_loc_age.x;
            sex_index = max_loc_sex.x;

            // 推論結果を出力
            std::cout << "age = " << age_list[age_index][0] << " ~ " << age_list[age_index][1] << ", sex = " << sex_list[sex_index] << std::endl;
            // std::cout << "Detection result: x = " << rect.x << ", y = " << rect.y << ", width = " << rect.width << ", height = " << rect.height << std::endl;



            res.detect_flag = true;
            res.feature.sex = sex_list[sex_index];
            res.feature.age_lower = age_list[age_index][0];
            res.feature.age_uper = age_list[age_index][1];
            res.feature.boundingbox.xmin = req.boundingbox.xmin;
            res.feature.boundingbox.xmax = req.boundingbox.xmax;
            res.feature.boundingbox.ymin = req.boundingbox.ymin;
            res.feature.boundingbox.ymax = req.boundingbox.ymax;



            return true;
        }
        bool human_features_callback_from_image(human_feature_detect::ImageToFeatures::Request &req, human_feature_detect::ImageToFeatures::Response &res)
        {
            res.detect_flag = false;
            res.detect_counter = 0;
            res.features.clear();
            cv_bridge::CvImagePtr cv_ptr;
            try
            {
                cv_ptr = cv_bridge::toCvCopy(req.image, sensor_msgs::image_encodings::BGR8);
            }
            catch (cv_bridge::Exception& e)
            {
                ROS_ERROR("cv_bridge exception: %s", e.what());
                return true;
            }
            cv::Mat image = cv_ptr->image;
            if (image.empty())
            {
                ROS_ERROR("NO IMAGE");
                return true;
            }

            cv::Mat gray;
            cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);
            std::vector<cv::Rect> results;
            cascade.detectMultiScale(image, results, 1.1, 5, 0, cv::Size(20,20));
            if (results.size() == 0)
            {
                ROS_ERROR("NO FACE");
                return true;
            }



            res.detect_counter = results.size();
            res.detect_flag = true;
            human_feature_detect::Feature feature;
            for (const cv::Rect& rect : results)
            {
                cv::rectangle(image, rect, cv::Scalar(0, 255, 0), 2);
                // 切り出す範囲を指定
                cv::Rect roi(rect.x, rect.y, rect.width, rect.height);

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

                // 予測結果の最大値となるindexを取得
                cv::Point max_loc_age, max_loc_sex;
                cv::minMaxLoc(age_preds, nullptr, nullptr, nullptr, &max_loc_age);
                cv::minMaxLoc(sex_preds, nullptr, nullptr, nullptr, &max_loc_sex);
                int age_index, sex_index;
                age_index = max_loc_age.x;
                sex_index = max_loc_sex.x;

                // 推論結果を出力
                std::cout << "age = " << age_list[age_index][0] << " ~ " << age_list[age_index][1] << ", sex = " << sex_list[sex_index] << std::endl;
                // std::cout << "Detection result: x = " << rect.x << ", y = " << rect.y << ", width = " << rect.width << ", height = " << rect.height << std::endl;
                
                // 推論結果の返還用に代入
                feature.sex = sex_list[sex_index];
                feature.age_lower = age_list[age_index][0];
                feature.age_uper = age_list[age_index][1];
                feature.boundingbox.xmin = rect.x;
                feature.boundingbox.xmax = rect.x + rect.width;
                feature.boundingbox.ymin = rect.y;
                feature.boundingbox.ymax = rect.y + rect.height;
                res.features.push_back(feature);
            }


            return true;
        }
        bool human_features_callback_from_path(human_feature_detect::PathToFeatures::Request &req, human_feature_detect::PathToFeatures::Response &res)
        {
            res.detect_flag = false;
            res.detect_counter = 0;
            res.features.clear();

            cv::Mat image = cv::imread(req.path);
            if (image.empty())
            {
                ROS_ERROR("NO IMAGE");
                return true;
            }

            cv::Mat gray;
            cv::cvtColor(image, gray, cv::COLOR_BGR2GRAY);
            std::vector<cv::Rect> results;
            cascade.detectMultiScale(image, results, 1.1, 5, 0, cv::Size(20,20));
            if (results.size() == 0)
            {
                ROS_ERROR("NO FACE");
                return true;
            }

            res.detect_counter = results.size();
            res.detect_flag = true;
            human_feature_detect::Feature feature;
            for (const cv::Rect& rect : results)
            {
                cv::rectangle(image, rect, cv::Scalar(0, 255, 0), 2);
                // 切り出す範囲を指定
                cv::Rect roi(rect.x, rect.y, rect.width, rect.height);

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

                // 予測結果の最大値となるindexを取得
                cv::Point max_loc_age, max_loc_sex;
                cv::minMaxLoc(age_preds, nullptr, nullptr, nullptr, &max_loc_age);
                cv::minMaxLoc(sex_preds, nullptr, nullptr, nullptr, &max_loc_sex);
                int age_index, sex_index;
                age_index = max_loc_age.x;
                sex_index = max_loc_sex.x;

                // 推論結果を出力
                std::cout << "age = " << age_list[age_index][0] << " ~ " << age_list[age_index][1] << ", sex = " << sex_list[sex_index] << std::endl;
                // std::cout << "Detection result: x = " << rect.x << ", y = " << rect.y << ", width = " << rect.width << ", height = " << rect.height << std::endl;
                
                // 推論結果の返還用に代入
                feature.sex = sex_list[sex_index];
                feature.age_lower = age_list[age_index][0];
                feature.age_uper = age_list[age_index][1];
                feature.boundingbox.xmin = rect.x;
                feature.boundingbox.xmax = rect.x + rect.width;
                feature.boundingbox.ymin = rect.y;
                feature.boundingbox.ymax = rect.y + rect.height;
                res.features.push_back(feature);
            }


            return true;
        }
};


int main(int argc, char **argv)
{
    ros::init(argc, argv, "human_feature_detect");
    FEATURE_SERVER feature_server;
    return 0;
}