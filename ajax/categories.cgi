#!/bin/bash -xv

dir=$(dirname $0)/..
pages=$dir/pages
tmp=/tmp/$$
limit=15
exec 2> $dir/../www-data/$(basename $0).$(date +%Y%m%d%H%M%S).$$

n=$(echo ${QUERY_STRING} | tr -dc '0-9')

echo "Content-Type: text/html"
echo
if ls -f $pages | grep -qE '^[0-9]{14}_' ; then
	cat <<-END > $tmp-html
	<div class="categories-list">
	<h2>Categories</h2>
		<ul>
	<!-- LIST -->
		<li><a href="?c=%2&n=$limit">%1</a></li>
	<!-- LIST -->
		</ul>
	</div>
	END

	ls -f $pages |
	grep -E '^[0-9]{14}_' |
	sed "s;\(.*\);$pages/\1/categories;" |
	xargs awk '
		{	
			category = $0
			gsub(/_/,"\\_",$0)
			gsub(/ /,"_",$0)
			gsub(/_/,"\\\\\\_",category)
			gsub(/ /,"\\_",category)
			print $0,category
		}' |
	sort -u |
	$dir/bin/insetd LIST $tmp-html -
else
	cat <<-END > $tmp-html
	<div class="categories-list">
	<h2>Categories</h2>
	</div>
	END
	cat $tmp-html	
fi	
	
rm $tmp-*
