cmake_minimum_required(VERSION 2.8.3)
project(bag_tools)

find_package(catkin REQUIRED COMPONENTS rospy rosbag sensor_msgs cv_bridge message_filters)
find_package(Boost REQUIRED COMPONENTS signals thread)
find_package(OpenCV REQUIRED)
find_package(console_bridge REQUIRED)

catkin_package(
  INCLUDE_DIRS include
  CATKIN_DEPENDS rosbag
)



install(PROGRAMS
    scripts/add_header_time_offset.py
    scripts/bag_add_time_offset.py
    scripts/batch_process.py

    scripts/change_frame_id.py
    scripts/change_topics.py
    scripts/check_delay.py
    scripts/check_drop.py
    scripts/cut.py
    scripts/extract_topics.py
    scripts/gps_to_std_gt.py

    scripts/make_video.py
    scripts/merge.py
    scripts/plot.py
    scripts/remove_tf.py
    scripts/replace_msg_time_with_hdr.py
  
    scripts/transform_tf.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
  PATTERN ".svn" EXCLUDE)