#!/usr/bin/env python

"""
    arm.py
    
    http://www.gnu.org/licenses/gpl.html
"""

import rospy, sys
import moveit_commander
from moveit_msgs.msg import RobotTrajectory , Constraints, OrientationConstraint, PositionConstraint
from trajectory_msgs.msg import JointTrajectoryPoint

from geometry_msgs.msg import PoseStamped, Pose
from tf.transformations import euler_from_quaternion, quaternion_from_euler

from arm_utils import *

#from IterativeParabolicTimeParameterization import *


from copy import deepcopy

class ARM:
	def __init__(self):
		# Initialize the move_group API
		#moveit_commander.roscpp_initialize(sys.argv)

		#rospy.init_node('arm', anonymous=True)


		# Initialize the move group for the right arm
		self.arm = moveit_commander.MoveGroupCommander('manipulator')
		#self.arm = moveit_arm
		# Get the name of the end-effector link
		self.end_effector_link = self.arm.get_end_effector_link()

		# Set the reference frame for pose targets
		reference_frame = 'world'

		# Set the right arm reference frame accordingly
		self.arm.set_pose_reference_frame(reference_frame)

		# Allow replanning to increase the odds of a solution
		self.arm.allow_replanning(True)

		# Allow some leeway in position (meters) and orientation (radians)
		self.arm.set_goal_position_tolerance(0.005)
		self.arm.set_goal_orientation_tolerance(0.005)

		self.speed = 0.5


	def cartesian_path(self):
		#self.back2home()
		waypoints = []

		#self.arm.set_pose_reference_frame('world')


		#-----'m' pos waypoints-----#
		start_pose = self.arm.get_current_pose(self.end_effector_link).pose
		mpose = deepcopy(start_pose)

		#point 0
		waypoints.append(start_pose)

		#set wpose
		wpose = deepcopy(start_pose)

		#set all points
		wpose.position.z -= 0.4
		waypoints.append(deepcopy(wpose))

		wpose.position.z += 0.4
		waypoints.append(deepcopy(wpose))

		wpose.position.x += 0.5
		waypoints.append(deepcopy(wpose))


		wpose.position.z -= 0.4
		waypoints.append(deepcopy(wpose))

		wpose.position.z += 0.4
		waypoints.append(deepcopy(wpose))


		#-----cartesian_path-----#
		fraction = 0.0
		maxtries = 100
		attempts = 0

		# Set the internal state to the current state
		self.arm.set_start_state_to_current_state()

		# Plan the Cartesian path connecting the waypoints
		while fraction < 1.0 and attempts < maxtries:
			(plan, fraction) = self.arm.compute_cartesian_path (
							waypoints,   # waypoint poses
							0.1,        # eef_step
							0.0,         # jump_threshold
							False)        # avoid_collisions

			# Increment the number of attempts
			attempts += 1

			# Print out a progress message
			if attempts % 10 == 0:
				rospy.loginfo("Still trying after " + str(attempts) + " attempts...")
		if fraction == 1.0:
			rospy.loginfo("Path computed successfully. Moving the arm.")

			#self.arm.execute(plan)
			#self.run_plan(plan)
			self.run_at_speed(plan,0.05)
			rospy.sleep(5)

			rospy.loginfo("Path execution complete.")
		else:
			rospy.loginfo("Path planning failed with only " + str(fraction) + " success after " + str(maxtries) + " attempts.")



	def shift_pose(self):
		# Shift the end-effector to the right 5cm
		self.arm.shift_pose_target(2, -0.1, self.end_effector_link)
		self.run()
		#rospy.sleep(1)


		# Rotate the end-effector 90 degrees
		self.arm.shift_pose_target(0, 0.1, self.end_effector_link)
		self.run()
		#rospy.sleep(1)


		# Rotate the end-effector 90 degrees
		self.arm.shift_pose_target(1, 0.15, self.end_effector_link)
		self.run()
		#rospy.sleep(1)



	
 
	def run_m(self):
		start_pose = self.arm.get_current_pose(self.end_effector_link).pose
		mpose = deepcopy(start_pose)

		mpose.position.x = -0.4
		mpose.position.y = 0.4
		mpose.position.z = 0.6

		#euler = [0.0 1.57 0.0]
		(x,y,z,w) = quaternion_from_euler(0,1.57,0)

		mpose.orientation.x = x
		mpose.orientation.y = y
		mpose.orientation.z = z
		mpose.orientation.w = w


		self.arm.set_pose_target(mpose)
		#self.arm.plan()
		self.run()

		self.arm.set_start_state_to_current_state()

		self.arm.shift_pose_target(2, -0.4, self.end_effector_link)
		self.run()

		return
		self.arm.shift_pose_target(2, +0.4, self.end_effector_link)
		self.run()

		self.arm.shift_pose_target(0, +0.6, self.end_effector_link)
		self.run()

		self.arm.shift_pose_target(2, -0.4, self.end_effector_link)
		self.run()

	

	

	def run(self):
		# Get back the planned trajectory
		traj = self.arm.plan()

		# Scale the trajectory speed by a factor of self.speed
		new_traj = scale_trajectory_speed(traj, self.speed)

		# Execute the new trajectory
		self.arm.execute(new_traj)

	def run_plan(self,plan):
		# Scale the trajectory speed by a factor of 0.25
		new_traj = scale_trajectory_speed(plan, self.speed)

		# Execute the new trajectory
		self.arm.execute(new_traj)


	def run_at_speed(self,plan,i_speed):
		# Scale the trajectory speed by a factor of 0.25
		new_traj = set_trajectory_speed(plan, i_speed)

		# Execute the new trajectory
		self.arm.execute(new_traj)


	def back2home(self):
		self.arm.set_named_target('up')
		self.run()
		print "At Home"

       
	def end(self):
		# Shut down MoveIt cleanly
		moveit_commander.roscpp_shutdown()

		# Exit MoveIt
		moveit_commander.os._exit(0)

