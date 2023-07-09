import select
import sys
import msvcrt
import _winapi
import os

def getKey():
    while True:
        if msvcrt.kbhit():
            key_byte = msvcrt.getch()
            key = key_byte.decode('ascii')
            if ord(key) == 27: # ESC
                break
            print(key)

def getLine():
    buf = []
    while True:
        if msvcrt.kbhit():
            key_byte = msvcrt.getch()
            key = key_byte.decode('ascii')
            if ord(key) == 27: # ESC
                break
            buf.append(key)
            if key == '\r':
                string = ''.join(buf)
                print(string)
                buf = []
            # print(key)

def getLine_andHandle(handler):
    buf = []
    while True:
        if msvcrt.kbhit():
            key_byte = msvcrt.getch()
            key = key_byte.decode('ascii')
            if ord(key) == 27: # ESC
                break
            buf.append(key)
            if key == '\r':
                string = ''.join(buf)
                handler(string)
                buf = []
            # print(key)

            
# The following function can't not use

def getInput_select():
    while True:
        rs, ws, es = select.select([sys.stdin,], [sys.stdout,], [sys.stdout,])
        if rs:
            data = sys.stdin.readline().strip()
            if data == "q":
                # callback()
                break
            print(data)
        pass

import subprocess
def getInput():
    handle = msvcrt.get_osfhandle(sys.stdout.fileno())
    read, avail_count, msg = _winapi.PeekNamedPipe(handle, 0)
    if avail_count > 0:
        data, errcode = _winapi.ReadFile(handle, avail_count)
        # logger.info(data.decode('cp936'))
    else:
        return b''
    pass

def getkey_():
    if os.name == 'nt':
        return msvcrt.getch()
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(3)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


# getKey()
