#!/usr/bin/env python

"""
    info.py - Version 0.1 2014-01-14

"""

import os

from mbot_control.srv import *
import rospy, sys
import moveit_commander
from std_msgs.msg import Header
from moveit_msgs.msg import RobotTrajectory, RobotState
from moveit_msgs.srv import GetPositionFK
from trajectory_msgs.msg import JointTrajectoryPoint

import time
from ur_driver.io_interface import *
from copy import deepcopy
from geometry_msgs.msg import PoseStamped, Pose
from geometry_msgs.msg import Twist


from tf.transformations import euler_from_quaternion, quaternion_from_euler
import rospkg



#const of this node default name
Node_Name = "info"
#const of config package name
Config_Pkg_Name = "mbot_config"
#const of teach file name
Teach_File_Name = "teach_mode.json"

class info_class:
    def __init__(self):
        # Initialize the move_group API
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node(Node_Name)


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

        s = rospy.Service('ui_server', UI_Server, self.handle_ui_server)



        #init ros package
        rospack = rospkg.RosPack()

        # Config_Pkg_Name's "PATH" + Teach_File_Name
        self.teach_file_path = rospack.get_path(Config_Pkg_Name) + "/" +  Teach_File_Name

        print "teach_file_path= " + self.teach_file_path

        '''
        rospy.wait_for_service('compute_fk')
        try:
            self.moveit_fk = rospy.ServiceProxy('compute_fk', GetPositionFK)
        except rospy.ServiceException, e:
            rospy.logerror("Service call failed: %s"%e)
        '''

    def get_tool_position(self,joint_positions):
        robot = moveit_commander.RobotCommander()
        #l_names = robot.get_link_names()
        #rospy.loginfo(["l_names:", l_names])

        header = Header(0,rospy.Time.now(),"/world")
        #fkln = l_names
        fkln = ['tool0']
        rs = RobotState()
        rs.joint_state.name = self.ur_arm.get_active_joints()
        rs.joint_state.position = joint_positions

        res = self.moveit_fk(header, fkln, rs)
        #rospy.loginfo(["FK LOOKUP:", self.moveit_fk(header, fkln, rs)])
        #rospy.loginfo(["fk pose= ", +res.pose_stamped[0].pose.position])

        return res.pose_stamped[0].pose.position


    def teach_get_pre_linear(self,req):
        if  req.float_ary != None and len(req.float_ary)==6:
            f_ary = req.float_ary
            #print 'f_ary[0] = '+ str(f_ary[0]) + 'f_ary[1] = '+str(f_ary[1])
            p = self.get_tool_position(f_ary)
            print 'pre x='+ str(p.x)+', y='+str(p.y)+', z='+str(p.z)

            return p

        elif req.pose !=None:
            print "pre_pose_z = "+ str(req.pose.linear.z)
            return req.pose.linear

    def handle_ui_server(self,req):
        cmd = req.cmd
        rospy.loginfo('Request cmd('+cmd+')')

        now_pose = self.get_eef_pos()
        res = UI_ServerResponse()

        if  cmd=="Teach:EEF_Pose":
            res.pose = now_pose
        elif cmd=="Teach:Shift_X":
            res.f = now_pose.linear.x - self.teach_get_pre_linear(req).x

        elif cmd=="Teach:Shift_Y":
            res.f = now_pose.linear.y - self.teach_get_pre_linear(req).y

        elif cmd=="Teach:Shift_Z":
            res.f = now_pose.linear.z - self.teach_get_pre_linear(req).z
        elif cmd=="Teach:SaveFile":

            f = open(self.teach_file_path, 'w')
            f.write(req.req_s)
            f.close()


        elif cmd=="Teach:ReadFile":
            f = open(self.teach_file_path, 'r')
            read_data = f.read()
            res.res_s = read_data
            f.close()


        res.result = "UI_Server Success (Process " + cmd + ")"
        return res


    def get_eef_pos(self):
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

        return twist


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
    print "--------Info Server Ready--------"
    info.pub_eef_pos()

    rospy.spin()

    info.end()


    
    
