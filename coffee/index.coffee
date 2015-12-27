txt = $ '#txt'
date = new Date()
posted = true
timer = 0

txt_val = ''

fav = (href)-> 
    $('#favicon').remove()
    link = document.createElement('link')
    link.type = 'image/gif'
    link.rel = 'shortcut icon'
    link.id = 'favicon'
    link.href = href
    document.getElementsByTagName('head')[0].appendChild(link)


post = ->
    if not posted
        val = $.trim(txt.val())
        if txt_val!=val
            posted = false
            fav("/css/img/load.gif")
            $.post(
                location.href,
                {txt: val},
                ->
                    fav("/css/img/fav.gif")
                    posted = true 
                    txt_val = val
            )
    timer && clearTimeout timer
    timer = setTimeout(post,3000)

key = ->
    if posted and txt_val!=$.trim(txt.val())
        fav('/css/img/favicon.gif')
        posted = false
    return 1

enableTextareaTabInsertion = (t, evt)->
    self = $ t
    now_top = self.scrollTop()
    kc =  if evt.which then evt.which else evt.keyCode
    isSafari = navigator.userAgent.toLowerCase().indexOf('safari') != -1

    if kc == 9 || (isSafari && kc == 25) 
        t.focus();
        
        # hack for ie
        if t.selectionStart == undefined  
            range = document.selection.createRange()
            stored_range = range.duplicate()
            stored_range.moveToElementText t
            stored_range.setEndPoint('EndToEnd', range)
            t.selectionStart = stored_range.text.length - range.text.length
            t.seletcionEnd = t.selectionStart + range.text.length
            t.setSelectionRange = (start, end)->
                range = this.creatTextRange()
                range.collapse true
                range.moveStart('character', start)
                range.moveEnd('character', end - start)
                range.select()
        tablen = 4
        tab = '    '
        tab_regexp = /\n\s\s\s\s/g
        ss = t.selectionStart
        se = t.selectionEnd
        ta_val = t.value
        sel = ta_val.slice(ss,se)
        shft = (isSafari && kc ==25) || evt.shiftKey
        was_tab = ta_val.slice(ss - tablen, ss) == tab
        starts_with_tab = ta_val.slice(ss, ss+tablen) == tab
        offset = if shft then 0-tablen else tablen
        full_indented_line = false
        num_lines = sel.split('\n').length

        if ss != se && sel[sel.length-1] == '\n'
            se--
            sel = ta_val.slice(ss,se)
            num_lines--
        if num_lines == 1 && starts_with_tab 
            full_indented_line = true
        if !shft || was_tab ||num_lines > 1 || full_indented_line
            # multi-line selection
            if num_lines > 1
                #tab each line
                if (shft && (was_tab || starts_with_tab) && sel.split(tab_regexp).length == num_lines)
                    if (!was_tab) 
                        sel = sel.substring(tablen)
                        t.value = ta_val.slice(0, ss - (was_tab ? tablen: 0)).concat(sel.replace(tab_regexp, "\n")).concat(ta_val.slice(se, ta_val.length))
                        ss += was_tab ? offset: 0
                        se += offset * num_lines  
                    else if (!shft)
                        t.value = ta_val.slice(0, ss).concat(tab).concat(sel.replace(/\n/g, "\n" + tab)).concat(ta_val.slice(se, ta_val.length))
                        se += offset * num_lines
            else
                if shft
                    t.value = ta_val.slice(0, ss - (full_indented_line ? 0 : tablen)).concat(ta_val.slice(ss + (full_indented_line ? tablen: 0), ta_val.length))
                else
                    t.value = ta_val.slice(0, ss).concat(tab).concat(ta_val.slice(ss, ta_val.length))
                if ss == se
                    ss = se = ss + offset
                else
                    se += offset
        #setTimeout("var t=$('" + t.class + "'); t.focus(); t.setSelectionRange(" + ss + ", " + se + ");", 0)
        t.setSelectionRange(ss,se)
        self.scrollTop(now_top)
        false

save = ->
    if not posted
        setTimeout(post,0)

$ ->
    txt_val = $.trim(txt.val())
    txt.keydown(key)
    txt.keyup(key)
    txt.blur(save)

    focus txt[0]
    post()


    txt.bind('keydown',
        (e)->
            self = $ this
            enableTextareaTabInsertion(this,e)
    )

    if !($.cookie.get('S'))
        $('.more').css("background-position","0 0").attr('target','_blank')

