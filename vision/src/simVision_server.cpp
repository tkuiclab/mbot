/*
File: strategy.py
Author: Tsung-Han Chang <zxc455233@gmail.com>
Created on:
Modified on:      2016/03/01 22:00 ------> determine action goal's goal_obj to result the obj's Pose

Description: Vision simulation for Amazon Picking Challenge 2016
    Action_Server: simVision_server
    Action_Client: simVision_client
*/
#include <ros/ros.h>
#include <ros/console.h>
#include <actionlib/server/simple_action_server.h>
#include <vision/vision_cmdAction.h>
#include <geometry_msgs/Twist.h>

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

	// determine goal.objID and result it's ID and Pose
	geometry_msgs::Twist twist;
	if(goal_ == "crayola_64_ct"){//bin_B
		twist.linear.x = 0.02;
		twist.linear.y = 0.23;
		twist.linear.z = -0.03;
		twist.angular.x = 0;
		twist.angular.y = 0;
		twist.angular.z = 0;
		result_.objPose = twist;
		result_.objID = goal_;
		ROS_INFO("%s : Succeeded",action_name_.c_str());
		// set the action state to succeeded
		as_.setSucceeded(result_);
	}else if(goal_ == "chortbread"){//bin_E
		twist.linear.x = 0.04;
		twist.linear.y = 0.29;
		twist.linear.z = -0.02;
		twist.angular.x = 0;
		twist.angular.y = 0;
		twist.angular.z = 0;
		result_.objPose = twist;
		result_.objID = goal_;
		ROS_INFO("%s : Succeeded",action_name_.c_str());
		// set the action state to succeeded
		as_.setSucceeded(result_);
	}else if(goal_ == "oreo_mega_stuf"){//bin_H
		twist.linear.x = 0.00;
		twist.linear.y = 0.24;
		twist.linear.z = -0.05;
		twist.angular.x = 0;
		twist.angular.y = 0;
		twist.angular.z = 0;
		result_.objPose = twist;
		result_.objID = goal_;
		ROS_INFO("%s : Succeeded",action_name_.c_str());
		// set the action state to succeeded
		as_.setSucceeded(result_);
	}else if(goal_ == "chocopie"){//bin_K
		twist.linear.x = 0.00;
		twist.linear.y = 0.23;
		twist.linear.z = -0.03;
		twist.angular.x = 0;
		twist.angular.y = 0;
		twist.angular.z = 0;
		result_.objPose = twist;
		result_.objID = goal_;
		ROS_INFO("%s : Succeeded",action_name_.c_str());
		// set the action state to succeeded
		as_.setSucceeded(result_);
	}else{
		ROS_INFO("%s: Aborted", action_name_.c_str());
		//set the action state to aborted
		as_.setAborted(result_);
	}
  }

  void preemptCB()
  {
    ROS_INFO("%s: Preempted", action_name_.c_str());
    // set the action state to preempted
    as_.setPreempted();
  }

  void analysisCB()
  {
    // make sure that the action hasn't been canceled
    if (!as_.isActive())
      return;

    feedback_.status = "Neet's status";
    as_.publishFeedback(feedback_);

    if(1) 
    {
	geometry_msgs::Twist twist;
	twist.linear.x = 0.02;
	twist.linear.y = 0.23;
	twist.linear.z = -0.03;
	twist.angular.x = 0;
	twist.angular.y = 0;
	twist.angular.z = 0;

      result_.objID = "orea";
      result_.objPose = twist;

      if(0)
      {
        ROS_INFO("%s: Aborted", action_name_.c_str());
        //set the action state to aborted
        as_.setAborted(result_);
      }
      else 
      {
        ROS_INFO("%s: Succeeded", action_name_.c_str());
        // set the action state to succeeded
        as_.setSucceeded(result_);
      }
    }
  }

/*
  void executeCB(const vision::vision_cmdGoalConstPtr &goal)
  {
    // helper variables
    ros::Rate r(1000);
    bool success = true;

    // push_back the status for the feedback_ status
	feedback_.status = "Vision is be ready.";

    // publish info to the console for the user
	ROS_INFO("%s : status is '%s'",action_name_.c_str(),feedback_.status.c_str());

    // start executing the action

      feedback_.status = "Vision's status";
      // publish the feedback
      as_.publishFeedback(feedback_);
      // this sleep is not necessary, the sequence is computed at 1 Hz for demonstration purposes
      r.sleep();

    if(success)
    {
	geometry_msgs::Twist twist;
	std::cout<<"Goal_obj: "<<goal_.goal_obj<<std::endl;
	if(goal_.goal_obj == "crayola_64_ct"){//bin_B
		twist.linear.x = 0.02;
		twist.linear.y = 0.23;
		twist.linear.z = -0.03;
		twist.angular.x = 0;
		twist.angular.y = 0;
		twist.angular.z = 0;
		result_.objPose = twist;
		result_.objID = goal_.goal_obj;
		ROS_INFO("%s : Succeeded",action_name_.c_str());
	}else if(goal_.goal_obj == "chortbread"){//bin_E
		twist.linear.x = 0.04;
		twist.linear.y = 0.29;
		twist.linear.z = -0.02;
		twist.angular.x = 0;
		twist.angular.y = 0;
		twist.angular.z = 0;
		result_.objPose = twist;
		result_.objID = goal_.goal_obj;
		ROS_INFO("%s : Succeeded",action_name_.c_str());
	}else if(goal_.goal_obj == "oreo_mega_stuf"){//bin_H
		twist.linear.x = 0.00;
		twist.linear.y = 0.24;
		twist.linear.z = -0.05;
		twist.angular.x = 0;
		twist.angular.y = 0;
		twist.angular.z = 0;
		result_.objPose = twist;
		result_.objID = goal_.goal_obj;
		ROS_INFO("%s : Succeeded",action_name_.c_str());
	}else if(goal_.goal_obj == "chocopie"){//bin_K
		twist.linear.x = 0.00;
		twist.linear.y = 0.23;
		twist.linear.z = -0.03;
		twist.angular.x = 0;
		twist.angular.y = 0;
		twist.angular.z = 0;
		result_.objPose = twist;
		result_.objID = goal_.goal_obj;
		ROS_INFO("%s : Succeeded",action_name_.c_str());
	}
      // set the action state to succeeded
      as_.setSucceeded(result_);
    }
  }*/
};

int main(int argc, char** argv)
{
  ros::init(argc, argv, "simVision_server");

  vision_cmdAction simVision_server(ros::this_node::getName());
  ros::spin();

  return 0;
}