#-----------------set-------------------#
	def set_orientation(self,i_euler):
		start_pose = self.arm.get_current_pose(self.end_effector_link).pose
		mpose = deepcopy(start_pose)

		(x,y,z,w) = quaternion_from_euler(i_euler[0], i_euler[1], i_euler[2])

		mpose.orientation.x = x
		mpose.orientation.y = y
		mpose.orientation.z = z
		mpose.orientation.w = w

		self.arm.set_pose_target(mpose)
		#self.arm.plan()
		self.run()

	def set_pose(self,i_position,i_euler):
		start_pose = self.arm.get_current_pose(self.end_effector_link).pose
		mpose = deepcopy(start_pose)

		mpose.position.x = i_position[0]
		mpose.position.y = i_position[1]
		mpose.position.z = i_position[2]

		#euler = [0.0 1.57 0.0]
		(x,y,z,w) = quaternion_from_euler(i_euler[0], i_euler[1], i_euler[2])

		mpose.orientation.x = x
		mpose.orientation.y = y
		mpose.orientation.z = z
		mpose.orientation.w = w

		self.arm.set_pose_target(mpose)
		#self.arm.plan()
		self.run()
		rospy.sleep(1)

	def set_position(self,i_position):
		start_pose = self.arm.get_current_pose(self.end_effector_link).pose
		mpose = deepcopy(start_pose)

		mpose.position.x = i_position[0]
		mpose.position.y = i_position[1]
		mpose.position.z = i_position[2]


		self.arm.set_pose_target(mpose)
		#self.arm.plan()
		self.run()
		'''
		def set_pose(self):
		start_pose = self.arm.get_current_pose(self.end_effector_link).pose
		mpose = deepcopy(start_pose)

		mpose.position.x = -0.4
			mpose.position.y = 0.4
		mpose.position.z = 0.6

		#euler = [0.0 1.57 0.0]
		(x,y,z,w) = quaternion_from_euler(0,1.57,0)

		mpose.orientation.x = x
			mpose.orientation.y = y
			mpose.orientation.z = z
			mpose.orientation.w = w

		self.arm.set_pose_target(mpose)
		#self.arm.plan()
		self.run()
		'''
	def set_joints(self,joint_positions):
		#home joint = [0 -1.5707 0 -1.5707 0 0]

		self.arm.set_joint_value_target(joint_positions)
		self.run()

	def set_speed(self,i_speed):
		# 0.0 ~ 1.0
		self.speed = i_speed

	def set_constraints(self):
		pass
		'''
		# Store the current pose
		start_pose = self.arm.get_current_pose(self.end_effector_link)

		# Create a contraints list and give it a name
		constraints = Constraints()
		constraints.name = "Keep gripper horizontal"


		position_constraints = PositionConstraint()
		position_constraints.constraint_region.
		# Create an orientation constraint for the right gripper
		orientation_constraint = OrientationConstraint()
		orientation_constraint.header = start_pose.header
		orientation_constraint.link_name = self.arm.get_end_effector_link()
		orientation_constraint.orientation.w = 0.0
		orientation_constraint.absolute_x_axis_tolerance = 0.2
		orientation_constraint.absolute_y_axis_tolerance = 0.2
		orientation_constraint.absolute_z_axis_tolerance = 0.2
		orientation_constraint.weight = 1.0

		# Append the constraint to the list of contraints
		constraints.orientation_constraints.append(orientation_constraint)

		# Set the path constraints on the self.arm
		self.arm.set_path_constraints(constraints)
		'''
	#-----------------show-------------------#
	def show_pose(self):
		now_pose = self.arm.get_current_pose(self.end_effector_link).pose

		quaternion = (
			now_pose.orientation.x,
			now_pose.orientation.y,
			now_pose.orientation.z,
			now_pose.orientation.w)
		euler = euler_from_quaternion(quaternion)

		show_str = "arm_position = (" + str(now_pose.position.x) + "," + str(now_pose.position.y) + "," + str(now_pose.position.z)  + ")"
		rospy.loginfo(show_str)
		show_str = "arm_euler = (" + str(euler[0]) + "," + str(euler[1]) + "," + str(euler[2]) + ")"
		rospy.loginfo(show_str)
        

	def show_joints(self):
		joints = self.arm.get_current_joint_values()
		show_str = "arm_pose = (" + str(joints[0])+ ","+ str(joints[1]) + "," + str(joints[2]) + "," + str(joints[3]) + ","+ str(joints[4])+ str(joints[5]) +")"
		rospy.loginfo(show_str)


	def shift_x(self, i_x):
		self.arm.set_start_state_to_current_state()
		self.arm.shift_pose_target(0, i_x, self.end_effector_link)
		self.run()
		rospy.sleep(1)

	def shift_y(self, i_y):
		self.arm.set_start_state_to_current_state()
		self.arm.shift_pose_target(1, i_y, self.end_effector_link)
		self.run()
		rospy.sleep(1)

	def shift_z(self, i_z):
		self.arm.set_start_state_to_current_state()
		self.arm.shift_pose_target(2, i_z, self.end_effector_link)
		self.run()
		rospy.sleep(1)

	
