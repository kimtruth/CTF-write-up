# 작성중.............

# DEF CON CTF Qualifier 2017: Leo es Pequeno

**write-up by [kimtruth](https://github.com/kimtruth)**

**Category:** Pwnable

**Description:**

> Connect to:
>
> leo_33e299c29ed3f0113f3955a4c6b08500.quals.shallweplayaga.me 61111
>
> Files: [leo](https://github.com/kimtruth/CTF-write-up/raw/master/DEF%20CON%20CTF%20Qualifier%202017/Leo%20es%20Pequeno/leo)

## [Step 1] 파일 형식 판정

```c
signed __int64 __fastcall categorize(_BYTE *input, int a2)
{
  signed __int64 result; // rax@25
  int table[256][2]; // [sp+10h] [bp-820h]@2
  unsigned int maxFreqChar; // [sp+814h] [bp-1Ch]@1
  unsigned int minFreqChar; // [sp+818h] [bp-18h]@1
  unsigned int unusedCnt; // [sp+81Ch] [bp-14h]@1
  unsigned int asciiCount; // [sp+820h] [bp-10h]@1
  unsigned int minFreq; // [sp+824h] [bp-Ch]@1
  unsigned int maxFreq; // [sp+828h] [bp-8h]@1
  int i; // [sp+82Ch] [bp-4h]@1

  maxFreq = 0;
  minFreq = -1;
  asciiCount = 0;
  unusedCnt = 0;
  minFreqChar = 511;
  maxFreqChar = 0;
  for ( i = 0; i <= 255; ++i )
  {
    table[i][0] = i;
    table[i][1] = 0;
  }
  for ( i = 0; i < a2; ++i )
    ++table[input[i]][1];                       // ascii frequency analysis
  for ( i = 0; i <= 255; ++i )
  {
    if ( table[i][1] > maxFreq )
      maxFreq = table[i][1];
    if ( table[i][1] < minFreq )
      minFreq = table[i][1];
    asciiCount += table[i][1];                  // asciiCount : 사용된 ascii값 종류
  }
  asciiCount >>= 8;
  sub_40185E((_DWORD *)table, 256);             // sort
  for ( i = 0; i <= 255; ++i )
  {
    if ( table[i][1] )
    {
      if ( table[i][0] < minFreqChar )
        minFreqChar = table[i][0];
      if ( table[i][0] > maxFreqChar )
        maxFreqChar = table[i][0];
    }
    else
    {
      ++unusedCnt;
    }
  }
  if ( unusedCnt > 4 || 10 * asciiCount <= maxFreq )
  {
    if ( maxFreqChar > 0x7F || minFreqChar <= 8 )
    {
      if ( minFreq && 10 * asciiCount < maxFreq )
      {
        result = 100LL;                         // Its an executable?  Let's see what 'file' says...
      }
      else if ( minFreq || 2 * asciiCount >= maxFreq )  // 1. minFreqChar <= 8   && asciiCount == maxFreq
                                                        // 2. maxFreqChar > 0x7f && asciiCount == maxFreq
      {
        result = 22LL;                          // This doesn't match my patterns.  Checking...
      }
      else
      {
        result = 25LL;                          // I guess its binary data. Let's see what 'file' says...
      }
    }
    else if ( table[255][0] == 32 )
    {
      result = 49LL;                            // This is ASCII text.
    }
    else
    {
      result = 50LL;                            // This is ASCII data.
    }
  }
  else
  {
    result = 2LL;
  }
  return result;
}
```

먼저 조건식을 분석하여 `This doesn't match my patterns. Checking...`이 나오게 했다.
이유는 그냥.. 뭔가 의심가는 부분이였고 다른 부분이 공격가능한지 몰랐었다.

## [Step 2] 공격 가능성

먼저 Checking...한다고 하면서 call하는 함수는 heap에서 코드가 실행이 된다.

```
push   rbp
mov    rbp,rsp
mov    QWORD PTR [rbp-0x28],rdi
mov    DWORD PTR [rbp-0x2c],esi
mov    eax,DWORD PTR [rbp-0x2c]
mov    edx,eax
shr    edx,0x1f
add    eax,edx
sar    eax,1
add    eax,0x1
mov    DWORD PTR [rbp-0x8],eax
mov    DWORD PTR [rbp-0x4],0x11
mov    DWORD PTR [rbp-0x4],0x0
jmp    0xca4062
mov    eax,DWORD PTR [rbp-0x2c]
mov    edx,eax
shr    edx,0x1f
add    eax,edx
sar    eax,1
add    eax,0x1
cmp    eax,DWORD PTR [rbp-0x8]
je     0xca4043
jmp    0xca406b
mov    eax,DWORD PTR [rbp-0x4]
movsxd rdx,eax
mov    rax,QWORD PTR [rbp-0x28]
add    rax,rdx
movzx  eax,BYTE PTR [rax]
mov    edx,eax
mov    eax,DWORD PTR [rbp-0x4]
cdqe   
mov    BYTE PTR [rbp+rax*1-0x20],dl
add    DWORD PTR [rbp-0x4],0x1
mov    eax,DWORD PTR [rbp-0x4]
cmp    eax,DWORD PTR [rbp-0x2c]
jl     0xca402d
nop
pop    rbp
ret
```

그냥 한번 귀찮으니 hexray를 돌려봤다.


```c
int __cdecl main(_BYTE *s, int num, const char **envp)
{
  int result; // eax@2
  char v4[24]; // [sp+Ch] [bp-20h]@3
  int v5; // [sp+24h] [bp-8h]@1
  int i; // [sp+28h] [bp-4h]@1

  v5 = num / 2 + 1;
  for ( i = 0; ; ++i )
  {
    result = i;
    if ( i >= num )
      break;
    result = num / 2 + 1;
    if ( result != v5 )
      break;
    v4[i] = s[i];
  }
  return result;
}
```
우리가 입력한 문자열을 어느 배열에 그대로 복붙을 하고 있다.

근데 일단 우리가 입력 가능한 문자가 16000자 였는데 그 배열이 rbp-0x20에 위치해 있다. 


