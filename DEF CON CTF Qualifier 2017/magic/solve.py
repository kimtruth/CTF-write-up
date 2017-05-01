import re
import base64
from pwn import *
r = remote('cm2k-magic_b46299df0752c152a8e0c5f0a9e5b8f0.quals.shallweplayaga.me', '12001')
print r.recvuntil('\n')

while True:
	data = r.recv(1024)
	print data
	name = './files/' + data.split()[0]
	print "name :", name
	data = open(name,'rb').read()

	output = ''
	for m in re.finditer('\x74\x0e\x48\x83', data):
	         output += data[m.start() - 1]
	         
	output = base64.b64encode(output)
	r.sendline(output)
	print output