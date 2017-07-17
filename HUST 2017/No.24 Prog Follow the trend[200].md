## No.24 Prog Follow the trend[200]

**점수:** 200

**분야:** Prog

**제목:** Follow the trend

**Description:**
> 이 프로그램은 점점 확산되고 있는 Machine Learning기반 정보보호 장비의 일부분 입니다.
> 실시간으로 HTTP데이터를 모니터링 하고 SQL-Injection에 대해 탐지합니다.
> 데이터를 가공하는 불필요한 작업(파싱, 디코딩, 등)을 하지 않고 문제 풀이에 집중 할 수 있도록 전 처리를 겨쳐 당신에게 전달됩니다.
> 전달 받은 데이터가 공격인지 판단하여 1(공격), 0(정상)으로 결과를 돌려주면 됩니다.
> 
> dataset.csv파일을 통해 feature를 정의하고 공격을 구분하는 과정에서 Machine Learning이 결코 완벽하지 않다는 것을 알게 될 것입니다.
> 
> *이 문제는 Machine Learning을 적용하지 않더라도 풀 수 있습니다.
> 문제는 풀 수 있지만, Machine Learning이 적용된 보안 장비의 장점, 우회방법, 한계점에 대해서는 알 수 없겠죠.
> 
> 당신은 미래의 보안 산업을 이끌어갈 우수한 인재 입니다.
> 
> Good Luck.
> 
> nc 223.194.105.182 16511
> 
> Download : https://goo.gl/GQg34n

요청된 내용이 SQL injection인지 아닌지 판별하는 문제기 때문에 몇몇 단여들을 필터링 해줬더니 문제를 풀 수 있었다.

```python
from pwn import *
 
def check(a):
	if a.lower().find('from information_schema.') != -1:
		return '1'
	if a.lower().find('concat(') != -1:
		return '1'
	if a.lower().find('sleep(') != -1:
		return '1'
	if a.lower().find('make_set(') != -1:
		return '1'
	if a.find('ORDER BY ') != -1:
		return '1'
	if a.find('IIF(') != -1:
		return '1'
	if a.lower().find('md5(') != -1:
		return '1'
	if a.find('ELT') != -1:
		return '1'
	if a.find('AND') != -1:
		return '1'
	if a.find('WHEN') != -1:
		return '1'
	if a.find('OR ') != -1:
		return '1'
	if a.find('SELECT') != -1:
		return '1'
	if a.find('UNION') != -1:
		return '1'
	return '0'
 
r = remote('223.194.105.182' ,16511)
r.recv()
 
i = 0
while True:
	i += 1
	data = r.recv()
	print data
	log.info(str(i) + ' ' + check(data))
	r.send(check(data))
  ```
