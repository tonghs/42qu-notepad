date_build = (timestamp) ->
    date = new Date(timestamp * 1000)
    month = date.getMonth() + 1
    year = date.getFullYear()
    day = date.getDate()
    "<p class=\"time\"><strong>" + year + "</strong>" + "<span>" + ("0" + month).substr(-2) + "&nbsp;.&nbsp;" + ("0" + day).substr(-2) + "</span>" + "</p>"


section_tmpl = (o) ->
    _ = $.html()
    for data in o[..-2]
       date_string = date_build(data[0])
       _ """
  <div class="section">
       #{date_string}
       <p class="content">
             #{$.escape(data[1])}
       </p>
       <a class="more" href="javascript:void(0)" rel="#{data[2]}">#{data[3]}<span>字<span></a>
  </div>
       """
    _.html() 

$(".section .more").live(
    "click"
    ->
        self = this
        self.href="/:id/"+this.rel
        setTimeout(
            -> 
                self.href = "javascript:void(0)"
            0
        ) 
)


window.page_history = (page) ->
    if not page
        page = 1 

    if page > 1
        hash = "#!"+page
    else
        hash = ''
    location.hash = hash
    note_list = $('#note-list')
    $('.page').html('<div id="note_list_loading"/>')
    $.getJSON(
       "/:j/history-#{page}",
       (data)->
           note_list.html(section_tmpl(data))
           href="javascript:page_history($page);void(0);"
           count = data[data.length-1][0]
           now = data[data.length-1][1]
           limit = data[data.length-1][2]
           $('.page').html(pager(href,count,now,limit))
           $(window).scrollTop(0)
    )



    

page_history(location.hash.slice(2))
