# pressh
A simple CMS written with shell script
![screenshot_of_pressh](https://user-images.githubusercontent.com/28914851/43356870-93b2d8d8-92b3-11e8-9c17-636c4e0e18ad.png)

## What's press?
pressh is a CMS written with shell script (bash).  
pressh doesn't use database(such as mysql or so).  
So you can edit files with your favorite text editor.  
And it's easy to make backup. Just copy the directory!  

## Requirements
Remote server which you can get Root Privileges.  
openssh-server  
apache2  
mailutils  
bash  
GNU sed  
GNU awk  
GNU date  
curl  
tree  

And if you use japanese, you need to install some additional packages.  
On Ubuntu, you need to install language-pack-ja-base and language-pack-ja  

## Setup apache2

Install apache2

```
sudo apt install apache2
```

Under /var/www/, make a directory named "pressh"  
change owner and group of pressh directory to your usename.   

```
Ex. $ chown Bob:Bob pressh
```

Make conf file.

```
# cd /etc/apache2/sites-available/
# cp 000-default.conf blog.conf
# cd ../sites-enabled/
# rm 000-default.conf
# ln -s ../sites-available/blog.conf blog.conf
# service apache2 restart
```

Edit /etc/apache2/sites-available/blog.conf like below.

```
ServerAdmin (your email address)
DocumentRoot /var/www/pressh

ErrorLog /var/log/pressh/error.log
CustomLog /var/log/pressh/access.log combined

<Directory /var/www/pressh>
  Options -Indexes +FollowSymLinks +MultiViews +ExecCGI
  AllowOverride None
  AddHandler cgi-script .cgi

  Require all granted
</Directory>
```

Make a directory for log files.

```
$ sudo -s
# mkdir www-data
# chown www-data:www-data www-data/
# mkdir /var/log/pressh
# chown root:adm /var/log/pressh
```

Activate apache CGI module.

```
# a2enmod cgi
```

Setting to not display version information on apache.  
Add the line below on the last line of /etc/apache2/apache2.conf  

```/etc/apache2/apache2.conf
ServerTokens Prod
```

Restart apache2

```
# service apache2 restart
```

Make some directories under /var/www/pressh directory on server side.

```
$ mkdir cache comments rss sitemap
$ sudo chown www-data:www-data cache
$ sudo chown www-data:www-data comments
$ sudo chown www-data:www-data rss
$ sudo chown www-data:www-data sitemap
$ sudo chmod 777 cache
$ sudo chmod 777 comments
$ sudo chmod 777 rss
$ sudo chmod 777 sitemap
```

Finally, Download zip file and extract in home directory.
