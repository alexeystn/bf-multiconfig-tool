import serial
import time
import json
import sys
import os
import random

import serial.tools.list_ports

ports_already_used = []

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
    try:
        ser = serial.Serial(port, 115200, timeout=1)
    except:
        print('Cannot open serial port')
        return None
    else:
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
        return mcu_id


def create_default_settings():
    s = {}
    s['path'] = 'C:/Users/Pilot/diff.txt'
    s['setups'] = {}
    names = ['White', 'Blue', 'Red']
    for n in names:
        mcu_id = '00'+'{0:.22f}'.format(random.random())[2:]
        s['setups'][mcu_id] = []
        s['setups'][mcu_id].append('set name = {0}'.format(n))
        if n == 'Red':
            s['setups'][mcu_id] += ['resource motor 1 A08',
                                 'set ibata_scale = 120']
    return s


def load_settings():
    settings_filename = 'settings.json'
    settings = {}
    try:
        f = open(settings_filename, 'r')
    except:
        print('Prepare "' + settings_filename + '" before using this app')
        f = open(settings_filename, 'w')
        settings = create_default_settings()
        json.dump(settings, f, indent=2)
        f.close()
        input()
        sys.exit(0)
    try:
        settings = json.load(f)
    except Exception as exc:
        print('Error: incorrect JSON file')
        print(exc)
        input()
        sys.exit(0)
    return settings


def load_diff(diff_filename):
    diff = []
    try:
        f = open(diff_filename, 'r')
    except:
        print('"' + diff_filename + '" not found')
        input()
        sys.exit(0)
    for line in f:
        line = line.strip()
        if len(line) > 0 and not line.startswith('#'):
            diff.append(line)
    f.close()
    if len(diff) == 0:
        print('Diff file is empty')
        input()
        sys.exit(0)
    if diff[-1] != 'save':
        print('Diff file does not end with "save" command')
        input()
        sys.exit(0)
    return diff


def get_line_timeout(ser):
    t = time.time() + 1.0
    while time.time() < t:
        try:
            get_line()
        except:
            break


def get_line(ser):
    s = b''
    while ser.in_waiting:
        a = ser.read()
        s += a
    s = s.decode()
    s = s.replace('\r\n\r\n', '\r\n')
    if not os.name == 'nt':
        s = s.replace('\r','')
    print(s, end='')
    time.sleep(0.01)


def upload_diff(diff, port):
    try:
        ser = serial.Serial(port, 115200, timeout=1)
    except:
        print('Cannot open serial port')
    else:
        ser.write(b'#cli\r\n')
        time.sleep(1)
        ser.reset_input_buffer()
        for line_out in diff:
            ser.write(line_out.encode() + b'\r\n')
            get_line(ser)
        get_line_timeout(ser)
        print()


def clear():
    if os.name == 'nt': # for windows
        os.system('cls')
    else: # for mac and linux(here, os.name is 'posix')
        os.system('clear')


clear()
settings = load_settings()
diff = load_diff(settings['path'])
custom_line = '############# CUSTOM SETTINGS #############'


while True:
    port = wait_for_new_port()
    print('Device detected: {0}'.format(port))
    print('Press Enter to read ID', end='')
    input()
    mcu_id = get_mcu_id(port)
    if not mcu_id:
        print()
        continue
    print('MCU ID: {0}'.format(mcu_id), end = '')
    diff_current = diff.copy()
    if mcu_id in settings['setups'].keys():
        print(' - found')
        for s in settings['setups'][mcu_id]:
            print('   ', s)
        print('Press Enter to load CUSTOM diff', end='')
        input()
        diff_current.insert(-1, custom_line)
        for s in settings['setups'][mcu_id]:
            diff_current.insert(-1, s)
    else:
        print(' - not found')
        print('Press Enter to load DEFAULT diff', end='')
        input()
    upload_diff(diff_current, port)
    print()

