#!/usr/bin/env python

"""
    moveit_ik_demo.py - Version 0.1 2014-01-14
    
    Use inverse kinemtatics to move the end effector to a specified pose
    
    Created for the Pi Robot Project: http://www.pirobot.org
    Copyright (c) 2014 Patrick Goebel.  All rights reserved.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.5
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details at:
    
    http://www.gnu.org/licenses/gpl.html
"""

import rospy, sys
import moveit_commander
from moveit_msgs.msg import RobotTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

import time
from ur_driver.io_interface import *
from copy import deepcopy
from geometry_msgs.msg import PoseStamped, Pose
from geometry_msgs.msg import Twist

from tf.transformations import euler_from_quaternion, quaternion_from_euler

class info_class:
    def __init__(self):
        # Initialize the move_group API
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('info')


        # Initialize the move group for the right arm
        self.ur_arm = moveit_commander.MoveGroupCommander('manipulator')

        # Get the name of the end-effector link
        self.end_effector_link = self.ur_arm.get_end_effector_link()

        # Set the reference frame for pose targets
        reference_frame = 'world'

        # Set the right arm reference frame accordingly
        self.ur_arm.set_pose_reference_frame(reference_frame)

        # Allow replanning to increase the odds of a solution
        self.ur_arm.allow_replanning(True)

    def pub_eef_pos(self):
        # Show pose
        pub = rospy.Publisher('/eef_states', Twist, queue_size=10)
        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            now_pose = self.ur_arm.get_current_pose(self.end_effector_link).pose
            show_str = "TCP_pose = (" + str(now_pose.position.x) + "," + str(now_pose.position.y) + "," + str(
            now_pose.position.z) + ")"
            #rospy.loginfo(show_str)
            twist = Twist()
            twist.linear.x = now_pose.position.x
            twist.linear.y = now_pose.position.y
            twist.linear.z = now_pose.position.z
            quaternion = (
                now_pose.orientation.x,
                now_pose.orientation.y,
                now_pose.orientation.z,
                now_pose.orientation.w)
            euler = euler_from_quaternion(quaternion)
            twist.angular.x = euler[0]
            twist.angular.y = euler[1]
            twist.angular.z = euler[2]
            pub.publish(twist)

            # joints = ur_arm.get_current_joint_values()
            # show_str = "joint_position = (" + str(joints[0])+ ","+ str(joints[1]) + "," + str(joints[2]) + "," + str(joints[3]) + ","+ str(joints[4]) + "," + str(joints[5]) +")"
            # rospy.loginfo(show_str)

    def end(self):
	    # Shut down MoveIt cleanly
        moveit_commander.roscpp_shutdown()

        # Exit MoveIt
        moveit_commander.os._exit(0)

if __name__ == "__main__":
    info = info_class()
    info.pub_eef_pos()
    info.end()


    
    
