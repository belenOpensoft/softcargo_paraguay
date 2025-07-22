var table  = false;
var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;

$(document).ready(function()
    {
        var contador = 1;

        $('#tabla_servicio tfoot th').each( function () {
            var title = $(this).text();
            if(title != ''){
                $(this).html( '<input type="text" class="form-control" id="buscoid_' + contador + '" type="text" placeholder="Buscar '+title+'"  autocomplete="off" />' );
                contador++;
            }else{
                var aux2 = 'Borrar';
                $(this).html( '<button class="btn" title="Borrar filtros" id="clear" ><span class="glyphicon glyphicon-erase"></span></button> ' );
            }
        });

        table = $('#tabla_servicio').DataTable( {
             "stateSave": true,
             dom: 'Btlipr',
//             dom: 'Brtl',
             buttons: [

                    {
                        text: 'Agregar',
                        action: function (e, dt, button, config) {
                            redirectConRol
("/agregar_servicio");
                        }
                    },
                    {
                        text: 'Clonar',
                        action: function (e, dt, button, config) {
                            var row = table.row('.table-secondary').data();
                            if (row) {
                                let opuesto = confirm('¿Desea crear el opuesto?');
                                var id_servicio = row[0]; // Obtiene el ID del servicio seleccionado

                                $.ajax({
                                    type: "POST",
                                    url: "/clonar_servicio/" + id_servicio,  // Llama a la vista en Django
                                    data: {
                                        csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                                        opuesto: opuesto
                                    },
                                    success: function(response) {
                                        if (response.status === "success") {
                                            alert(response.message);
                                            table.ajax.reload();  // Recargar la tabla después de clonar
                                        } else {
                                            alert("Error: " + response.message);
                                        }
                                    },
                                    error: function() {
                                        alert("Ocurrió un error al clonar el servicio.");
                                    }
                                });

                            } else {
                                alert('Debe seleccionar un servicio para clonar.');
                            }
                        }
                    },
                    {
                        text: 'Modificar',
                        action: function (e, dt, button, config) {
                            if(row = table.row('.table-secondary').data()){
                                redirectConRol
("/modificar_servicio/" + row[0]);
                            }else{
                                alert('Debe seleccionar un registro');
                            }
                        }
                    },
                    {
                        text: 'Eliminar',
                        action: function (e, dt, button, config) {
                            if(row = table.row('.table-secondary').data()){
                                if(confirm('Esta seguro de eliminar: ' + row[2])){
                                    miurl = "/eliminar_servicio";
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
                                }
                            }else{
                                alert('Debe seleccionar un registro');
                            }
                        }
                    },

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
            ],
            "order": [[ 1, "asc" ]],
            "processing": true,
            "serverSide": true,
            "ajax": "/source_servicios",
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

        $('#tabla_servicio tbody').on( 'click', 'tr', function()
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

    $(".alert").delay(4000).slideUp(200, function() {$(this).alert('close');});
    }
);