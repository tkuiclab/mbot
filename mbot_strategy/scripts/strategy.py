#!/usr/bin/env python

import roslib
import actionlib
import mbot_control.msg
import geometry_msgs.msg
from geometry_msgs.msg import Twist
import json
import rospy
import rospkg


MBot_Control_Action_Name = "mbot_control"
#const of config package name
Config_Pkg_Name = "mbot_config"
APC_JSON_File_Name = "apc.json"

class Bin:
    Bin_A = 'Bin_A'
    Bin_B = 'Bin_B'
    Bin_C = 'Bin_C'
    Bin_D = 'Bin_D'
    Bin_E = 'Bin_E'
    Bin_F = 'Bin_F'
    Bin_Up = 'Bin_Up'
    Bin_Down = 'Bin_Down'

class MBot_Joint:
    Init_Pose      = [3.1415698528289795,-1.5708050727844238,                 0,-1.5708013772964478,-1.5708670616149902,0]
 #   Bin_Up         = [3.1206839084625244,-0.3524255156517029,-1.662269115447998,-1.1624271869659424,-1.6004770994186401,0]
    Bin_Up         = [3.089456558227539,-1.842522382736206,1.6045348644256592,-2.919060468673706,-1.5979101657867432,-0.0006531999097205698]
    Bin_Up_Vision  = [3.0256364345550537,-1.8619954586029053,1.3036588430404663,-2.2293457984924316,-1.5384762287139893,-0.000050249571359017864]

    Bin_Mid   = [3.089456558227539,-1.770250678062439,2.2311136722564697,-3.617886781692505,-1.5979101657867432,-0.0006531999097205698]
    Bin_Mid_Vision   = [3.0256364345550537,-2.0109002590179443,2.0640923976898193,-2.8409671783447266,-1.5384762287139893,-0.0000340468977810815]

    Bin_Down  = [3.0886847972869873,-1.115041971206665,2.4834556579589844,-4.51420783996582,-1.5775349140167236,-0.0006531999097205698]
    Bin_Down_Vision  = [3.0256364345550537,-1.582160472869873,2.5714526176452637,-3.777014970779419,-1.5384600162506104,-0.000050249571359017864]

    Put_1     = [2.760157823562622,-0.6895775198936462,-1.8603730201721191,-0.6046839952468872 ,-0.38617709279060364,0.02900535985827446]
    Put_2     = [2.095847368240356,-1.1780940294265747,-2.1087863445281982, 0.10603345185518265, 1.1103659868240356 ,0.08324931561946869]





