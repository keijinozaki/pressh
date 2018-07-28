#!/bin/bash -xv

dir=$(dirname $0)/..
pages=$dir/pages
tmp=/tmp/$$
exec 2> $dir/../www-data/$(basename $0).$(date +%Y%m%d%H%M%S).$$

num=$(echo ${QUERY_STRING} | tr -dc '0-9')
period=$(date -d '7 days ago' +%s)

ls -f $pages | grep -E '[0-9]{14}_'  | sort | sed 's/_/\\_/g' > $tmp-pageslist

echo "Content-Type: text/html"
echo
if [ -n "$(cat $tmp-pageslist | head -n 1)" ] ; then
	cat /var/log/pressh/access.log |
	grep -i 'Mozilla' |
	grep -ioE '\[.* "GET /\?p=[0-9]{14}[^ ]* ' |
	tr -d '[]' |
	sed 's/+0900//' |
	sed 's/ //g' |
	sed 's;/; ;g' |
	sed 's/:/ /' |
	sed 's/"GET ?p=/ /' |
	awk '{gsub(/_/,"\\_",$5);print $5 > "'$tmp-pages'"; print $1,$2,$3,$4 > "'$tmp-date'"}'

	cat <<-END > $tmp-html
	<div class="popular">
	<h2>Popular Posts</h2>
		<ul>
	<!-- LIST -->
		<li><a href="?p=%2"><img src="%4" />%3 (%1pv)</a></li>
	<!-- LIST -->
		</ul>
	</div>
	END

	cat $tmp-date |
	date -f - "+%s" |
	paste -d ' ' - $tmp-pages |
	awk -v period=$period 'period <= $1{print $2}' |
	sort |
	join $tmp-pageslist - |
	uniq -c |
	sort -k1 -nr |
	head -n $num |
	sed 's/^ *//' |
	awk '{print $0 > "'$tmp-list'"; print $2 > "'$tmp-pagedir'"}'

	cat $tmp-pagedir |
	sed "s;.*;$pages/&/html;" |
	xargs awk '
		/<h1/{
				gsub(/<\/*h1[^>]*>/, "",$0)
				print $0
		}' |
	paste -d ' ' $tmp-list - > $tmp-list2

	cat $tmp-pagedir |
	sed "s;^;$pages/;" |
	while read pagedir; do
		thumb=$(ls -f $pagedir | grep -oE '^thumb_s\.(jpg|png)$')
		if [ -n "$thumb" ]; then
			echo "/pages/$(basename $pagedir)/$thumb" | sed 's/_/\\_/g'
		else
			echo "/default_thumb.png" | sed 's/_/\\_/g'
		fi
	done |
	paste -d ' ' $tmp-list2 - |
	$dir/bin/insetd LIST $tmp-html -
else
	cat <<-END > $tmp-html
	<div class="popular">
	<h2>Popular Articles</h2>
	</div>
	END
	cat $tmp-html
fi

rm $tmp-*
