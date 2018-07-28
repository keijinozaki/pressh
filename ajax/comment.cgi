#!/bin/bash -xv

dir=$(dirname $0)/..
tmp=/tmp/$$
#email="your mail address"

echo "Content-Type: text/html"
echo
eval $(dd bs=${CONTENT_LENGTH} | sed 's/&/;/g')
pagedir=$(echo $pagedir | nkf --url-input)
name=$(echo $name | nkf --url-input | sed -e 's/+/ /g' -e 's/_/\\_/g' -e 's/ /_/g' | $dir/bin/entref)
text=$(echo $text | sed 's;%0A;<br />;g' | nkf --url-input | sed -e 's/+/ /g' -e 's/_/\\\\_/g' -e 's/ /_/g' | $dir/bin/entref | sed 's/&lt;br_\/&gt;/<br_\/>/g')
date=$(date "+%Y%m%d%H%M%S" | sed 's/\(....\)\(..\)\(..\)\(..\)\(..\)\(..\)/\1-\2-\3_\4:\5:\6/')
comments=$dir/comments/$pagedir/comments

if ls $dir/pages | grep -q $pagedir && [ ! -d $dir/comments/$pagedir ] && [ ! -e $comments ]; then
   mkdir $dir/comments/$pagedir
   touch $comments
   chmod 777 $dir/comments/$pagedir
   chmod 777 $comments
fi

if [ -z "$(echo $text)" ] && [ -n "$(cat $comments)" ]; then
	$dir/bin/insetd COMMENT $dir/comment_template.html $comments
elif [ -n "$(echo $text)" ]; then
	awk -v name="$name" -v date="$date" -v text="$text" '
		BEGIN{print name, date, text}
		{print}' $comments |
	tee $tmp-comments |
	$dir/bin/insetd COMMENT $dir/comment_template.html -
fi

if [ -n "$email" ] && [ -n "$(echo $text)" ]; then
	cat $tmp-comments > $comments

	cat <<-END | mail -s '[pressh]: comment' $email
	コメントが投稿されました:
	[name]: $name
	[date]: $date
	[text]: $text

	このコメントを削除する場合は下のコマンドをコピペしてローカルの端末で実行して下さい
	ssh ${HTTP_HOST} '$dir/bin/delcomment p=$pagedir\&d=$date 2> /dev/null'
	END
fi

rm $tmp-*
