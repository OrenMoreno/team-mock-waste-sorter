cmake_minimum_required(VERSION 3.0.2)
project(vision_node)

find_package(catkin REQUIRED COMPONENTS
  message_generation
  std_msgs
  sensor_msgs
)

add_message_files(
  FILES
  DetectionResult.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS message_runtime std_msgs sensor_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

install(PROGRAMS
  scripts/vision_node.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)