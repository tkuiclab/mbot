"""
File: fake_json_publisher.py
Author: Chien-Ming Lin <jianming1481@gmail.com>
Created on:     2016/02/21 ---------------------> Create file & Add read file
Modified on:    None

Description: For test strategy
    Action_Server: None
    Action_Client: UI_INFO
"""

#!/usr/bin/env python
import rospy
import roslib
import actionlib
import mbot_control.msg
import rospkg

def UI_client(file_path):
    f = open(file_path, 'r')
    data = f.read()
    f.close()
    client = actionlib.SimpleActionClient('strategy_uifo',mbot_control.msg.UIFOAction)
    client.wait_for_server()
    goal = mbot_control.msg.UIFOGoal(cmd = data)
    client.send_goal(goal)
    client.wait_for_result()
    rospy.loginfo(client.get_result())

if __name__ == '__main__':
    try:
        node_name = "fake_json_publisher"
        rospy.init_node(node_name)

        global file_path
        rospack = rospkg.RosPack()

        pkg_name = 'mbot_control'
        file_name = 'apc.json'
        file_path = rospack.get_path(pkg_name) + '/scripts/' + file_name

        UI_client(file_path)
    except rospy.ROSInterruptException:
        print "program interrupted before completion"