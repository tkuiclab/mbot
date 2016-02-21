"""
File: strategy.py
Author: Chien-Ming Lin <jianming1481@gmail.com>
Created on:       2016/02/18 --------------------> Create file & read json file
Modified on:      2016/02/21 --------------------> Add Action Server for UIFO & Action Client for Vision

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

from std_msgs.msg import String

class strategy_class(object):
    _feedback = mbot_control.msg.UIFOFeedback()
    _result = mbot_control.msg.UIFOResult()

    ################################################## Class Initialize ##################################################
    def __init__(self,node_name,file_name):
        with open(file_name) as data_file:
            self.data = json.load(data_file)

        self.uifo_action_name = "%s_uifo" % node_name
        self._as = actionlib.SimpleActionServer(self.uifo_action_name,mbot_control.msg.UIFOAction,execute_cb=self.uifo_cb,auto_start=False)

        self._as.start()

    ############################################## UI_INFO Execute Callback ##############################################
    def uifo_cb(self,goal):
        rospy.loginfo("uifo_cb_execute")
        rospy.loginfo(goal)
        success = True



        for i in range(0,3,1):
            self._feedback.tag = "Jianming is Super hot %d!" % i
            self._feedback.msg = "Jianming is Super cool %d!" % i
            self._as.publish_feedback(self._feedback)

        if success:
            rospy.loginfo('------Jianming is Super hot!------')
            self._result.result = "Hello moto"
            self._as.set_succeeded(self._result)


    #################################################### Vision Client ###################################################
    def vision_client(self,bin_ID):
        client = actionlib.SimpleActionClient('simVision_server', vision.msg.vision_cmdAction)
        client.wait_for_server()
        goal = vision.msg.vision_cmdGoal(binID=bin_ID)
        client.send_goal(goal)
        client.wait_for_result()
        pose = client.get_result()
        rospy.loginfo(pose)

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