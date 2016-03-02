#include <ros/ros.h>
#include <actionlib/client/simple_action_client.h>
#include <actionlib/client/terminal_state.h>
#include <vision/vision_cmdAction.h>

std::string testID[4] = {"crayola_64_ct","chortbread","oreo_mega_stuf","chocopie"};

int main (int argc, char **argv)
{
  ros::init(argc, argv, "simVision_client");

  // create the action client
  // true causes the client to spin its own thread
  actionlib::SimpleActionClient<vision::vision_cmdAction> ac("simVision_server", true);

  ROS_INFO("Waiting for action server to start.");
  // wait for the action server to start
  ac.waitForServer(); //will wait for infinite time

  ROS_INFO("Action server started, sending goal.");
  // send a goal to the action
  vision::vision_cmdGoal goal;
  goal.goal_obj = testID[3];
  goal.bin_content = "crayola_64_ct";//bin_B's contents : "potato_chips","crayola_64_ct"
  ac.sendGoal(goal);

  //wait for the action to return
  bool finished_before_timeout = ac.waitForResult(ros::Duration(30.0));

  if (finished_before_timeout)
  {
    actionlib::SimpleClientGoalState state = ac.getState();
    ROS_INFO("Action finished: %s",state.toString().c_str());
  }
  else
    ROS_INFO("Action did not finish before the time out.");

  //exit
  return 0;
}
