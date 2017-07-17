## No.2 Crypto Maware Maware Maware[50]

**점수:** 50

**분야:** Crpyto

**제목:** Maware Maware Maware

**Description:**

> Sometimes it is necessary to look backwards.
> Authenticate according to the key format.
> key format : HU37_HF2017{key}
> 
> Download : https://goo.gl/ydjQtV

문제 이름이 回れ回れ回れ다. 뭔가 돌려야 할 것 같다. 

일단 압축을 풀어보면 암호문 `7jXb7eQ_r00r_b1_0ytBtD`이 나온다.

backwards에서 힌트를 얻어서 거꾸로 읽으면  `DtBty0_1b_r00r_Qe7bXj7`가 나온다.

일단 카이사르 방식의 암호를 의심해봐서 25개의 키(0 제외)에 대한 전수조사를 해보았다.

```python
C = "DtBty0_1b_r00r_Qe7bXj7"
def dec(k):
	rotor = {}
	for i in range(26):
		rotor[chr((i+k)%26 + 65)] = chr(i+65)
		rotor[chr((i+k)%26 + 97)] = chr(i+97)
	return rotor
 
for i in range(1, 26):
	rotor = dec(i)
	P = ""
	for c in C:
			if c in rotor:
				P += rotor[c]
			else:
				P += c
	print (P)
 
 
CsAsx0_1a_q00q_Pd7aWi7
BrZrw0_1z_p00p_Oc7zVh7
AqYqv0_1y_o00o_Nb7yUg7
ZpXpu0_1x_n00n_Ma7xTf7
YoWot0_1w_m00m_Lz7wSe7
XnVns0_1v_l00l_Ky7vRd7
WmUmr0_1u_k00k_Jx7uQc7
VlTlq0_1t_j00j_Iw7tPb7
UkSkp0_1s_i00i_Hv7sOa7
TjRjo0_1r_h00h_Gu7rNz7
SiQin0_1q_g00g_Ft7qMy7
RhPhm0_1p_f00f_Es7pLx7
QgOgl0_1o_e00e_Dr7oKw7
PfNfk0_1n_d00d_Cq7nJv7
OeMej0_1m_c00c_Bp7mIu7
NdLdi0_1l_b00b_Ao7lHt7
McKch0_1k_a00a_Zn7kGs7
LbJbg0_1j_z00z_Ym7jFr7
KaIaf0_1i_y00y_Xl7iEq7
JzHze0_1h_x00x_Wk7hDp7
IyGyd0_1g_w00w_Vj7gCo7
HxFxc0_1f_v00v_Ui7fBn7
GwEwb0_1e_u00u_Th7eAm7
FvDva0_1d_t00t_Sg7dZl7
EuCuz0_1c_s00s_Rf7cYk7
```

전수조사 결과를 보다보니 대각선으로 읽으면 `CrYpt0`가 보인다. 

따라서 글자를 읽을때마다 키를 하나씩 높혀서 읽으면 답이 나올것이라 생각했다.
 
```python
for i in range(26):
	rotor = dec(i)
	P = ""
	for c in C:
			if c in rotor:
				P += rotor[c]
			else:
				P += c
	result += P[i-1]
 
>>> result
'CrYpt0_1s_g00d_An7iDo7'
```

result값을 키로 넣어주면 된다.
