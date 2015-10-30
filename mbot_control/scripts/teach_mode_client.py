#! /usr/bin/env python

import roslib; roslib.load_manifest('mbot_control')
import rospy

import actionlib

import mbot_control.msg

def feedback_cb(fb_data):
    rospy.loginfo("Teach Server Feedback -> " + fb_data.status)

def done_cb(done_data):
    rospy.loginfo("Teach Server Done -> " + done_data.notify)

def teach_mode_client():
    # Creates the SimpleActionClient, passing the type of the action
    # (FibonacciAction) to the constructor.
    client = actionlib.SimpleActionClient('teach_mode_server', mbot_control.msg.TeachCommandListAction)

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()

    # Creates a goal to send to the action server.
    m_cmd_list = []
    cmd_1 = mbot_control.msg.TeachCommand()
    cmd_1.cmd = "Vaccum"
    cmd_1.vaccum = False
    m_cmd_list.append(cmd_1)

    cmd_2 = mbot_control.msg.TeachCommand()
    cmd_2.cmd = "JointPosition"
    cmd_2.joint_position = [0.0, -1.57, 0.0, -1.57, 0.0, 0.0]
    m_cmd_list.append(cmd_2)

    cmd_3 = mbot_control.msg.TeachCommand()
    cmd_3.cmd = "EEFPosition"
    cmd_3.pose.linear.x = 0.0
    cmd_3.pose.linear.y = 0.4
    cmd_3.pose.linear.z = 1.6

    cmd_3.pose.angular.x = 0
    cmd_3.pose.angular.y = 1.57
    cmd_3.pose.angular.z = 0
    m_cmd_list.append(cmd_3)

    cmd_4 = mbot_control.msg.TeachCommand()
    cmd_4.cmd = "ShiftY"
    cmd_4.pose.linear.y = 0.1
    m_cmd_list.append(cmd_4)

    cmd_5 = mbot_control.msg.TeachCommand()
    cmd_5.cmd = "ShiftZ"
    cmd_5.pose.linear.z = -0.1
    m_cmd_list.append(cmd_5)

    goal = mbot_control.msg.TeachCommandListGoal(cmd_list=m_cmd_list)

    # Sends the goal to the action server.
    client.send_goal(goal,feedback_cb = feedback_cb )

    # Waits for the server to finish performing the action.
    client.wait_for_result()

    # Prints out the result of executing the action
    #return client.get_result()


def myhook():
  print "shutdown time!"

if __name__ == '__main__':
    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('teach_mode_client')
        result = teach_mode_client()
        #print result
        rospy.on_shutdown(myhook)
        #print "Result:", ', '.join([str(n) for n in result.sequence])
    except rospy.ROSInterruptException:
        print "program interrupted before completion"
