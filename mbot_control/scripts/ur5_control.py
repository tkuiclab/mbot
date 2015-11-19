#!/usr/bin/env python
'''
Testing script that runs many of the urx methods, while attempting to keep robot pose around its starting pose
'''

from math import pi
import time
import rospy
import sys
import threading
from ur_control.srv import *
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import logging
import urx
import roslib
roslib.load_manifest('mbot_control')
import actionlib
import mbot_control.msg
from sensor_msgs.msg import JointState

class ur_control(object):
    _feedback = mbot_control.msg.TeachCommandListFeedback()
    _result = mbot_control.msg.TeachCommandListResult()

    def __init__(self,name,v,a):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, mbot_control.msg.TeachCommandListAction,
                                                execute_cb=self.cmd_handler, auto_start = False)
        self.set_speed(v,a)
        self._as.start()

    def set_speed(self,v,a):
        global vel,acc
        vel = v
        acc = a

    def cmd_handler(self,goal):
        success = True

        for i in range(goal.cmd_list.__len__()):
            # check that preempt has not been requested by the client
            if self._as.is_preempt_requested():
                rospy.loginfo('%s: Preempted' % self._action_name)
                self._as.set_preempted()
                success = False
                break
            self._feedback.status = 'Execute Command ' + str(i)

            #rospy.loginfo('Execute Command ' + str(i))

            cmd = goal.cmd_list[i]
            show_str = "(%2d) Execute %s " % (i, cmd.cmd)
            rospy.loginfo(show_str)

            if cmd.cmd == 'Vaccum':
                if cmd.vaccum:
                    rob.set_digital_out(1,True)
                else:
                    rob.set_digital_out(1,False)
                rospy.sleep(2)


            elif cmd.cmd == 'Joint':
                #target joints shoulder_pan shoulder_lift elbow wrist1 wrist2 wrist3
                target_joints = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                for j in range(len(cmd.joint_position)):
                    target_joints[j] = cmd.joint_position[j]

                rob.movej(target_joints,acc,vel)
                rospy.sleep(2)

            elif cmd.cmd == 'PTP':
                # target pose x y z r p y
                p_target_pose = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                #for k in range(len(cmd.joint_position)/2):
                    #target_joints[k] = cmd.joint_position[k]
                    #target_pose[k] = cmd.joint_position[3+k]
                p_target_pose[0] = cmd.pose.linear.x
                p_target_pose[1] = cmd.pose.linear.y
                p_target_pose[2] = cmd.pose.linear.z
                p_target_pose[3] = cmd.pose.angular.x
                p_target_pose[4] = cmd.pose.angular.y
                p_target_pose[5] = cmd.pose.angular.z

                #print "x={0}, y={1}, z={2}, rx={3}, ry={4}, rz={5} ...);".\
                #    format(target_position[0],target_position[1],target_position[2],target_pose[0],target_pose[1],target_pose[2])

                rob.movep(p_target_pose,acc,vel)
                rospy.sleep(2)

            elif cmd.cmd == 'Line':
                l_target_pose = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                l_target_pose[0] = cmd.pose.linear.x
                l_target_pose[1] = cmd.pose.linear.y
                l_target_pose[2] = cmd.pose.linear.z
                l_target_pose[3] = cmd.pose.angular.x
                l_target_pose[4] = cmd.pose.angular.y
                l_target_pose[5] = cmd.pose.angular.z

                rob.movel(l_target_pose,acc,vel)
                rospy.sleep(2)

            elif cmd.cmd == 'Shift_X':
                int_X = cmd.pose.linear.x
                pose = [0.0,0.0,0.0,0.0,0.0,0.0]
                pose[0] += int_X
                rob.movel(pose,acc,vel,False,True)
                rospy.sleep(2)

            elif cmd.cmd == 'Shift_Y':
                int_Y = cmd.pose.linear.y
                pose = [0.0,0.0,0.0,0.0,0.0,0.0]
                pose[1] += int_Y
                rob.movel(pose,acc,vel,False,True)
                rospy.sleep(2)

            elif cmd.cmd == 'Shift_Z':
                int_Z = cmd.pose.linear.z
                pose = [0.0,0.0,0.0,0.0,0.0,0.0]
                '''
                print("int_Z:")
                print(int_Z)
                print("pose:")
                print(pose)
                '''
                pose[2] += int_Z
                rob.movel(pose,acc,vel,False,True)
                rospy.sleep(2)

            elif cmd.cmd == 'Shift_RX':
                ang = cmd.pose.angular.x
                pose = [0.0,0.0,0.0,0.0,0.0,0.0]
                pose[3] += ang
                rob.movel(pose,acc,vel,False,True)
                rospy.sleep(2)

            elif cmd.cmd == 'Shift_RY':
                ang = cmd.pose.angular.y
                pose = [0.0,0.0,0.0,0.0,0.0,0.0]
                pose[4] += ang
                rob.movel(pose,acc,vel,False,True)
                rospy.sleep(2)

            elif cmd.cmd == 'Shift_RZ':
                ang = cmd.pose.angular.z
                pose = [0.0,0.0,0.0,0.0,0.0,0.0]
                pose[5] += ang
                rob.movel(pose,acc,vel,False,True)
                rospy.sleep(2)

        if success:
            self._result.notify = 'Success'
            self._as.set_succeeded(self._result)


            # publish the feedback
            self._as.publish_feedback(self._feedback)
            # this step is not necessary, the sequence is computed at 1 Hz for demonstration purposes
            # r.sleep()

