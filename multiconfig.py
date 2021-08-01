import serial
import time
import json

import serial.tools.list_ports

def wait_for_new_port():
    ports_current = set()
    ports_previous = set()
    ports_initialized = False
    while True:
        ports_current = set([c.device for c in serial.tools.list_ports.comports()])
        ports_new = ports_current - ports_previous
        ports_previous = ports_current
        if any(ports_new) and ports_initialized:
            print()
            return(list(ports_new)[0])
        ports_initialized = True
        print('.', end='')
        time.sleep(0.5)
        

def get_mcu_id(port_name):
    mcu_id = None
    with serial.Serial(port_name, 115200, timeout=1) as ser:
        ser.write(b'#cli\r\n')
        time.sleep(1)
        ser.reset_input_buffer()
        ser.write(b'mcu_id\r\n')
        ser.readline()
        while True:
            line = ser.readline()
            if not line:
                break
            else:
                s = line.decode()
                if s.startswith('mcu_id'):
                    mcu_id = s.strip().split()[1]
    return mcu_id
                

with open('config.json') as f:
    config = json.load(f)

while True:
    port = wait_for_new_port()
    print('Device detected: {0}. Would you like to get ID?'.format(port))
    input()
    mcu_id = get_mcu_id(port)
    print('Device ID: {0}'.format(mcu_id))
    print(mcu_id in config.keys())



#with open('config.json') as f:
#    students = json.load(f)



