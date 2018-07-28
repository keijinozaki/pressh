#!/bin/bash -xv

dir=$(dirname $0)/..
pages=$dir/pages
tmp=/tmp/$$
limit=15
exec 2> $dir/../www-data/$(basename $0).$(date +%Y%m%d%H%M%S).$$

n=$(echo ${QUERY_STRING} | tr -dc '0-9')

echo "Content-Type: text/html"
echo
if ls -f $pages | grep -qE '[0-9]{14}_' ; then
	cat <<-END > $tmp-html
	<div class="tags-list">
	<h2>Tags</h2>
		<ul>
	<!-- LIST -->
		<li><a href="?t=%2&n=$limit">%1</a></li>
	<!-- LIST -->
		</ul>
	</div>
	END

	ls -f $pages |
	grep -E '^[0-9]{14}_' |
	sed "s;\(.*\);$pages/\1/tags;" |
	xargs awk '
		{	
			tag = $0
			gsub(/_/,"\\_",$0)
			gsub(/ /,"_",$0)
			gsub(/_/,"\\\\\\_",tag)
			gsub(/ /,"\\_",tag)
			print $0,tag
		}' |
	sort -u |
	$dir/bin/insetd LIST $tmp-html -
else
	cat <<-END > $tmp-html
	<div class="tags-list">
	<h2>Tags</h2>
	</div>
	END
	cat $tmp-html
fi

rm $tmp-*
