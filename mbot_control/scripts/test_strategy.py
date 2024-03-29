"""
File: strategy.py
Author: Chien-Ming Lin <jianming1481@gmail.com>
Created on:       2016/02/18 --------------------> Creating file & read json file
Modified on:      2016/02/21 --------------------> Adding Action Server for UIFO & Action Client for Vision
                  2016/02/22 --------------------> Adding mbot_control server

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
    _feedback = mbot_control.msg.UIFOFeedback()
    _result = mbot_control.msg.UIFOResult()

    ################################################## Class Initialize ##################################################
    def __init__(self,node_name,file_name):
        with open(file_name) as data_file:
            self.data = json.load(data_file)
            data_file.close()

        self.uifo_action_name = "%s_uifo" % node_name
        self._as = actionlib.SimpleActionServer(self.uifo_action_name,mbot_control.msg.UIFOAction,execute_cb=self.uifo_cb,auto_start=False)

        self._as.start()

    ##################################################### Control Mbot ####################################################
    def control_mbot(self,bin_ID,json_data):
        client = actionlib.SimpleActionClient('mbot_control', mbot_control.msg.TeachCommandListAction)
        client.wait_for_server()
        TeachCMD_list = mbot_control.msg.TeachCommandListGoal()
        cmd = mbot_control.msg.TeachCommand()
        if bin_ID==1 or bin_ID==4 or bin_ID==7 or bin_ID==10:
            rospy.loginfo("Controlling the Mbot move to section LEFT")
            if bin_ID==1:
                cmd.cmd = 'Joint'
                cmd.joint_position = [0, -1.57, 0, -1.57, 0, 0]
                tmp_twist = Twist()
                tmp_twist.linear.x = 0
                tmp_twist.linear.y = 0
                tmp_twist.linear.z = 0
                tmp_twist.angular.x = 0
                tmp_twist.angular.y = 0
                tmp_twist.angular.z = 0
                cmd.pose = tmp_twist

                #cmd.pose.linear.x = 0;
                TeachCMD_list.cmd_list = []
                TeachCMD_list.cmd_list.append(cmd)
                #print TeachCMD_list.cmd_list[0].cmd
                #print TeachCMD_list[0].cmd_list.cmd
                goal = mbot_control.msg.TeachCommandListGoal(TeachCMD_list.cmd_list)

        elif bin_ID==2 or bin_ID==5 or bin_ID==8 or bin_ID==11:
            rospy.loginfo("Controlling the Mbot move to section CENTER")
        elif bin_ID==3 or bin_ID==6 or bin_ID==9 or bin_ID==12:
            rospy.loginfo("Controlling the Mbot move to section RIGHT")
        else:
            rospy.loginfo("BIN_ID ERROR")

        client.send_goal(goal)
        client.wait_for_result()
        result = client.get_result()
        rospy.loginfo("Mbot_control Result:%s"%result.notify)

        rospy.loginfo("Controlling the Mbot move to bin %d" % bin_ID)
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
        rospy.loginfo("Grapping items in bin_%d" % bin_ID)
        return obj

    ############################################## UI_INFO Execute Callback ##############################################
    def uifo_cb(self,goal):
        rospy.loginfo("uifo_cb_execute")
        success = True

        with open('apc_echo.json', 'w') as f:
            f.write(goal.cmd)
            f.close()
        with open('apc_echo.json') as data_file:
            json_data = json.load(data_file)
            data_file.close()

        for x in range(1,4,1):
            for y in range(0,4,1):
                bin_ID = y*3+x
                obj = self.control_mbot(bin_ID,json_data)
                self._feedback.tag = "Jianming is Super hot %d!" % bin_ID
                self._feedback.msg = "Jianming is Super cool %d!" % bin_ID
                self._as.publish_feedback(self._feedback)

        if success:
            rospy.loginfo('------Jianming is Super hot!------')
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