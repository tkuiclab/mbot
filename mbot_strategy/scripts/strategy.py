import roslib
roslib.load_manifest('mbot_control')
import actionlib
import mbot_control.msg
import geometry_msgs.msg
from geometry_msgs.msg import Twist
import json

APC_JSON_File_Name = "apc.json"
MBot_Control_Action_Name = "mbot_control"


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
    Init_Pose = [0,0,0,0,0,0]
    Bin_Up    = [0,1,0,0,0,0]
    Bin_Mid   = [0,2,0,0,0,0]
    Bin_Down  = [0,0,0,0,0,0]





class MBot_Strategy(object):

    def __init__(self,name):
        self.work_order=[]
        self.bin_contents=[]
        self.bin_out_joint=[]
        self.set_bin_out_joint()
        self.mbot_client = actionlib.SimpleActionClient(MBot_Control_Action_Name, mbot_control.msg.TeachCommandListAction)
        self.mbot_client.wait_for_server()



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
        f = open(APC_JSON_File_Name, 'r')
        f_data = f.read()
        f.close()
        j = json.loads(f_data)
        self.work_order = j['work_order']
        self.bin_contents = j['bin_contents']

        #for target in j['work_order']:
        #    print 'target_bin = ' + target['bin'] + ', pick_item = '+target['item']

    def go_bin_out(self, bin):
        #need variable
        cmd_list = []
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


        #cmd_0 = mbot_control.msg.TeachCommand()
        #cmd_0.cmd = "JointPosition"

    def run(self):
        print 'in run'




if __name__ == "__main__":
    #run()
    #parseJSON()
    #print work_order
    s = MBot_Strategy('aa')
    s.parseJSON()
    s.run()
    s.go_bin_out(Bin.Bin_B)
