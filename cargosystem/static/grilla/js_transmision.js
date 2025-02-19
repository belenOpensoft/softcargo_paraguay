var table  = false;
var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;

$(document).ready(function()
    {

    table = $('#tabla_transmision').DataTable( {
        "language": {
            url: "/static/datatables/es_ES.json"
        },"columnDefs": [
                 {
                   "targets": [ 0 ],
                    "orderable": false,
                    "defaultContent": '',
                    "visible": false
        },],
        select: {
            style: 'multi'
        }
    } );

    $('#informar').on('click', function () {
        var selectedData = table.rows({ selected: true }).data().toArray();
        if (selectedData.length === 0) {
              alert('Por favor, seleccione al menos una fila antes de enviar.');
              return;
        }
        var toData = {
                    'data': JSON.stringify(selectedData),
                    'csrfmiddlewaretoken': csrf_token,
                };
        $.ajax({
          url: '/desconsolidar_aereo/',
          type: 'GET',
          data: toData,
          contentType: 'application/json; charset=utf-8',
          success: function (response) {
                console.log(response['resultado']);
                alert('XML generado correctamente');
          },
          error: function (error) {
            alert(error);
          }
        });
    });





});


function format(d) {
    // `d` is the original data object for the row
    return '<table class="table table-sm table-responsive   " cellpadding="5" cellspacing="0" border="0" style="padding-left:30px;">' +
        '<tbody>' +
        '<tr>' +
        '<th class="derecha">Cliente:</th>' +
        '</tr>' +
        '</tbody>' +
        '</table>';
}