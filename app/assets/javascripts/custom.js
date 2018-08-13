$(document).on('turbolinks:load',function(){

  $('[data-alert-swal]').on('click', function(e) {
    e.preventDefault()
    $this = $(this)
    var message = $this.data('alert-swal')
    var text = $this.data('text')

    swal({
      title: message || '',
      text: text || '',
      type: 'warning'
    })
  })
})
