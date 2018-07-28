#!/bin/bash -xv

dir=$(dirname $0)
tmp=/tmp/$$

# １ページに表示する記事リストの数
LIMIT=15
export LIMIT

# デバッグ用コマンド実行記録
exec 2> $dir/../www-data/$(basename $0).$(date +%Y%m%d%H%M%S).$$

# クエリから余計な記号を削除した後、evalを使って代入を実行
eval $(echo ${QUERY_STRING} | tr -d ' `|<>{}()[]/;' | sed 's/&/;/')

# 変数nは表示する記事リストの最後の記事No
n=$(echo "$n" | tr -dc '0-9')

# nに値がない場合$LIMITで初期化
[ -z "$n" ] && n=$LIMIT

# 特定のカテゴリーの記事一覧を表示
# 変数$cはカテゴリー名
# 記事一覧には($n - $LIMIT)本目の記事からn本目の記事までが表示される
if [ -n "$c" ]; then
	$dir/show_category "$c" "$n"

# 特定のタグが付けられた記事一覧を表示
# 変数$tはカテゴリー名
# 記事一覧には($n - $LIMIT)本目の記事からn本目の記事までが表示される
elif [ -n "$t" ]; then
	$dir/show_tag "$t" "$n"

# 記事ページを表示
# 変数$pは記事ディレクトリ名
elif [ -n "$p" ]; then
	$dir/show_page "$p"

# 全文検索の結果を表示
# 変数$wは検索ワード
# 結果一覧には($n - $LIMIT)本目の記事からn本目の記事までが表示される
elif [ -n "$w" ]; then
	$dir/full_search "$w" "$n"

# 記事が存在すれば記事一覧を表示
elif [ -n "$(cat $dir/cache/info | head -n 1)" ]; then
	# 前の一覧ページの表示範囲
	prev=$((n - $LIMIT))
	# 次の一覧ページの表示範囲
	next=$((n + $LIMIT))
	# 総記事数
	max=$(cat $dir/cache/info | wc -l)

	# ナビゲーション文字と表示範囲を計算するための値を一時ファイルに出力
	awk "BEGIN{if($prev>=$LIMIT){print \"PREV\",$prev}
			   if($next<($max+$LIMIT)){print \"NEXT\",$next}}" > $tmp-pagenavi

	# ナビゲーションを表示する必要があればHTMLを作って一時ファイルに出力
	if [ -n "$(cat $tmp-pagenavi)" ]; then
	cat <<-END > $tmp-navi
	<div class="listnavi">
	<!-- PAGENAVI -->
		<div class="prevnext"><a href="?n=%2">%1</a></div>
	<!-- PAGENAVI -->
	</div>
	END
	fi

	echo "Content-Type: text/html"
	echo
	cat $dir/cache/info |
	# キャッシュから一覧表示に必要な分だけデータを取り出す
	awk "NR==($n - $LIMIT + 1),NR==$n{print}" |
	# データをmklistに渡して記事サマリのリストを作る
	$dir/bin/mklist |
	# 記事サマリのリストの最初と最後にCSS用のタグを出力
	awk 'BEGIN{print "<div class=\"summary-list\">"}
		 {print}
		 END{print "</div>"}' |
	# 最後に部分的に作ったHTMLをつなげて
	# 最終的にブラウザに出力するHTMLを組み立てる
	$dir/bin/insetf DOCUMENT template.html - |
	$dir/bin/insetf HEADER - header.html |
	$dir/bin/insetf NAVI - $tmp-navi |
	$dir/bin/insetd PAGENAVI - $tmp-pagenavi |
	$dir/bin/insetf SIDE - side.html |
	$dir/bin/insetf ADSIDE - ad_side.html |
	$dir/bin/insetf FOOTER - footer.html |
	# 記事一覧の場合はブラウザのタブに
	# 記事タイトルを表示する必要はないので削除
	sed 's/@title &#124; //'

	rm $tmp-*

# 記事が一つもない場合は本体部分には何も表示しない
else
	echo "Content-Type: text/html"
	echo
	$dir/bin/insetf HEADER template.html header.html |
	$dir/bin/insetf SIDE - side.html |
	$dir/bin/insetf ADSIDE - ad_side.html |
	$dir/bin/insetf FOOTER - footer.html |
	sed 's/@title &#124; //'
fi
