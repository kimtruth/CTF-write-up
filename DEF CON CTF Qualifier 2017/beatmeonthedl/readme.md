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

id : mcfly

pw : awesnap

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


현재는 이런 circular doubly linked list를 이루고 있다.

저기에 chunk가 하나 더 붙는다면 어떻게 될까?

```
+---------------------------------------+
|                                       |
|      ----------   fd   ---------      |
+---->|          |----->|         |-----+
      | 0x609b88 |      | chunk_1 |
+-----|          |<-----|         |<----+
|      ----------   bk   ---------      |
|                                       |
+---------------------------------------+
```

[\*] 이때 주의할 점은 연속한 청크를 free하게 되면 unlink가 일어나므로 저기 doubly linked list에 추가되지 않는다.
ex) 1번 free후 2번 free는 unlink를 일으킴.

그러면 이번엔 5개를 할당한 후, 1번 free, 3번 free를 순서대로 해보자.

1, 3번 chunk를 free한 후의 heap은 이렇다.

| 주소   |  영역       | 값|
| ----- |:-----------:| ----:|
|&chunk_0| prev_size  |  0|
|&chunk_0(+ 0x8)| size (FLAG) |  0x40 (IS_MMAPPED,PREV_INUSE)|
|&chunk_0(+ 0x10 ~ +0x38)| data |  유저가 입력한 값들 |
|&chunk_1| prev_size  |  0|
|&chunk_1(+ 0x8)| size (FLAG) |  0x40 (PREV_INUSE)|
|&chunk_1(+ 0x10)| fd |  0x609b88 |
|&chunk_1(+ 0x18)| bk |  &chunk_3 |
|&chunk_2| prev_size  |  0|
|&chunk_2(+ 0x8)| size (FLAG) |  0x40 (IS_MMAPPED)|
|&chunk_2(+ 0x10 ~ +0x38)| data |  유저가 입력한 값들 |
|&chunk_2(+ 0x20 ~ +0x38)| ... |  ... |
|&chunk_3| prev_size  |  0|
|&chunk_3(+ 0x8)| size (FLAG) |  0x40 (PREV_INUSE)|
|&chunk_3(+ 0x10)| fd |  &chunk_1 |
|&chunk_3(+ 0x18)| bk |  0x609b88 |
|&chunk_4| prev_size  |  0|
|&chunk_4(+ 0x8)| size (FLAG) |  0x40 (IS_MMAPPED)|
|&chunk_4(+ 0x10 ~ +0x38)| data |  유저가 입력한 값들 |

```
+--------------------------------------------------------+
|                                                        |
|      ----------   fd   ---------   fd   ---------      |
+---->|          |----->|         |----->|         |-----+
      | 0x609b88 |      | chunk_3 |      | chunk_1 |
+-----|          |<-----|         |<-----|         |<----+
|      ----------   bk   ---------   bk   ---------      |
|                                                        |
+--------------------------------------------------------+
```

chunk_1의 bk에 chunk_3의 주소가 담겼다! 그렇다면 어떻게 leak할 수 있을까?

```c
// ida hexray results
// add_request
  printf("Request text > ", (unsigned int)i);
  result = read(0, *(&reqlist + i), 0x80uLL);

// update_request
  printf("data: ");
  LODWORD(v0) = read(0, *(&reqlist + v2), 0x80uLL);
```

0x80 bytes나 쓸 수 있다. 현재 할당되고 있는 chunk의 사이즈보다 크다. 

chunk_1에 담긴 bk값을 출력시키려면 chunk_0의 내용을 bk전까지 모두 'A'같은걸로 채우면 NULL문자가 없기 때문에 bk도 같이 출력되어 leak 될 것이다!
이렇게 !

| 주소   |  영역       | 값|
| ----- |:-----------:| ----:|
|&chunk_0| prev_size  |  0|
|&chunk_0(+ 0x8)| size (FLAG) |  0x40 (IS_MMAPPED,PREV_INUSE)|
|&chunk_0(+ 0x10)| data |  AAAAAAAA |
|&chunk_0(+ 0x18)| data |  AAAAAAAA |
|&chunk_0(+ 0x20)| data |  AAAAAAAA |
|&chunk_0(+ 0x28)| data |  AAAAAAAA |
|&chunk_0(+ 0x30)| data |  AAAAAAAA |
|&chunk_0(+ 0x38)| data |  AAAAAAAA |
|&chunk_1| prev_size  |  AAAAAAAA|
|&chunk_1(+ 0x8)| size (FLAG) |  AAAAAAAA|
|&chunk_1(+ 0x10)| fd |  AAAAAAAA|
|&chunk_1(+ 0x18)| bk |  &chunk_3 |

