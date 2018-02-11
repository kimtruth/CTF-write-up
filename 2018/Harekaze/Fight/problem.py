import random
import base64
import key

def xor(msg, key):
    return bytes([ch1^ch2 for ch1, ch2 in zip(msg, key)])

def gcd(x, y):
  while y != 0:
    r = x % y
    x = y
    y = r
  return x

def gen_seed(n):
  seed = 0
  for k in range(1,n):
    if gcd(k,n)==1:
      seed += 1
  return seed

s = 1
for p in b"Enjoy_HarekazeCTF!!":
  s *= p
seed = gen_seed(s)
random.seed(str(seed).rstrip("0"))

flag = key.FLAG
key = bytes([random.randint(0,255) for _ in flag])

enc = xor(flag, key)
print(base64.b64encode(enc).decode('utf-8')) #7XDZk9F4ZI5WpcFOfej3Dbau3yc1kxUgqmRCPMkzgyYFGjsRJF9aMaLHyDU=
