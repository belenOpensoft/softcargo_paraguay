var table  = false;
var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;
var vertodo = false;

$(document).ready(function()
    {
        var contador = 1;

        $('#tabla_guias tfoot th').each( function () {
            var title = $(this).text();
            if(title != ''){
                $(this).html( '<input type="text" class="form-control" id="buscoid_' + contador + '" type="text" placeholder="Buscar '+title+'"  autocomplete="off" />' );
                contador++;
            }else{
                var aux2 = 'Borrar';
                $(this).html( '<button class="btn" title="Borrar filtros" id="clear" ><span class="glyphicon glyphicon-erase"></span></button> ' );
            }
        });

        table = $('#tabla_guias').DataTable( {
             "stateSave": true,
             dom: 'Btlipr',
//             dom: 'Brtl',
             buttons: [
                    {
                        text: 'MANTENIMIENTO DE GUIAS AEREAS',
                        className: 'btn btn-dark',
                        action: function (e, dt, button, config) {

                        }
                    },
                    {
                        text: 'Agregar',
                        action: function (e, dt, button, config) {
                            window.location.replace("/agregar_guias");
                        }
                    },
                    {
                        text: 'Anular',
                        action: function (e, dt, button, config) {
                            if(row = table.row('.selected').data()){
                                miurl = "/anular_guia";
                                    var toData = { 'id' : row[0] };
                                    $.ajax({
                                        type: "GET",
                                        url: miurl,
                                        data: toData,
                                        success:function(resultado){
                                            aux = resultado['resultado'];
                                            if(aux == 'exito'){
                                                table.ajax.reload();
                                            }else{
                                                alert(aux);
                                            }
                                        }
                                    });
                            }else{
                                alert('Debe seleccionar un registro');
                            }
                        }
                    }

            ],
             "columnDefs": [
                {
                    "targets": [ 0 ],
                    "orderable": false,
                    "data": null,
                    "defaultContent": '',
                    "visible": false
                },
                {
                    "targets": [ 1],
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
                },
                {
                    "targets": [ 6],
                },
                {
                    "targets": [ 7],
                },
            ],
            "order": [[ 1, "asc" ]],
            "processing": true,
            "serverSide": true,
            "ajax": {
                "url": "/source_guias",
                'type':'GET',
                "data": function ( d ) {
                      return $.extend( {}, d, {
                        "vertodo": vertodo,
                      } );
                }
            },
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

        $('#tabla_guias tbody').on( 'click', 'tr', function()
        {
            if ($(this).hasClass('selected') )
            {
                $(this).removeClass('selected');
            }
            else
            {
                var row = table.row( $(this).closest('tr') ).data();
                table.$('tr.selected').removeClass('selected');
                $(this).addClass('selected');
            }
        });

         $('#vertodo').click(function() {
            if (this.checked) {
                vertodo = true;
            } else {
                vertodo = false;
            }
            table.clear().draw();
            return true;
        });



    $(".alert").delay(4000).slideUp(200, function() {$(this).alert('close');});
    }
);