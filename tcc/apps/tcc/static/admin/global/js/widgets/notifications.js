function generateNotification(content) {
  var position = 'topRight';
  var n = noty({
    text: content,
    layout: position,
    theme: 'made',
    animation: {
      open: 'animated fadeIn',
      close: 'animated fadeOut'
    },
    timeout: 4500,
    callback: {
      onShow: function() {
        $('#noty_topRight_layout_container, .noty_container_type_success').css('width', 350).css('bottom', 10);
      }
    }
  });
}

$(function() {
  setTimeout(function() {
    $('[data-notification]').each(function() {
        $this = $(this);
        type = $this.data('notification-type');
        if(type == 'error') {
          type = 'danger';
        }
        $this.addClass('alert-'+type);
        generateNotification($this, type);
      })
  }, 1000)
});
