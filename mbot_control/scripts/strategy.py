#!/usr/bin/env python
# license removed for brevity
import rospy
import json
from pprint import pprint

from std_msgs.msg import String

with open('apc.json') as data_file:
    data = json.load(data_file)

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        #hello_str = "hello world %s" % rospy.get_time()
        hello_str = "%s" % data['work_order'][0]['bin']
        #if(data['work_order'][0]['bin']=='bin_A')
        #    rospy.loginfo("BIN_A")
        if hello_str == "bin_A":
            rospy.loginfo("BIN_A")
            pub.publish(hello_str)
        else:
            rospy.loginfo(hello_str)

        #hello_str = "hello world %s" % data['bin_contents']['bin_A']
        #rospy.loginfo(hello_str)

        #pprint(data['bin_contents']['bin_A'])
        #pprint('')
        #pprint(data['work_order'][0]['bin'])
        #pprint(data['work_order'][0]['item'])
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()

    except rospy.ROSInterruptException:
        pass