$(function() {
  $('[data-not-enough-points]').on('click', function(e) {
    e.preventDefault();
    var value = $(this).text();
    swal({
      type: "error",
      title: "Saldo insuficiente!",
      text: "Este item custa <strong>"+value+"</strong> e você não possui pontos o suficiente para adquirí-lo.",
      html: true
    });
  });
  $('[data-purchase-product]').on('click', function(e) {
    e.preventDefault();
    $this = $(this);
    var value = $this.text();
    swal({
      title: "Deseja mesmo comprar?",
      text: "Este item custa <strong>"+value+"</strong>. Deseja mesmo adquirí-lo?",
      type: "info",
      showCancelButton: true,
      confirmButtonColor: "#a5dc86",
      confirmButtonText: "Sim, comprar!",
      cancelButtonText: "Não, cancele!",
      closeOnConfirm: true,
      html: true,
      closeOnCancel: true },
    function(isConfirm){
      if (isConfirm) {
        window.location = $this.attr('href');
      }
    });
  });
})
