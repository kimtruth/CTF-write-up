## No.3 Mobile Trouble Maker[100]

**점수:** 100

**분야:** Mobile

**제목:** Trouble Maker

**Description:**

> The first input is 5 characters consisting of 0 ~ 9 a ~ z A ~ Z.
> The second input string can be found by looking at the SO file carefully.
> 
> Download : https://goo.gl/yWFqGo

1. 주어진 apk 파일을 7zip으로 풀고 
1. classes.dex 파일을 dex2jar를 이용해 jar 파일로 변환한다.
1. 변환된 jar 파일을 다시 7zip으로 압축을 푼다.
1. jad 파일을 이용하여 class파일을 java 파일로 디컴파일 한다.

위 단계를 거친 후 MainActivity 파일을 분석하면

```java
static Long getValue(String s)
    {
        CRC32 crc32 = new CRC32();
        crc32.update(s.getBytes());
        return Long.valueOf(crc32.getValue());
    }
 
    protected void onCreate(Bundle bundle)
    {
        super.onCreate(bundle);
        setContentView(0x7f04001b);
        bundle = (Button)findViewById(0x7f0b0059);
        text = (EditText)findViewById(0x7f0b005a);
        text2 = (EditText)findViewById(0x7f0b0058);
        key = (TextView)findViewById(0x7f0b0057);
        getKey = new GetKey();
        bundle.setOnClickListener(new android.view.View.OnClickListener() {
 
            public void onClick(View view)
            {
                if(MainActivity.getValue(text.getText().toString()).longValue() == 0x8be36a7cL)
                {
                    view = MainActivity.Xor((new StringBuilder()).append(text.getText().toString()).append(text2.getText().toString()).toString(), MainActivity.getByte(subKey));
                    key.setText(view);
                }
            }
 
            final MainActivity this$0;
            final String val$subKey;
 
            
            {
                this$0 = MainActivity.this;
                subKey = s;
                super();
            }
        }
);
}
 ```
 
 에서 text 변수는 문제 설명에 나와있는 5글자의 알파벳 대소문자 + 숫자라는 힌트와 getValue 구하는 함수를 그대로 이용하여 구하면 된다.
 
 ```python
from zlib import crc32
import string
import itertools
 
charset = string.ascii_lowercase + string.ascii_uppercase + string.digits
 
for delta in itertools.product(charset, repeat=5):
    val = ''.join(delta)
    if crc32(val) & 0xffffffff == 0x8BE36A7C:
        print 'Found: ' + val
        break
```

`text = sl33p`
 
`apk` 파일에 존재하는 `lib.so` 파일을 분석하면 `subkey`를 알 수 있다.
 
> subkey = 3B3900042F3C2E4640465B1A2D1D1D0C16030F4416
 
`flag = (text + text2) ^ subkey` 이므로 우선 앞의 5byte를 구해보면, `HU37_` 가 나온다.
 
대회의 키 형식을 이용하여 text2의 8byte를 구할 수 있다.
 
> text2 = thtpwlaXXXXXXXXk
 
XXXXXXXX의 8byte는 게싱으로 맞춰야 하는데 text2의 앞뒤의 글자를 해석하면 `소세지ㅁ       ㅏ`다.
 
`ㅏ`와 조합될 모음 1개를 빼면 7byte가 남는다.  여러 조합을 생각해서 구한 8byte와 xor를 해보니 답이 나왔다.
 
답 : HU37_HF2017{Goodboy!}
 
text2 = thtpwlajrrhtlvek (소세지먹고싶다)


