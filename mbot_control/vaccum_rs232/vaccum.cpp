/*
 * csll is for serial port (RS232)
 */

// %Tag(FULLTEXT)%
#include "ros/ros.h"
//#include "std_msgs/String.h"
#include "geometry_msgs/Twist.h"

#include "MotorControl.h"



//-------ROS variable-------//
const char *motion_topic_name = "/base_vel";


//====================//
//ROS motion callback //
//====================//
void motionCallback(const geometry_msgs::Twist::ConstPtr& msg)
{

    ROS_INFO("motor : x[%lf], y[%lf], yaw[%lf], cmd[%lf], cmd_2[%lf]", msg->linear.x,msg->linear.y, msg->angular.z, msg->angular.x, msg->angular.y);
    if(msg->angular.x==1){
	mcssl_motor_init();
	return;
    }else if(msg->angular.x==2){
	mcssl_motor_stop();
	return;
    }else if(msg->angular.x==3){
	int index = msg->angular.y;

	if(index <= 0 || index > 3){
		ROS_INFO("Error Point");
		return ;
	}	

	mcssl_base_position_index(index);
		
	return;
    }else{
	mcssl_base_spped(msg->linear.x, msg->linear.y,msg->angular.z);
    }
}



int main(int argc, char **argv)
{

    //RS232 init
    if(mcssl_init()<=0){
        return 0;
    }
    
    mcssl_motor_init();

    //ros init
    ros::init(argc, argv, "base");

   //node handle
    ros::NodeHandle n;

    //motion subscriber
    ros::Subscriber sub = n.subscribe(motion_topic_name, 1, motionCallback);

    //spin
    ros::spin();


    //RS232 finish
    mcssl_finish();

    return 0;
}
