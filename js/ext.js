(function() {

  jQuery.fn.extend({
    ctrl_enter: function(callback) {
      return $(this).keydown(function(event) {
        event = event.originalEvent;
        if (event.keyCode === 13 && (event.metaKey || event.ctrlKey)) {
          if (typeof callback === "function") {
            callback();
          }
          return false;
        }
      });
    },
    click_drop: function(drop, callback1, callback2) {
      var html;
      html = $("html,body");
      return $(this).click(function(e) {
        var clicked, self, _;
        self = this;
        self.blur();
        _ = function() {
          drop.hide();
          html.unbind('click', _);
          return callback2 && callback2();
        };
        if (drop.is(":hidden")) {
          drop.show();
          e.stopPropagation();
          html.click(_);
          clicked = true;
          return callback1 && callback1();
        } else {
          return _();
        }
      });
    }
  });

  jQuery.extend({
    escape: function(txt) {
      return $('<div/>').text(txt).html();
    },
    html: function() {
      var r, _;
      r = [];
      _ = function(o) {
        return r.push(o);
      };
      _.html = function() {
        return r.join('');
      };
      return _;
    }
  });

}).call(this);