class MBot_Strategy(object):

    def __init__(self,name):
        self.work_order=[]
        self.bin_contents=[]
        self.bin_out_joint=[]
        self.set_bin_out_joint()
        self.control_client = actionlib.SimpleActionClient(MBot_Control_Action_Name, mbot_control.msg.TeachCommandListAction)
        self.control_client.wait_for_server()
        self.parseJSON()


    def set_bin_out_joint(self):
        self.bin_out_joint={
            Bin.Bin_A: [0,0,0,0,0,0],
            Bin.Bin_B: [0,1,0,0,0,0],
            Bin.Bin_C: [0,2,0,0,0,0],
            Bin.Bin_D: [0,3,0,0,0,0],
            Bin.Bin_E: [0,4,0,0,0,0],
            Bin.Bin_F: [0,5,0,0,0,0],
            Bin.Bin_Up: [0,0,0,0,0,0],
            Bin.Bin_Down: [0,1,0,0,0,0]
        }

    #parse json to self.work_order & self.bin_contents
    def parseJSON(self):
        #get json path
        rospack = rospkg.RosPack()
        json_path = rospack.get_path(Config_Pkg_Name) + "/" +  APC_JSON_File_Name

        #open file
        f = open(json_path, 'r')
        f_data = f.read()
        f.close()
        j = json.loads(f_data)
        #stroe data to work_order & bin_contents
        self.work_order = j['work_order']
        self.bin_contents = j['bin_contents']

        #show info
        rospy.loginfo('Parse ' + APC_JSON_File_Name + ' finish');
        #for target in j['work_order']:
        #    print 'target_bin = ' + target['bin'] + ', pick_item = '+target['item'


    def go_init(self):
        rospy.loginfo('(Strategy) Go Init Pose')

        m_cmd_list = []
        cmd_0 = mbot_control.msg.TeachCommand()
        cmd_0.cmd = "Joint"
        cmd_0.joint_position = MBot_Joint.Init_Pose
        m_cmd_list.append(cmd_0)

        self.send_gaol(m_cmd_list)


    def go_bin_out(self, bin):
        rospy.loginfo('(Strategy) Go Bin Out:'+str(bin))

        #need variable
        m_cmd_list = []
        base_cmd = ''
        joint = []

        #switch all case
        if bin == Bin.Bin_A:
            base_cmd = 'Base_Pos_Index_1'
            joint = MBot_Joint.Bin_Up
        elif bin == Bin.Bin_D:
            base_cmd = 'Base_Pos_Index_1'
            joint = MBot_Joint.Bin_Mid
        elif bin == Bin.Bin_B:
            base_cmd = 'Base_Pos_Index_2'
            joint = MBot_Joint.Bin_Up
        elif bin == Bin.Bin_E:
            base_cmd = 'Base_Pos_Index_2'
            joint = MBot_Joint.Bin_Mid
        elif bin == Bin.Bin_C:
            base_cmd = 'Base_Pos_Index_3'
            joint = MBot_Joint.Bin_Up
        elif bin == Bin.Bin_F:
            base_cmd = 'Base_Pos_Index_3'
            joint = MBot_Joint.Bin_Mid

        print 'base_cmd = ' +base_cmd + ', joint='+str(joint)


        cmd_0 = mbot_control.msg.TeachCommand()
        cmd_0.cmd = base_cmd
        cmd_0.joint_position = joint
        m_cmd_list.append(cmd_0)

        cmd_1 = mbot_control.msg.TeachCommand()
        cmd_1.cmd = "Joint"
        cmd_1.joint_position = joint
        m_cmd_list.append(cmd_1)

        self.send_gaol(m_cmd_list)


    def pick_obj(self,y,x,z):
        rospy.loginfo('(Strategy) Pick Object')

        #check input data
        if x < 0 or z <0 :
            rospy.logerr('pick_obj say error x(' + x + ') or y(' + y + ')')
            return
        #init list
        m_cmd_list = []

        #cmd_0 Shift_Y
        cmd_0 = mbot_control.msg.TeachCommand()
        cmd_0.cmd = 'Shift_Y'
        cmd_0.pose.linear.y = y
        m_cmd_list.append(cmd_0)


        #cmd_1 Shift_X(IN)
        cmd_1 = mbot_control.msg.TeachCommand()
        cmd_1.cmd = 'Shift_X'
        cmd_1.pose.linear.x = x
        m_cmd_list.append(cmd_1)

        #cmd_2 Shift_Z(DOWN)
        cmd_2 = mbot_control.msg.TeachCommand()
        cmd_2.cmd = 'Shift_Z'
        cmd_2.pose.linear.z = -z
        m_cmd_list.append(cmd_2)

        #cmd_3 Vaccum
        cmd_3 = mbot_control.msg.TeachCommand()
        cmd_3.cmd = 'Vaccum'
        cmd_3.vaccum = True
        m_cmd_list.append(cmd_3)

        #cmd_4 Shift_Z(UP)
        cmd_4 = mbot_control.msg.TeachCommand()
        cmd_4.cmd = 'Shift_Z'
        cmd_4.pose.linear.z = z
        m_cmd_list.append(cmd_4)

        #cmd_5 Shift_X(OUT)
        cmd_5 = mbot_control.msg.TeachCommand()
        cmd_5.cmd = 'Shift_X'
        cmd_5.pose.linear.x = -x
        m_cmd_list.append(cmd_5)

        self.send_gaol(m_cmd_list)


    def put_obj(self):
        rospy.loginfo('(Strategy) Put Object')

        #init list
        m_cmd_list = []

        #cmd_0 Put_1
        cmd_0 = mbot_control.msg.TeachCommand()
        cmd_0.cmd = "Joint"
        cmd_0.joint_position = MBot_Joint.Put_1
        m_cmd_list.append(cmd_0)

        #cmd_1 Put_1
        cmd_1 = mbot_control.msg.TeachCommand()
        cmd_1.cmd = "Joint"
        cmd_1.joint_position = MBot_Joint.Put_2
        m_cmd_list.append(cmd_1)

        #cmd_2 Shift_Z(DOWN)
        cmd_2 = mbot_control.msg.TeachCommand()
        cmd_2.cmd = 'Shift_Z'
        cmd_2.pose.linear.z = -0.15
        m_cmd_list.append(cmd_2)

        #cmd_3 Vaccum Release
        cmd_3 = mbot_control.msg.TeachCommand()
        cmd_3.cmd = 'Vaccum'
        cmd_3.vaccum = False
        m_cmd_list.append(cmd_3)

        #cmd_4 Shift_Z(UP)
        cmd_4 = mbot_control.msg.TeachCommand()
        cmd_4.cmd = 'Shift_Z'
        cmd_4.pose.linear.z = 0.15
        m_cmd_list.append(cmd_4)

        self.send_gaol(m_cmd_list)

    def send_gaol(self,i_cmd_list):
        #send goal
        goal = mbot_control.msg.TeachCommandListGoal(cmd_list=i_cmd_list)
        self.control_client.send_goal(goal,feedback_cb = self.control_feedback_cb, done_cb=self.control_done_cb )
        self.control_client.wait_for_result()


    def run_pick(self):
        print 'in run_pick'
        #target_bin = ""
        #target_obj = ""
        for target in self.work_order:
            rospy.loginfo('(Strategy) Pick Object [' + target['item'] + '] in ['+ target['bin'] +']')

            self.go_init()
            self.go_bin_out(target['bin'])
            self.pick_obj(0,0.35,0.09)
            self.put_obj()


    def control_feedback_cb(self,fb_data):
        rospy.loginfo("(Strategy) Feedback: " + fb_data.status)

    def control_done_cb(self,goal_status,get_result):
        #rospy.loginfo("(Strategy) Done -> goal_status=" + str(goal_status) +' ,get_result = '+ get_result.notify)
        rospy.loginfo('(Strategy) Done -> Result = '+ get_result.notify)





def myhook():
  print "mbot_strategy:strategy run finish!"


if __name__ == "__main__":

    try:
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
        rospy.init_node('mbot_strategy')

        s = MBot_Strategy('mbot_strategy')
        s.run_pick()
        #s.go_init()

        rospy.on_shutdown(myhook)

    except rospy.ROSInterruptException:
        print "program interrupted before completion"


