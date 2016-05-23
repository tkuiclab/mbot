import json
#from enum import Enum

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



class MBot_Strategy(object):

    def __init__(self,name):
        self.work_order=[]
        self.bin_contents=[]
        self.bin_out_joint=[]
        self.set_bin_out_joint()


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

        for target in j['work_order']:
            print 'target_bin = ' + target['bin'] + ', pick_item = '+target['item']
    def go_bin_out(self, bin):
        if bin == Bin.Bin_A:
            print self.bin_out_joint[Bin.Bin_A]
        elif bin == Bin.Bin_B:
            print self.bin_out_joint[Bin.Bin_B]
        elif bin == Bin.Bin_C:
            print self.bin_out_joint[Bin.Bin_C]
        elif bin == Bin.Bin_D:
            print self.bin_out_joint[Bin.Bin_D]
        elif bin == Bin.Bin_E:
            print self.bin_out_joint[Bin.Bin_E]
        elif bin == Bin.Bin_F:
            print self.bin_out_joint[Bin.Bin_F]


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
