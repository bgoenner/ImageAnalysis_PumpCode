# -*- coding: utf-8 -*-
"""
Spyder Editor

1This is a temporary script file.
"""

import sys
sys.path.append("./") 

def test(client, testNum):
    if testNum == 1:
        client.write_coil(0, 0)
        client.write_coil(2, 0)
        client.write_coil(4, 1)
        client.write_coil(6, 1)
    elif testNum == 2:
        client.write_coil(0, 1)
        client.write_coil(2, 0)
        client.write_coil(4, 1)
        client.write_coil(6, 0)
    elif  testNum == 3:
        client.write_coil(0, 0)
        client.write_coil(2, 1)
        client.write_coil(4, 0)
        client.write_coil(6, 1)
    elif  testNum == 4:
        client.write_coil(0, 1)
        client.write_coil(2, 1)
        client.write_coil(4, 0)
        client.write_coil(6, 0)
    elif  testNum == 0:
        client.write_coil(0, 1)
        client.write_coil(1, 1)    
        client.write_coil(2, 1)
        client.write_coil(3, 1)        
        client.write_coil(4, 1)
        client.write_coil(5, 1)
        client.write_coil(6, 1)
        client.write_coil(7, 1)
    elif  testNum == 5:
        client.write_coil(0, 0)
        client.write_coil(1, 0)
        client.write_coil(2, 0)
        client.write_coil(3, 0)
        client.write_coil(4, 0)
        client.write_coil(5, 0)
        client.write_coil(6, 0)
        client.write_coil(7, 0)        
        
def wait():
    i_cmd = 1
    while True:
        s = input('Input [{0:d}] '.format(i_cmd))
        i_cmd += 1
        n = len(s)
        if n > 0 and s == '1':
            test(client, 1)            
        elif n > 0 and s == '2':
            test(client, 2)
        elif n > 0 and s == '3':
            test(client, 3)
        elif n > 0 and s == '4':
            test(client, 4)
        elif n > 0 and s == '0':
            test(client, 0)
        elif n > 0 and s == '5':
            test(client, 5)
        elif n > 0 and s == 'q':
            break
        exec(s)

# main function

from pymodbus3.client.sync import ModbusTcpClient

client = ModbusTcpClient('192.168.0.102')

client.write_coils(0, [0]*40)

test(client, 4)

wait()

result = client.read_coils(1,1)
print(result.bits[0])
client.close()
