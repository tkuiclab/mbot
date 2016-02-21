#!/usr/bin/env python
# license removed for brevity
import rospy
import roslib
import actionlib
import mbot_control.msg
import json
from pprint import pprint

from std_msgs.msg import String

class strategy_class(object):
    _feedback = mbot_control.msg.task_cmdActionFeedback()
    _result = mbot_control.msg.task_cmdActionResult()

    def __init__(self,node_name,file_name):
        with open('apc.json') as data_file:
            self.data = json.load(data_file)

        self._action_name = node_name

    def test_read_json(self):
        rate = rospy.Rate(10) # 10hz
        hello_str = "%s" % self.data['work_order'][0]['bin']

        if hello_str == "bin_A":
            rospy.loginfo("BIN_A")
        else:
            rospy.loginfo("FAIL! The message is %s",hello_str)
        rate.sleep()


if __name__ == '__main__':
    try:
        rospy.init_node('strategy',anonymous=True)
        file_name = 'apc.json'
        strategy = strategy_class(rospy.get_name(),file_name)
        strategy.test_read_json();


    except rospy.ROSInterruptException:
        pass