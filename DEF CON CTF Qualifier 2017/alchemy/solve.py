import re
import base64
from pwn import *
r = remote('cm2k-alchemy_c745e862098878b8052e1e9588c59bff.quals.shallweplayaga.me', '12004')
print r.recvuntil('\n')

cnt = 0
while True:
	cnt += 1
	data = r.recv(1024)
	print data
	name = './files/' + data.split()[0]
	print "name :", name
	data = open(name,'rb').read()

	output = ''
	data = data[0xf190:]
	data = data[:data.find('\x48\x83\xF8')+4]
	print len(data)
	for m in re.finditer('\x48\x83\xf9', data):
		output += data[m.start() + 3]
		
	output += data[-1]
	print output
	
	output = base64.b64encode(output)
	r.sendline(output)
	print cnt, output