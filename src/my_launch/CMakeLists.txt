cmake_minimum_required(VERSION 2.8.3)
project(my_launch)

find_package(catkin REQUIRED COMPONENTS
  gazebo_ros
  my_maze_world
  robot_state_publisher
  turtlebot3_description
  xacro
)

catkin_package(CATKIN_DEPENDS
  gazebo_ros
  my_maze_world
  robot_state_publisher
  turtlebot3_description
  xacro
)

# Install launch files
file(GLOB_RECURSE LAUNCH_FILES "*.launch")
install(FILES ${LAUNCH_FILES} DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch)
