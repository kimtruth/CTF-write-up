## No.22 Reversing Mind Control[200]

**점수:** 200

**분야:** Reversing

**제목:** Mind Control

**Description:**

> I am definitely sure. You can find the keys.
> * This problem has a different key format. Do not get confused.
> 
> Download : https://goo.gl/5T5RjU

문제의 정답은 AES로 암호화되어 있다.

그리고 주어진 db에서 userid와 name 값을 가져와 crypt 한 뒤 이전의 암호문과 xor 연산한다.

이 때 암호문을 4비트씩 잘라서 xor하기 때문에 각 바이트의 상위 4비트는 변하지 않는다.

따라서 주어진 암호문을 crypt된 값과 다시 xor 할 경우 0A0B0C0D0E0F010203040506 처럼 상위 4비트가 0으로 나오게 된다. 

이를 이용하여 브루트 포싱을 돌리면 정답을 복호화할 수 있다.

```python
import sqlite3
from crypt import crypt
from Crypto.Cipher import AES
 
#target = '3147373A3F3A3D3F3D3B36303D4338363B3032383A3D373C3C4B33393D38334E'.decode('hex')
target = '31303C33324D3636323138393C46304E314A3C373047393E3730383E39353B41'.decode('hex')
 
def xor(x, y):
    ret = ''
    for i in xrange(min(len(x), len(y))):
        ret += chr(ord(x[i]) ^ ord(y[i]))
 
    return ret
 
conn = sqlite3.connect('../user.db')
 
count = 0
c = conn.cursor()
for row in c.execute('select * from USERINFORMATION'):
    userid = str(row[1])
    name = row[2].decode('utf-8')
    crypted = (crypt(userid, name) + 'erz').encode('hex').upper()
 
    key = xor(target, crypted)
 
    skip = False
    for c in key:
        if ord(c) & 0xf0 != 0:
            skip = True
            break
 
    if skip:
        continue
 
    msg = ''
    key = key.encode('hex')
    for i in xrange(1, len(key), 2):
        msg += key[i]
 
    aes = AES.new('WE1C0Me2HUST!@#$', AES.MODE_ECB)
    print aes.decrypt(msg.decode('hex'))
 
conn.close()

```