class joint_states_publisher(threading.Thread):
    def __init__(self):
        #super(joint_states_publisher,self).__init__(name="thread-pub_joint_states")
        threading.Thread.__init__(self)
        #************Subscribe ur_speed to control ur5
        rospy.Subscriber("ur_speed", Twist, self.speed_callback)
        #rospy.init_node('ur_control_server')

    def speed_callback(self,data):
        speeds = [0,0,0,0,0,0]
        print(data.linear.x)

    def run(self):
        joint_states_pub = rospy.Publisher('joint_states', JointState, queue_size=10)
        eef_pub = rospy.Publisher('eef_states',Twist,queue_size=10)

        eef_states = Twist()
        joint_states = JointState()
        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():

            #*************Publish Joint states & EEF states
            joint_tmp = rob.getj()
            eef_tmp = rob.getl()
            #print(pose)

            now = rospy.get_rostime()

            joint_states.header.stamp = now
            joint_states.header.frame_id = "From real-time state data"

            joint_names = ['elbow_joint','shoulder_lift_joint','shoulder_pan_joint','wrist_1_joint','wrist_2_joint','wrist_3_joint']
            joint_states.name = joint_names

            joint_states.position = [0.0]*6
            for i in range(6):
                joint_states.position[i] = joint_tmp[i]

            joint_states.velocity =[0.0,0.0,0.0,0.0,0.0,0.0]
            joint_states.effort = [0.0,0.0,0.0,0.0,0.0,0.0]

            eef_states.linear.x = eef_tmp[0]
            eef_states.linear.y = eef_tmp[1]
            eef_states.linear.z = eef_tmp[2]
            eef_states.angular.x = eef_tmp[3]
            eef_states.angular.y = eef_tmp[4]
            eef_states.angular.z = eef_tmp[5]

            joint_states_pub.publish(joint_states)
            eef_pub.publish(eef_states)


            rate.sleep()






if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    global rob
    rob = urx.Robot("192.168.5.5")
    #rob = urx.Robot("localhost")
    rob.set_tcp((0, 0, 0, 0, 0, 0))
    rob.set_payload(0.5, (0, 0, 0))
    rospy.init_node('teach_mode_server')

    try:
        js_p = joint_states_publisher()
        js_p.start()
        ur_commander = ur_control(rospy.get_name(),0.8,0.2)
        ur_commander.set_speed(0.8,0.2)
        rospy.spin()
    finally:
        rob.close()
