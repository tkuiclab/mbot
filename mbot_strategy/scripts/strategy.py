import json

APC_JSON_File_Name = "apc.json"

if __name__ == "__main__":
    f = open(APC_JSON_File_Name, 'r')
    f_data = f.read()
    f.close()
    #print f_data
    j = json.loads(f_data)
    print j['bin_contents']['bin_A']



