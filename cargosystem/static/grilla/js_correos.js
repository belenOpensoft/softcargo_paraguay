var table  = false;
var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;

$(document).ready(function()
    {
        var contador = 1;
        $('#tabla_correos tfoot th').each( function () {
            var title = $(this).text();
            if(title != ''){
                $(this).html( '<input type="search" class="form-control" id="buscoid_' + contador + '" type="text" placeholder="Buscar '+title+'"  autocomplete="off"/>' );
                contador++;
            }else{
                var aux2 = 'Borrar';
                $(this).html( '<button class="btn" title="Borrar filtros" id="clear" ><span class="glyphicon glyphicon-erase"></span></button> ' );
            }
        });
        table = $('#tabla_correos').DataTable( {
             "stateSave": true,
             "scrollX": true,
             "bAutoWidth": false,
             'dom': 'Btlipr',
            "rowCallback": function(row, data, index) {
                var modulo = data[11];

                // Limpiar clases anteriores solo en la columna 7
                $('td:eq(7)', row).removeClass('bg-success bg-primary bg-opacity-75 text-white bg-success-light bg-primary-light');

                if (modulo === 'SG') {
                    $('td:eq(7)', row).addClass('bg-success-light text-dark'); // verde claro
                } else if (modulo) {
                    $('td:eq(7)', row).addClass('bg-primary-light text-dark'); // azul claro
                }
            },
             "columnDefs": [
                {
                   "targets": [ 0 ],
                    "className": 'details-control',
                    "orderable": false,
                    "data": null,
                    "defaultContent": ''
                },
                {
                    "targets": [ 1 ],
                },
                {
                    "targets": [ 2],
                },
                {
                    "targets": [ 3],
                },
                {
                    "targets": [ 4],
                },
                {
                    "targets": [ 5],
//                    "class": 'text-right'
                },
                 {
                    "targets": [ 6],
                },
                 {
                    "targets": [ 7],
                },
                 {
                    "targets": [ 8],
                }

            ],
            "order": [[ 1, "desc" ]],
            "processing": true,
            "serverSide": true,
            "ajax": "/source_correos",
            "language": {
                url: "/static/datatables/es_ES.json"
            },
            initComplete: function() {
//                  $(".dataTables_length select").addClass("form-control");
                  var api = this.api();
                  // Apply the search
                  api.columns().every(function() {
                    var that = this;
                    $('input', this.footer()).on('keyup change', function() {
                      if (that.search() !== this.value) {
                        that
                          .search(this.value)
                          .draw();
                      }
                    });
                  });
                },
                "drawCallback": function( settings ) {
                }
        } );
        $( table.table().container() ).on( 'keyup', 'tfoot input', function () {
            table
                .column( $(this).data('index') )
                .search( this.value )
                .draw();
        } );
        var state = table.state.loaded();
        if ( state ) {

          table.columns().eq( 0 ).each( function ( colIdx ) {
                var colSearch = state.columns[colIdx].search;
                if ( colSearch.search) {
                  var aux = colSearch.search;
                  document.getElementById('buscoid_' + colIdx).value = aux;
                }
          } );
          table.draw();
        };

        $('#tabla_correos tbody').on( 'click', 'tr', function()
        {
            if ($(this).hasClass('table-secondary') )
            {
                $(this).removeClass('table-secondary');
            }
            else
            {
                var row = table.row( $(this).closest('tr') ).data();
                table.$('tr.table-secondary').removeClass('table-secondary');
                $(this).addClass('table-secondary');
            }
        });
        $('#tabla_correos tbody').on('click', 'td.details-control', function () {
            var tr = $(this).closest('tr');
            var row = table.row( tr );
            if(row.child.isShown()){
                row.child.hide();
                tr.removeClass('shown');
            }else{
                table.row(".shown").child.hide();
                $("#tabla_grupo tr").removeClass("shown");
                if ( row.child.isShown() ) {} else {
                    row.child( format(row.data()), 'addinfowrapper').show();
                    tr.addClass('shown');
                }
            }
        } );
    });

/* eXTRA FUNCTIONs*/
function format ( d ) {
    // `d` is the original data object for the row
    text = '<table cellpadding="5" class="table table-condensed" cellspacing="0" border="0" style="padding-left:50px;"><tfoot>';
    mensaje = d[10].replace('\n','<br>');
    text += '<tr><td><p>MENSAJE: ' + mensaje + '</p></td></tr>';
    if(d[9].length > 0){
        text += '<tr><td>ERROR: ' + d[9] + '</td></tr>';
    }
    text += '</table>';
    return text
}