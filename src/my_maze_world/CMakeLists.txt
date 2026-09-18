cmake_minimum_required(VERSION 2.8.3)
project(my_maze_world)

find_package(catkin REQUIRED COMPONENTS
  gazebo_msgs
  geometry_msgs
  rospy
)

catkin_package(CATKIN_DEPENDS
  gazebo_msgs
  geometry_msgs
  rospy
)

# Install executable Python nodes
install(PROGRAMS
  scripts/dynamic_obstacles.py
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
