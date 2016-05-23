import json

APC_JSON_File_Name = "apc.json"

if __name__ == "__main__":
    f = open(APC_JSON_File_Name, 'r')
    f_data = f.read()
    f.close()
    #print f_data
    j = json.loads(f_data)
    bin=[j['bin_contents']['bin_A'],j['bin_contents']['bin_B'],j['bin_contents']['bin_C'],j['bin_contents']['bin_D'],j['bin_contents']['bin_E'],j['bin_contents']['bin_F']]
    for x in bin:
        print x
    print j['work_order']







