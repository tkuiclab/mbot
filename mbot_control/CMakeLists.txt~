cmake_minimum_required(VERSION 2.8.3)
project(mbot_control)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  actionlib
  actionlib_msgs
  message_generation
  roscpp
  rospy
  std_msgs
  geometry_msgs
)

## System dependencies are found with CMake's conventions
find_package(Boost REQUIRED COMPONENTS system)

################################################
## Declare ROS messages, services and actions ##
################################################

## Generate messages in the 'msg' folder
add_message_files(
   FILES
   TeachCommand.msg
   WebChat.msg
 )

## Generate services in the 'srv' folder
add_service_files(
  FILES
  UI_Server.srv
)

## Generate actions in the 'action' folder
add_action_files(
  DIRECTORY action
  FILES TeachCommandList.action
)

## Generate added messages and services with any dependencies listed here
generate_messages(
   DEPENDENCIES
   actionlib_msgs
   std_msgs
   geometry_msgs
   
)

###################################
## catkin specific configuration ##
###################################
## The catkin_package macro generates cmake config files for your package
## Declare things to be passed to dependent projects
## INCLUDE_DIRS: uncomment this if you package contains header files
## LIBRARIES: libraries you create in this project that dependent projects also need
## CATKIN_DEPENDS: catkin_packages dependent projects also need
## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
  CATKIN_DEPENDS actionlib_msgs geometry_msgs
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
# include_directories(include)
include_directories(
  ${catkin_INCLUDE_DIRS}
)




##############################################################################
# Subprojects
##############################################################################

foreach(subdir
    base
    )
  #install(DIRECTORY ${subdir} DESTINATION ${CMAKE_INSTALL_PREFIX}/share/qt_tutorials)
  add_subdirectory(${subdir})
endforeach()
