import string

def rot_n(n, s):
    lc = string.ascii_lowercase
    uc = string.ascii_uppercase
    trans = string.maketrans(lc + uc, lc[n:] + lc[:n] + uc[n:] + uc[:n])
    return string.translate(s, trans)

data = "BTJSX{1b'c_Z0h_q_jtWx0Ll_D0i}"
output = ''
for i in range(len(data)):
    output += rot_n(25 - i, data[i])
print output
