import re
import base64
import string
from pwn import *
r = remote('cm2k-sorcery_13de8e6bf26e435fc43efaf46b488eae.quals.shallweplayaga.me', '12002')
print r.recvuntil('\n')

while True:
	data = r.recv(1024)
	print data
	name = './files/' + data.split()[0]
	print "name :", name
	data = open(name,'rb').read()

	output = ''
	data = data[0x36a5:]
	
	for m in re.finditer('\x80\xf9', data):
		if data[m.start() + 2] in string.printable:
			output += data[m.start() + 2]
		else:
			break
	output += data[data.find('\x3c')+1]

	print output
	
	output = base64.b64encode(output)
	r.sendline(output)
	print output