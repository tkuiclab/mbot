#!/usr/bin/env python

"""
    info.py - Version 0.1 2014-01-14

"""
import rospy, sys
import moveit_commander
from std_msgs.msg import Header
from moveit_msgs.msg import RobotTrajectory, RobotState
from moveit_msgs.srv import GetPositionFK

from trajectory_msgs.msg import JointTrajectoryPoint

import time
from copy import deepcopy
from geometry_msgs.msg import PoseStamped, Pose
from geometry_msgs.msg import Twist


from tf.transformations import euler_from_quaternion, quaternion_from_euler


if __name__ == "__main__":
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('test_comput_fk')
    robot = moveit_commander.RobotCommander()

    # Initialize the move group for the right arm
    ur_arm = moveit_commander.MoveGroupCommander('manipulator')
    ur_arm.set_pose_reference_frame('/world')

    end_effector_link = ur_arm.get_end_effector_link()
    #ur_arm.set_named_target("home")
    #ur_arm.go()


    print "init OK"

    j_names = ur_arm.get_active_joints()
    for name in j_names:
        print name

    l_names = robot.get_link_names()
    print "====links name===="
    for name in l_names:
        print name
    print "=================="

    g_names = robot.get_group_names()
    print "====group name===="
    for name in g_names:
        print name
    print "=================="


    rospy.wait_for_service('compute_fk')
    try:
        moveit_fk = rospy.ServiceProxy('compute_fk', GetPositionFK)
    except rospy.ServiceException, e:
        rospy.logerror("Service call failed: %s"%e)
    #fkln = l_names
    fkln = [ur_arm.get_end_effector_link()]
    joint_names = []
    joint_positions = []
    #for i in range(6):
    #    joint_names.append(j_names[i]) # your names may vary
    #    joint_positions.append(0.0) # try some arbitrary joint angle
    #joint_positions[1] = -1.57
    joint_names = j_names

    joint_positions = [1.55469861260765, -2.3450513424352186, 0.00017115454217631054, -2.1260608462508035, -4.6844348487340426e-05, -0.22517671695127994]


    header = Header(0,rospy.Time.now(),"world")
    rs = RobotState()
    rs.joint_state.name = joint_names
    rs.joint_state.position = joint_positions

    res = moveit_fk(header, fkln, rs)

    '''
    for pose_stamp in res.pose_stamped:
        p = pose_stamp.pose.position
        print str(p.x) + "," + str(p.y) + "," + str(p.z)
        print '-------'
    '''
    p = res.pose_stamped[0].pose.position

    print '-------'

    rospy.loginfo(["FK LOOKUP:", moveit_fk(header, fkln, rs)])

    #rospy.loginfo(["End effetor link:", ur_arm.get_end_effector_link()])

    print str(p.x) + "," + str(p.y) + "," + str(p.z)



    rospy.loginfo(["Now Pose wit end_effector_link:", ur_arm.get_current_pose(end_effector_link)])

    rospy.loginfo([" get_planning_frame", ur_arm.get_planning_frame()])
    print "log finish"
    moveit_commander.roscpp_shutdown()
    # Exit MoveIt
    moveit_commander.os._exit(0)



    '''
    pass
    rospy.wait_for_service('compute_fk')
    try:
        moveit_fk = rospy.ServiceProxy('compute_fk', GetPositionFK)
    except rospy.ServiceException, e:
        rospy.logerror("Service call failed: %s"%e)
    fkln = ['palm']
    joint_names = []
    joint_positions = []
    for i in range(6):
      joint_names.append('right_arm_j'+str(i)) # your names may vary
      joint_positions.append(0.8) # try some arbitrary joint angle
    header = Header(0,rospy.Time.now(),"/world")
    rs = RobotState()
    rs.joint_state.name = joint_names
    rs.joint_state.position = joint_positions
    rospy.loginfo(["FK LOOKUP:", moveit_fk(header, fkln, rs)]) # Lookup the pose
    #### To test, execute joint_positions here ####
    rospy.loginfo(["POST MOVE:", right_arm.get_current_pose()])
    '''