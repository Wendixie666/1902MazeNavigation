cmake_minimum_required(VERSION 2.8.3)
project(my_launch)

find_package(catkin REQUIRED)

catkin_package()

# Install launch files
file(GLOB_RECURSE LAUNCH_FILES "*.launch")
install(FILES ${LAUNCH_FILES} DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch)
install(FILES turtlebot3_empty_world.launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

install(DIRECTORY
  config
  launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
