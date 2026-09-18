cmake_minimum_required(VERSION 2.8.3)
project(my_maze_world)

find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  gazebo_msgs
  geometry_msgs
  image_transport
  rospy
  sensor_msgs
  std_msgs
)

catkin_package(CATKIN_DEPENDS
  cv_bridge
  gazebo_msgs
  geometry_msgs
  image_transport
  rospy
  sensor_msgs
  std_msgs
)

# Install executable Python nodes
install(PROGRAMS
  scripts/compare_planners.py
  scripts/dynamic_obstacles.py
  scripts/green_goal_detector.py
  scripts/person_walking.py
  scripts/walking_person.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

# Install Gazebo worlds and custom models
install(DIRECTORY
  models/
  worlds/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
