#-*- coding:utf-8 -*-
from Crypto.Util.number import *
from gmpy2 import *
from pwn import *

r = remote('problem.harekaze.com', 30214)

# m = [ bytes_to_long(['WIN 💎', 'LOSE 💩'][bool(i)].encode()) for i in range(3) ]
m = [6289644257982517902, 1407668537961767473833, 1407668537961767473833]
win = m[0]

for j in range(30):
    for i in range(3):
        r.recvuntil('%d. (' % (i + 1))
        m = r.recvuntil(')', drop=True).split(', ')
        N = int(m[0], 16)
        e = int(m[1])
        C = int(m[2], 16)
        if pow(win, e, N) == C:
            r.sendline(str(i+1))
    print j, r.recvuntil('you')

r.interactive()
# [+] you got the flag 🏁: HarekazeCTF{92f4187adbbafd3c592bfdfa8689de3be26b770d}
