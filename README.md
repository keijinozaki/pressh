# pressh

A simple CMS written with shell script.

![screenshot_of_pressh](https://user-images.githubusercontent.com/28914851/43356870-93b2d8d8-92b3-11e8-9c17-636c4e0e18ad.png)
  

## What's pressh?
pressh is a CMS written with shell script (bash).  
pressh doesn't use database(such as mysql or so).  
So you can edit files with your favorite text editor.  
And it's easy to make backup. Just copy the directory!  

For japanese instruction, please visit [http://pressh.net](http://pressh.net) .

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

Install apache2.

```
sudo apt install apache2
```

Under /var/www , make a directory named "pressh".  
Change owner and group of pressh directory to your username.   

```
# cd /var/www
# mkdir pressh
# chown [your_username]:[your_username] pressh
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

Restart apache2.

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

# How to Use pressh

After you cloned or extracted zip file in your home directory,  
move to pressh directory.

```
$ cd pressh
```

The subsequent operations are performed in the pressh directory of the local machine.

## Work flow

Editing of article files, shell scripts, etc. is done on the local machine, and then the edited file is sent to the server by the publish command.

## Writing a draft

To write a draft, you use 'draft' commnad in bin directory.

```
$ draft [draft_name]
```

Draft name can only contain alphabets, numbers, and underscores.  
You can pass multiple draft names with space delimiters for the draft command.  

```
$ draft draft_1 draft_2 ...
```

When you execute the draft command, three files of html, categories, tags are created under the drafts/[draft_name] directory.  
To edit the draft text, edit the html file in it with an editor.

For example, when editing with vim  

```
$ vim drafts/[draft_name]/html
```

Surround the article title with h1 tag.  
Please do not use the h1 tag except the article title.  

You do not need to write headers and footers such as \<head\> and \<title\> in this html file. The header part is written in the head.html file, the footer part is written in footer.html, and it is added automatically when outputting. So write only the contents to be written between \<body\> ~ \</ body\> (you do not need to write \<body\> and \</ body\> tags).

### Creating thumbnails

To create thumbnails, use the mkthumb command.  
Please put the image you want to use as a thumbnail in the same directory as html.  

```
$ bin/mkthumb drafts/[draft_name]/[image_name]
```

A thumbnail image called thumb_s.(jpg | png) is automatically created.

### Making link to image or some kind of files

Put the images and PDF files used in the article in the draft directory.  
Image file format is limited to jpg and png.  

For example, link to image file.

```
<img src="imagefile.jpg">
```

url of src can contain only file name.

### In-site link

For example, making a in-site link to article "20180715144436_how_to_use".

```
<a href="?p=20180715144436_how_to_use">How to use</a>
```

### Link to external site

As usual.

```
<a href="http://github.com">Github</a>
```

### Adding category or tag

If you want to add categories and tags to articles, edit the categories and tags files.  
Please write one item per line.

## Publishing article

To publish a article, you can use "publish" command.

Before you use publish command, you need to edit bin/publish .  
Open bin/publish with editor and you will see "remote" variable at the beginning of the file.  
Delete "#" at the head of the line and subsutitute the IP address of the server for the remote variable.

After editing bin/publish, execute the publish command.
For example,

```
$ bin/publish drafts/[draft_name]
```

if you pass no argument to publish command, all drafts in the drafts directory will be published.

By executing publish command, 14 digit number representing release date and time will be added to draft name. And the draft will be moved to pages directory.

Thereafter, pages directory on the local machine and /var/www/pressh/pages directory on the server will be synchronized. In addition to it, files other than article files are also synchronized.

# Unpublish article (making article private)

To make article private, use "unpublish" command.

```
$ bin/unpublish pages/[article_name]
```

Like the publish command, you need to edit bin/unpublish .  
Open bin/unpublish with editor and you will see "remote" variable at the beginning of the file. Delete "#" at the head of the line and subsutitute the IP address of the server for the remote variable.

The article to be made private will be moved from pages directory on the local machine to draft directory on local machine with 14 digit number at the head of the article name.

Thereafter, pages directory on the local machine and /var/www/pressh/pages directory on the server will be synchronized. 

# Notify by email that comment has been posted

Install mailutils on the server.

```
$ sudo apt install mailutils
```

Next, edit ajax/comment.cgi .
Subsutitute your email address for the "email" variable At the beginngin of the file

# Show ADs

To display advertisements under the article body please paste the ad into the file ad_main.html.  
To display ads in the sidebar please paste the advertisement in the file ad_side.html.  
# Change quiz and answer in comment field

When posting comments to prevent spam you have to answer quizzes.  
To change the contents of the quiz edit the comments.html file.  
By default it is a question like below, so please freely change the sentences between the div tags.

```
<div id="quiz">Quiz: 日本の総理大臣の名前は？（漢字）</div>
```

To change the answer to the quiz, substitute the answer of the new quiz to the variable called ANSWER in the first line of the comment function of the file called functions.js. The default is as shown below.

```
function comment(name,answer,text) {
  var ANSWER = "安倍晋三";
```

