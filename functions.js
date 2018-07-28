window.onload = function () {
	recentPosts(3);
	popularPosts(5)
	categoriesList();
	tagsList();
	showComment();
}

function showComment() {
	var httpReq = new XMLHttpRequest();
	httpReq.onreadystatechange = function(){
		if(httpReq.readyState != 4 || httpReq.status != 200)
			return;
		
		text = httpReq.responseText;
		text = text.replace(/%3perc;/g, '%;');
		text = text.replace(/%3lt;/g, '&lt;');
		text = text.replace(/%3gt;/g, '&gt;');
		text = text.replace(/%3/g, '&amp;');
		text = text.replace(/%;/g, '%');
		document.getElementById("comments").innerHTML = text;
	}

		var page = location.search;	
		var pagedir = page.substr(3);
		if (pagedir.match(/[0-9]{14}_/)){
			var data = { pagedir: pagedir };
			var urlEncodedData = encodeHTMLForm(data);
			var url = "/ajax/comment.cgi";
			httpReq.open('POST',url,true);
			httpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
			httpReq.send(urlEncodedData);
		}
}

function comment(name,answer,text) {
	var ANSWER = "安倍晋三";
	var httpReq = new XMLHttpRequest();
	httpReq.onreadystatechange = function(){
		if(httpReq.readyState != 4 || httpReq.status != 200)
			return;

		text = httpReq.responseText;
		text = text.replace(/%3perc;/g, '%;');
		text = text.replace(/%3lt;/g, '&lt;');
		text = text.replace(/%3gt;/g, '&gt;');
		text = text.replace(/%3/g, '&amp;');
		text = text.replace(/%;/g, '%');
		document.getElementById("comments").innerHTML = text;
	}

	if(answer == ANSWER && text != "") {
		if(name == ""){name = "通りすがりのシェル芸人";}

		text = text.replace(/\(/g, '&pl;');
		text = text.replace(/\)/g, '&pr;');
		text = text.replace(/\%/g, '&perc;');
		text = text.replace(/\+/g, '&plus;');

		var page = location.search;	
		var pagedir = page.substr(3);
		var data = { pagedir: pagedir, name: name, text: text };
		var urlEncodedData = encodeHTMLForm(data);
		var url = "/ajax/comment.cgi";
		httpReq.open('POST',url,true);
		httpReq.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
		httpReq.send(urlEncodedData);
		document.getElementById("yourname").value = "";
		document.getElementById("answer").value = "";
		document.getElementById("text").value = "";
	} else if(answer != ANSWER) {
		alert("クイズに答えて下さい。");
	}
}

function encodeHTMLForm(data) {
	var params = [];

	for(var name in data) {
		var value = data[name];
		var param = encodeURIComponent(name) + '=' + encodeURIComponent(value);

		params.push(param);
	}

	return params.join('&').replace(/%20/g, '+');
}

function recentPosts(num) {
	var httpReq = new XMLHttpRequest();
	httpReq.onreadystatechange = function(){
		if(httpReq.readyState != 4 || httpReq.status != 200)
			return;

		document.getElementById("recent-posts").innerHTML = httpReq.responseText;
	}

	var url = "/ajax/recent.cgi?num=" + num;
	httpReq.open("GET",url,true);
	httpReq.send(null);
}

function popularPosts(num) {
	var httpReq = new XMLHttpRequest();
	httpReq.onreadystatechange = function(){
		if(httpReq.readyState != 4 || httpReq.status != 200)
			return;

		document.getElementById("popular-posts").innerHTML = httpReq.responseText;
	}

	var url = "/ajax/popular.cgi?num=" + num;
	httpReq.open("GET",url,true);
	httpReq.send(null);
}
	
function categoriesList() {
	var httpReq = new XMLHttpRequest();
	httpReq.onreadystatechange = function(){
		if(httpReq.readyState != 4 || httpReq.status != 200)
			return;

		document.getElementById("categories").innerHTML = httpReq.responseText;
	}

	var url = "/ajax/categories.cgi";
	httpReq.open("GET",url,true);
	httpReq.send(null);
}

function tagsList() {
	var httpReq = new XMLHttpRequest();
	httpReq.onreadystatechange = function(){
		if(httpReq.readyState != 4 || httpReq.status != 200)
			return;

		document.getElementById("tags").innerHTML = httpReq.responseText;
	}

	var url = "/ajax/tags.cgi";
	httpReq.open("GET",url,true);
	httpReq.send(null);
}

function toggle() {
	var mymenu = document.querySelector(".menu");

	if (mymenu.style.maxHeight) {
		mymenu.style.maxHeight = null;
	} else {
		mymenu.style.maxHeight = mymenu.scrollHeight + "px";
	}
}
