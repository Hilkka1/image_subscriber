#!/bin/bash
exec > /home/rlab/testingStarting.log 2>&1
export HOME=/home/rlab/ros_logs
export ROS_LOG_DIR=/home/rlab/ros_logs
sudo loadkeys fi
cd /home/rlab/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run image_subscriber subscriber #Here put the appropriate subscriber node number
