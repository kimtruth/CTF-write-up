import random
import base64

def xor(msg, key):
    return bytes([ch1 ^ ch2 for ch1, ch2 in zip(msg, key)])

seed = 765753154007029226621575888896000000

enc = base64.b64decode('7XDZk9F4ZI5WpcFOfej3Dbau3yc1kxUgqmRCPMkzgyYFGjsRJF9aMaLHyDU=')
random.seed(str(seed).rstrip("0"))

key = bytes([random.randint(0,255) for _ in enc])

print(xor(enc, key)) # HarekazeCTF{3ul3rrrrrrrrr_t0000000t1nt!!!!!}
