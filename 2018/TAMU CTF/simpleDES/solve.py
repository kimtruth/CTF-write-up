enc = '01100101 00100010 10001100 01011000 00010001 10000101'.replace(' ', '')
N = len(enc) / 12
R = 2
key = '0100110101110101' #'Mu'
def xor(str1, str2):
    return ''.join([str(int(ch1) ^ int(ch2)) for ch1, ch2 in zip(str1, str2)])
def F(Rr, key):
    print '====== Expand Rr ======'
    Re = Rr[0] + Rr[1] + Rr[3] + Rr[2] + Rr[3] + Rr[2] + Rr[4] + Rr[5]
    print 'Re (8bit) :', Re
    print '====== Re ^ k ======'
    print 'k :', k
    Rs = xor(Re, k)
    S1, S2 = Rs[:4], Rs[4:]
    print 'S1 : %s, S2 : %s' % (S1, S2)
    return S1box[S1] + S2box[S2]
S1box = {'0000': '101',
         '0001': '010',
         '0010': '001',
         '0011': '110',
         '0100': '011',
         '0101': '100',
         '0110': '111',
         '0111': '000',
         '1000': '001',
         '1001': '100',
         '1010': '110',
         '1011': '010',
         '1100': '000',
         '1101': '111',
         '1110': '101',
         '1111': '011'}
S2box = {'0000': '100',
         '0001': '000',
         '0010': '110',
         '0011': '101',
         '0100': '111',
         '0101': '001',
         '0110': '011',
         '0111': '010',
         '1000': '101',
         '1001': '011',
         '1010': '000',
         '1011': '111',
         '1100': '110',
         '1101': '010',
         '1110': '001',
         '1111': '110'}
print 'N: ', N
p = ''
for i in range(0, N):
    block = enc[i * 12 : i * 12 + 12]
    print '\n\nBlock :', block
    Lr, Rr = block[:6], block[6:]
    Lr, Rr = Rr, Lr
    for r in range(R - 1, -1, -1):
        start = i * R + r
        k = key[start: start + 8]
        Lr, Rr = Rr, xor(Lr, F(Rr, k))
    Lr, Rr = Rr, Lr
    print 'block: ', Lr + Rr
    p += Lr + Rr
print hex(int(p, 2))[2:].decode('hex') # AIN0n!