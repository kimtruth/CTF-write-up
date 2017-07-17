import subprocess
import os

def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell='/bin/bash/')
    return p.stdout.read()

table = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz0123456789!=~?}'
answer = '=ze=/<fQCGSNVzfDnlk$&?N3oxQp)K/CVzpznK?NeYPx0sz5'
flag = 'SCTF{'

def brute(flag, idx):
	for ch in table:
		name = flag + ch
		os.rename('reset', name)
		d = eval(system_call('./' + name))
		os.rename(name, 'reset')
		
		if d == answer:
			print name
			exit()

		if d.find(answer[:idx + 1]) != -1:
			print name
			brute(name, idx + 2)
		elif d.find(answer[:idx]) != -1:
			print name
			brute(name, idx + 1)
		
brute(flag, 8)