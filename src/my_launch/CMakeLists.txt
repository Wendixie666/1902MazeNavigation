cmake_minimum_required(VERSION 2.8.3)
project(my_launch)

find_package(catkin REQUIRED)

catkin_package()

# Install launch files
install(FILES turtlebot3_empty_world.launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

install(DIRECTORY
  config
  launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
