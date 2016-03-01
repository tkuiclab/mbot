"""
File: strategy.py
Author: Chien-Ming Lin <jianming1481@gmail.com>
Created on:       2016/02/18 --------------------> Creating file & read json file
Modified on:      2016/02/21 --------------------> Adding Action Server for UIFO & Action Client for Vision
                  2016/02/22 --------------------> Adding mbot_control server
                  2016/02/25 --------------------> Adding move2standby function & Modify ur5_control.py for rotate TCP
                  2016/03/01 --------------------> Change the name of action file "UIFO" -> "UI_Info"

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

from std_msgs.msg import String

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
            cmd.joint_position = [1.273, -2.016, 2.301, -3.407, -1.2, 0.0]
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
        rospy.loginfo("Moving to watch position...")
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
    ##################################################### Control Mbot ####################################################
    def control_mbot(self,bin_ID,json_data):
        rospy.loginfo("Controlling mbot")
        client = actionlib.SimpleActionClient('mbot_control', mbot_control.msg.TeachCommandListAction)
        client.wait_for_server()

        TeachCMD_list = mbot_control.msg.TeachCommandListGoal()
        TeachCMD_list.cmd_list = []

        ##------------------ Standby ------------------ ##
        if bin_ID==1 or bin_ID==4 or bin_ID==7 or bin_ID==10:
            rospy.loginfo("Controlling the Mbot move to section LEFT")
        elif bin_ID==2 or bin_ID==5 or bin_ID==8 or bin_ID==11:
            rospy.loginfo("Controlling the Mbot move to section CENTER")
            TeachCMD_list = self.move2standby(bin_ID)
        elif bin_ID==3 or bin_ID==6 or bin_ID==9 or bin_ID==12:
            rospy.loginfo("Controlling the Mbot move to section RIGHT")
        else:
            rospy.loginfo("BIN_ID ERROR!")

        goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()
        rospy.loginfo("Mbot_control Result:%s"%result.notify)

        ##------------------ Watch inside bin ------------------ ##
        TeachCMD_list = self.move2watch()
        goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()
        rospy.loginfo("Mbot_control Result:%s"%result.notify)

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
        obj = switch[bin_ID](bin_ID)
        ##------------------ Ready 2 Pick ------------------ ##
        TeachCMD_list = self.ready2pick()
        goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)
        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()
        rospy.loginfo("Mbot_control Result:%s"%result.notify)

        rospy.loginfo("Grapping items in bin_%d" % bin_ID)

        return obj

    ############################################## UI_INFO Execute Callback ##############################################
    def ui_info_cb(self,goal):
        rospy.loginfo("uifo_cb_execute")
        success = True



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
        elif goal.cmd=='Stow_Run':
            rospy.loginfo("Stow_Run")
        else:
            rospy.loginfo("HAHAHA!")
        #obj = self.control_mbot(8,json_data)

        if success:
            rospy.loginfo('------Jianming done!------')
            self._result.result = "Hello moto"
            self._as.set_succeeded(self._result)


    #################################################### Vision Client ###################################################
    def vision_client(self,bin_ID):
        #rospy.loginfo("vision_client_execute")
        rospy.loginfo("Vision processing bin_%d"%bin_ID)
        client = actionlib.SimpleActionClient('simVision_server', vision.msg.vision_cmdAction)
        client.wait_for_server()
        goal = vision.msg.vision_cmdGoal(binID=bin_ID)
        client.send_goal(goal)
        client.wait_for_result()
        obj = client.get_result()
        #rospy.loginfo(obj.objID)
        #rospy.loginfo(obj.objPose)
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
        strategy = strategy_class(rospy.get_name(),file_name)
        #strategy.test_read_json()
        #strategy.vision_client(5)


    except rospy.ROSInterruptException:
        pass