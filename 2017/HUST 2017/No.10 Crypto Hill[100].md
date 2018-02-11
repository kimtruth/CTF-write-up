## No.10 Crypto Hill[100]

**점수:** 100

**분야:** Crypto

**제목:** Hill

**Description:**

> This problem is very easy(?) Cryptography problem.
> Authenticate according to the key format.
> key format : HU37_HF2017{key}
> 
> Download : https://goo.gl/KwDylm

E = P * Kn

E = 암호문
P = 평문
K = 키
n = 제곱수
 
바이너리 안에 하드코딩 된 4x4 key matrix의 역행렬을 인터넷에서 구한다. (key_inv)
주어진 암호문에서 count를 알아낸 뒤 역행렬을 다시 count 만큼 곱해준다.

```python
import numpy as np
 
def decrypt(enc, key, count):
    t = enc
    for _ in xrange(count):
        t = np.matmul(t, key)
 
    return t
 
enc = [
    [164845022, 194846903, 258237904, 166782954],			
    [210425942, 249349389, 330056130, 213716910],
    [196223440, 232924323, 307918857, 199897032],
    [173490804, 205813716, 272275442, 176726624]
]
 
key_inv = [
    [-0.016321740985705185, 0.06262001280136549, 0.009174311926605505, -0.030509921058246202],
    [-0.09053410141526202, -0.07531470023469172, 0.13149847094801226, 0.0355593485527345],
    [0.07289666453310575, -0.0029869852784297005, -0.006116207951070339, -0.018419742550316476],
    [0.034634805490363414, 0.06101984211649244, -0.11314984709480123, 0.0429556930517033]
]
 
flag = decrypt(enc, key_inv, 4)
 
value = ''
for y in xrange(4):
    for x in xrange(4):
        value += chr(int(round(flag[y][x])))
 
print value
```
