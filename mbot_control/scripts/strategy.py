"""
File: strategy.py
Author: Chien-Ming Lin <jianming1481@gmail.com>
Created on:       2016/02/18 --------------------> Creating file & read json file
Modified on:      2016/02/21 --------------------> Adding Action Server for UIFO & Action Client for Vision
                  2016/02/22 --------------------> Adding mbot_control server
                  2016/02/25 --------------------> Adding move2standby function & Modify ur5_control.py for rotate TCP
                  2016/03/01 --------------------> Change the name of action file "UIFO" -> "UI_Info"
                  2016/03/02 --------------------> Finish first version of Pick Task
                  2016/03/03 --------------------> Modify first version of Pick Task
                  2016/03/06 --------------------> Adding Stow Task

Description: Strategy for Amazon Picking Challenge 2016
    Action_Server: UI_INFO
    Action_Client: Vision, Mbot_control
"""

#!/usr/bin/env python
# license removed for brevity
import rospy
import roslib
import actionlib
import mbot_control.msg
import vision.msg
import json
from geometry_msgs.msg import Twist
import time

from std_msgs.msg import String

json_data = []
pick_num = 0
middle = None
right = None
left = None

class strategy_class(object):
    _feedback = mbot_control.msg.UI_InfoFeedback()
    _result = mbot_control.msg.UI_InfoResult()

    ################################################## Class Initialize ##################################################
    def __init__(self,node_name,file_name):
        with open(file_name) as data_file:
            self.data = json.load(data_file)
            data_file.close()

        self.uifo_action_name = "%s_ui_info" % node_name
        self._as = actionlib.SimpleActionServer(self.uifo_action_name,mbot_control.msg.UI_InfoAction,execute_cb=self.ui_info_cb,auto_start=False)

        self._as.start()

    ##################################################### move 2 standby ####################################################
    def move2standby(self,bin_ID):
        rospy.loginfo("Moving to standby position...")
        TeachCMD_list = mbot_control.msg.TeachCommandListGoal()
        cmd = mbot_control.msg.TeachCommand()
        TeachCMD_list.cmd_list = []

        if bin_ID < 6.5:
            updown = True
            rospy.loginfo("Moving to up level...")
        else:
            updown = False
            rospy.loginfo("Moving to down level...")

        if updown:
            cmd.cmd = 'Joint'
            cmd.joint_position = [1.004, -2.16, 2.36,-3.34, -1.0039, 0]
            cmd.pose.linear.x = 0.0
            cmd.pose.linear.y = 0.0
            cmd.pose.linear.z = 0.0
            cmd.pose.angular.x = 0.0
            cmd.pose.angular.y = 0.0
            cmd.pose.angular.z = 0.0
            TeachCMD_list.cmd_list.append(cmd)
        else:
            cmd.cmd = 'Joint'
            cmd.joint_position = [1.133, -1.863, 2.365, -0.517, 1.104, -3.13]
            cmd.pose.linear.x = 0.0
            cmd.pose.linear.y = 0.0
            cmd.pose.linear.z = 0.0
            cmd.pose.angular.x = 0.0
            cmd.pose.angular.y = 0.0
            cmd.pose.angular.z = 0.0
            TeachCMD_list.cmd_list.append(cmd)

        cmd = mbot_control.msg.TeachCommand()

        if bin_ID==1 or bin_ID==2 or bin_ID==3:
            cmd.cmd = 'Shift_Z'
            cmd.joint_position = []
            cmd.pose.linear.x = 0.0
            cmd.pose.linear.y = 0.0
            cmd.pose.linear.z = 0.26
            cmd.pose.angular.x = 0.0
            cmd.pose.angular.y = 0.0
            cmd.pose.angular.z = 0.0
            rospy.loginfo("Bin_%s in position!", bin_ID)
        elif bin_ID==4 or bin_ID==5 or bin_ID==6:
            rospy.loginfo("Bin_%s in position!", bin_ID)
        elif bin_ID==7 or bin_ID==8 or bin_ID==9:
            rospy.loginfo("Bin_%s in position!", bin_ID)
        elif bin_ID==10 or bin_ID==11 or bin_ID==12:
            cmd.cmd = 'Shift_Z'
            cmd.joint_position = []
            cmd.pose.linear.x = 0.0
            cmd.pose.linear.y = 0.0
            cmd.pose.linear.z = -0.26
            cmd.pose.angular.x = 0.0
            cmd.pose.angular.y = 0.0
            cmd.pose.angular.z = 0.0
            rospy.loginfo("Bin_%s in position!",bin_ID)
        else:
            rospy.loginfo("Bin_ID error in move2standby!")
        TeachCMD_list.cmd_list.append(cmd)

        return TeachCMD_list

    ################################################### Control base ##################################################
    def ControlBase(self,cmd_vel):
        rospy.loginfo("Controlling base...")
        TeachCMD_list = mbot_control.msg.TeachCommandListGoal()
        cmd = mbot_control.msg.TeachCommand()
        TeachCMD_list.cmd_list = []

        cmd.cmd = 'Base_Vel'
        cmd.joint_position = []
        cmd.pose.linear.x = cmd_vel.linear.x
        cmd.pose.linear.y = cmd_vel.linear.y
        cmd.pose.linear.z = cmd_vel.linear.z
        cmd.pose.angular.x = cmd_vel.angular.x
        cmd.pose.angular.y = cmd_vel.angular.y
        cmd.pose.angular.z = cmd_vel.angular.z

        TeachCMD_list.cmd_list.append(cmd)
        return TeachCMD_list
    ################################################### move 2 watch_pose ##################################################
    def move2watch(self):
        rospy.loginfo("Moving to watch position...")
        TeachCMD_list = mbot_control.msg.TeachCommandListGoal()
        cmd = mbot_control.msg.TeachCommand()
        TeachCMD_list.cmd_list = []

        cmd.cmd = 'Shift_RX'
        cmd.joint_position = []
        cmd.pose.linear.x = 0
        cmd.pose.linear.y = 0
        cmd.pose.linear.z = 0
        cmd.pose.angular.x = 0.262
        cmd.pose.angular.y = 0
        cmd.pose.angular.z = 0

        TeachCMD_list.cmd_list.append(cmd)
        return TeachCMD_list
    ################################################### ready 2 pick ##################################################
    def ready2pick(self):
        rospy.loginfo("Read to Pick...")
        TeachCMD_list = mbot_control.msg.TeachCommandListGoal()
        cmd = mbot_control.msg.TeachCommand()
        TeachCMD_list.cmd_list = []

        cmd.cmd = 'Shift_RX'
        cmd.joint_position = []
        cmd.pose.linear.x = 0
        cmd.pose.linear.y = 0
        cmd.pose.linear.z = 0
        cmd.pose.angular.x = -0.262
        cmd.pose.angular.y = 0
        cmd.pose.angular.z = 0

        TeachCMD_list.cmd_list.append(cmd)
        return TeachCMD_list
    ##################################################### Picking ####################################################
    def picking(self,obj):
        rospy.loginfo("Picking...")
        TeachCMD_list = mbot_control.msg.TeachCommandListGoal()
        i_cmd_x = mbot_control.msg.TeachCommand()
        i_cmd_y = mbot_control.msg.TeachCommand()
        i_cmd_z = mbot_control.msg.TeachCommand()
        o_cmd_x = mbot_control.msg.TeachCommand()
        o_cmd_y = mbot_control.msg.TeachCommand()
        o_cmd_z = mbot_control.msg.TeachCommand()
        vaccum_cmd = mbot_control.msg.TeachCommand()
        TeachCMD_list.cmd_list = []

        i_cmd_x.cmd = 'Shift_X'
        i_cmd_x.joint_position = []
        i_cmd_x.pose.linear.x = -obj.objPose.linear.x
        i_cmd_x.pose.linear.y = 0
        i_cmd_x.pose.linear.z = 0
        i_cmd_x.pose.angular.x = 0
        i_cmd_x.pose.angular.y = 0
        i_cmd_x.pose.angular.z = 0

        i_cmd_y.cmd = 'Shift_Y'
        i_cmd_y.joint_position = []
        i_cmd_y.pose.linear.x = 0
        i_cmd_y.pose.linear.y = -obj.objPose.linear.y
        i_cmd_y.pose.linear.z = 0
        i_cmd_y.pose.angular.x = 0
        i_cmd_y.pose.angular.y = 0
        i_cmd_y.pose.angular.z = 0

        i_cmd_z.cmd = 'Shift_Z'
        i_cmd_z.joint_position = []
        i_cmd_z.pose.linear.x = 0
        i_cmd_z.pose.linear.y = 0
        i_cmd_z.pose.linear.z = obj.objPose.linear.z
        i_cmd_z.pose.angular.x = 0
        i_cmd_z.pose.angular.y = 0
        i_cmd_z.pose.angular.z = 0

        vaccum_cmd.cmd = 'Vaccum'
        vaccum_cmd.vaccum = True

        o_cmd_z.cmd = 'Shift_Z'
        o_cmd_z.joint_position=[]
        o_cmd_z.pose.linear.x = 0
        o_cmd_z.pose.linear.y = 0
        o_cmd_z.pose.linear.z = -obj.objPose.linear.z
        o_cmd_z.pose.angular.x = 0
        o_cmd_z.pose.angular.y = 0
        o_cmd_z.pose.angular.z = 0

        o_cmd_y.cmd = 'Shift_Y'
        o_cmd_y.joint_position=[]
        o_cmd_y.pose.linear.x = 0
        o_cmd_y.pose.linear.y = obj.objPose.linear.y
        o_cmd_y.pose.linear.z = 0
        o_cmd_y.pose.angular.x = 0
        o_cmd_y.pose.angular.y = 0
        o_cmd_y.pose.angular.z = 0

        o_cmd_x.cmd = 'Shift_X'
        o_cmd_x.joint_position=[]
        o_cmd_x.pose.linear.x = obj.objPose.linear.x
        o_cmd_x.pose.linear.y = 0
        o_cmd_x.pose.linear.z = 0
        o_cmd_x.pose.angular.x = 0
        o_cmd_x.pose.angular.y = 0
        o_cmd_x.pose.angular.z = 0

        TeachCMD_list.cmd_list.append(i_cmd_x)
        TeachCMD_list.cmd_list.append(i_cmd_y)
        TeachCMD_list.cmd_list.append(i_cmd_z)
        TeachCMD_list.cmd_list.append(vaccum_cmd)
        TeachCMD_list.cmd_list.append(o_cmd_z)
        TeachCMD_list.cmd_list.append(o_cmd_y)
        TeachCMD_list.cmd_list.append(o_cmd_x)
        return TeachCMD_list
    ################################################### Pick 2 tote ##################################################
    def pick2tote(self):
        rospy.loginfo("Picking to stow")
        TeachCMD_list = mbot_control.msg.TeachCommandListGoal()
        cmd = mbot_control.msg.TeachCommand()
        cmd_shift_x = mbot_control.msg.TeachCommand()
        cmd_shift_z = mbot_control.msg.TeachCommand()
        cmd_vaccum = mbot_control.msg.TeachCommand()
        TeachCMD_list.cmd_list = []
        global pick_num
        pick_num = pick_num + 1

        cmd.cmd = 'Joint'
        cmd.joint_position = [-1.779, -2.065, 2.089, -3.194, -1.365, 0.007]
        cmd.pose.linear.x = 0.0
        cmd.pose.linear.y = 0.0
        cmd.pose.linear.z = 0.0
        cmd.pose.angular.x = 0.0
        cmd.pose.angular.y = 0.0
        cmd.pose.angular.z = 0.0

        if pick_num%4==1:
            cmd_shift_x.cmd = 'Shift_X'
            cmd_shift_x.joint_position = []
            cmd_shift_x.pose.linear.x = -0.125
            cmd_shift_x.pose.linear.y = 0.0
            cmd_shift_x.pose.linear.z = 0.0
            cmd_shift_x.pose.angular.x = 0.0
            cmd_shift_x.pose.angular.y = 0.0
            cmd_shift_x.pose.angular.z = 0.0

            cmd_shift_z.cmd = 'Shift_Z'
            cmd_shift_z.joint_position = []
            cmd_shift_z.pose.linear.x = 0.0
            cmd_shift_z.pose.linear.y = 0.0
            cmd_shift_z.pose.linear.z = -0.25
            cmd_shift_z.pose.angular.x = 0.0
            cmd_shift_z.pose.angular.y = 0.0
            cmd_shift_z.pose.angular.z = 0.0

            cmd_vaccum.cmd = 'Vaccum'
            cmd_vaccum.vaccum = True
        elif pick_num%4==2:
            cmd_shift_z.cmd = 'Shift_Z'
            cmd_shift_z.joint_position = []
            cmd_shift_z.pose.linear.x = 0.0
            cmd_shift_z.pose.linear.y = 0.0
            cmd_shift_z.pose.linear.z = -0.25
            cmd_shift_z.pose.angular.x = 0.0
            cmd_shift_z.pose.angular.y = 0.0
            cmd_shift_z.pose.angular.z = 0.0

            cmd_vaccum.cmd = 'Vaccum'
            cmd_vaccum.vaccum = True
        elif pick_num%4==3:
            cmd_shift_x.cmd = 'Shift_X'
            cmd_shift_x.joint_position = []
            cmd_shift_x.pose.linear.x = 0.125
            cmd_shift_x.pose.linear.y = 0.0
            cmd_shift_x.pose.linear.z = 0.0
            cmd_shift_x.pose.angular.x = 0.0
            cmd_shift_x.pose.angular.y = 0.0
            cmd_shift_x.pose.angular.z = 0.0

            cmd_shift_z.cmd = 'Shift_Z'
            cmd_shift_z.joint_position = []
            cmd_shift_z.pose.linear.x = 0.0
            cmd_shift_z.pose.linear.y = 0.0
            cmd_shift_z.pose.linear.z = -0.25
            cmd_shift_z.pose.angular.x = 0.0
            cmd_shift_z.pose.angular.y = 0.0
            cmd_shift_z.pose.angular.z = 0.0

            cmd_vaccum.cmd = 'Vaccum'
            cmd_vaccum.vaccum = True
        elif pick_num%4==0:
            cmd_shift_x.cmd = 'Shift_X'
            cmd_shift_x.joint_position = []
            cmd_shift_x.pose.linear.x = 0.25
            cmd_shift_x.pose.linear.y = 0.0
            cmd_shift_x.pose.linear.z = 0.0
            cmd_shift_x.pose.angular.x = 0.0
            cmd_shift_x.pose.angular.y = 0.0
            cmd_shift_x.pose.angular.z = 0.0

            cmd_shift_z.cmd = 'Shift_Z'
            cmd_shift_z.joint_position = []
            cmd_shift_z.pose.linear.x = 0.0
            cmd_shift_z.pose.linear.y = 0.0
            cmd_shift_z.pose.linear.z = -0.25
            cmd_shift_z.pose.angular.x = 0.0
            cmd_shift_z.pose.angular.y = 0.0
            cmd_shift_z.pose.angular.z = 0.0

            cmd_vaccum.cmd = 'Vaccum'
            cmd_vaccum.vaccum = False
        else:
            rospy("Pick2Tote Error: Pick_Num Wrong!")
        if pick_num>12:
            pick_num=0

        TeachCMD_list.cmd_list.append(cmd)
        TeachCMD_list.cmd_list.append(cmd_shift_x)
        TeachCMD_list.cmd_list.append(cmd_shift_z)
        TeachCMD_list.cmd_list.append(cmd_vaccum)
        TeachCMD_list.cmd_list.append(cmd)
        return TeachCMD_list
    ##################################################### Pick Task ####################################################
    def Pick_task(self,bin_ID,bin_contents,goal_obj):
        rospy.loginfo("Executing Pick Task!")
        rospy.loginfo("Controlling mbot")
        client = actionlib.SimpleActionClient('mbot_control', mbot_control.msg.TeachCommandListAction)
        client.wait_for_server()
        cmd_vel = Twist()

        TeachCMD_list = mbot_control.msg.TeachCommandListGoal()
        TeachCMD_list.cmd_list = []

        ##------------------ Standby ------------------ ##
        global left,middle,right
        rospy.loginfo("LEFT=%d",left)
        rospy.loginfo("MIDDLE=%d",middle)
        rospy.loginfo("RIGHT=%d",right)
        if bin_ID==1 or bin_ID==4 or bin_ID==7 or bin_ID==10:
            if not left:
                if right:
                    rospy.loginfo("Controlling the Mbot move from RIGHT to section LEFT")
                    cmd_vel.linear.x = -50
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    time.sleep(9)
                    cmd_vel.linear.x = 0
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    left = True
                    right = middle = False
                elif middle:
                    rospy.loginfo("Controlling the Mbot move from MIDDLE to section LEFT")
                    cmd_vel.linear.x = -50
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    time.sleep(4.5)
                    cmd_vel.linear.x = 0
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    left = True
                    right = middle = False
            TeachCMD_list = self.move2standby(bin_ID)
            left = True
            right = middle = False

        elif bin_ID==2 or bin_ID==5 or bin_ID==8 or bin_ID==11:
            if not middle:
                if right:
                    rospy.loginfo("Controlling the Mbot move from right to section CENTER")
                    cmd_vel.linear.x = -50
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    time.sleep(4.5)
                    cmd_vel.linear.x = 0
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    left = True
                    right = middle = False
                elif left:
                    rospy.loginfo("Controlling the Mbot move from left to section CENTER")
                    cmd_vel.linear.x = 50
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    time.sleep(4.5)
                    cmd_vel.linear.x = 0
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    left = True
                    right = middle = False
            middle = True
            right = left = False
            TeachCMD_list = self.move2standby(bin_ID)
        elif bin_ID==3 or bin_ID==6 or bin_ID==9 or bin_ID==12:
            if not right:
                if middle:
                    rospy.loginfo("Controlling the Mbot move from CENTER to section RIGHT")
                    cmd_vel.linear.x = 50
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    time.sleep(4.5)
                    cmd_vel.linear.x = 0
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    left = True
                    right = middle = False
                elif left:
                    rospy.loginfo("Controlling the Mbot move from LEFT to section RIGHT")
                    cmd_vel.linear.x = 50
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    time.sleep(9)
                    cmd_vel.linear.x = 0
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    left = True
                    right = middle = False

            right = True
            middle = left = False
            TeachCMD_list = self.move2standby(bin_ID)
        else:
            rospy.loginfo("BIN_ID ERROR!")

        goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()
        rospy.loginfo("Standby Result:%s"%result.notify)

        ##------------------ Watch inside bin ------------------ ##
        TeachCMD_list = self.move2watch()
        goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()
        rospy.loginfo("Watch inside bin Result:%s"%result.notify)

        switch = {
            1:self.vision_client,
            2:self.vision_client,
            3:self.vision_client,
            4:self.vision_client,
            5:self.vision_client,
            6:self.vision_client,
            7:self.vision_client,
            8:self.vision_client,
            9:self.vision_client,
            10:self.vision_client,
            11:self.vision_client,
            12:self.vision_client
        }
        obj = switch[bin_ID](bin_contents,goal_obj)

        ##------------------ Ready 2 Pick ------------------ ##
        TeachCMD_list = self.ready2pick()
        goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()
        rospy.loginfo("Ready 2 Pick Result:%s"%result.notify)

        ##------------------ Picking ------------------ ##
        TeachCMD_list = self.picking(obj)
        goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()
        rospy.loginfo("Picking Result:%s"%result.notify)

        ##------------------ Pick2Tote ------------------ ##
        TeachCMD_list = self.pick2tote()
        goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()
        rospy.loginfo("Pick 2 Stow Result:%s"%result.notify)

        rospy.loginfo("Grapping items in bin_%d" % bin_ID)
        obj=0
        return obj

    ##################################################### Move2Tote ####################################################
    def move2tote(self):
        rospy.loginfo("Moving to tote and watch")
        TeachCMD_list = mbot_control.msg.TeachCommandListGoal()
        cmd = mbot_control.msg.TeachCommand()
        TeachCMD_list.cmd_list = []

        cmd.cmd = 'Joint'
        cmd.joint_position = [-1.78, -1.506, 1.053,-1.12, -1.57, -0.21]
        cmd.pose.linear.x = 0
        cmd.pose.linear.y = 0
        cmd.pose.linear.z = 0
        cmd.pose.angular.x = 0
        cmd.pose.angular.y = 0
        cmd.pose.angular.z = 0

        TeachCMD_list.cmd_list.append(cmd)
        return TeachCMD_list
    ##################################################### Ready to Stow ####################################################
    def ready2stow(self):
        rospy.loginfo("Ready to Stow")
        TeachCMD_list = mbot_control.msg.TeachCommandListGoal()
        cmd = mbot_control.msg.TeachCommand()
        TeachCMD_list.cmd_list = []

        cmd.cmd = 'Joint'
        cmd.joint_position = [-1.309, -1.714, 1.3,-1.158, -1.57, 0.26]
        cmd.pose.linear.x = 0
        cmd.pose.linear.y = 0
        cmd.pose.linear.z = 0
        cmd.pose.angular.x = 0
        cmd.pose.angular.y = 0
        cmd.pose.angular.z = 0

        TeachCMD_list.cmd_list.append(cmd)
        return TeachCMD_list
    ##################################################### Ready to Stow ####################################################
    def ready2stow(self):
        rospy.loginfo("Ready to Stow")
        TeachCMD_list = mbot_control.msg.TeachCommandListGoal()
        cmd = mbot_control.msg.TeachCommand()
        TeachCMD_list.cmd_list = []

        cmd.cmd = 'Joint'
        #cmd.joint_position = [-1.309, -1.714, 1.3,-1.158, -1.57, 0.26]
        cmd.joint_position = [1.004, -2.16, 2.36,-3.34, -1.0039, 0]
        cmd.pose.linear.x = 0
        cmd.pose.linear.y = 0
        cmd.pose.linear.z = 0
        cmd.pose.angular.x = 0
        cmd.pose.angular.y = 0
        cmd.pose.angular.z = 0

        TeachCMD_list.cmd_list.append(cmd)
        return TeachCMD_list
    ##################################################### Place item into bin ####################################################
    def shift_z(self,dist):
        rospy.loginfo("Shift_Z")
        TeachCMD_list = mbot_control.msg.TeachCommandListGoal()
        TeachCMD_list.cmd_list = []
        cmd = mbot_control.msg.TeachCommand()

        cmd.cmd = 'Shift_Z'
        cmd.pose.linear.x = 0;
        cmd.pose.linear.y = 0;
        cmd.pose.linear.z = dist;
        cmd.pose.angular.x = 0;
        cmd.pose.angular.y = 0;
        cmd.pose.angular.z = 0;
        TeachCMD_list.cmd_list.append(cmd)

        return  TeachCMD_list

    def shit_y(self,dist):
        rospy.loginfo("Shift_Y")
        TeachCMD_list = mbot_control.msg.TeachCommandListGoal()
        TeachCMD_list.cmd_list = []
        cmd = mbot_control.msg.TeachCommand()

        cmd.cmd = 'Shift_Y'
        cmd.pose.linear.x = 0;
        cmd.pose.linear.y = dist;
        cmd.pose.linear.z = 0;
        cmd.pose.angular.x = 0;
        cmd.pose.angular.y = 0;
        cmd.pose.angular.z = 0;
        TeachCMD_list.cmd_list.append(cmd)
        return  TeachCMD_list

    def low_pose(self):
        TeachCMD_list = mbot_control.msg.TeachCommandListGoal()
        TeachCMD_list.cmd_list = []
        cmd = mbot_control.msg.TeachCommand()
        cmd.cmd = 'Joint'
        cmd.joint_position = [1.133, -1.863, 2.365, -0.517, 1.104, -3.13]
        cmd.pose.linear.x = 0.0
        cmd.pose.linear.y = 0.0
        cmd.pose.linear.z = 0.0
        cmd.pose.angular.x = 0.0
        cmd.pose.angular.y = 0.0
        cmd.pose.angular.z = 0.0
        TeachCMD_list.cmd_list.append(cmd)
        return  TeachCMD_list

    ##################################################### Stow Task ####################################################
    def Stow_task(self,tote_contents,work_order):
        rospy.loginfo("Executing Pick Task!")
        rospy.loginfo("Controlling mbot")
        client = actionlib.SimpleActionClient('mbot_control', mbot_control.msg.TeachCommandListAction)
        client.wait_for_server()
        cmd_vel = Twist()

        TeachCMD_list = mbot_control.msg.TeachCommandListGoal()
        TeachCMD_list.cmd_list = []
        cmd = mbot_control.msg.TeachCommand()

        ##------------------ Moving to tote and watch ------------------ ##
        TeachCMD_list = self.move2tote()
        goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()
        rospy.loginfo("Standby Result:%s"%result.notify)
        ##------------------ Recognizing items ------------------ ##
        rospy.loginfo("Recognizing items!")
        obj = self.stow_vision_client(tote_contents,work_order)
        ############Don't forget to pick
        ##------------------ Ready to Stow ------------------ ##
        #############Don't forget to compare Work order##########
        global left,right,middle
        rospy.loginfo("LEFT=%d",left)
        rospy.loginfo("MIDDLE=%d",middle)
        rospy.loginfo("RIGHT=%d",right)
        if obj.objID=='A' or obj.objID=='D' or obj.objID=='G' or obj.objID=='J':
            if not left:
                if middle:
                    rospy.loginfo("Controlling the Mbot move from CENTER to section LEFT")
                    cmd_vel.linear.x = -50
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    time.sleep(4.5)
                    cmd_vel.linear.x = 0
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                elif right:
                    rospy.loginfo("Controlling the Mbot move from RIGHT to section LEFT")
                    cmd_vel.linear.x = -50
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    time.sleep(9)
                    cmd_vel.linear.x = 0
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                left=True
                right=False
                middle=False
        elif obj.objID=='B' or obj.objID=='E' or obj.objID=='H' or obj.objID=='K':
            if not middle:
                if left:
                    rospy.loginfo("Controlling the Mbot move from LEFT to section CENTER")
                    cmd_vel.linear.x = 50
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    time.sleep(4.5)
                    cmd_vel.linear.x = 0
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                elif right:
                    rospy.loginfo("Controlling the Mbot move from RIGHT to section CENTER")
                    cmd_vel.linear.x = -50
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    time.sleep(4.5)
                    cmd_vel.linear.x = 0
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                left=False
                right=False
                middle=True
        elif obj.objID=='C' or obj.objID=='F' or obj.objID=='I' or obj.objID=='L':
            if not right:
                if left:
                    rospy.loginfo("Controlling the Mbot move from LEFT to section RIGHT")
                    cmd_vel.linear.x = 50
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    time.sleep(9)
                    cmd_vel.linear.x = 0
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                elif middle:
                    rospy.loginfo("Controlling the Mbot move from CENTER to section RIGHT")
                    cmd_vel.linear.x = 50
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                    time.sleep(4.5)
                    cmd_vel.linear.x = 0
                    cmd_vel.linear.y = 0
                    cmd_vel.linear.z = 0
                    cmd_vel.angular.x = 0
                    cmd_vel.angular.y = 0
                    cmd_vel.angular.z = 0
                    TeachCMD_list = self.ControlBase(cmd_vel)
                    goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
                    client.send_goal(goal)
                    client.wait_for_result()
                    result = client.get_result()
                    rospy.loginfo("Standby Result:%s"%result.notify)
                left=False
                right=True
                middle=False

        rospy.loginfo("Ready to Stow!")
        TeachCMD_list = self.ready2stow()
        goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()
        rospy.loginfo("Standby Result:%s"%result.notify)
        ##------------------ Ready to Stow ------------------ ##
        rospy.loginfo("Placing item into bin")
        bin_ID = 0
        if obj.objID=='A':
            bin_ID = 1
        elif obj.objID=='B':
            bin_ID = 2
        elif obj.objID=='C':
            bin_ID = 3
        elif obj.objID=='D':
            bin_ID = 4
        elif obj.objID=='E':
            bin_ID = 5
        elif obj.objID=='F':
            bin_ID = 6
        elif obj.objID=='G':
            bin_ID = 7
        elif obj.objID=='H':
            bin_ID = 8
        elif obj.objID=='I':
            bin_ID = 9
        elif obj.objID=='J':
            bin_ID = 10
        elif obj.objID=='K':
            bin_ID = 11
        elif obj.objID=='L':
            bin_ID = 12

        TeachCMD_list = self.move2standby(bin_ID)
        goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()
        rospy.loginfo("Standby Result:%s"%result.notify)

    ############################################## UI_INFO Execute Callback ##############################################
    def ui_info_cb(self,goal):
        rospy.loginfo("uifo_cb_execute")
        success = True
        global json_data


        '''for x in range(1,4,1):
            for y in range(0,4,1):
                bin_ID = y*3+x
                obj = self.control_mbot(bin_ID,json_data)
                self._feedback.tag = "Jianming is Super hot %d!" % bin_ID
                self._feedback.msg = "Jianming is Super cool %d!" % bin_ID
                self._as.publish_feedback(self._feedback)'''

        if goal.cmd=='Read_File':
            rospy.loginfo("Read_File")
            with open('apc_echo.json', 'w') as f:
                f.write(goal.data)
                f.close()
            with open('apc_echo.json') as data_file:
                json_data = json.load(data_file)
                data_file.close()
        elif goal.cmd=='Pick_Run':
            rospy.loginfo("Pick_Run")

            '''for x in range(1,4,1):
                for y in range(0,4,1):
                    bin_ID = y*3+x
                    if bin_ID==1:
                        obj = self.Pick_task(bin_ID,json_data['bin_contents']['bin_A'],json_data['work_order'][0]['item'])
                    elif bin_ID==2:
                        obj = self.Pick_task(bin_ID,json_data['bin_contents']['bin_B'],json_data['work_order'][1]['item'])
                    elif bin_ID==3:
                        obj = self.Pick_task(bin_ID,json_data['bin_contents']['bin_C'],json_data['work_order'][2]['item'])
                    elif bin_ID==4:
                        obj = self.Pick_task(bin_ID,json_data['bin_contents']['bin_D'],json_data['work_order'][3]['item'])
                    elif bin_ID==5:
                        obj = self.Pick_task(bin_ID,json_data['bin_contents']['bin_E'],json_data['work_order'][4]['item'])
                    elif bin_ID==6:
                        obj = self.Pick_task(bin_ID,json_data['bin_contents']['bin_F'],json_data['work_order'][5]['item'])
                    elif bin_ID==7:
                        obj = self.Pick_task(bin_ID,json_data['bin_contents']['bin_G'],json_data['work_order'][6]['item'])
                    elif bin_ID==8:
                        obj = self.Pick_task(bin_ID,json_data['bin_contents']['bin_H'],json_data['work_order'][7]['item'])
                    elif bin_ID==9:
                        obj = self.Pick_task(bin_ID,json_data['bin_contents']['bin_I'],json_data['work_order'][8]['item'])
                    elif bin_ID==10:
                        obj = self.Pick_task(bin_ID,json_data['bin_contents']['bin_J'],json_data['work_order'][9]['item'])
                    elif bin_ID==11:
                        obj = self.Pick_task(bin_ID,json_data['bin_contents']['bin_K'],json_data['work_order'][10]['item'])
                    elif bin_ID==12:
                        obj = self.Pick_task(bin_ID,json_data['bin_contents']['bin_L'],json_data['work_order'][11]['item'])
                    else:
                        rospy("Bin_ID Wrong!")
                    self._feedback.tag = "Jianming is Super hot %d!" % bin_ID
                    self._feedback.msg = "Jianming is Super cool %d!" % bin_ID
                    self._as.publish_feedback(self._feedback)'''
            obj = self.Pick_task(9,json_data['bin_contents']['bin_A'],json_data['work_order'][0]['item'])

        elif goal.cmd=='Stow_Run':
            rospy.loginfo("Stow_Run")
            self.Stow_task('A','B')
            self.Stow_task('A','B')
            self.Stow_task('A','B')
            self.Stow_task('A','B')
            self.Stow_task('A','B')
            self.Stow_task('A','B')
            #print json_data
        else:
            rospy.loginfo("WTF!CMD WRONG!!!")

        if success:
            rospy.loginfo('------Jianming done!------')
            self._result.result = "Hello moto"
            self._as.set_succeeded(self._result)


    #################################################### Vision Client ###################################################
    def vision_client(self,bin_contents,goal_obj):
        #rospy.loginfo("vision_client_execute")
        rospy.loginfo("Vision processing ...")
        rospy.loginfo("Searching goal_obj:%s",goal_obj)
        goal_obj_str = "%s" % goal_obj
        bin_contents_str = "%s" % bin_contents
        client = actionlib.SimpleActionClient('simVision_server', vision.msg.vision_cmdAction)
        client.wait_for_server()
        goal = vision.msg.vision_cmdGoal(goal_obj=goal_obj_str,bin_content=bin_contents_str)
        client.send_goal(goal)
        client.wait_for_result()
        obj = client.get_result()
        rospy.loginfo(obj.objID)
        rospy.loginfo(obj.objPose)
        return obj
    #################################################### Vision Client ###################################################
    def stow_vision_client(self,tote_contents,goal_obj):
        #rospy.loginfo("vision_client_execute")
        rospy.loginfo("Vision processing ...")
        rospy.loginfo("Searching goal_obj:%s",goal_obj)
        goal_obj_str = "%s" % goal_obj
        bin_contents_str = "%s" % tote_contents
        client = actionlib.SimpleActionClient('fake_stow_vision', vision.msg.vision_cmdAction)
        client.wait_for_server()
        goal = vision.msg.vision_cmdGoal(goal_obj=goal_obj_str,bin_content=bin_contents_str)
        client.send_goal(goal)
        client.wait_for_result()
        obj = client.get_result()
        rospy.loginfo(obj.objID)
        rospy.loginfo(obj.objPose)
        return obj

    ###################################################### For Test ######################################################
    def test_read_json(self):
        hello_str = "%s" % self.data['work_order'][0]['bin']

        if hello_str == "bin_A":
            rospy.loginfo("BIN_A")
        else:
            rospy.loginfo("FAIL! The message is %s",hello_str)


######################################################  Main is here  ######################################################
if __name__ == '__main__':
    try:
        node_name = 'strategy'
        file_name = 'apc.json'
        rospy.init_node(node_name,anonymous=False)
        #global middle,left,right
        middle =True
        left = False
        right = False
        strategy = strategy_class(rospy.get_name(),file_name)
        #strategy.test_read_json()
        #strategy.vision_client(5)


    except rospy.ROSInterruptException:
        pass