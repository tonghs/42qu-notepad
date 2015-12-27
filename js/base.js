function _focus(sel, start, end) {
    if (sel.setSelectionRange) {
    sel.focus();
    sel.setSelectionRange(start,end);
    }
    else if (sel.createTextRange) {
        var range = sel.createTextRange();
        range.collapse(true);
        range.moveEnd('character', end);
        range.moveStart('character', start);
        range.select();
    }
}
function focus(sel) {
    length=sel.value.length;
    _focus(sel, length, length);
}



$(function(){
    $('.back').click(function(){
        $(window).scrollTop(0)
    });
})


