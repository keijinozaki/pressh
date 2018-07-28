#!/bin/bash -xv

dir=$(dirname $0)/..
pages=$dir/pages
tmp=/tmp/$$
exec 2> $dir/../www-data/$(basename $0).$(date +%Y%m%d%H%M%S).$$

num=$(echo ${QUERY_STRING} | tr -dc '0-9')
[ -z $num ] && num=3

echo "Content-Type: text/html"
echo
if [ -n "$(cat $dir/cache/info | head -n 1)" ]; then
	cat <<-END > $tmp-html
	<div class="recent">
	<h2>Recent Posts</h2>
		<ul>
	<!-- LIST -->
		<li><a href="?p=%2"><img src="%4" />%3 (%1)</a></li>
	<!-- LIST -->
		</ul>
	</div>
	END

	cat $dir/cache/info |
	awk '{print $1}' |
	sed 's/\\\\_/_/g' |
	head -n $num > $tmp-pages

	cat $tmp-pages |
	sed "s;\(.*\);$pages/\1/html;" |
	xargs awk '
		/<h1/{
			  gsub(/<\/*[^>]*>/,"",$0)
			  gsub(/_/,"\\_",$0)
			  gsub(/ /,"_",$0)
			  date = gensub(/.*\/pages\/(....)(..)(..).*\/html$/,"\\1/\\2/\\3",1,FILENAME)
			  url = gensub(/.*\/pages\/([0-9]{14}.*)\/html$/,"\\1",1,FILENAME)
			  gsub(/_/,"\\_",url)
			  print date,url,$0
			}' > $tmp-list

	cat $tmp-pages |
    sed "s;^;$pages/;" |
    while read pagedir; do
        thumb=$(ls -f $pagedir | grep -oE '^thumb_s\.(jpg|png)$')
        if [ -n "$thumb" ]; then
            echo "/pages/$(basename $pagedir)/$thumb" | sed 's/_/\\_/g'
        else
            echo "/default_thumb.png" | sed 's/_/\\_/g'
        fi
    done |
	paste -d ' ' $tmp-list - |
	$dir/bin/insetd LIST $tmp-html -
else
	cat <<-END > $tmp-html
	<div class="latest">
	<h2>Latest Articles</h2>
	</div>
	END
	cat $tmp-html	
fi

rm $tmp-*
