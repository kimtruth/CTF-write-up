## No.6 Prog Catch JACK If you can[50]

**점수:** 50

**분야:** Prog

**제목:** Catch JACK If you can

**Description:**

> The first input is 5 characters consisting of 0 ~ 9 a ~ z A ~ Z.
> The second input string can be found by looking at the SO file carefully.
> 
> Download : https://goo.gl/yWFqGo

아무 함정이 없는 그냥 블랙잭이다.

블랙잭에서 이론적으로 플레이어의 승률은 49퍼라고 하는데, 

카드 카운팅을 통해 승률을 끌어올 수 있다고 한다.

아래는 사용한 코드이다. 

pc함수에서 내가 죽게되는 카드가 나올 확률을 계산한다. 

main에서 배팅 가능한 금액의 5분의 1을 배팅하여 진행하며, 

A가 나오거나 내가 죽을 확률이 0.5보다 작거나 스코어가 17보다 작은 경우 같은 과정을 반복한다. 

(스코어가 17보다 작으면 딜러의 알고리즘 상 무조건 내가 지거나 딜러가 파산하게 된다. 딜러가 파산하는 확률은 낮다고 가정했다.)
 
아래 코드로 여러 개의 쉘을 열어 공격하면 확률적으로 딜러를 이길 수 있다.

```python
from pwn import *
from time import *
 
def pc(ls):
	many = 0.0
	summ = 0.0
	for i in range(len(cardt)):
                summ += cardt[i]
		if i<10:
			if ls<i:
				many+=cardt[i]
		else:
			if ls<10:
				many+=cardt[i]
	return (many/summ)
 
def sendhit():
        print r.recvuntil('\n')
        data1 = r.recvuntil('pick')
        data1 = r.recvuntil('\n')
        print data1
        data1 = data1.replace('♦','').replace('♣','').replace('♥','').replace('♠','')
        data1 = data1.replace('J','11').replace('Q','12').replace('K','13').replace('A','1').replace(' ','')
        data1 = data1.split(':')[1]
        cardt[int(data1)]-=1
 
        data1 = r.recvuntil('\n')
        score = data1.replace(' ','').split(':')[1]
        score = int(score)
        if score>21:
                return False
        lastscore = 21 - int(score)
        percentage = pc(lastscore)
        if percentage<0.5 or lastscore>4:
                r.sendline('1')
                return True
        else:
                r.sendline('2')
                return False
 
idx = ['2','3','4','5','6','7','8','9','10','J','K','Q','A']
 
 
r=remote('223.194.105.182',28345)
 
while(1):
        print r.recvuntil('\n')
        print r.recvuntil('Betting(10~')
        data = r.recvuntil(')')[:-1]
        print data
        log.info(data)
        r.sendline(str(int(int(data)/5)))
 
        cardt = [0,4,4,4,4,4,4,4,4,4,4,4,4,4]
        print cardt
        
        print r.recvuntil('\n')
        print r.recvuntil('\n')
        data1= r.recvuntil('\n')
        print data1
 
        data1 = data1.replace('♦','').replace('♣','').replace('♥','').replace('♠','').split(':')
 
        score = data1[2].replace(' ','')
        log.info("score : "+score)
 
        lastscore = 21 - int(score)
        data1 = data1[1].split('[')[1].split(']')[0]
 
        data1 = data1.replace(' ','').replace('J','11').replace('Q','12').replace('K','13').replace('A','1').split('\'')
        MyA = False
        for i in range(len(data1)):
                if(i%2==1):
                        cardt[int(data1[i])]-=1
        if cardt[1]!=4 and lastscore > 3:
                MyA = True
 
        data1 = r.recvuntil('\n')
        print data1
 
        data1 =data1.replace('♦','').replace('♣','').replace('♥','').replace('♠','')
        data1 = data1.split(':')[1].split('[')[1].split(']')[0].replace(' ','')
        data1 = data1.replace('J','11').replace('Q','12').replace('K','13').replace('A','1').split('\'')
 
        cardt[int(data1[1])]-=1
 
        percentage = pc(lastscore)
        if percentage<0.5 or MyA == True or lastscore>4:
                r.sendline('1')
                MyA = False
                a=sendhit()
                while (a):
                        a=sendhit()
        else:
                r.sendline('2')
```
