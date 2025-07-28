var table  = false;
var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;

$(document).ready(function()
    {
        var contador = 1;

        $('#tabla_servicio tfoot th').each(function(index) {
            let title = $('#tabla_servicio thead th').eq(index).text();

            if (index === 0) {
                // Si es la primera columna, colocar el botón de limpiar filtros
                $(this).html('<button class="btn btn-danger" title="Borrar filtros" id="clear"><span class="glyphicon glyphicon-erase"></span> Limpiar</button>');
            } else if (title !== '') {
                // Agregar inputs de búsqueda en las demás columnas
                $(this).html('<input type="text" class="form-control filter-input" autocomplete="off" id="buscoid_' + index + '" placeholder="Buscar ' + title + '" />');
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
let api = this.api();

                    // Cargar estado guardado
                    let state = table.state.loaded();
                    if (state) {
                        // Restaurar filtros en los inputs y aplicar clase si tienen valor
                        api.columns().every(function(index) {
                            let colState = state.columns[index];
                            if (colState && colState.search.search) {
                                let input = $('#buscoid_' + index);
                                input.val(colState.search.search); // Restaurar valor
                                if (colState.search.search.trim() !== "") {
                                    input.addClass("is-invalid"); // Agregar clase roja si hay filtro
                                }
                            }
                        });
                    }

                    // Evento para resaltar inputs cuando tienen contenido
                    $(document).on("input", ".filter-input", function() {
                        if ($(this).val().trim() !== "") {
                            $(this).addClass("is-invalid"); // Se pone en rojo
                        } else {
                            $(this).removeClass("is-invalid"); // Se quita el rojo si se vacía
                        }
                    });

                    // Agregar funcionalidad de filtrado
                    api.columns().every(function() {
                        let that = this;
                        $('input', this.footer()).on('keyup change', function() {
                            if (that.search() !== this.value) {
                                that.search(this.value).draw();
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