if __name__ == "__main__":

	#moveit_commander.roscpp_initialize(sys.argv)

	#rospy.init_node('arm', anonymous=True)
	rospy.init_node('arm')

	print "init_node finish"
	# Initialize the move group for the right arm
	#global moveit_arm=moveit_commander.MoveGroupCommander('manipulator')

	mbot = ARM()
	mbot.set_speed(0.75)
	mbot.back2home()
	#mbot.show_pose()
	#mbot.shift_pose()
	#mbot.show_pose()
	#mbot.cartesian_path()
	
	#mbot.run_m()
	#mbot.show_joints()

	
	#mbot.set_pose()
	#mbot.cartesian_path()

	#5: yaw
	#6: roll
	#======set_joints_test======#
	target_joints = [0.0,0.0, 0.0,-1.57, 0.0, 0.0]
	#mbot.set_joints(target_joints)

	#======set_position_test======#
	#w_position = [0.0,0.4,0.6]
	#mbot.set_position(w_position)

	#======set_pose_tes======#
	print '------set_pose()------'
	w_position = [0.0, 0.4, 1.6]
	w_euler = [0.0, 1.57, 0.0]
	mbot.set_pose(w_position,w_euler)
	mbot.show_pose()
	#rospy.sleep(1)


	#======set_orientation_test======#
	#w_euler = [0.0,1.57,0.0]
	#mbot.set_orientation(w_euler)




	#======shift_y test======#
	print '------shift_y()------'
	mbot.shift_y(0.1)
	mbot.show_pose()
	#rospy.sleep(1)


	#======shift_z test======#
	print '------shift_z()------'
	#mbot.shift_z(-0.1)
	#mbot.show_pose()
	#rospy.sleep(1)



	mbot.show_pose()
	mbot.show_joints()


	mbot.end()

    
    
