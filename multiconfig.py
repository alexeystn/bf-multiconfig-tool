import serial
import time
import json
import sys

import serial.tools.list_ports

def wait_for_new_port():
    ports_current = set()
    ports_previous = set()
    ports_initialized = False
    print('Connect flight controller to your PC ', end='')
    while True:
        ports_current = set([c.device for c in serial.tools.list_ports.comports()])
        ports_new = ports_current - ports_previous
        ports_previous = ports_current
        if any(ports_new) and ports_initialized:
            print()
            return(list(ports_new)[0])
        ports_initialized = True
        print('.', end='')
        sys.stdout.flush()
        time.sleep(1)
        

def get_mcu_id(port_name):
    mcu_id = None
    name = None
    with serial.Serial(port_name, 115200, timeout=1) as ser:
        ser.write(b'#cli\r\n')
        time.sleep(0.5)
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
                    break
        ser.write(b'get name\r\n')
        ser.readline()
        while True:
            line = ser.readline()
            if not line:
                break
            else:
                s = line.decode()
                if s.startswith('name ='):
                    name = s.strip()[7:]
                    break
    return mcu_id, name
                

def load_settings():
    settings = {}
    key = None
    with open('settings.txt') as f:
        for line in f:
            if not (line.startswith('\t') or line.startswith(' ')):
                key = line.strip()
                settings[key] = []
            elif len(line.strip()) > 0:
                settings[key].append(line.strip())
    return settings


def load_diff():
    diff = []
    with open('diff.txt') as f:
        for line in f:
            line = line.strip()
            if len(line) > 0 and not line.startswith('#'):
                diff.append(line)
    if diff[-1] != 'save':
        print('Diff file does not end with "save" command')
    return diff


#settings = load_settings()
#diff = load_diff()

while True:
    port = wait_for_new_port()
    print('Device detected: {0}'.format(port))
    print('Press Enter to read Name and ID', end='')
    input()
    mcu_id, name = get_mcu_id(port)
    print('MCU ID: {0}'.format(mcu_id))
    print('Name: {0}'.format(name))
    print()
    #print(mcu_id in config.keys())


#with open('config.json') as f:
#    students = json.load(f)



