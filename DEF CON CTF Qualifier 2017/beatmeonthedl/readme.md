# DEF CON CTF Qualifier 2017: beatmeonthedl

**write-up by [kimtruth](https://github.com/kimtruth)**

**Category:** Baby's First

**Description:**

> I really like to be beaten but keep it on the dl.
>
> Connect to:
>
> beatmeonthedl_498e7cad3320af23962c78c7ebe47e16.quals.shallweplayaga.me 6969
>
> Files: [beatmeonthedl](https://github.com/kimtruth/CTF-write-up/raw/master/DEF%20CON%20CTF%20Qualifier%202017/beatmeonthedl/beatmeonthedl)

## [Step 1] Login

![](./caps/1.png)

login에 필요한 id와 password는 하드코딩 되어있으므로 쉽게 구할 수 있었다.

![](./caps/2.png)

## [Step 2] Leak

malloc chunk의 변화를 먼저 살펴보자.
<table>
  <tr>
    <th>malloc
    <th>After free
  <tr>
    <td>prev_size
    <td>prev_size
  <tr>
    <td>size
    <td>size
  <tr>
    <tr>
    <td rowspan="3">data
    <td>fd
  <tr>
    <td>bk
  <tr>
    <td>...
</table>

#### 삽질의 시작
fd, bk에는 다음, 이전 chunk의 주소가 들어가므로 이것을 이용해서 우리가 지금 할당하고 있는 heap의 주소를 leak하기로 했다.

먼저 프로그램의 1번 메뉴(I) Request Exploit.)를 통해서 3개정도의 데이터를 넣었다. 그리고 중간에 위치한 1번을 free시킨뒤 heap을 확인해 보았다.

chunk_1만 free가 진행된 상황

| 주소   |  영역       | 값|
| ----- |:-----------:| ----:|
|&chunk_0| prev_size  |  0|
|&chunk_0(+ 0x8)| size (FLAG) |  0x40 (IS_MMAPPED,PREV_INUSE)|
|&chunk_0(+ 0x10 ~ +0x38)| data |  유저가 입력한 값들 |
|&chunk_1| prev_size  |  0|
|&chunk_1(+ 0x8)| size (FLAG) |  0x40 (PREV_INUSE)|
|&chunk_1(+ 0x10)| fd |  0x609b88 |
|&chunk_1(+ 0x18)| bk |  0x609b88 |
|&chunk_1(+ 0x20 ~ +0x38)| ... |  ... |
|&chunk_2| prev_size  |  0|
|&chunk_2(+ 0x8)| size (FLAG) |  0x40 (IS_MMAPPED)|
|&chunk_2(+ 0x10 ~ +0x38)| data |  유저가 입력한 값들 |

