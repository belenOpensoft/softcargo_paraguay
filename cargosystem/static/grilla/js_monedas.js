var table  = false;
var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;

$(document).ready(function()
    {
        var contador = 1;


        $('#tabla_moneda tfoot th').each(function(index) {
            let title = $('#tabla_moneda thead th').eq(index).text();

            if (index === 0) {
                // Si es la primera columna, colocar el botón de limpiar filtros
                $(this).html('<button class="btn btn-danger" title="Borrar filtros" id="clear"><span class="glyphicon glyphicon-erase"></span> Limpiar</button>');
            } else if (title !== '') {
                // Agregar inputs de búsqueda en las demás columnas
                $(this).html('<input type="text" class="form-control filter-input" autocomplete="off" id="buscoid_' + index + '" placeholder="Buscar ' + title + '" />');
            }
        });
        table = $('#tabla_moneda').DataTable( {
             "stateSave": true,
             dom: 'Btlipr',
//             dom: 'Brtl',
             buttons: [
                    {
                        text: 'Agregar',
                        action: function (e, dt, button, config) {
                            redirectConRol
("/agregar_moneda");
                        }
                    },
                    {
                        text: 'Modificar',
                        action: function (e, dt, button, config) {
                            let row = table.row('.selected').data();
                            if(row){
                                redirectConRol
("/modificar_moneda/" + row[0]);
                            }else{
                                alert('Debe seleccionar un registro');
                            }
                        }
                    },
                    {
                        text: 'Eliminar',
                        action: function (e, dt, button, config) {
                            let row = table.row('.selected').data();
                            if (row) {
                                if (confirm('Esta seguro de eliminar: ' + row[2])) {
                                    let path = "/eliminar_moneda";
                                    let toData = {'id': row[0]};
                                    $.ajax({
                                        type: "GET",
                                        url: path,
                                        data: toData,
                                        success: function (result) {
                                            let aux = result['resultado'];
                                            if (aux === 'exito') {
                                                table.ajax.reload();
                                            } else {
                                                alert(aux);
                                            }
                                        }
                                    });
                                }
                            } else {
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
                {
                    "targets": [ 5],
                },
                {
                    "targets": [ 6],
                },
                {
                    "targets": [ 7],
                },
                {
                    "targets": [ 8],
                },
                {
                    "targets": [ 9],
                },
                {
                    "targets": [ 10],
                },
                {
                    "targets": [ 11],
                },
            ],
            "order": [[ 1, "asc" ]],
            "processing": true,
            "serverSide": true,
            "ajax": "/source_monedas",
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
        let state = table.state.loaded();

        if ( state ) {
          table.columns().eq( 0 ).each( function ( colIdx ) {
                var colSearch = state.columns[colIdx].search;
                if ( colSearch.search) {
                  var aux = colSearch.search;
                  document.getElementById('buscoid_' + colIdx).value = aux;
                }
          } );
          table.draw();
        }

        $('#tabla_moneda tbody').on( 'click', 'tr', function()
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

    $(".alert").delay(4000).slideUp(200, function() {$(this).alert('close');});
    }
);