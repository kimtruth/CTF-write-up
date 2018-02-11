## No.17 Prog iamrandom[50]

**점수:** 50

**분야:** Prog

**제목:** iamrandom

C언어의 Int를 기반으로 +, -, *, /, <<, >>연산의 결과를 보내줘야 하는 문제다.

문제상의 오류인지 아닌지 모르겠지만 예를 들어서 8 >> 33이 나오면 8 >> (33 % 32)로 8 >> 1이 되어서 4가 결과가 된다.

즉 비트 시프트 연산을 할때는 mod 32를 해줘야 했다.

```python
from pwn import *
import re
import subprocess
 
def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell="/bin/bash")
    return p.stdout.read()
 
r = remote('223.194.105.182', 22902)
while True:
	print r.recvuntil('Problem: ')
	prob = r.recvline()
	print prob
	prob = re.sub(r'<<(.+?)\)', '<<(\\1%32))', prob)
	prob = re.sub(r'>>(.+?)\)', '>>(\\1%32))', prob)
 
	f = open('code.c', 'w')
	code = '#include<stdio.h>\nint main(){printf("%%d", %s);}' % prob
	f.write(code)
	f.close()
 
	result = system_call('gcc -w -o code code.c;./code')
	r.sendline(result)
 
	print r.recvline()
	print r.recvline()
  ```
