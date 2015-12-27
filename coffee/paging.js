var PAGE_LIMIT = 42
var PAGE_NO_TEMPLATE = '<a href="%s">%s</a>'


var template = '<div class="page"></div>'

var formatstr= function(href,page_template,hreftext,templatetext){
	href=href.replace('%s', hreftext);
	page_template=page_template.replace(/\"%s\"/, href);
	page_template=page_template.replace(/%s/,templatetext);
	return page_template
	}
var page = function(href,count,now,limit){
	var now = parseInt(now);
	if (now <= 0)
		now = 1;
		
	var end = Math.floor((count + limit-1)/limit);
	if (now > end)
		now = end;
	
	var scope = 2;
	var total = Math.floor((count + limit-1)/limit);
	
	if (total > 1){
		var merge_begin = false;
		var merge_end = false;
		var omit_len = scope + 3;
		
		if (total <= (scope + omit_len + 1)){
			var begin = 1;
			var end = total;
			}
		else{
			if (now > omit_len){
				merge_begin = true;
				begin = now - scope;
				}
			else
				begin = 1;
			if ((total - now) >=omit_len){
				merge_end = true
				end = now + scope
				}
			else
				end = total
				
			if ((end - begin) < (scope*2)){
				if (now <= omit_len)
					end = Math.min(begin + scope*2, total)
				else
					begin = Math.max(end - scope*2,1)
				
				if (begin > omit_len)
					merge_begin = true;
				else{
					merge_begin = false;
					begin = 1;}
				if ((total - end) >= omit_len)
					merge_end = true
				else{
					merge_end = false
					end = total
					}					
				}
		 }
	}
	var links = [];	
	if (now > 1){

		var pageLink=formatstr(href,PAGE_NO_TEMPLATE,now-1,'&lt')
		links.push(
			pageLink
		)
		}
	else 
		links.push('<span class="plt">&lt;</span>')
	
	if (merge_begin){
		
		
		pageLink=formatstr(href,PAGE_NO_TEMPLATE,1,1)
		pageLink += '...';
		links.push(pageLink)
		
		show_begin_mid = false;
		
		if (begin > 8)
			show_begin_mid = Math.floor(begin/2);
		if (show_begin_mid){
			pageLink=formatstr(href,PAGE_NO_TEMPLATE,show_begin_mid,show_begin_mid)
			pageLink += '...'
			links.push(pageLink)
			}
		}
		for(i= begin; i< now; i++){
			pageLink=formatstr(href,PAGE_NO_TEMPLATE,i,i);
			links.push(pageLink)
			}
		var spanNow='<span class="now">%s</span>'
		spanNow=spanNow.replace(/%s/,now)
		links.push(spanNow)
		
		for (i=now+1;i< end+1;i++){
			pageLink=formatstr(href,PAGE_NO_TEMPLATE,i,i);
			links.push(pageLink)
			}
		if (merge_end){
			links.push('...')
			
			
			}
		if (now < total){
			pageLink=formatstr(href,PAGE_NO_TEMPLATE,now+1,'&gt')
			links.push(pageLink)
			}
		else
			links.push('<span class="pgt">&gt;</span>')
	var htm='';
	for(i=0;i<links.length;i++)
		htm+=links[i]
	var paging=$(template)
	$(htm).appendTo(paging)
	paging.appendTo($('body'))
	
	
		
}
/*
var href="http://google.com%s",
		count=500,
		limit=42,
		now=10;
		
    $(document).ready(page(href,count,now,limit))*/
