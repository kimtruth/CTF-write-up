import re
import base64
import string
from pwn import *
r = remote('cm2k-witchcraft_5f60e994e19a100de1dee736608d639f.quals.shallweplayaga.me', '12003')
print r.recvuntil('\n')

cnt = 0
while True:
	cnt += 1
	data = r.recv(1024)
	print data
	name = './files/' + data.split()[0]
	print "name :", name
	tmp = open(name,'rb').read()
	output = ''
	for i in range(0, 0x180 * 100, 0x180):
		data = tmp
		data = data[0x2120 + i:]
		
		flag_1 = False
		flag_2 = False
		if data.find("\x48\x83\xFF") != -1:
			flag_1 = True
			data = data[:data.find("\x48\x83\xFF")+4]
		if data.find("\x48\x81\xFF") != -1:
			flag_1 = False
			flag_2 = True
			data = data[:data.find("\x48\x81\xFF")+7]
		
		addList = []
		for m in re.finditer('\x48\x83\xc7', data): # add rdi,
			addList.append(ord(data[m.start() + 3]))

		subList = []
		for m in re.finditer('\x48\x83\xef', data): # sub rdi,
			subList.append(ord(data[m.start() + 3]))

		if flag_1:
			val = ord(data[-1])
		else:
			val = u32(data[-4:])

		if flag_1 and val & 128 == 128:
			val -= 256
		if flag_2 and val & 0x80000000 == 0x80000000:
			val -= 0x100000000

		for num in subList:
			val += num
		for num in addList:
			val -= num
		if not chr(val) in string.printable:
			break
		output += chr(val)

	print cnt, output
	
	output = base64.b64encode(output)
	r.sendline(output)
	print output