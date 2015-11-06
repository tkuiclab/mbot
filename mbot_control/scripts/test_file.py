#!/usr/bin/env python

Teach_File_Name = "teach_mode.json"

if __name__ == "__main__":


    f = open(Teach_File_Name, 'w')
    f.write("hello\ntest 2222 you")
    f.close()
    '''
    f = open(Teach_File_Name, 'r')
    r_data = f.read()
    print r_data
    f.close()
    '''