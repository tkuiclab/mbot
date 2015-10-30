#! /usr/bin/env python

import roslib;

roslib.load_manifest('mbot_control')
import rospy, sys

import actionlib

import strategy.msg

#import moveit_commander
from arm import ARM


class TeachModeServer(object):
    # create messages that are used to publish feedback/result
    _feedback = strategy.msg.TeachCommandListFeedback()
    _result = strategy.msg.TeachCommandListResult()

    def __init__(self, name):
        print 'Action Name=' + name
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, strategy.msg.TeachCommandListAction,
                                                execute_cb=self.execute_cb, auto_start=False)
        self._as.start()

    def execute_cb(self, goal):
        # helper variables
        # r = rospy.Rate(1)
        success = True

        # publish info to the console for the user
        rospy.loginfo('-------Teach Mode Start-------')
        rospy.loginfo('Command Count : %d', goal.cmd_list.__len__())

        # cmd_list = goal.cmd_list
        # start executing the action
        for i in range(goal.cmd_list.__len__()):
            # check that preempt has not been requested by the client
            if self._as.is_preempt_requested():
                rospy.loginfo('%s: Preempted' % self._action_name)
                self._as.set_preempted()
                success = False
                break
            self._feedback.status = 'Execute Command ' + str(i)

            cmd = goal.cmd_list[i]
            show_str = "(%2d) Execute %s -> " % (i, cmd.cmd)

            if cmd.cmd == 'Vaccum':
                show_str += str(cmd.vaccum)

            elif cmd.cmd == 'JointPosition':
                #target joints shoulder_pan shoulder_lift elbow wrist1 wrist2 wrist3
                target_joints = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                for j in range(len(cmd.joint_position)):
                    target_joints[j] = cmd.joint_position[j]

                #target_joints = cmd.joint_position;
                g_arm.set_joints(target_joints)
                #show_str += str(cmd.joint_position[1])

            elif cmd.cmd == 'EEFPosition':
                # target pose x y z r p y
                target_position = [0.0, 0.0, 0.0]
                target_pose = [0.0, 0.0, 0.0]
                #for k in range(len(cmd.joint_position)/2):
                    #target_joints[k] = cmd.joint_position[k]
                    #target_pose[k] = cmd.joint_position[3+k]
                target_position[0] = cmd.pose.linear.x
                target_position[1] = cmd.pose.linear.y
                target_position[2] = cmd.pose.linear.z
                target_pose[0] = cmd.pose.angular.x
                target_pose[1] = cmd.pose.angular.y
                target_pose[2] = cmd.pose.angular.z
                g_arm.set_pose(target_position,target_pose)

            elif cmd.cmd == 'ShiftX':
                int_X = cmd.pose.linear.x
                g_arm.shift_x(int_X);

            elif cmd.cmd == 'ShiftY':
                int_Y = cmd.pose.linear.y
                g_arm.shift_y(int_Y)

            elif cmd.cmd == 'ShiftZ':
                int_Z = cmd.pose.linear.z
                g_arm.shift_z(int_Z)




            #rospy.loginfo(show_str)
            # publish the feedback
            self._as.publish_feedback(self._feedback)
            # this step is not necessary, the sequence is computed at 1 Hz for demonstration purposes
            # r.sleep()

        if success:
            self._result.notify = 'Success'
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)


def init_g_arm():
    global g_arm
    g_arm = ARM()
    g_arm.set_speed(0.75)
    g_arm.back2home()

if __name__ == '__main__':
    #moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('teach_mode_server')
    rospy.Rate(100)

    init_g_arm()

    TeachModeServer(rospy.get_name())

    rospy.spin()
