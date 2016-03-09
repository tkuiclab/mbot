/*
File: fake_stow_vision.cpp
Author: Chien-Ming Lin <jianming1481@gmail.com>
Created on: 	  2016/03/06	
Modified on:      

Description: Vision simulation for Amazon Picking Challenge 2016
    Action_Server: fake_stow_vision
    Action_Client: 
*/
#include <ros/ros.h>
#include <ros/console.h>
#include <actionlib/server/simple_action_server.h>
#include <vision/vision_cmdAction.h>
#include <geometry_msgs/Twist.h>

int item_num;

class vision_cmdAction
{
protected:

  ros::NodeHandle nh_;
  // NodeHandle instance must be created before this line. Otherwise strange error may occur.
  actionlib::SimpleActionServer<vision::vision_cmdAction> as_; 
  std::string action_name_;
  // create messages that are used to published feedback/result
  vision::vision_cmdFeedback feedback_;
  vision::vision_cmdResult result_;
//  vision::vision_cmdGoal goal_;
  std::string goal_;
  ros::Subscriber sub_;

public:

  vision_cmdAction(std::string name) :
    as_(nh_, name, false),//, boost::bind(&vision_cmdAction::executeCB, this, _1)
    action_name_(name)
  {
    //register the goal and feeback callbacks
    as_.registerGoalCallback(boost::bind(&vision_cmdAction::goalCB, this));
    as_.registerPreemptCallback(boost::bind(&vision_cmdAction::preemptCB, this));

	item_num = 0;
    //subscribe to the data topic of interest
    //sub_ = nh_.subscribe("/random_number", 1, &vision_cmdAction::analysisCB, this);

    as_.start();
  }

  ~vision_cmdAction(void)
  {
  }
  void goalCB()
  {
	// accept the new goal
	goal_ = as_.acceptNewGoal()->goal_obj;
	std::cout<<"goalCB(): "<<goal_<<std::endl;

	// feedback
	feedback_.status = "Vision status";
	as_.publishFeedback(feedback_);
	geometry_msgs::Twist twist;
	switch(item_num)
	{
		case 0:
			twist.linear.x = 0.02;
			twist.linear.y = 0.23;
			twist.linear.z = -0.03;
			twist.angular.x = 0;
			twist.angular.y = 0;
			twist.angular.z = 0;
			result_.objPose = twist;
			result_.objID = "A";
			ROS_INFO("%s : Succeeded",action_name_.c_str());
			as_.setSucceeded(result_);
			break;
		case 1:
			twist.linear.x = 0.02;
			twist.linear.y = 0.23;
			twist.linear.z = -0.03;
			twist.angular.x = 0;
			twist.angular.y = 0;
			twist.angular.z = 0;
			result_.objPose = twist;
			result_.objID = "B";
			ROS_INFO("%s : Succeeded",action_name_.c_str());
			as_.setSucceeded(result_);
			break;
		case 2:
			twist.linear.x = 0.02;
			twist.linear.y = 0.23;
			twist.linear.z = -0.03;
			twist.angular.x = 0;
			twist.angular.y = 0;
			twist.angular.z = 0;
			result_.objPose = twist;
			result_.objID = "C";
			ROS_INFO("%s : Succeeded",action_name_.c_str());
			as_.setSucceeded(result_);
			break;
		case 3:
			twist.linear.x = 0.02;
			twist.linear.y = 0.23;
			twist.linear.z = -0.03;
			twist.angular.x = 0;
			twist.angular.y = 0;
			twist.angular.z = 0;
			result_.objPose = twist;
			result_.objID = "D";
			ROS_INFO("%s : Succeeded",action_name_.c_str());
			as_.setSucceeded(result_);
			break;
		case 4:
			twist.linear.x = 0.02;
			twist.linear.y = 0.23;
			twist.linear.z = -0.03;
			twist.angular.x = 0;
			twist.angular.y = 0;
			twist.angular.z = 0;
			result_.objPose = twist;
			result_.objID = "E";
			ROS_INFO("%s : Succeeded",action_name_.c_str());
			as_.setSucceeded(result_);
			break;
		case 5:
			twist.linear.x = 0.02;
			twist.linear.y = 0.23;
			twist.linear.z = -0.03;
			twist.angular.x = 0;
			twist.angular.y = 0;
			twist.angular.z = 0;
			result_.objPose = twist;
			result_.objID = "F";
			ROS_INFO("%s : Succeeded",action_name_.c_str());
			as_.setSucceeded(result_);
			break;
		case 6:
			twist.linear.x = 0.02;
			twist.linear.y = 0.23;
			twist.linear.z = -0.03;
			twist.angular.x = 0;
			twist.angular.y = 0;
			twist.angular.z = 0;
			result_.objPose = twist;
			result_.objID = "G";
			ROS_INFO("%s : Succeeded",action_name_.c_str());
			as_.setSucceeded(result_);
			break;
		case 7:
			twist.linear.x = 0.02;
			twist.linear.y = 0.23;
			twist.linear.z = -0.03;
			twist.angular.x = 0;
			twist.angular.y = 0;
			twist.angular.z = 0;
			result_.objPose = twist;
			result_.objID = "H";
			ROS_INFO("%s : Succeeded",action_name_.c_str());
			as_.setSucceeded(result_);
			break;
		case 8:
			twist.linear.x = 0.02;
			twist.linear.y = 0.23;
			twist.linear.z = -0.03;
			twist.angular.x = 0;
			twist.angular.y = 0;
			twist.angular.z = 0;
			result_.objPose = twist;
			result_.objID = "I";
			ROS_INFO("%s : Succeeded",action_name_.c_str());
			as_.setSucceeded(result_);
			break;
		case 9:
			twist.linear.x = 0.02;
			twist.linear.y = 0.23;
			twist.linear.z = -0.03;
			twist.angular.x = 0;
			twist.angular.y = 0;
			twist.angular.z = 0;
			result_.objPose = twist;
			result_.objID = "J";
			ROS_INFO("%s : Succeeded",action_name_.c_str());
			as_.setSucceeded(result_);
			break;
		case 10:
			twist.linear.x = 0.02;
			twist.linear.y = 0.23;
			twist.linear.z = -0.03;
			twist.angular.x = 0;
			twist.angular.y = 0;
			twist.angular.z = 0;
			result_.objPose = twist;
			result_.objID = "K";
			ROS_INFO("%s : Succeeded",action_name_.c_str());
			as_.setSucceeded(result_);
			break;
		case 11:
			twist.linear.x = 0.02;
			twist.linear.y = 0.23;
			twist.linear.z = -0.03;
			twist.angular.x = 0;
			twist.angular.y = 0;
			twist.angular.z = 0;
			result_.objPose = twist;
			result_.objID = "L";
			ROS_INFO("%s : Succeeded",action_name_.c_str());
			as_.setSucceeded(result_);
			break;
		default:
			as_.setAborted(result_);
			break;
	}
	item_num++;
	if(item_num>=12)
		item_num=0;
  }

  void preemptCB()
  {
    ROS_INFO("%s: Preempted", action_name_.c_str());
    // set the action state to preempted
    as_.setPreempted();
  }
};

int main(int argc, char** argv)
{
  ros::init(argc, argv, "fake_stow_vision");

  vision_cmdAction simVision_server(ros::this_node::getName());
  ros::spin();

  return 0;
}
