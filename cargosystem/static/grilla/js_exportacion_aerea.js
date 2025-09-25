/* INITIAL CONTROL PAGE */
var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;

/* INITIAL TABLES */
var table = false;
var table_envases = false;
var table_logs = false;
var table_embarques = false;
var table_gastos = false;
var table_archivos = false;

/* ROWS SELECTED FOR TABLES */
var row_selected = 0;
var row_selected_envase = 0;
var row_selected_embarque = 0;
var row_selected_archivo = 0;
var row_selected_ruta = 0;


/* JOB NUMBER SELECTED */
var row_number = 0;
var row_number_embarque = 0;
var row_number_archivo = 0;
var row_number_envase = 0;
var row_number_ruta = 0;



/* INITIAL PAYMENTS */
var ingresos = 0;
var egresos = 0;
var diferencia = 0;

/* DATA AUXILIAR */
var tipo_seguimiento = '';
var archivos_adjuntos = {};
var buscar = '';
var que_buscar = '';
var nombre_form = 'Nuevo'
var awbRegex = "";


let table_add_ea;

$(document).ready(function () {
    $(document).on("submit", "#searchForm", function(e) {
        e.preventDefault();
        let formData = $(this).serialize();
        filtrar_tabla_master(formData, e);
        $("#searchModal").dialog("close");
    });

    $("#modalSeleccionEmailHouse5").dialog({
        autoOpen: false,
        modal: true,
        width: 400,
        height: 400,
        resizable: false,
        draggable: false,
        title: 'Seleccione el tipo de aviso House',
        open: function (event, ui) {
            $(this).parent().css('overflow', 'hidden');
            $('#buscadorEmailsHouse5').val('');
            $("#listaEmailsHouse5 tr").show();

            $('#buscadorEmailsHouse5').on('keyup', function () {
                let valor = $(this).val().toLowerCase();
                $("#listaEmailsHouse5 tr").filter(function () {
                    $(this).toggle($(this).text().toLowerCase().indexOf(valor) > -1);
                });
            });
        }
    });

     $('input.autocomplete').on('keydown', function(event) {
        var keyCode = event.keyCode || event.which;

        if (keyCode === 13 || keyCode === 9) { // 'Enter' (13) o 'Tab' (9)
            var activeItem = $(".ui-menu-item:hover");
            if (activeItem.length > 0) {
                var selectedValue = activeItem.find("a").text();
                $(this).val(selectedValue);  // Establece el valor automáticamente
            }
        }
    });
    setTimeout(function(){
        $('.navbar-collapse').collapse('hide');
    }, 5000);

    /* AUTOMATIC DELETION FOR ALER  T SET IN 4 SECONDS */
    $(".alert").delay(4000).slideUp(200, function () {
        $(this).alert('close');
    });



    getCookie('row_selected_impomarit');
    let contador = 0;

    /* DATATABLES */
    //buscadores
    $('#tabla_exportaerea tfoot th').each(function(index) {
    let title = $('#tabla_exportaerea thead th').eq(index).text();

    if (index === 0) {
        $(this).html('<button class="btn btn-danger" title="Borrar filtros" id="clear"><span class="glyphicon glyphicon-erase"></span> Limpiar</button>');
    } else if (title !== '') {
        $(this).html('<input type="text" class="form-control filter-input" autocomplete="off" id="buscoid_' + index + '" placeholder="Buscar ' + title + '" />');
    }
});

    // Evento para limpiar todos los filtros
    $(document).on("click", "#clear", function() {
        awbRegex='';
        $(".filter-input").val("").trigger("keyup"); // Limpia los inputs y activa la búsqueda
        $(".filter-input").removeClass("is-invalid"); // Se quita el rojo si se vacía
        table.ajax.reload();
    });

    // Evento para resaltar los inputs cuando tienen contenido
    $(document).on("input", ".filter-input", function() {
        if ($(this).val().trim() !== "") {
            $(this).addClass("is-invalid"); // Se pone en rojo
        } else {
            $(this).removeClass("is-invalid"); // Se quita el rojo si se vacía
        }
    });

    //tabla general master
    table = $('#tabla_exportaerea').DataTable({
        "stateSave": true,
        "dom": 'Btlipr',
        "scrollX": true,
        "bAutoWidth": false,
        "scrollY": wHeight * 0.60,
        "columnDefs": [
            {
                "targets": [0],
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": '',
                render: function (data, type, row) {

                }
            },
            {
                "targets": [1],
                "className": 'derecha archivos',
                "visible":false
            },

            {
                "targets": [3],
            },
            {
                "targets": [2],
                "className": 'text-primary',
                render: function (data, type, row, meta) {
                    if (type === 'display' && data) {
                        const partes = data.split(';');
                        if (partes.length <= 3) {
                            return `<span class="badge bg-primary text-light">${data}</span>`;
                        }
                        const visibles = partes.slice(0, 3).join(';') + ';...';
                        return `<span class="badge bg-primary text-light" title="${data}">${visibles}</span>`;
                    }
                    return data;
                }
            },
            {
                "targets": [5],
                render: function (data, type, row, meta) {
                if (type === 'display' && data) {
                    const partes = data.split(';');
                    if (partes.length <= 4) return data;
                    const visibles = partes.slice(0, 4).join(';') + ';...';
                    return `<span title="${data}">${visibles}</span>`;
                }
                return data;
            }
            }


        ],
        "order": [[1, "desc"],],
        "processing": true,
        "serverSide": true,
        "pageLength": 100,
        "ajax": {
            "url": "/exportacion_aerea/source_master",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "buscar": buscar,
                    "que_buscar": que_buscar,
                    "awb_filter": JSON.stringify(awbRegex)

                });


            }
        },
//
//         "drawCallback": function (settings) {
//        // Guardar los datos en localStorage después de que la tabla se haya dibujado
//        var data = table.rows({search: 'applied'}).data().toArray();
//        localStorage.setItem('lista_masters', JSON.stringify(data));
//        },
        "language": {
            url: "/static/datatables/es_ES.json"
        },
                initComplete: function () {
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
        "rowCallback": function (row, data) {

        },
    });
    let state = table.state.loaded();

    table.columns().iterator('column', function (ctx, idx) {
        table.column(idx).nodes().to$().addClass('columna-acciones');
    });

    table.on('draw', function () {
    });
    $(table.table().container()).on('keyup', 'tfoot input', function () {
        table
            .column($(this).data('index'))
            .search(this.value)
            .draw();
    });

    if(state){
        table.columns().eq(0).each(function (colIdx) {
            var colSearch = state.columns[colIdx].search;
            if (colSearch.search) {
                var aux = colSearch.search;
                document.getElementById('buscoid_' + colIdx).value = aux;
            }
        });
        table.draw();
    }

    //descargar guias
    $('#descargar_guia').click(function () {
         let selectedRowN = localStorage.getItem('id_master_editar');
            $.ajax({
                url: '/exportacion_aerea/master-detail/',
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    row = table.rows('.table-secondary').data();
                    if (row.length === 1) {
                        window.open('/exportacion_aerea/descargar_awb/' + row[0][0], '_blank');
                    } else {
                        alert('Debe seleccionar al menos un registro');
                    }
                }
        });
    });
    $('#descargar_guia_draft').click(function () {
         let selectedRowN = localStorage.getItem('id_master_editar');
            $.ajax({
                url: '/exportacion_aerea/master-detail/',
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    row = table.rows('.table-secondary').data();
                    if (row.length === 1) {
                        window.open('/exportacion_aerea/descargar_awb_draft/' + row[0][0] + '/d', '_blank');
                    } else {
                        alert('Debe seleccionar al menos un registro');
                    }
                }
            });
    });

    //autocompletes add master form
    $("#transportista_add").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#transportista_i').val(ui.item['id']);
                 guia_master();
                 $('#transportista_i').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#transportista_i').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#transportista_i').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#agente_add").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#agente_i').val(ui.item['id']);
                 $('#agente_i').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#agente_i').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#agente_i').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#consignatario_add").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                $('#consignatario_i').val(ui.item['id']);
                $('#consignatario_i').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#consignatario_i').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#consignatario_i').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#loading_add").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#discharge_add").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#origen_add").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $('#loading_add').val(ui.item['value']);

        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#destino_add").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $('#disharge_add').val(ui.item['value']);

        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });

    // auto completes add house form
    $("#armador_addh").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#armador_ih').val(ui.item['id']);
                 $('#armador_ih').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#armador_ih').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#armador_ih').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#vendedor_addh").autocomplete({
        source: '/autocomplete_vendedores/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#vendedor_ih').val(ui.item['id']);
                 $('#vendedor_ih').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#vendedor_ih').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#vendedor_ih').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#transportista_addh").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#transportista_ih').val(ui.item['id']);
                 $('#transportista_ih').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#transportista_ih').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#transportista_ih').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#consignatario_addh").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#consignatario_ih').val(ui.item['id']);
                 $('#consignatario_ih').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#consignatario_ih').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#consignatario_ih').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#agente_addh").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#agente_ih').val(ui.item['id']);
                 $('#agente_ih').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#agente_ih').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#agente_ih').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#cliente_addh").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#cliente_ih').val(ui.item['id']);
                 $('#cliente_ih').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#cliente_ih').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#cliente_ih').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#embarcador_addh").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#embarcador_ih').val(ui.item['id']);
                 $('#embarcador_ih').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#embarcador_ih').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#embarcador_ih').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#agecompras_addh").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#agcompras_ih').val(ui.item['id']);
                 $('#agcompras_ih').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#agcompras_ih').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#agcompras_ih').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#ageventas_addh").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#agventas_ih').val(ui.item['id']);
                 $('#agventas_ih').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#agventas_ih').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#agventas_ih').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#loading_addh").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#discharge_addh").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#origen_addh").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#destino_addh").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });

        //autocompletes edit master form
    $("#transportista_edit").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#transportista_ie').val(ui.item['id']);
                 $('#transportista_i').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
            /*
                $(this).val('');
                $('#transportista_ie').val(''); */
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#transportista_ie').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#agente_edit").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#agente_ie').val(ui.item['id']);
                 $('#agente_ie').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#agente_ie').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#agente_ie').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#consignatario_edit").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                $('#consignatario_ie').val(ui.item['id']);
                $('#consignatario_ie').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#consignatario_ie').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#consignatario_ie').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#loading_edit").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#discharge_edit").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#origen_edit").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#destino_edit").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    //productos para el embarque
    $("#id_producto").autocomplete({
    source: function (request, response) {
        $.getJSON('/autocomplete_productos/', { term: request.term }, response);
    },
    minLength: 2,
    select: function (event, ui) {
        $(this).attr('data-id', ui.item['id']);  // Guarda el ID si es un item de la lista
        $('#cod_producto').val(ui.item['id']);
    },
    change: function (event, ui) {
        var input = $(this);
        var valorIngresado = input.val();

        if (ui.item) {
            input.css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
        } else {
            if (valorIngresado.trim() !== '') {
                $.ajax({
                    url: '/agregar_producto/',
                    method: 'POST',
                    data: {
                        nombre: valorIngresado,
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                    },
                    success: function (data) {
                        if (data.success) {
                            input.attr('data-id', data.id);
                            $('#cod_producto').val(data.id);
                            input.css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                        } else {
                            alert("No se pudo guardar el vapor.");
                        }
                    },
                    error: function () {
                        alert("Error en la comunicación con el servidor.");
                    }
                });
            } else {
                input.val('');
                input.css({"border-color": "", 'box-shadow': ''});
            }
        }
    }
});

    // autocompletes edit house form
    $("#armador_addh_e").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#armador_ih_e').val(ui.item['id']);
                 $('#armador_ih_e').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#armador_ih_e').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#armador_ih_e').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#vendedor_addh_e").autocomplete({
        source: '/autocomplete_vendedores/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#vendedor_ih_e').val(ui.item['id']);
                 $('#vendedor_ih_e').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#vendedor_ih_e').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#vendedor_ih_e').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#transportista_addh_e").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#transportista_ih_e').val(ui.item['id']);
                 guia_master();
                 $('#transportista_ih_e').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#transportista_ih_e').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#transportista_ih_e').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#consignatario_addh_e").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#consignatario_ih_e').val(ui.item['id']);
                 $('#consignatario_ih_e').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#consignatario_ih_e').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#consignatario_ih_e').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#agente_addh_e").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#agente_ih_e').val(ui.item['id']);
                 $('#agente_ih_e').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#agente_ih_e').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#agente_ih_e').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#cliente_addh_e").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#cliente_ih_e').val(ui.item['id']);
                 $('#cliente_ih_e').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#cliente_ih_e').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#embarcador_addh_e").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#embarcador_ih_e').val(ui.item['id']);
                 $('#embarcador_ih_e').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#embarcador_ih_e').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#embarcador_ih_e').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#agecompras_addh_e").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#agcompras_ih_e').val(ui.item['id']);
                 $('#agcompras_ih_e').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#agcompras_ih_e').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#agcompras_ih_e').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#ageventas_addh_e").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#agventas_ih_e').val(ui.item['id']);
                 $('#agventas_ih_e').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#agventas_ih_e').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#agventas_ih_e').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#loading_addh_e").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#discharge_addh_e").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#origen_addh_e").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#destino_addh_e").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });

    //autocomplete cliente importar house
    $("#filtro_cliente").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });

    //autocomplete rutas house
    $("#id_origen").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                //$(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#id_destino").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#id_origen_master").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#id_destino_master").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                $(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    //botones funcionalidades

    //form addmaster
    $('#add_btn').click(function () {
        //generar_posicion();
//        if (localStorage.getItem('master')) {
//            document.getElementById('id_awb').value=localStorage.getItem('master');
//            cargar_hauses_master();
//        }
        document.getElementById("add_master_form").reset();
        $('#agregar_master').css({'display':'block'});
        $("#add_master_modal").dialog({
                    autoOpen: true,
                    open: function (event, ui) {

                    var contentWidth = $('#add_master_modal #add_master_form').outerWidth(true);
                    $(this).dialog("option", "width", contentWidth);

                    },
                    modal: true,
                    title: "Ingresar un nuevo máster",
                    height: wHeight * 0.85,
                    width: wWidth*0.90,

                    position: { my: "top", at: "top+20", of: window },
                    buttons: [
                        {
                           text: "Salir",
                           class: "btn btn-dark",
                           style: "width:100px",
                           click: function () {
                           validarCoincidenciaAcumulados();
                                $('#agregar_hijo').css({'visibility':'hidden'});
                                $('#importar_hijo_add_master').css({'visibility':'hidden'});
                                $('#segment_response').css({'display':'none'});
                               $(this).dialog("close");
                           },
                       },

                    ],
                    beforeClose: function (event, ui) {
                    if ($.fn.dataTable.isDataTable('#tabla_exportaerea')) {
                        $('#tabla_exportaerea').DataTable().ajax.reload(null, false);
                    }
                    }
                });
        if ($('#table_add_ea tbody tr').length === 0) {
            $('#segment_response').hide();
        } else {
            $('#segment_response').show();
        }

        // Recalcular altura del modal
        $("#add_master_modal").dialog("option", "height", 'auto');
        });
    $('#add_master_form').submit(function(e){

    e.preventDefault();
    e.stopPropagation();

    if(document.getElementById('id_tarifa').value<0||document.getElementById('id_arbitraje').value<0||document.getElementById('id_trafico').value<0||document.getElementById('id_kilos').value<0||document.getElementById('id_cotizacion').value<0){
    alert('No se admiten valores negativos.');
    }else{
    if($('#id_status').val()=='CANCELADO'){
    alert('Máster con status CANCELADO, no se asignará la guía.');
    }
    $('#id_awb').val($('#id_awb_select').val());
    let awbValue = $('#id_awb_select').val();
    let awbParts = awbValue.split('-');
    let numeroDerecha = parseInt(awbParts[1], 10);
    let numeroiz = parseInt(awbParts[0], 10);
    $('#numero_guia_add').val(numeroDerecha);
    $('#prefijo_guia_add').val(numeroiz);
    let formData = $(this).serialize();
    formData += '&csrfmiddlewaretoken=' + csrf_token;

    $.ajax({
        type: "POST",
        url: "/exportacion_aerea/add_master/",
        data: formData,
        success: function(response) {
            if (response.success) {
            alert('Posición generada: ' + response.posicion);
            $('#agregar_hijo').css({'visibility':'visible'});
            $('#importar_hijo_add_master').css({'visibility':'visible'});
            $('#agregar_master').css({'display':'none'});

            table.ajax.reload(null, false);

                 //guardar master en la sesion
                 let master = document.getElementById('id_awb').value;
                 localStorage.setItem('master',master );
                 //let posicion = document.getElementById('posicion_g').value;
                 localStorage.setItem('posicion',response.posicion );
                //document.getElementById("add_master_form").reset();
                $('#transportista_add').css({"border-color": "", 'box-shadow': ''});
                $('#transportista_i').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#agente_add').css({"border-color": "", 'box-shadow': ''});
                $('#agente_i').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#consignatario_add').css({"border-color": "", 'box-shadow': ''});
                $('#consignatario_i').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#armador_add').css({"border-color": "", 'box-shadow': ''});
                $('#armador_i').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#vapor_add').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#origen_add').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#destino_add').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#loading_add').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#discharge_add').css({"border-color": "", 'box-shadow': '', 'font-size': ''});

            } else {
            if (response.code === 'DUPLICATE_MASTER') {
                alert('Ya existe un registro con el mismo valor para Master.');
            } else {
                alert('Error: ' + response.message);
            }

            }
        },
        error: function(xhr, status, error) {
            alert('Ocurrió un error al agregar el master: ' + error);
        }
    });
    }
    $('#td:contains("Master")').css('display','none');
    $('#id_awb').css('display','none');
});
    //calculo aplicable
    $('#id_volumen, #id_kilos').on('input', function() {
    let volumen =  $('#id_volumen').val();
    let peso =  $('#id_kilos').val();
    let coef = 166.67;
    let valor1;

    if(volumen && peso){
        valor1=volumen*coef;

        if(valor1>peso){
        //marcar volumen
        valor1=Math.round(valor1 * 2) / 2;
        $('#id_aplicable').val(valor1);
        $('#radio').val('volumen');
        $('#volumen_radio').prop('checked', true);
        }else{
        //marcar peso
        $('#id_aplicable').val(peso);
        $('#peso_radio').prop('checked', true);
        $('#radio').val('peso');
        }
    }

});
    $('input[type="radio"]').on('change', function() {
    let tarifa = $('#id_tarifa').val();
    let volumen =  $('#id_volumen').val();
    let peso =  $('#id_kilos').val();

    let tarifa_e = $('#id_tarifa_e').val();
    let volumen_e =  $('#id_volumen_e').val();
    let peso_e =  $('#id_kilos_e').val();

    let medidas =  $('#id_medidas_embarque').val();
    let volumen_embarque=0;
    if(medidas){
        let medidasArray = medidas.split('*');
        volumen_embarque = medidasArray.reduce((total, num) => total * parseFloat(num), 1);
    }
    let peso_embarque =  $('#id_bruto_embarque').val();

    let aplicable1;

    // Verificar cuál radio button fue seleccionado
    let radioSeleccionado = $(this).attr('id');

        if ($(this).is(':checked')) {
            if(radioSeleccionado=='volumen_radio'){
                if(volumen){
                    aplicable1=aplicable_volumen(volumen);
                    $('#id_aplicable').val(aplicable1);
                    $('#radio').val('volumen');
                }
            }else if(radioSeleccionado=='peso_radio'){
                if(peso){
                    $('#id_aplicable').val(peso);
                    $('#radio').val('peso');
                }
            }else if(radioSeleccionado=='manual_radio'){
                $('#id_aplicable').val(0);
                $('#radio').val('manual');
            }else if(radioSeleccionado=='volumen_radio_e'){
                if(volumen_e){
                    aplicable1=aplicable_volumen(volumen_e);
                    $('#id_aplicable_e').val(aplicable1);
                    $('#radio_e').val('volumen');
                }
            }else if(radioSeleccionado=='peso_radio_e'){
                if(peso_e){
                    $('#id_aplicable_e').val(peso_e);
                    $('#radio_e').val('peso');
                }
            }else if(radioSeleccionado=='manual_radio_e'){
                $('#id_aplicable_e').val(0);
                $('#radio_e').val('manual');
            }else if(radioSeleccionado=='volumen_radio_embarque'){
                if(volumen_embarque){
                    aplicable1=aplicable_volumen(volumen_embarque);
                    $('#id_aplicable_embarque').val(aplicable1);
                    $('#radio_embarque').val('volumen');
                }
            }else if(radioSeleccionado=='peso_radio_embarque'){
                if(peso_embarque){
                    $('#id_aplicable_embarque').val(peso_embarque);
                    $('#radio_embarque').val('peso');
                }
            }else if(radioSeleccionado=='manual_radio_embarque'){
                $('#id_aplicable_embarque').val(0);
                $('#radio_embarque').val('manual');
            }
            else{
                console.log(radioSeleccionado);
            }
        }


  });

    //calculo aplicable embarque
    $('#id_medidas_embarque, #id_bruto_embarque').on('input', function() {
    let medidas =  $('#id_medidas_embarque').val();
    let medidasArray = medidas.split('*');
    let volumen = medidasArray.reduce((total, num) => total * parseFloat(num), 1);
    let peso =  $('#id_bruto_embarque').val();
    let coef = 166.67;
    let valor1;

    if(volumen && peso){
        valor1=volumen*coef;

        if(valor1>peso){
        //marcar volumen
        valor1=Math.round(valor1 * 2) / 2;
        $('#id_aplicable_embarque').val(valor1);
        $('#radio_embarque').val('volumen');
        $('#volumen_radio_embarque').prop('checked', true);
        }else{
        //marcar peso
        $('#id_aplicable_embarque').val(peso);
        $('#peso_radio_embarque').prop('checked', true);
        $('#radio_embarque').val('peso');
        }
    }

});


function aplicable_volumen(volumen){
    let valor1;
    let coef = 166.67;
    let aplicable1;

    valor1=volumen*coef;

    return Math.round(valor1 * 2) / 2;
}

        //ver mas
    var expandedRow;
    $('#tabla_exportaerea tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);

        if (row.child.isShown()) {
        row.child.hide();
        tr.removeClass('shown');
        } else {

            if (expandedRow && expandedRow !== row) {
                expandedRow.child.hide();
                expandedRow.node().classList.remove('shown');
            }
            var rowData = row.data();
            var selectedRowId = rowData[4];

            $.ajax({
                url: '/exportacion_aerea/source_embarque_aereo/',
                type: 'POST',
                data: {
                    master: selectedRowId
                },
                headers: {
                    'X-CSRFToken': csrf_token
                },
                success: function (response) {
                    row.child(
                        format(response.data)).show();
                    tr.addClass('shown');
                    expandedRow = row;
                },
                error: function (xhr, status, error) {
                    console.error('Error al cargar los detalles:', error);
                }
            });
        }
    });
     //modificar master
    $('#tabla_exportaerea tbody').on('click', 'td', function () {


        var tr = $(this).closest('tr');
        var row = table.row(tr);
        var rowData = row.data();

        if (rowData) {
            var selectedRowId = rowData[0];
            var selectedRowNumber = rowData[1];
            localStorage.setItem('id_master_editar', selectedRowId);
            localStorage.setItem('numero_master_seleccionado', selectedRowNumber);
        }
    });
    $('#editar_btn').on('click', function () {
    let selectedRowId = localStorage.getItem('id_master_editar');

    if (selectedRowId !== null) {
        $.ajax({
            url: '/exportacion_aerea/master-detail',
            data: { id: selectedRowId },
            method: 'GET',
            success: function (data) {
                $("#edit_master_modal").dialog({
                    autoOpen: true,
                    open: function (event, ui) {
                        var contentWidth = $('#edit_master_modal #edit_master_form').outerWidth(true);
                        $(this).dialog("option", "width", contentWidth);
                    },
                    modal: true,
                    title: "Editar máster",
                    height: wHeight * 0.85,
                    width: 'auto',
                    position: { my: "top", at: "top+20", of: window },
                    buttons: [
                        {
                            text: "Salir",
                            class: "btn btn-dark",
                            style: "width:100px",
                            click: function () {
                            validarCoincidenciaAcumulados();
                                $(this).dialog("close");
                                localStorage.removeItem('id_master_editar');
                                $('#table_edit_ea').DataTable().destroy();
                                $('#segment_response_2').css({'display':'none'});
                            },
                        },
                    ],
                    beforeClose: function (event, ui) {
                                                    try {
                                desbloquearDatos();
                            } catch (error) {
                                console.error("⚠️ Error en desbloquearDatos:", error);
                            }
                        localStorage.removeItem('fecha_editada_master');
                        localStorage.removeItem('id_master_editar');
                        localStorage.removeItem('num_house_gasto');
                        localStorage.removeItem('id_house_gasto');
                    if ($.fn.dataTable.isDataTable('#tabla_exportaerea')) {
                        $('#tabla_exportaerea').DataTable().ajax.reload(null, false);
                    }

                    }
                });

                // Llenar el formulario con los datos
                fillFormWithData(data);
                //cargar tabla de houses
                cargar_hauses_master_edit();
                if(data.bloqueado){
                        alert(data.mensaje);
                        $('#modificar_master').prop('disabled',true);
                    } else{
                        $('#modificar_master').prop('disabled',false);
                    }
            },
            error: function (xhr, status, error) {
                console.error("Error fetching data:", error);
            }
        });
    } else {
        alert('Por favor, selecciona una fila para editar.');
    }
});
    $('#tabla_exportaerea tbody').on('dblclick', 'tr', function() {
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        var rowData = row.data();

        if (rowData) {
            var selectedRowId = rowData[0];
            var selectedRowNumber = rowData[1];
            localStorage.setItem('id_master_editar', selectedRowId);
            localStorage.setItem('numero_master_seleccionado', selectedRowNumber);
        }

        $('#editar_btn').trigger('click');
    });
    $('#edit_master_form').submit(function(e){
       e.preventDefault();
    if(document.getElementById('id_tarifa_e').value<0||document.getElementById('id_arbitraje_e').value<0||document.getElementById('id_trafico_e').value<0||document.getElementById('id_kilos_e').value<0||document.getElementById('id_cotizacion_e').value<0){
    alert('No se admiten valores negativos.');
    }else{

        var id_master = localStorage.getItem('id_master_editar');
        $('#id_awd_e').val($('#id_awb_select_e').val());
        let awbValue = $('#id_awb_select_e').val();
        let awbParts = awbValue.split('-');
        let numeroDerecha = parseInt(awbParts[1], 10);
        let numeroiz = parseInt(awbParts[0], 10);
        $('#numero_guia').val(numeroDerecha);
        $('#prefijo_guia').val(numeroiz);
        var formData = $(this).serialize();
        let radio;
        if ($('#volumen_radio_e').is(':checked')){
            radio = 'volumen';
        } else if ($('#peso_radio_e').is(':checked')){
            radio = 'peso';
        } else {
            radio = 'manual';
        }

        formData += '&radio=' + encodeURIComponent(radio);

        $('#edit_master_form').attr('action', '/exportacion_aerea/edit_master/' + id_master + '/');

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: formData,
            dataType: 'json',
            success: function (response) {
                if (response.success) {
                    alert('Datos actualizados con éxito');
                    if(localStorage.getItem('fecha_editada_master')){
                        if(confirm('Desea modificar la fecha en los houses (si existen)?')){
                        modificar_fecha_retiro(0);
                        }else{
                        localStorage.removeItem('fecha_editada_master');
                        }
                    }
                    table.ajax.reload(null, false);
                    $('#edit_master_modal').dialog('close');
//                    $('#table_edit_ea').DataTable().destroy();
                } else {
                    // mensaje general
                    let msg = response.message || 'Error inesperado';

                    // si hay errores de campos, los convierto a string legible
                    if (response.errors) {
                        let errores = JSON.parse(response.errors);
                        let detalle = '';
                        for (let campo in errores) {
                            detalle += campo + ': ' + errores[campo][0].message + '\n';
                        }
                        msg += '\n\nDetalles:\n' + detalle;
                    }

                    alert(msg);
                }
            },
            error: function (xhr, status, error) {
                alert('Error en la solicitud: ' + error);
            }
        });
    $('#td:contains("Master")').css('display','none');
    $('#id_awd_e').css('display','none');
                $('#transportista_edit').css({"border-color": "", 'box-shadow': ''});
                $('#transportista_ie').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#agente_edit').css({"border-color": "", 'box-shadow': ''});
                $('#agente_ie').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#consignatario_edit').css({"border-color": "", 'box-shadow': ''});
                $('#consignatario_ie').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#armador_edit').css({"border-color": "", 'box-shadow': ''});
                $('#armador_ie').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#vapor_edit').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#origen_edit').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#destino_edit').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#loading_edit').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#discharge_edit').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
        }
    });
    //evento al modificar fecha del master
   $('#id_fecha_e').on('change', function() {

        let vector = JSON.parse(localStorage.getItem('fecha_editada_master')) || [];
        var nuevaFecha = $(this).val();
        let master = localStorage.getItem('master_editar');

        let itemEncontrado = vector.find(item => item.master === master);

        if (!itemEncontrado) {
            vector.push({ master: master, fecha: nuevaFecha });
        } else {
            itemEncontrado.fecha = nuevaFecha;
        }
       localStorage.setItem('fecha_editada_master', JSON.stringify(vector));

});
    //evento modificar fecha del house
   $('#fecha_retiro_e').on('change', function() {

   let vector = JSON.parse(localStorage.getItem('fecha_editada_house')) || [];
    var nuevaFecha = $(this).val();
    let master = $('#id_awbhijo_e').val();

    let itemEncontrado = vector.find(item => item.master === master);

    if (!itemEncontrado) {
        vector.push({ master: master, fecha: nuevaFecha });
    } else {
        itemEncontrado.fecha = nuevaFecha;
    }
    localStorage.setItem('fecha_editada_house', JSON.stringify(vector));

});

    //evento fila marcada
    $(document).on('click', function (event) {
    // tabla general
//    if (!$(event.target).closest('#tabla_exportaerea').length) {
//        $('#tabla_exportaerea tbody tr').removeClass('table-secondary');
//    }
//    //tabla de houses en edit master
//    if (!$(event.target).closest('#table_edit_ea').length) {
//        $('#table_edit_ea tbody tr').removeClass('table-secondary');
//    }
//    //tabla de houses en add master
//    if (!$(event.target).closest('#table_add_ea').length) {
//        $('#table_add_ea tbody tr').removeClass('table-secondary');
//    }
});
    $('#tabla_exportaerea tbody').on('click', 'tr', function (event) {
    // Evita que el clic en la tabla dispare la eliminación de la clase
    event.stopPropagation();

    if ($(this).hasClass('table-secondary')) {
        // Aquí puedes decidir si la fila debe desmarcarse o no
    } else {
        let row = table.row($(this).closest('tr')).data();
        row_selected = row[0];
        row_number = row[1];
        setCookie(row_selected);

        // Quita la clase 'table-secondary' de cualquier fila previamente seleccionada
        $('#tabla_exportaerea tbody tr').removeClass('table-secondary');
        // Agrega la clase 'table-secondary' a la fila seleccionada
        $(this).addClass('table-secondary');
    }
});

   //form add house
    $('#agregar_hijo').click(function () {
        $("#add_house_modal").dialog({
                    autoOpen: true,
                    open: function (event, ui) {
                    },
                    modal: true,
                    title: "Ingresar un nuevo hijo/house",
                     width: 'auto',
                     height: 'auto',
                     position: { my: "center", at: "center", of: window },
                    buttons: [
                        {
                           text: "Salir",
                           class: "btn btn-dark",
                           style: "width:100px",
                           click: function () {
                               $(this).dialog("close");
                               if (table_add_ea instanceof $.fn.dataTable.Api) {
                               $('#table_add_ea').DataTable().destroy();
                               $('#segment_response').css({'display':'none'});
                               }
                           },
                       },

                    ],
                    beforeClose: function (event, ui) {

                    }
                });
                //cargar con la id desde la sesion
                let master = localStorage.getItem('master');
                $('#id_awbhijo').val(master);
                let posicion = localStorage.getItem('posicion');
                $('#posicion_gh').val(posicion);
                localStorage.setItem('lugar_editar','agregar');

                $('#cliente_addh').addClass('input-sobrepasar');
                $('#embarcador_addh').addClass('input-sobrepasar');
                $('#consignatario_addh').addClass('input-sobrepasar');
                $('#agente_addh').addClass('input-sobrepasar');
                $('#transportista_addh').addClass('input-sobrepasar');
                $('#armador_addh').addClass('input-sobrepasar');
                $('#agecompras_addh').addClass('input-sobrepasar');
                $('#ageventas_addh').addClass('input-sobrepasar');
                $('#deposito_addh').addClass('input-sobrepasar');
                $('#vendedor_addh').addClass('input-sobrepasar');




        });
    $('#add_house_form').submit(function(e){
    e.preventDefault();
    e.stopPropagation();
    lugar_editar=localStorage.getItem('lugar_editar');
    if(document.getElementById('pago_house').value<0||document.getElementById('arbitraje_house').value<0){
    alert('No se admiten valores negativos en los campos numéricos.')
    }else{
    let formData = $(this).serialize();
    formData += '&csrfmiddlewaretoken=' + csrf_token;

        if(lugar_editar==='edit_directo'){
        formData += '&consolidado=1';
        }
    $.ajax({
        type: "POST",
        url: "/exportacion_aerea/add_house/",
        data: formData,
        success: function(response) {
            if (response.success) {
            if(lugar_editar==='agregar'){
            if (table_add_ea instanceof $.fn.dataTable.Api) {
                    table_add_ea.ajax.reload(null, false);
                } else {
                    cargar_hauses_master();
                }
            }else if(lugar_editar==='editar'){
            if (table_edit_ea instanceof $.fn.dataTable.Api) {
                    table_edit_ea.ajax.reload(null, false);
                } else {
                    cargar_hauses_master_edit();
                }
            }else if(lugar_editar==='edit_directo'){
                $('#tabla_house_directo_ea').DataTable().ajax.reload(null, false);
                }

                 $('#add_house_modal').dialog('close');
                 document.getElementById("add_house_form").reset();

                $('#transportista_addh').css({"border-color": "", 'box-shadow': ''});
                $('#transportista_ih').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#agente_addh').css({"border-color": "", 'box-shadow': ''});
                $('#agente_ih').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#consignatario_addh').css({"border-color": "", 'box-shadow': ''});
                $('#consignatario_ih').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#armador_addh').css({"border-color": "", 'box-shadow': ''});
                $('#armador_ih').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#embarcador_addh').css({"border-color": "", 'box-shadow': ''});
                $('#embarcador_ih').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#cliente_addh').css({"border-color": "", 'box-shadow': ''});
                $('#cliente_ih').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#agecompras_addh').css({"border-color": "", 'box-shadow': ''});
                $('#agcompras_ih').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#ageventas_addh').css({"border-color": "", 'box-shadow': ''});
                $('#agventas_ih').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#vapor_addh').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#origen_addh').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#destino_addh').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#loading_addh').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#discharge_addh').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#deposito_addh').css({"border-color": "", 'box-shadow': ''});
                $('#deposito_ih').css({"border-color": "", 'box-shadow': '', 'font-size': ''});
                $('#vendedor_addh').css({"border-color": "", 'box-shadow': ''});
                $('#vendedor_ih').css({"border-color": "", 'box-shadow': ''});

            } else {
                console.log(response.errors);
            }
        },
        error: function(xhr, status, error) {
            alert('Ocurrió un error al agregar el house: ' + error);
        }
    });
    }
});
   //modificar house
    $('#edit_house_form').submit(function(e){
    let lugar=localStorage.getItem('lugar');
       e.preventDefault();
        if(document.getElementById('arbitraje_house_e').value<0){
    alert('No se admiten valores negativos en los campos numéricos.')
    }else{
        var numero = localStorage.getItem('numero_embarque');
        // var numero = localStorage.getItem('numero_embarque');
        var formData = $(this).serialize();
        $('#edit_house_form').attr('action', '/exportacion_aerea/edit_house/' + numero + '/');
        // if(lugar==='edit_directo'){
        // formData += '&consolidado=1';
        // }

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: formData,
            dataType: 'json',
            success: function (response) {
                if (response.success) {
                    alert('Datos actualizados con éxito');
                    if(lugar!='edit_directo'){
                        if(localStorage.getItem('fecha_editada_house')){
                        if(confirm('Desea modificar la fecha en los demás houses (si existen)?')){
                        modificar_fecha_retiro(1);
                        }else{
                        localStorage.removeItem('fecha_editada_house');
                        }
                    }
                    }

                    if(lugar==='add_master'){
                    table_add_ea.ajax.reload(null, false);
                    }else if(lugar==='edit_master'){
                    table_edit_ea.ajax.reload(null, false);
                    }else if(lugar==='edit_directo'){
                    $('#tabla_house_directo_ea').DataTable().ajax.reload(null, false);
                    }
                    else{
                    console.log('error en el lugar '+lugar);
                    }

                  $('#edit_house_modal').dialog('close');
                } else {
                    // mensaje general
                    let msg = response.message || 'Error inesperado';

                    // si hay errores de campos, los convierto a string legible
                    if (response.errors) {
                        let errores = JSON.parse(response.errors);
                        let detalle = '';
                        for (let campo in errores) {
                            detalle += campo + ': ' + errores[campo][0].message + '\n';
                        }
                        msg += '\n\nDetalles:\n' + detalle;
                    }

                    alert(msg);
                }
            },
            error: function (xhr, status, error) {
                alert('Error en la solicitud: ' + error);
            }
        });
        }
    });

    //agregar house desde edit master
    $('#agregar_hijo_edit_master').click(function () {
        $("#add_house_modal").dialog({
                    autoOpen: true,
                    open: function (event, ui) {
                    },
                    modal: true,
                    title: "Ingresar un nuevo hijo/house",
                     width: 'auto',
                     height: 'auto',
                     position: { my: "center", at: "center", of: window },
                    buttons: [
                        {
                           text: "Salir",
                           class: "btn btn-dark",
                           style: "width:100px",
                           click: function () {

                               $(this).dialog("close");
                           },
                       },

                    ],
                    beforeClose: function (event, ui) {

                    }
                });
                //cargar con la id desde la sesion
                let master = localStorage.getItem('master_editar');
                $('#id_awbhijo').val(master);
                let posicion = localStorage.getItem('posicion_editar');
                $('#posicion_gh').val(posicion);
                localStorage.setItem('lugar_editar','editar');

                $('#cliente_addh').addClass('input-sobrepasar');
                $('#embarcador_addh').addClass('input-sobrepasar');
                $('#consignatario_addh').addClass('input-sobrepasar');
                $('#agente_addh').addClass('input-sobrepasar');
                $('#transportista_addh').addClass('input-sobrepasar');
                $('#armador_addh').addClass('input-sobrepasar');
                $('#agecompras_addh').addClass('input-sobrepasar');
                $('#ageventas_addh').addClass('input-sobrepasar');
                $('#deposito_addh').addClass('input-sobrepasar');
                $('#vendedor_addh').addClass('input-sobrepasar');

        });

    //gastos master
    $('#gastos_btn_master').click(function () {
        $("#id_gasto_id_").val('');
 let id = localStorage.getItem('id_master_editar');
        let selectedRowN = localStorage.getItem('numero_master_seleccionado');

        if (selectedRowN!=null) {
            $.ajax({
                url: '/exportacion_aerea/master-detail/',
                data: {id: id},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    get_datos_gastos();
                    $('#gastos_form').trigger("reset");
                    $("#gastos_modal").dialog({
                        autoOpen: true,
                        open: function () {
                            document.getElementById('numero_gasto_master').value = selectedRowN;
                        },
                        modal: true,
                        title: "Gastos para el master N°: " + selectedRowN,
                        height: wHeight * 0.90,
                        width: wWidth * 0.90,
                        class: 'modal fade',
                        buttons: [
                            {
                                text: "Eliminar",
                                class: "btn btn-danger",
                                style: "width:100px",
                                click: function () {
                                    if (confirm('¿Confirma eliminar el gasto seleccionado?')) {
                                        row = table_gastos.rows('.table-secondary').data();
                                        if (row.length === 1) {
                                            miurl = "/exportacion_aerea/eliminar_gasto_master/";
                                            var toData = {
                                                'id': row[0][0],
                                                'csrfmiddlewaretoken': csrf_token,
                                            };
                                            $.ajax({
                                                type: "POST",
                                                url: miurl,
                                                data: toData,
                                                success: function (resultado) {
                                                    aux = resultado['resultado'];
                                                    if (aux === 'exito') {
                                                        $("#table_gastos").dataTable().fnDestroy();
                                                        get_datos_gastos();
                                                        alert('Eliminado correctamente');
                                                        // $('#gastos_btn_master').addClass('triggered').trigger('click');
                                                        // mostrarToast('¡Gasto eliminado correctamente!', 'success');
                                                    } else {
                                                        alert(aux);
                                                    }
                                                }
                                            });
                                        } else {
                                            alert('Debe seleccionar un unico registro');
                                        }
                                    }
                                },
                            }, {
                                text: "Salir",
                                class: "btn btn-dark",
                                style: "width:100px",
                                click: function () {
                                    $(this).dialog("close");
                                },
                            }],
                        beforeClose: function (event, ui) {
                            localStorage.removeItem('numero_master_seleccionado');
                            try {
                                desbloquearDatos();
                            } catch (error) {
                                console.error("⚠️ Error en desbloquearDatos:", error);
                            }
                            // $("#tabla_gastos").dataTable().fnDestroy();
                        }
                    })
                }
            });
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#ingresar_gasto_master').click(function (event) {
    event.preventDefault();
     if(document.getElementById('id_pinformar').value<0||document.getElementById('id_arbitraje_id').value<0||document.getElementById('id_costo').value<0){
    alert('No se admiten valores negativos en los campos numéricos.')
    }else{
    if (confirm("¿Confirma guardar el gasto?")) {
        var form = $('#gastos_form');
        var formData = new FormData(form[0]);
        if (form[0].checkValidity()) {
        let numero=localStorage.getItem('numero_master_seleccionado');
            //row = table.rows('.table-secondary').data();
            let formData = $("#gastos_form").serializeArray();
            let data = JSON.stringify(formData);
            miurl = "/exportacion_aerea/add_gasto_master/";
            var toData = {
                'numero':numero ,
                'data': data,
                'csrfmiddlewaretoken': csrf_token,
            };
            $.ajax({
                type: "POST",
                url: miurl,
                data: toData,
                async: false,
                success: function (resultado) {
                    if (resultado['resultado'] === 'exito') {
                          $("#id_gasto_id_").val('');
                        alert('Guardado con éxito.');
                        $("#tabla_gastos").dataTable().fnDestroy();
                        $("#ingresar_gasto_master").html('Agregar');
                       get_datos_gastos();
                       let aux= document.getElementById('numero_gasto_master').value;
                       $('#gastos_form').trigger("reset");
                       document.getElementById('numero_gasto_master').value=aux;

                    } else {
                        alert(resultado['resultado']);
                    }
                }
            });
        }else{
        alert('Debe completar todos los campos.');
        }
    }
    }
});
    $('#tabla_gastos tbody').on('dblclick', 'tr', function () {
        var data = table_gastos.row(this).data();
        $("#id_gasto_id").val(data[0]);
        if(data[3] > 0){

            $("#id_costo").val(data[3]);
        }else{

            $("#id_costo").val(data[4]);
        }
        //$("#id_detalle").val(data[5]);
        if(data[6] === 'Collect'){
            $("#id_modo_id").val('C');
        }else{
            $("#id_modo_id").val('P');
        }
        $("#id_tipogasto").val(data[7]);
        $("#id_arbitraje_id").val(data[8]);
        if(data[9] === 'SI'){
            $("#id_notomaprofit").prop("checked",true);
        }else{
            $("#id_notomaprofit").prop("checked",false);
        }
        $("#id_secomparte").val(data[10].substr(0,1));
        $("#id_pinformar").val(data[11]);
        $("#id_servicio").val(data[14]);
        $("#id_moneda_id").val(data[15]);
        $("#id_socio").val(data[16]);
        $("#ingresar_gasto_master").html('Modificar');
        $("#cancelar_gasto_master").show();
    });
    $('#tabla_gastos tbody').on('click', 'tr', function () {
        $('#tabla_gastos tbody tr').removeClass('table-secondary');
        $(this).addClass('table-secondary');
    });

    //gastos house
    $('#ingresar_gasto_house').off('click').click(function (event) {
    event.preventDefault();
    if(document.getElementById('id_pinformar_h').value<0||document.getElementById('id_arbitraje_h').value<0||document.getElementById('id_precio_h').value<0){
    alert('No se admiten valores negativos en los campos numéricos.')
    }else{
    if (confirm("¿Confirma guardar el gasto?")) {
        var form = $('#gastos_form_house');
        let numero=localStorage.getItem('num_house_gasto');
            let formData = $("#gastos_form_house").serializeArray();
            let data = JSON.stringify(formData);
            miurl = "/exportacion_aerea/add_gasto_house/";
            var toData = {
                'numero':numero ,
                'data': data,
                'csrfmiddlewaretoken': csrf_token,
            };
            $.ajax({
                type: "POST",
                url: miurl,
                data: toData,
                async: false,
                success: function (resultado) {
                    if (resultado['resultado'] === 'exito') {
                        $("#id_gasto_id_house").val('');
                        alert('Guardado con éxito.');
                        $("#tabla_gastos_house").dataTable().fnDestroy();
                        $("#ingresar_gasto_house").html('Agregar');
                       get_datos_gastos_house();
                       let aux= document.getElementById('numero_gasto_house').value;
                       $('#gastos_form_house').trigger("reset");
                       document.getElementById('numero_gasto_house').value=aux;
                        if ($.fn.DataTable.isDataTable('#table_add_ea')) {
                            $('#table_add_ea').DataTable().ajax.reload(null, false);
                        }

                        if ($.fn.DataTable.isDataTable('#table_edit_ea')) {
                            $('#table_edit_ea').DataTable().ajax.reload(null, false);
                        }
                        if ($.fn.DataTable.isDataTable('#tabla_house_directo_ea')) {
                            $('#tabla_house_directo_ea').DataTable().ajax.reload(null, false);
                        }
                    } else {
                        alert(resultado['resultado']);
                    }
                }
            });

    }
    }
});
    $('#tabla_gastos_house tbody').off('dblclick').on('dblclick', 'tr', function () {
        var data = table_gastos.row(this).data();
        $("#id_gasto_id_house").val(data[0]);
        $("#id_costo_h").val(data[4]);
        $("#id_precio_h").val(data[3]);
        $("#id_detalle_h").val(data[5]);
        if(data[6] === 'Collect'){
            $("#id_modo_h").val('C');
        }else{
            $("#id_modo_h").val('P');
        }
        $("#id_tipogasto_h").val(data[7]);
        $("#id_arbitraje_h").val(data[8]);
        if(data[9] === 'SI'){
            $("#id_notomaprofit_h").prop("checked",true);
        }else{
            $("#id_notomaprofit_h").prop("checked",false);
        }
        $("#id_secomparte_h").val(data[10].substr(0,1));
        $("#id_pinformar_h").val(data[11]);
        $("#id_servicio_h").val(data[14]);
        $("#id_moneda_h").val(data[15]);
        $("#id_socio_h").val(data[16]);
        $("#ingresar_gasto_house").html('Modificar');
        $("#cancelar_gasto_house").show();
    });
    $('#tabla_gastos_house tbody').off('click').on('click', 'tr', function () {
        $('#tabla_gastos_house tbody tr').removeClass('selected');
        $(this).addClass('selected');
    });

    //rutas house
    $('#ingresar_ruta_house').off('click').click(function (event) {
    event.preventDefault();

    if (confirm("¿Confirma guardar la ruta?")) {
        var form = $('#rutas_form_house');
        var formData = new FormData(form[0]);
        if (form[0].checkValidity()) {
        let numero=localStorage.getItem('num_house_gasto');
            let formData = $("#rutas_form_house").serializeArray();
            let data = JSON.stringify(formData);
            miurl = "/exportacion_aerea/add_ruta_house/";
            var toData = {
                'numero':numero ,
                'data': data,
                'csrfmiddlewaretoken': csrf_token,
            };
            $.ajax({
                type: "POST",
                url: miurl,
                data: toData,
                async: false,
                success: function (resultado) {
                    if (resultado['resultado'] === 'exito') {
                        $("#id_house_ruta").val('');
                        alert('Guardado con éxito.');
                        $("#tabla_rutas_house").dataTable().fnDestroy();
                        $("#ingresar_ruta_house").html('Agregar');
                       get_datos_rutas_house();
                       let aux= document.getElementById('id_ruta_id').value;
                       $('#rutas_form_house').trigger("reset");
                       document.getElementById('id_ruta_id').value=aux;
                       $("#id_origen, #id_destino").css({"border-color": "", 'box-shadow': ''});
                       if ($.fn.DataTable.isDataTable('#table_add_ea')) {
                            $('#table_add_ea').DataTable().ajax.reload(null, false);
                        }

                        if ($.fn.DataTable.isDataTable('#table_edit_ea')) {
                            $('#table_edit_ea').DataTable().ajax.reload(null, false);
                        }
                        if ($.fn.DataTable.isDataTable('#tabla_house_directo_ea')) {
                            $('#tabla_house_directo_ea').DataTable().ajax.reload(null, false);
                        }
                    } else {
                        alert(resultado['resultado']);
                    }
                }
            });
        }else{
            const invalidFields = form[0].querySelectorAll(':invalid'); // Selecciona los campos no válidos
            invalidFields.forEach(field => {
                console.log('Campo no válido:', field.name); // Muestra los campos no válidos
            });

            alert('Debe completar todos los campos.');
        }
    }
});
    $('#tabla_rutas_house tbody').off('click').on('click', 'tr', function () {
        $('#tabla_rutas_house tbody tr').removeClass('selected');
        $(this).addClass('selected');
    });
    $('#tabla_rutas_house tbody').off('dblclick').on('dblclick', 'tr', function () {
        var data = table_rutas.row(this).data();
        $("#id_house_ruta").val(data[0]);
        $("#id_origen").val(data[1]);
        $("#id_destino").val(data[2]);
        $("#id_vuelo").val(data[3]);
        $("#id_salida").val(data[4]);
        $("#id_llegada").val(data[5]);
        $("#id_viaje_ruta").val(data[6]);
        $("#id_modo_ruta").val(data[8]);
        $("#id_ciavuelo").val(data[7]);

        $("#ingresar_ruta_house").html('Modificar');
        $("#cancelar_ruta_house").show();
    });

    //rutas master
    $('#ingresar_ruta_master').off('click').click(function (event) {
    event.preventDefault();

    if (confirm("¿Confirma guardar la ruta?")) {
        var form = $('#rutas_form_master');
        var formData = new FormData(form[0]);
        if (form[0].checkValidity()) {
        let numero=localStorage.getItem('numero_master_seleccionado');
            let formData = $("#rutas_form_master").serializeArray();
            let data = JSON.stringify(formData);
            miurl = "/exportacion_aerea/add_ruta_master/";
            var toData = {
                'numero':numero ,
                'data': data,
                'csrfmiddlewaretoken': csrf_token,
            };
            $.ajax({
                type: "POST",
                url: miurl,
                data: toData,
                async: false,
                success: function (resultado) {
                    if (resultado['resultado'] === 'exito') {
                        $("#id_master_ruta").val('');
                        alert('Guardado con éxito.');
                        $("#tabla_rutas_master").dataTable().fnDestroy();
                        $("#ingresar_ruta_master").html('Agregar');
                       get_datos_rutas_master();
                       let aux= document.getElementById('id_ruta_id_master').value;
                       $('#rutas_form_masterr').trigger("reset");
                       document.getElementById('id_ruta_id_master').value=aux;
                       $("#id_origen_master, #id_destino_master").css({"border-color": "", 'box-shadow': ''});
                       /*
                       if ($.fn.DataTable.isDataTable('#table_add_ea')) {
                            $('#table_add_ea').DataTable().ajax.reload(null, false);
                        }*/

                    } else {
                        alert(resultado['resultado']);
                    }
                }
            });
        }else{
            const invalidFields = form[0].querySelectorAll(':invalid'); // Selecciona los campos no válidos
            invalidFields.forEach(field => {
                console.log('Campo no válido:', field.name); // Muestra los campos no válidos
            });

            alert('Debe completar todos los campos.');
        }
    }
});
    $('#tabla_rutas_master tbody').off('click').on('click', 'tr', function () {
        $('#tabla_rutas_master tbody tr').removeClass('selected');
        $(this).addClass('selected');
    });
    $('#tabla_rutas_master tbody').off('dblclick').on('dblclick', 'tr', function () {
        var data = table_rutas.row(this).data();
        $("#id_master_ruta").val(data[0]);
        $("#id_origen_master").val(data[1]);
        $("#id_destino_master").val(data[2]);
        $("#id_vuelo_master").val(data[3]);
        $("#id_salida_master").val(data[4]);
        $("#id_llegada_master").val(data[5]);
        $("#id_ciavuelo_master").val(data[6]);

        $("#ingresar_ruta_master").html('Modificar');
        $("#cancelar_ruta_master").show();
    });

    //embarques house
    $('#ingresar_embarque_house').off('click').click(function (event) {
    event.preventDefault();
    if(document.getElementById('id_bruto_embarque').value<0||document.getElementById('id_bultos_embarque').value<0){
    alert('No se admiten valores negativos en los campos numéricos.')
    }else{
    if (confirm("¿Confirma guardar el embarque?")) {
        var form = $('#embarques_form_house');
        var formData = new FormData(form[0]);
        if (form[0].checkValidity()) {
        let numero=localStorage.getItem('num_house_gasto');
            let formData = $("#embarques_form_house").serializeArray();
            let data = JSON.stringify(formData);
            miurl = "/exportacion_aerea/add_embarque_house/";
            var toData = {
                'numero':numero ,
                'data': data,
                'csrfmiddlewaretoken': csrf_token,
            };
            $.ajax({
                type: "POST",
                url: miurl,
                data: toData,
                async: false,
                success: function (resultado) {
                    if (resultado['resultado'] === 'exito') {
                            $("#id_producto").val('');
                        $("#id_producto").css({"border-color": "", 'box-shadow': ''});
                        $("#id_embarque_id").val('');
                        alert('Guardado con éxito.');
                        $("#tabla_embarques_house").dataTable().fnDestroy();
                        $("#ingresar_embarque_house").html('Agregar');
                       get_datos_embarques_house();
                       let aux= document.getElementById('numero_embarque').value;
                       $('#embarques_form_house').trigger("reset");
                       document.getElementById('numero_embarque').value=aux;
                       if ($.fn.DataTable.isDataTable('#table_add_ea')) {
                            $('#table_add_ea').DataTable().ajax.reload(null, false);
                        }

                        if ($.fn.DataTable.isDataTable('#table_edit_ea')) {
                            $('#table_edit_ea').DataTable().ajax.reload(null, false);
                        }
                        if ($.fn.DataTable.isDataTable('#tabla_house_directo_ea')) {
                            $('#tabla_house_directo_ea').DataTable().ajax.reload(null, false);
                        }
                    } else {
                        alert(resultado['resultado']);
                    }
                }
            });
        }else{
            const invalidFields = form[0].querySelectorAll(':invalid'); // Selecciona los campos no válidos
            invalidFields.forEach(field => {
                console.log('Campo no válido:', field.name); // Muestra los campos no válidos
            });

            alert('Debe completar todos los campos.');
        }
    }
    }
});
    $('#tabla_embarques_house tbody').off('click').on('click', 'tr', function () {
        $('#tabla_embarques_house tbody tr').removeClass('selected');
        $(this).addClass('selected');
    });
    $('#tabla_embarques_house tbody').off('dblclick').on('dblclick', 'tr', function () {
    var data = table_embarques.row(this).data();
    $("#id_embarque_id").val(data[0]);         // ID del registro
    $("#id_producto").val(data[1]);                // Unidad
    $("#id_bultos_embarque").val(data[2]);                  // Tipo
    $("#id_tipo_embarque").val(data[3]);            // Movimiento
    $("#id_bruto_embarque").val(data[4]);              // Términos
    $("#id_medidas_embarque ").val(data[5]);              // Cantidad
    $("#id_aplicable_embarque ").val(data[7]);
    $("#id_tarifa_embarque ").val(data[8]);

    $("#ingresar_embarque_house").html('Modificar');
    $("#cancelar_embarque_house").show();
});

    //importar hijo desde seguimeintos edit master form
    var table_seg;
    $('#importar_hijo_edit_master').click(function () {
         let selectedRowN = localStorage.getItem('id_master_editar');

            $.ajax({
                url: '/exportacion_aerea/master-detail/',
                data: { id: selectedRowN },
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    localStorage.setItem('lugar_importarhijo', 'editmaster');
                    importar_hijo_tabla();

                    $("#importar_hijo_modal").dialog({
                        autoOpen: true,
                        open: function () {

                        },
                        modal: true,
                        title: "Importar hijo desde seguimientos",
                        height: wHeight * 0.90,
                        width: wWidth * 0.90,
                        class: 'modal fade',
                        buttons: [
                            {
                                text: "Salir",
                                class: "btn btn-dark",
                                style: "width:100px",
                                click: function () {
                                    $(this).dialog("close");
                                    $('#tabla_seguimiento_IH').DataTable().destroy();
                                },
                            }
                        ],
                        beforeClose: function (event, ui) {
                            // Optional actions before closing
                        }
                    });
                }
                });
    });
    $('#filtrar_seguimientos').click(function () {
        var filtroNumero = $('#filtro_numero').val();
        var filtroCliente = $('#filtro_cliente').val();

        // Aplicar filtros a la tabla
        var table = $('#tabla_seguimiento_IH').DataTable();
        table
            .column(1).search(filtroNumero)
            .column(3).search(filtroCliente)
            .draw();
    });
    $('#limpiar_filtros').click(function () {
    // Limpiar los valores de los inputs
    $('#filtro_numero').val('');
    $('#filtro_cliente').val('');
    $('#filtro_cliente').css({"border-color": "", 'box-shadow': ''});
    // Resetear los filtros de la tabla
    var table = $('#tabla_seguimiento_IH').DataTable();
    table
        .search('')  // Limpia la búsqueda general
        .columns().search('')  // Limpia las búsquedas por columna
        .draw();  // Redibuja la tabla
});
    $('#guardar_importados').click(function (e) {
        e.preventDefault();
        e.stopPropagation();
        let seleccionados = JSON.parse(localStorage.getItem('seleccionados'));
        let cant = seleccionados ? seleccionados.length : 0;
        if(confirm('Desea importar '+cant+'house/s?')){
        traer_seguimientos();
        }

        });
    $('#tabla_seguimiento_IH tbody').on('click', 'tr', function () {
        let table = $('#tabla_seguimiento_IH').DataTable();

        // Si la fila ya tiene la clase 'highlighted', quítasela y desmarca el checkbox
        if ($(this).hasClass('highlighted') ) {
            $(this).removeClass('highlighted');
        } else {
            $(this).addClass('highlighted');
        }

            let checkbox = $(this).find('.checkbox_seleccion');
            checkbox.prop('checked', !checkbox.prop('checked'));
            checkbox.trigger('change');

});
    $('#tabla_seguimiento_IH tbody').on('change', '.checkbox_seleccion', function () {
            let id = $(this).val();
            let seleccionados = JSON.parse(localStorage.getItem('seleccionados')) || [];
            let row = $(this).closest('tr');

            if (this.checked) {
                if (!seleccionados.includes(id)) {
                    seleccionados.push(id);
                }
                row.addClass('highlighted');
            } else {
                seleccionados = seleccionados.filter(item => item !== id);
                row.removeClass('highlighted');
            }

            localStorage.setItem('seleccionados', JSON.stringify(seleccionados));
        });

    //importar hijos desde seguimientos add master form
    $('#importar_hijo_add_master').click(function () {
    localStorage.setItem('lugar_importarhijo','addmaster');
        importar_hijo_tabla();

        $("#importar_hijo_modal").dialog({
            autoOpen: true,
            open: function () {

            },
            modal: true,
            title: "Importar hijo desde seguimientos",
            height: wHeight * 0.90,
            width: wWidth * 0.90,
            class: 'modal fade',
            buttons: [
                {
                    text: "Salir",
                    class: "btn btn-dark",
                    style: "width:100px",
                    click: function () {
                        $(this).dialog("close");
                        $('#tabla_seguimiento_IH').DataTable().destroy();
                    },
                }
            ],
            beforeClose: function (event, ui) {
                // Optional actions before closing
            }
        });
    });

    //menu sobre la lista de houses en editmaster y addmaster
    document.addEventListener('DOMContentLoaded', function () {
    const dropdownToggle = document.getElementById('navbarScrollingDropdown3');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    dropdownToggle.addEventListener('click', function (event) {
        event.preventDefault();  // Evita el comportamiento predeterminado del enlace

        // Verifica si el dropdown está abierto
        if (dropdownMenu.classList.contains('show')) {
            dropdownMenu.classList.remove('show');  // Cierra el dropdown
        } else {
            dropdownMenu.classList.add('show');  // Abre el dropdown
        }
    });

    // Cerrar el menú si se hace clic fuera de él
    document.addEventListener('click', function (event) {
        if (!dropdownToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.remove('show');  // Cierra el dropdown si se hace clic fuera de él
        }
    });
});

    //mails acciones adjuntar
    $('#adjuntar_btn').click(function () {
    $("#tabla_archivos").dataTable().fnDestroy();
    row = table.rows('.table-secondary').data();
    get_datos_archivos();

        $("#archivos_modal").dialog({
            autoOpen: true,
            open: function (event, ui) {

            },
            modal: true,
            title: "Archivos para el House N°: " + localStorage.getItem('num_house_gasto') ,
            height: wHeight * 0.70,
            width: wWidth * 0.70,
            class: 'modal fade',
            buttons: [
             {
                        text: "Adjuntar",
                        class: "btn btn-dark",
                        style: "width:100px",
                        click: function () {
                            if (confirm('¿Confirma adjuntar el archivo seleccionado?')) {
                                    let table = $('#tabla_archivos').DataTable();
                                    let row = table.rows('.table-secondary').data();
                                let nombre = row[0][2].split("/")[1];
                                let id = row[0][0];
                                if(id in archivos_adjuntos) {
                                    alert('El archivo adjunto ya se encuentra seleccionado');
                                }else{
                                    archivos_adjuntos[id] = nombre;
                                    alert('¡Archivo adjuntado correctamente!');
                                    let archivoHTML = '<div class="archivo" id="' + id + '">' +
                                        '<span>' + nombre + '</span>' +
                                        '<button type="button" class="btn btn-sm eliminar-archivo bg-dark" onclick="return eliminar_adjunto(' + id + ')" aria-label="Eliminar">' +
                                        '&nbsp;<span class="badge badge-light" aria-hidden="true">&times;</span>' +
                                        '</button>' +
                                        '</div>';
                                    $("#arhivos_adjuntos").append(archivoHTML);
                                }
                            }
                        },
                    },
                {
                    text: "Descargar",
                    class: "btn btn-dark",
                    style: "width:100px",
                    click: function () {
                        if (confirm('¿Confirma descargar el archivo seleccionado?')) {
                            var url = '/exportacion_aerea/descargar_archivo/' + localStorage.getItem('id_archivo');  // Ruta de la vista que devuelve el archivo
                            window.open(url, '_blank');
                        }
                    },
                },{
                    text: "Eliminar",
                    class: "btn btn-danger",
                    style: "width:100px",
                    click: function () {
                        if (confirm('¿Confirma eliminar archivo?')) {
                            if (localStorage.getItem('id_archivo')) {
                                miurl = "/exportacion_aerea/eliminar_archivo/";
                                var toData = {
                                    'id': localStorage.getItem('id_archivo'),
                                    'csrfmiddlewaretoken': csrf_token,
                                };
                                $.ajax({
                                    type: "POST",
                                    url: miurl,
                                    data: toData,
                                    success: function (resultado) {
                                        aux = resultado['resultado'];
                                        if (aux == 'exito') {
                                            var idx = table.cell('.table-secondary', 0).index();
                                            $("#tabla_archivos tr.selected").removeClass('selected');
                                            $('#tabla_archivos').DataTable().ajax.reload(null, false);
                                                if ($.fn.DataTable.isDataTable('#table_add_ea')) {
                                                    $('#table_add_ea').DataTable().ajax.reload(null, false);
                                                }

                                                if ($.fn.DataTable.isDataTable('#table_edit_ea')) {
                                                    $('#table_edit_ea').DataTable().ajax.reload(null, false);
                                                }
                                                if ($.fn.DataTable.isDataTable('#tabla_house_directo_ea')) {
                                                    $('#tabla_house_directo_ea').DataTable().ajax.reload(null, false);
                                                }
                                        } else {
                                            alert(aux);
                                        }
                                    }
                                });
                            } else {
                                alert('Debe seleccionar un unico registro');
                            }
                        }
                    },
                },
                {
                    text: "Cerrar",
                    class: "btn btn-info",
                    style: "width:100px",
                    click: function () {
                        $(this).dialog("close");
                    },
                },
            ],
            beforeClose: function (event, ui) {
                // table.ajax.reload();
                $("#tabla_archivos").dataTable().fnDestroy();
            }
        })

});
    $('#guardar_archivo').click(function () {
        if (confirm("¿Confirma guardar archivo?")) {
            var formData = new FormData(document.getElementById("archivos_form"));
            formData.append('numero',localStorage.getItem('num_house_gasto'));
            miurl = "/exportacion_aerea/guardar_archivo/";
            $.ajax({
                type: "POST",
                url: miurl,
                data: formData,
                processData: false,
                contentType: false,
                async:false,
                success: function (resultado) {
                    if (resultado['resultado'] === 'exito') {
                        $('#tabla_archivos').DataTable().ajax.reload(null, false);
                         if ($.fn.DataTable.isDataTable('#table_add_ea')) {
                            $('#table_add_ea').DataTable().ajax.reload(null, false);
                        }

                        if ($.fn.DataTable.isDataTable('#table_edit_ea')) {
                            $('#table_edit_ea').DataTable().ajax.reload(null, false);
                        }
                        if ($.fn.DataTable.isDataTable('#tabla_house_directo_ea')) {
                            $('#tabla_house_directo_ea').DataTable().ajax.reload(null, false);
                        }
                    } else {
                        alert(resultado['resultado']);
                    }
                }, error: function (xhr, status, error) {
                    // Manejar el error en caso de que ocurra
                }
            });

        }
    })
    $('#tabla_archivos tbody').on('click', 'tr', function () {
    let table = $('#tabla_archivos').DataTable();

    if ($(this).hasClass('selected')) {
        $(this).removeClass('selected');
    } else {
        table.$('tr.selected').removeClass('selected');
        $(this).addClass('selected');
    }
    let datos_fila = $('#tabla_archivos').DataTable().row(this).data();

    if (datos_fila) {
      localStorage.setItem('id_archivo',datos_fila[0]);
    }
});

    const campoPrecio = document.getElementById("id_precio_h");
    const campoCosto = document.getElementById("id_costo_h");
    const campoInformar = document.getElementById("id_pinformar_h");

    campoInformar.addEventListener("keydown", function (event) {
        if (event.key === "Tab" && !event.shiftKey) {
            // Buscar valores
            let valor = campoPrecio.value || campoCosto.value;

            if (valor) {
                campoInformar.value = valor;
            }
        }
    });
});

$(document).on('select2:open', () => {
    document.querySelector('.select2-search__field').focus();
});

function setCookie(row_selected) {
    select_row = row_selected;
    document.cookie = 'row_selected_impomarit' + "=" + select_row + "; path=/";
}
function getCookie(name) {
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        row_selected = c.split('=')[1];
    }
    return null;
}
function getCookie2(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Verifica si esta cookie comienza con el nombre que buscamos
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function cargar_hauses_master(){
$('#table_add_ea').DataTable().destroy();
//tabla dentro del add-master form
localStorage.setItem('lugar','add_master');
let master = localStorage.getItem('master');
//let master='MOLU13000250048';
let csrftoken = getCookie2('csrftoken');
table_add_ea = $('#table_add_ea').DataTable({
    "stateSave": true,
    "info":false,
    "dom": 'Btipr',
    "bAutoWidth": false,
    "scrollX": true,
    "scrollY": wHeight * 0.60,
    "columnDefs": [
    {
        "targets": [0],  // Nueva columna para detalles
        "className": '',
        "orderable": false,
        "data": null,
        "defaultContent": '',  // Contenido por defecto
        "render": function (data, type, row) {
            // Define el contenido para la columna de detalles
            // return '<button class="btn btn-info btn-sm">Detalles</button>';  // Ejemplo de contenido
        }
    },
    {
        "targets": [1],
        "render": function (data, type, row, meta) {
            return row[19]; //seguimiento
        }
    },
    {
        "targets": [2],
            "render": function (data, type, row, meta) {
            return row[21]; // etd
        }
    },
    {
        "targets": [3],
        "visible": false,
        "className": 'derecha',
    },
    {
        "targets": [4],
        "className": 'derecha',
        "render": function (data, type, row, meta) {
            return row[25]; //vuelo
        }
    },
    {
        "targets": [5],
        "render": function (data, type, row, meta) {
            return row[10]; // Toma el índice 4 para la columna 5
        }
    },
    {
        "targets": [6],
        "render": function (data, type, row, meta) {
            return row[11]; // Toma el índice 5 para la columna 6
        }
    },
    {
        "targets": [7],
        "render": function (data, type, row, meta) {
            return row[28]; // embarcador
        }
    },
    {
        "targets": [8],
        "render": function (data, type, row, meta) {
            return row[27]; // Toma el índice 7 para la columna 8
        }
    },
    {
        "targets": [9],
        "render": function (data, type, row, meta) {
            return row[26]; // Toma el índice 8 para la columna 9
        }
    },


],

    "order": [[0, "desc"]],
    "processing": true,
    "serverSide": true,
    "pageLength": 100,
    "ajax": {
        "url": `/exportacion_aerea/source_embarque_aereo/`,
        "type": 'POST',
        "headers": {
            "X-CSRFToken": csrftoken
        },
                "data": function (d) {
        d.master = master;  // acá mandás el valor como POST
    },
        "dataSrc": function (json) {
         $('#table_add_ea th').css({'width':'auto'});
         $('#table_add_ea_wrapper .dataTables_scrollBody').css({
        'height': 'fit-content',
        });

         if (json.data.length === 0) {
            console.log('No se encontraron datos.');
        } else {
      $('#segment_response').css({'display':'block'});
        }
        return json.data;

        },
        "error": function(xhr, status, error) {
            console.error('Error en la llamada AJAX:', error);
        }
    },
    "language": {
        "url": "/static/datatables/es_ES.json"
    },
    "rowCallback": function (row, data) {
        $('td:eq(1)', row).html('');
            let texto = ''
            if (data[12] > 0) {
            //archivo
                texto += ' <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-filetype-docx" viewBox="0 0 16 16"' +
                            '><path fill-rule="evenodd" d="M14 4.5V11h-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5L14 4.5Zm-6.839 9.688v-.522a1.54 1.54 0 0 0-.117-.641.861.861 0 0 0-.322-.387.862.862 0 0 0-.469-.129.868.868 0 0 0-.471.13.868.868 0 0 0-.32.386 1.54 1.54 0 0 0-.117.641v.522c0 .256.04.47.117.641a.868.868 0 0 0 .32.387.883.883 0 0 0 .471.126.877.877 0 0 0 .469-.126.861.861 0 0 0 .322-.386 1.55 1.55 0 0 0 .117-.642Zm.803-.516v.513c0 .375-.068.7-.205.973a1.47 1.47 0 0 1-.589.627c-.254.144-.56.216-.917.216a1.86 1.86 0 0 1-.92-.216 1.463 1.463 0 0 1-.589-.627 2.151 2.151 0 0 1-.205-.973v-.513c0-.379.069-.704.205-.975.137-.274.333-.483.59-.627.257-.147.564-.22.92-.22.357 0 .662.073.916.22.256.146.452.356.59.63.136.271.204.595.204.972ZM1 15.925v-3.999h1.459c.406 0 .741.078 1.005.235.264.156.46.382.589.68.13.296.196.655.196 1.074 0 .422-.065.784-.196 1.084-.131.301-.33.53-.595.689-.264.158-.597.237-.999.237H1Zm1.354-3.354H1.79v2.707h.563c.185 0 .346-.028.483-.082a.8.8 0 0 0 .334-.252c.088-.114.153-.254.196-.422a2.3 2.3 0 0 0 .068-.592c0-.3-.04-.552-.118-.753a.89.89 0 0 0-.354-.454c-.158-.102-.361-.152-.61-.152Zm6.756 1.116c0-.248.034-.46.103-.633a.868.868 0 0 1 .301-.398.814.814 0 0 1 .475-.138c.15 0 .283.032.398.097a.7.7 0 0 1 .273.26.85.85 0 0 1 .12.381h.765v-.073a1.33 1.33 0 0 0-.466-.964 1.44 1.44 0 0 0-.49-.272 1.836 1.836 0 0 0-.606-.097c-.355 0-.66.074-.911.223-.25.148-.44.359-.571.633-.131.273-.197.6-.197.978v.498c0 .379.065.704.194.976.13.271.321.48.571.627.25.144.555.216.914.216.293 0 .555-.054.785-.164.23-.11.414-.26.551-.454a1.27 1.27 0 0 0 .226-.674v-.076h-.765a.8.8 0 0 1-.117.364.699.699 0 0 1-.273.248.874.874 0 0 1-.401.088.845.845 0 0 1-.478-.131.834.834 0 0 1-.298-.393 1.7 1.7 0 0 1-.103-.627v-.495Zm5.092-1.76h.894l-1.275 2.006 1.254 1.992h-.908l-.85-1.415h-.035l-.852 1.415h-.862l1.24-2.015-1.228-1.984h.932l.832 1.439h.035l.823-1.439Z"' +
                            '/></svg>';
            }
            if (data[13] > 0) {
            //embarque
            texto += '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-truck" viewBox="0 0 16 16">\n' +
                         '<path d="M0 3.5A1.5 1.5 0 0 1 1.5 2h9A1.5 1.5 0 0 1 12 3.5V5h1.02a1.5 1.5 0 0 1 1.17.563l1.481 1.85a1.5 1.5 0 0 1 .329.938V10.5a1.5 1.5 0 0 1-1.5 1.5H14a2 2 0 1 1-4 0H5a2 2 0 1 1-3.998-.085A1.5 1.5 0 0 1 0 10.5zm1.294 7.456A2 2 0 0 1 4.732 11h5.536a2 2 0 0 1 .732-.732V3.5a.5.5 0 0 0-.5-.5h-9a.5.5 0 0 0-.5.5v7a.5.5 0 0 0 .294.456M12 10a2 2 0 0 1 1.732 1h.768a.5.5 0 0 0 .5-.5V8.35a.5.5 0 0 0-.11-.312l-1.48-1.85A.5.5 0 0 0 13.02 6H12zm-9 1a1 1 0 1 0 0 2 1 1 0 0 0 0-2m9 0a1 1 0 1 0 0 2 1 1 0 0 0 0-2"/>\n' +
                         '</svg>';


            }
            if (data[15] > 0) {
            //gastos
                texto += '   <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-currency-dollar" viewBox="0 0 16 16"' +
                    '><path d="M4 10.781c.148 1.667 1.513 2.85 3.591 3.003V15h1.043v-1.216c2.27-.179 3.678-1.438 3.678-3.3 0-1.59-.947-2.51-2.956-3.028l-.722-.18' +
                    '7V3.467c1.122.11 1.879.714 2.07 1.616h1.47c-.166-1.6-1.54-2.748-3.54-2.875V1H7.591v1.233c-1.939.23-3.27 1.472-3.27 3.156 0 1.454.966 2.483 2.' +
                    '661 2.917l.61.162v4.031c-1.149-.17-1.94-.8-2.131-1.718H4zm3.391-3.836c-1.043-.263-1.6-.825-1.6-1.616 0-.944.704-1.641 1.8-1.828v3.495l-.2-.05z' +
                    'm1.591 1.872c1.287.323 1.852.859 1.852 1.769 0 1.097-.826 1.828-2.2 1.939V8.73l.348.086z"/>sss</svg>';
            }
            if (data[16] > 0) {
            //rutas
                texto += '   <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-geo-alt" viewBox="0 0 16 16">\n' +
                    '<path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"/>\n' +
                    '<path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>\n' +
                    '</svg>';
            }
            if (data[17] > 0) {
            //notas
            texto += '   <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-sticky" viewBox="0 0 16 16">\n' +
                '<path d="M2.5 1A1.5 1.5 0 0 0 1 2.5v11A1.5 1.5 0 0 0 2.5 15h6.086a1.5 1.5 0 0 0 1.06-.44l4.915-4.914A1.5 1.5 0 0 0 15 8.586V2.5A1.5 1.5 0 0 0 13.5 1zM2 2.5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 .5.5V8H9.5A1.5 1.5 0 0 0 8 9.5V14H2.5a.5.5 0 0 1-.5-.5zm7 11.293V9.5a.5.5 0 0 1 .5-.5h4.293z"/>\n' +
                '</svg>';

            }
            $('td:eq(1)', row).html(texto + " " + data[19]);

        },
    "initComplete": function() {
     //doble click modificar house en add_master form
    $('#table_add_ea tbody').off('dblclick').on('dblclick', 'tr', function () {
        var tr = $(this).closest('tr');
        var row = table_add_ea.row(tr);
        var rowData = row.data();

        if (rowData) {
            var selectedRowId = rowData[3];
            localStorage.setItem('numero_embarque', selectedRowId);

            $.ajax({
            url: '/exportacion_aerea/house-detail',
            data: { id: selectedRowId},
            method: 'GET',
            success: function (data) {
                $("#edit_house_modal").dialog({
                    autoOpen: true,
                    open: function (event, ui) {
                    },
                    modal: true,
                    title: "Editar house",
                     width: 'auto',  // Ajusta el ancho al contenido
                     height: 'auto', // Ajusta la altura al contenido
                     position: { my: "center", at: "center", of: window },
                    buttons: [
                        {
                           text: "Salir",
                           class: "btn btn-dark",
                           style: "width:100px",
                           click: function () {
                               $(this).dialog("close");
                           },
                       },
                                              {
                           text: "Modificar",
                           class: "btn btn-primary",
                           style: "width:100px",
                           click: function () {
                                                           if (confirm('¿Confirma la acción de modificar el H B/L?')) {
                                $('#edit_house_form').trigger('submit'); // Dispara el evento submit del formulario
                            }
                           },
                       },

                    ],
                    beforeClose: function (event, ui) {
                    localStorage.removeItem('fecha_editada_house');
                    }

                });

                fillFormWithDataHouse(data);
            },
            error: function (xhr, status, error) {
                console.error("Error fetching data:", error);
            }
        });
                    $('#cliente_addh_e').addClass('input-sobrepasar');
                    $('#embarcador_addh_e').addClass('input-sobrepasar');
                    $('#consignatario_addh_e').addClass('input-sobrepasar');
                    $('#agente_addh_e').addClass('input-sobrepasar');
                    $('#transportista_addh_e').addClass('input-sobrepasar');
                    $('#armador_addh_e').addClass('input-sobrepasar');
                    $('#agecompras_addh_e').addClass('input-sobrepasar');
                    $('#ageventas_addh_e').addClass('input-sobrepasar');
                    $('#deposito_addh_e').addClass('input-sobrepasar');
                    $('#vendedor_addh_e').addClass('input-sobrepasar');
        }else{
        alert('Seleccione una fila.');
        }
    });
    $('#table_add_ea tbody').off('click').on('click', 'tr', function (event) {
    event.stopPropagation();
    if ($(this).hasClass('table-secondary')) {
    } else {
        $('#table_add_ea tbody tr').removeClass('table-secondary');
        $(this).addClass('table-secondary');
    }

    var tr = $(this).closest('tr');
    var row = table_add_ea.row(tr);
    var rowData = row.data();

    if (rowData) {
        var selectedRowId = rowData[0];
        var selectedRowN = rowData[3];
        localStorage.setItem('id_house_gasto', selectedRowId);
        localStorage.setItem('num_house_gasto', selectedRowN);
        localStorage.setItem('tabla_origen', 'table_add_ea');
        localStorage.setItem('clase_house', 'EA');

    }
});
    }
});

}
function fillFormWithDataHouse(data) {

        $('#transportista_addh_e').val(!data.transportista_e || data.transportista_e === 0 ? '' : getNameById(data.transportista_e));
        $('#agente_addh_e').val(!data.agente_e || data.agente_e === 0 ? '' : getNameById(data.agente_e));
        $('#consignatario_addh_e').val(!data.consignatario_e || data.consignatario_e === 0 ? '' : getNameById(data.consignatario_e));
        $('#armador_addh_e').val(!data.armador_e || data.armador_e === 0 ? '' : getNameById(data.armador_e));
        $('#cliente_addh_e').val(!data.cliente_e || data.cliente_e === 0 ? '' : getNameById(data.cliente_e));
        $('#vendedor_addh_e').val(!data.vendedor_e || data.vendedor_e === 0 ? '' : getNameByIdVendedor(data.vendedor_e));
        $('#embarcador_addh_e').val(!data.embarcador_e || data.embarcador_e === 0 ? '' : getNameById(data.embarcador_e));
        $('#agecompras_addh_e').val(!data.agcompras_e || data.agcompras_e === 0 ? '' : getNameById(data.agcompras_e));
        $('#ageventas_addh_e').val(!data.agventas_e || data.agventas_e === 0 ? '' : getNameById(data.agventas_e));



        $('#armador_ih_e').val(data.armador_e);
        $('#transportista_ih_e').val(data.transportista_e);
        $('#agente_ih_e').val(data.agente_e);
        $('#consignatario_ih_e').val(data.consignatario_e);
        $('#cliente_ih_e').val(data.cliente_e);
        $('#vendedor_ih_e').val(data.vendedor_e);
        $('#embarcador_ih_e').val(data.embarcador_e);
        $('#agcompras_ih_e').val(data.agcompras_e);
        $('#agventas_ih_e').val(data.agventas_e);

        $('#origen_addh_e').val(data.origen_e);
        $('#destino_addh_e').val(data.destino_e);
        $('#loading_addh_e').val(data.loading_e);
        $('#discharge_addh_e').val(data.discharge_e);
        $('#viaje_house_e').val(data.viaje_e);
        $('#vapor_addh_e').val(data.vapor_e);
        $('#dias_demora_e').val(data.demora_e);
        $('#moneda_e').val(data.moneda_e);
        $('#arbitraje_house_e').val(data.arbitraje_e);
        $('#pago_house_e').val(data.pagoflete_e);
        $('#id_pago').val(data.pagoflete_e);

        $('#status_h_e').val(data.status_e);
        $('#wreceipt_he').val(data.wreceipt_e);
        $('#id_awbhijo_e').val(data.awb_e);
        $('#house_addh_e').val(data.hawb_e);
        $('#posicion_gh_e').val(data.posicion_e);
        $('#operacion_editar').val(data.operacion_e);

        $('#notificar_cliente_e').val(data.notifcliente_e ? formatDateToYYYYMMDD(data.notifcliente_e) : '');
        $('#notificar_agente_e').val(data.notifagente_e ? formatDateToYYYYMMDD(data.notifagente_e) : '');
        $('#eta_e').val(data.eta_e ? formatDateToYYYYMMDD(data.eta_e) : '');
        $('#etd_e').val(data.etd_e ? formatDateToYYYYMMDD(data.etd_e) : '');


    }
function getNameByIdVendedor(id) {
    var name = "";
    $.ajax({
        url: '/exportacion_aerea/get_name_by_id_vendedor',
        data: { id: id},
        async: false,
        success: function (response) {
            name = response.name;
        }
    });
    return name;
}
function fillFormWithData(data) {
    localStorage.setItem('master_editar',data.awd_e);
    localStorage.setItem('posicion_editar',data.posicion_e);
    $('#transportista_edit').val(!data.transportista_e || data.transportista_e === 0 ? '' : getNameById(data.transportista_e));

    $('#agente_edit').val(!data.agente_e || data.agente_e === 0 ? '' : getNameById(data.agente_e));
    $('#consignatario_edit').val(!data.consignatario_e || data.consignatario_e === 0 ? '' : getNameById(data.consignatario_e));

    $('#edit_master_form [name="transportista_ie"]').val(data.transportista_e);
    $('#edit_master_form [name="agente_ie"]').val(data.agente_e);
    $('#edit_master_form [name="consignatario_ie"]').val(data.consignatario_e);
    $('#edit_master_form [name="vapor_e"]').val(data.vapor_e);
    $('#edit_master_form [name="viaje_e"]').val(data.viaje_e);
    $('#edit_master_form [name="aduana_e"]').val(data.aduana_e);
    $('#edit_master_form [name="volumen"]').val(data.volumen_e);
    $('#edit_master_form [name="aplicable"]').val(data.aplicable_e);
    $('#edit_master_form [name="tarifa_e"]').val(data.tarifa_e);
    $('#edit_master_form [name="moneda_e"]').val(data.moneda_e);
    $('#edit_master_form [name="arbitraje_e"]').val(data.arbitraje_e);
    $('#edit_master_form [name="kilos_e"]').val(data.kilos_e);

    $('#edit_master_form [name="pagoflete_e"]').val(data.pagoflete_e);
    $('#edit_master_form [name="trafico_e"]').val(data.trafico_e);
    $('#edit_master_form [name="fecha_e"]').val(formatDateToYYYYMMDD(data.fecha_e));
    $('#edit_master_form [name="fecha_e"]').val(data.fecha_e ? formatDateToYYYYMMDD(data.fecha_e) : '');
    $('#edit_master_form [name="cotizacion_e"]').val(data.cotizacion_e);
    $('#edit_master_form [name="destino_e"]').val(data.destino_e);
    $('#edit_master_form [name="origen_e"]').val(data.origen_e);
    $('#edit_master_form [name="status_e"]').val(data.status_e);
    $('#edit_master_form [name="posicion_e"]').val(data.posicion_e);
    $('#edit_master_form [name="operacion_e"]').val(data.operacion_e);
    $('#edit_master_form [name="awd_e"]').val(data.awd_e);
    guia_master_edit(data.awd_e);
    if(data.radio=='volumen'){
    $('#volumen_radio_e').prop('checked', true);
    }else if(data.radio=='peso'){
    $('#peso_radio_e').prop('checked', true);
    }else{
    $('#manual_radio_e').prop('checked', true);
    }
    let awbValue = data.awd_e;
    let awbParts = awbValue.split('-');
    let numeroDerecha = parseInt(awbParts[1], 10);
    let numeroiz = parseInt(awbParts[0], 10);
    $('#numero_old').val(numeroDerecha);
    $('#prefijo_old').val(numeroiz);
        acumulados(data.awd_e, function(result) {
            // Asegúrate de que estos elementos están disponibles en el DOM
            if ($("#cantidad_acumulados").length && $("#peso_acumulados").length && $("#volumen_acumulados").length) {
                $('#cantidad_acumulados').val(result.cantidad);
                $('#peso_acumulados').val(result.peso);
                $('#volumen_acumulados').val(result.volumen);
                $('#bultos_acumulados').val(result.bultos);

            } else {
                console.log("Elementos de entrada no encontrados en el DOM.");
            }
        });



}

function formatDateToYYYYMMDD(isoDate) {
    // Asegúrate de que la fecha esté en formato ISO
    const date = new Date(isoDate);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Los meses van de 0 a 11
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}
function getNameById(id) {
var name = "";
$.ajax({
    url: '/exportacion_aerea/get_name_by_id',
    data: { id: id},
    async: false,
    success: function (response) {
        name = response.name;
    }
});
return name;
}
function cargar_hauses_master_edit(){
$('#table_edit_ea').DataTable().destroy();
//tabla dentro del edit-master form
localStorage.setItem('lugar','edit_master');
let master = localStorage.getItem('master_editar');
//let master='MOLU13000250048';
let csrftoken = getCookie2('csrftoken');
table_edit_ea = $('#table_edit_ea').DataTable({
    "info":false,
    "stateSave": true,
    "dom": 'Btipr',
    "bAutoWidth": false,
    "scrollX": true,
    "scrollY": wHeight * 0.60,
    "columnDefs": [
    {
        "targets": [0],  // Nueva columna para detalles
        "className": '',
        "orderable": false,
        "data": null,
        "defaultContent": '',  // Contenido por defecto
        "render": function (data, type, row) {
            // Define el contenido para la columna de detalles
            // return '<button class="btn btn-info btn-sm">Detalles</button>';  // Ejemplo de contenido
        }
    },
    {
        "targets": [1],
        "render": function (data, type, row, meta) {
            return row[19]; //seguimiento
        }
    },
    {
        "targets": [2],
            "render": function (data, type, row, meta) {
            return row[21]; // etd
        }
    },
    {
        "targets": [3],
        "visible": false,
        "className": 'derecha',
    },
    {
        "targets": [4],
        "className": 'derecha',
        "render": function (data, type, row, meta) {
            return row[25]; //vuelo
        }
    },
    {
        "targets": [5],
        "render": function (data, type, row, meta) {
            return row[10]; // Toma el índice 4 para la columna 5
        }
    },
    {
        "targets": [6],
        "render": function (data, type, row, meta) {
            return row[11]; // Toma el índice 5 para la columna 6
        }
    },
    {
        "targets": [7],
        "render": function (data, type, row, meta) {
            return row[28]; // embarcador
        }
    },
    {
        "targets": [8],
        "render": function (data, type, row, meta) {
            return row[27]; // Toma el índice 7 para la columna 8
        }
    },
    {
        "targets": [9],
        "render": function (data, type, row, meta) {
            return row[26]; // Toma el índice 8 para la columna 9
        }
    },


],
    "order": [[0, "desc"]],
    "processing": true,
    "serverSide": true,
    "pageLength": 100,
    "ajax": {
        "url": `/exportacion_aerea/source_embarque_aereo/`,
        "type": 'POST',
        "headers": {
            "X-CSRFToken": csrftoken
        },
                "data": function (d) {
        d.master = master;  // acá mandás el valor como POST
    },
        "dataSrc": function (json) {
         $('#table_edit_ea th').css({'width':'auto'});
         $('#table_edit_ea_wrapper .dataTables_scrollBody').css({
        'height': 'fit-content',
        });

         if (json.data.length === 0) {
            console.log('No se encontraron datos.');
        } else {
      $('#segment_response_2').css({'display':'block'});
        }
        return json.data;
        },
        "error": function(xhr, status, error) {
            console.error('Error en la llamada AJAX:', error);
        }
    },
    "language": {
        "url": "/static/datatables/es_ES.json"
    },
    "rowCallback": function (row, data) {
        $('td:eq(1)', row).html('');
            let texto = ''
            if (data[12] > 0) {
            //archivo
                texto += ' <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-filetype-docx" viewBox="0 0 16 16"' +
                            '><path fill-rule="evenodd" d="M14 4.5V11h-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5L14 4.5Zm-6.839 9.688v-.522a1.54 1.54 0 0 0-.117-.641.861.861 0 0 0-.322-.387.862.862 0 0 0-.469-.129.868.868 0 0 0-.471.13.868.868 0 0 0-.32.386 1.54 1.54 0 0 0-.117.641v.522c0 .256.04.47.117.641a.868.868 0 0 0 .32.387.883.883 0 0 0 .471.126.877.877 0 0 0 .469-.126.861.861 0 0 0 .322-.386 1.55 1.55 0 0 0 .117-.642Zm.803-.516v.513c0 .375-.068.7-.205.973a1.47 1.47 0 0 1-.589.627c-.254.144-.56.216-.917.216a1.86 1.86 0 0 1-.92-.216 1.463 1.463 0 0 1-.589-.627 2.151 2.151 0 0 1-.205-.973v-.513c0-.379.069-.704.205-.975.137-.274.333-.483.59-.627.257-.147.564-.22.92-.22.357 0 .662.073.916.22.256.146.452.356.59.63.136.271.204.595.204.972ZM1 15.925v-3.999h1.459c.406 0 .741.078 1.005.235.264.156.46.382.589.68.13.296.196.655.196 1.074 0 .422-.065.784-.196 1.084-.131.301-.33.53-.595.689-.264.158-.597.237-.999.237H1Zm1.354-3.354H1.79v2.707h.563c.185 0 .346-.028.483-.082a.8.8 0 0 0 .334-.252c.088-.114.153-.254.196-.422a2.3 2.3 0 0 0 .068-.592c0-.3-.04-.552-.118-.753a.89.89 0 0 0-.354-.454c-.158-.102-.361-.152-.61-.152Zm6.756 1.116c0-.248.034-.46.103-.633a.868.868 0 0 1 .301-.398.814.814 0 0 1 .475-.138c.15 0 .283.032.398.097a.7.7 0 0 1 .273.26.85.85 0 0 1 .12.381h.765v-.073a1.33 1.33 0 0 0-.466-.964 1.44 1.44 0 0 0-.49-.272 1.836 1.836 0 0 0-.606-.097c-.355 0-.66.074-.911.223-.25.148-.44.359-.571.633-.131.273-.197.6-.197.978v.498c0 .379.065.704.194.976.13.271.321.48.571.627.25.144.555.216.914.216.293 0 .555-.054.785-.164.23-.11.414-.26.551-.454a1.27 1.27 0 0 0 .226-.674v-.076h-.765a.8.8 0 0 1-.117.364.699.699 0 0 1-.273.248.874.874 0 0 1-.401.088.845.845 0 0 1-.478-.131.834.834 0 0 1-.298-.393 1.7 1.7 0 0 1-.103-.627v-.495Zm5.092-1.76h.894l-1.275 2.006 1.254 1.992h-.908l-.85-1.415h-.035l-.852 1.415h-.862l1.24-2.015-1.228-1.984h.932l.832 1.439h.035l.823-1.439Z"' +
                            '/></svg>';
            }
            if (data[13] > 0) {
            //embarque
            texto += '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-truck" viewBox="0 0 16 16">\n' +
                         '<path d="M0 3.5A1.5 1.5 0 0 1 1.5 2h9A1.5 1.5 0 0 1 12 3.5V5h1.02a1.5 1.5 0 0 1 1.17.563l1.481 1.85a1.5 1.5 0 0 1 .329.938V10.5a1.5 1.5 0 0 1-1.5 1.5H14a2 2 0 1 1-4 0H5a2 2 0 1 1-3.998-.085A1.5 1.5 0 0 1 0 10.5zm1.294 7.456A2 2 0 0 1 4.732 11h5.536a2 2 0 0 1 .732-.732V3.5a.5.5 0 0 0-.5-.5h-9a.5.5 0 0 0-.5.5v7a.5.5 0 0 0 .294.456M12 10a2 2 0 0 1 1.732 1h.768a.5.5 0 0 0 .5-.5V8.35a.5.5 0 0 0-.11-.312l-1.48-1.85A.5.5 0 0 0 13.02 6H12zm-9 1a1 1 0 1 0 0 2 1 1 0 0 0 0-2m9 0a1 1 0 1 0 0 2 1 1 0 0 0 0-2"/>\n' +
                         '</svg>';


            }
            if (data[15] > 0) {
            //gastos
                texto += '   <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-currency-dollar" viewBox="0 0 16 16"' +
                    '><path d="M4 10.781c.148 1.667 1.513 2.85 3.591 3.003V15h1.043v-1.216c2.27-.179 3.678-1.438 3.678-3.3 0-1.59-.947-2.51-2.956-3.028l-.722-.18' +
                    '7V3.467c1.122.11 1.879.714 2.07 1.616h1.47c-.166-1.6-1.54-2.748-3.54-2.875V1H7.591v1.233c-1.939.23-3.27 1.472-3.27 3.156 0 1.454.966 2.483 2.' +
                    '661 2.917l.61.162v4.031c-1.149-.17-1.94-.8-2.131-1.718H4zm3.391-3.836c-1.043-.263-1.6-.825-1.6-1.616 0-.944.704-1.641 1.8-1.828v3.495l-.2-.05z' +
                    'm1.591 1.872c1.287.323 1.852.859 1.852 1.769 0 1.097-.826 1.828-2.2 1.939V8.73l.348.086z"/>sss</svg>';
            }
            if (data[16] > 0) {
            //rutas
                texto += '   <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-geo-alt" viewBox="0 0 16 16">\n' +
                    '<path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"/>\n' +
                    '<path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>\n' +
                    '</svg>';
            }
            if (data[17] > 0) {
    //notas
            texto += '   <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-sticky" viewBox="0 0 16 16">\n' +
            '<path d="M2.5 1A1.5 1.5 0 0 0 1 2.5v11A1.5 1.5 0 0 0 2.5 15h6.086a1.5 1.5 0 0 0 1.06-.44l4.915-4.914A1.5 1.5 0 0 0 15 8.586V2.5A1.5 1.5 0 0 0 13.5 1zM2 2.5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 .5.5V8H9.5A1.5 1.5 0 0 0 8 9.5V14H2.5a.5.5 0 0 1-.5-.5zm7 11.293V9.5a.5.5 0 0 1 .5-.5h4.293z"/>\n' +
            '</svg>';

                }
            $('td:eq(1)', row).html(texto + " " + data[19]);

        },
    "initComplete": function() {
     //doble click modificar house en edit_master form
    $('#table_edit_ea tbody').off('dblclick').on('dblclick', 'tr', function () {
        let selectedRowN = localStorage.getItem('id_master_editar');
        let selected = this;

            $.ajax({
                url: '/exportacion_aerea/master-detail/',
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    var tr = $(selected).closest('tr');
                    var row = table_edit_ea.row(tr);
                    var rowData = row.data();

                    if (rowData) {
                        var selectedRowId = rowData[3];
                        localStorage.setItem('numero_embarque', selectedRowId);

                        $.ajax({
                            url: '/exportacion_aerea/house-detail',
                            data: {id: selectedRowId},
                            method: 'GET',
                            success: function (data) {
                                $("#edit_house_modal").dialog({
                                    autoOpen: true,
                                    open: function (event, ui) {
                                    },
                                    modal: true,
                                    title: "Editar house",
                                    width: 'auto',
                                    height: 'auto',
                                    position: {my: "center", at: "center", of: window},
                                    buttons: [
                                        {
                                            text: "Salir",
                                            class: "btn btn-dark",
                                            style: "width:100px",
                                            click: function () {
                                                $(this).dialog("close");
                                            },
                                        },
                                        {
                                            text: "Modificar",
                                            class: "btn btn-primary",
                                            style: "width:100px",
                                            click: function () {
                                                if (confirm('¿Confirma la acción de modificar el H B/L?')) {
                                                    $('#edit_house_form').trigger('submit'); // Dispara el evento submit del formulario
                                                }
                                            },
                                        },
                                    ],
                                    beforeClose: function (event, ui) {

                                    }

                                });

                                fillFormWithDataHouse(data);
                            },
                            error: function (xhr, status, error) {
                                console.error("Error fetching data:", error);
                            }
                        });
                        $('#cliente_addh_e').addClass('input-sobrepasar');
                        $('#embarcador_addh_e').addClass('input-sobrepasar');
                        $('#consignatario_addh_e').addClass('input-sobrepasar');
                        $('#agente_addh_e').addClass('input-sobrepasar');
                        $('#transportista_addh_e').addClass('input-sobrepasar');
                        $('#armador_addh_e').addClass('input-sobrepasar');
                        $('#agecompras_addh_e').addClass('input-sobrepasar');
                        $('#ageventas_addh_e').addClass('input-sobrepasar');
                        $('#deposito_addh_e').addClass('input-sobrepasar');
                        $('#vendedor_addh_e').addClass('input-sobrepasar');
                    } else {
                        alert('Seleccione una fila.');
                    }
                }
            });
    });
    $('#table_edit_ea tbody').off('click').on('click', 'tr', function (event) {
    event.stopPropagation();
    if ($(this).hasClass('table-secondary')) {
    } else {
        $('#table_edit_ea tbody tr').removeClass('table-secondary');
        $(this).addClass('table-secondary');
    }

    var tr = $(this).closest('tr');
    var row = table_edit_ea.row(tr);
    var rowData = row.data();

    if (rowData) {
        var selectedRowId = rowData[0];
        var selectedRowN = rowData[3];
        localStorage.setItem('id_house_gasto', selectedRowId);
        localStorage.setItem('num_house_gasto', selectedRowN);
        localStorage.setItem('tabla_origen', 'table_edit_ea');
        localStorage.setItem('clase_house', 'EA');

    }
});
    }
});

}
function format(data) {
var tableContent;
 if (data.length === 0) {
        tableContent = `
            <div style="text-align:center; color:red; font-size:14px; margin:20px;">
                No existen houses para este máster.
            </div>`;
    } else {
    tableContent = `
         <table id="tabla_detalles" class="table table-striped" style="font-size:12px; margin:0; padding:0;">
            <thead>
                <tr style="color: #3392a1">
                    <th class="text-right">ETD</th>
                    <th class="text-right">ETA</th>
                    <th class="text-right">N° Seguimiento</th>
                    <th class="text-right">Cliente</th>
                    <th class="text-right">Origen</th>
                    <th class="text-right">Destino</th>
                    <th class="text-right">Estado</th>
                    <th class="text-right">Posición</th>
                    <th class="text-right">Operación</th>
                    <th class="text-right">Master</th>
                    <th class="text-right">House</th>
                    <th class="text-right">Vapor</th>
                    <th class="text-right">Notificar Agente</th>
                    <th class="text-right">Notificar Cliente</th>
                </tr>
            </thead>
            <tbody style="border-style:none; border: solid transparent;">`;

    data.forEach(function (item) {
        tableContent += `
            <tr>
                <td>${item[23]}</td>
                <td>${item[24]}</td>
                <td>${item[19]}</td>
                <td>${item[4]}</td>
                <td>${item[5]}</td>
                <td>${item[6]}</td>
                <td>${item[7]}</td>
                <td>${item[8]}</td>
                <td>${item[9]}</td>
                <td>${item[10]}</td>
                <td>${item[11]}</td>
                <td>${item[12]}</td>
                <td>${item[13]}</td>
                <td>${item[14]}</td>
            </tr>`;
    });

    tableContent += `
            </tbody>
        </table>`;
    }
    return tableContent;
}
//importar hijos seguimientos
function importar_hijo_tabla(){
    let master;
    if(localStorage.getItem('lugar_importarhijo')==='editmaster'){
     master = localStorage.getItem('master_editar');
    }else if(localStorage.getItem('lugar_importarhijo')==='addmaster'){
     master = localStorage.getItem('master');
    }else{
    alert('ocurrio error con lugar_importarhijo');
    }
    let agregados = JSON.parse(localStorage.getItem('agregados')) || [];
    let agregadosMaster = [];
    let masterData = agregados.find(item => item.master === master);
    if (masterData) {
        agregadosMaster = masterData.agregados;
    }

table_seg = $('#tabla_seguimiento_IH').DataTable({
        "destroy": true,

        "dom": 'Btlipr',
        "scrollX": true,
        "bAutoWidth": false,
        "scrollY": wHeight * 0.60,
        "columnDefs": [
            {
                "targets": [0], // La primera columna, donde se colocará el checkbox
                "orderable": false, // Desactivar la ordenación en esta columna
                "className": 'dt-body-center', // Alinear al centro
                "render": function (data, type, row) {
                    // El checkbox, donde el valor del checkbox será la ID del registro
                    return '<input type="checkbox" class="checkbox_seleccion" value="' + row[0] + '">';
                }
            },
            {
                "targets": [1],
                "className": 'derecha archivos',
            },
            {
                "targets": [2],
            },
            {
                "targets": [3],
            },
            {
                "targets": [4],
            },
            {
                "targets": [5],
            },
            {
                "targets": [6],
            },
            {
                "targets": [7],
            },
        ],
        "order": [[1, "desc"],],
        "processing": true,
        "serverSide": true,
        "pageLength": 100,
        "ajax": {
            "url": "/exportacion_aerea/source_seguimientos_modo/EXPORT%20AEREO/",
            'type': 'GET',
            "data": function (d) {
                console.log(d);
                return $.extend({}, d, {
                    "buscar": buscar,
                    "que_buscar": que_buscar,
                    "ids_agregados": agregadosMaster
                });
            }
        },
        "language": {
            url: "/static/datatables/es_ES.json"
        },
       "rowCallback": function (row, data) {
//        let seleccionados = JSON.parse(localStorage.getItem('seleccionados')) || [];
//
//        if (seleccionados.includes(data[0])) {
//            $(row).addClass('highlighted');
//            $(row).find('.checkbox_seleccion').prop('checked', true);
//        } else {
//            $(row).removeClass('highlighted');
//            $(row).find('.checkbox_seleccion').prop('checked', false);
//        }
//
//
//        $(row).find('.checkbox_seleccion').off('change').on('change', function () {
//            let id = $(this).val();
//            let seleccionados = JSON.parse(localStorage.getItem('seleccionados')) || [];
//
//            if (this.checked) {
//                if (!seleccionados.includes(id)) {
//                    seleccionados.push(id);
//                }
//                $(row).addClass('highlighted');
//            } else {
//                seleccionados = seleccionados.filter(item => item !== id);
//                $(row).removeClass('highlighted');
//            }
//
//            localStorage.setItem('seleccionados', JSON.stringify(seleccionados));
//        });
    }

    });
}
function traer_seguimientos() {
    // Recupera el array de IDs del localStorage (asegúrate que esté guardado como JSON string)
    let ids_seleccionados = JSON.parse(localStorage.getItem('seleccionados')) || [];

    // Verifica si el array tiene datos
    if (ids_seleccionados.length === 0) {
        alert("No hay seguimientos seleccionados.");
        return;
    }

    // Hacer la solicitud AJAX para enviar los IDs al servidor
     const csrftoken = getCookie2('csrftoken');
    $.ajax({
        url: '/exportacion_aerea/source_seguimientos_importado/',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({ ids: ids_seleccionados }),
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(response) {
            if (response.data) {
            let master;
            let posicion;
            if(localStorage.getItem('lugar_importarhijo')==='editmaster'){
             master = localStorage.getItem('master_editar');
             posicion=localStorage.getItem('posicion_editar');
            }else if(localStorage.getItem('lugar_importarhijo')==='addmaster'){
             master = localStorage.getItem('master');
             posicion=localStorage.getItem('posicion');
            }else if(localStorage.getItem('lugar_importarhijo')==='directo'){
             master = 0;
             $.ajax({
                type: "GET",
                url: "/exportacion_aerea/generar_posicion/",
                success: function(res) {
                posicion = String(res.posicion);
                let posicionInicial = posicion; // El formato inicial de la posición

                response.data.forEach(function (item, index) {
                    item.awb = master;
                    let partes = posicionInicial.split('-');
                    let numeroCentral = partes[1];
                    let nuevoNumero = String(parseInt(numeroCentral, 10) + index).padStart(5, '0');
                    nuevoNumero = `C${nuevoNumero.slice(1)}`;
                    item.posicion = `${partes[0]}-${nuevoNumero}-${partes[2]}`;
                });
                 let seguimientos = response.data.map(item => item.seguimiento);
                 guardar_importado_house_directo(response.data, seguimientos);
                },
                error: function(error) {
                    console.log('Error:', error);
                }
                });

             return;
            }
            else{
            alert('ocurrio error con lugar_importarhijo');
            }
            response.data.forEach(function (item) {
            item.awb = master;
            item.posicion = posicion;
            });
            let seguimientos = response.data.map(item => item.seguimiento);
            guardar_importado_house(response.data, seguimientos);

            }
        },
        error: function(xhr, status, error) {
            console.error("Error al traer los seguimientos:", error);
        }
    });
}
function guardar_importado_house(data, seguimientos) {
    $.ajax({
        url: '/exportacion_aerea/add_house_importado/',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (response) {
            if (response.success) {
                traer_gastos_importado(seguimientos, response.numeros_guardados);
                traer_rutas_importado(seguimientos, response.numeros_guardados);
                traer_embarques_importado(seguimientos, response.numeros_guardados);
                traer_archivos_importado(seguimientos, response.numeros_guardados);

                alert('House/s importado/s con éxito');
               agregarASeleccionados();
                $("#importar_hijo_modal").dialog('close');
                $('#tabla_seguimiento_IH').DataTable().destroy();
                //location.reload();
                if ($.fn.DataTable.isDataTable('#table_edit_ea')) {
                    table_edit_ea.ajax.reload(null, false);
                } else {
                    if(localStorage.getItem('lugar_importarhijo')==='editmaster'){
                     cargar_hauses_master_edit();
                    }else if(localStorage.getItem('lugar_importarhijo')==='addmaster'){
                     cargar_hauses_master();
                    }else{
                    alert('ocurrio error con lugar_importarhijo');
                    }
                }

            } else {
                console.log(response.message);
                alert('Error: ' + response.message);
            }
        },
        error: function (xhr, status, error) {
            console.error('Error al guardar el house:', error);
            alert('Ocurrió un error al intentar guardar el house.');
        }
    });
}
function agregarASeleccionados() {
    let master = localStorage.getItem('master_editar');
    let nuevosAgregados = JSON.parse(localStorage.getItem('seleccionados')) || []; // Asegúrate de que sea un array
    let seleccionados = JSON.parse(localStorage.getItem('agregados')) || [];

    // Busca si ya existe un objeto para el master actual
    let masterExistente = seleccionados.find(item => item.master === master);

    if (masterExistente) {
        // Asegúrate de que masterExistente.agregados sea un array
        if (!Array.isArray(masterExistente.agregados)) {
            masterExistente.agregados = [];
        }

        // Verifica que nuevosAgregados es un array antes de iterarlo
        nuevosAgregados.forEach(id => {
            if (!masterExistente.agregados.includes(id)) {
                masterExistente.agregados.push(id);
            }
        });
    } else {
        // Si no existe, crea una nueva entrada para ese master
        seleccionados.push({
            master: master,
            agregados: nuevosAgregados // Debe ser un array
        });
    }

    // Guarda los datos actualizados en localStorage
    localStorage.setItem('agregados', JSON.stringify(seleccionados));
    localStorage.removeItem('seleccionados'); // Limpia 'seleccionados' después de agregar
}
//gastos importado
function traer_gastos_importado(numeros, numeros_guardados){

    if (numeros.length === 0) {
        console.log("No hay seguimientos seleccionados. gastos");
        return;
    }

    // Hacer la solicitud AJAX para enviar los IDs al servidor
     const csrftoken = getCookie2('csrftoken');
    $.ajax({
        url: '/exportacion_aerea/source_gastos_importado/',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({ ids: numeros }),
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(response) {
            if (response.data.length > 0) {
                    response.data.forEach(function(item) {
                        numeros_guardados.forEach(function(guardado) {
                            if (item.seguimiento_control === guardado.seguimiento) {
                                // Si coinciden los seguimientos, asignar el numero
                                item.numero = guardado.numero;
                            }
                        });
                    });

                    guardar_gasto_importado(response.data);
            }
        },
        error: function(xhr, status, error) {
            console.error("Error al traer los seguimientos:", error);
        }
    });
}
function guardar_gasto_importado(data){
    miurl = "/exportacion_aerea/add_gasto_importado/";

    $.ajax({
        type: "POST",
        url: miurl,
        contentType: "application/json", // Enviar datos como JSON
        data: JSON.stringify(data),
        headers: { 'X-CSRFToken': csrf_token }, // Enviar token CSRF en el encabezado
        success: function (resultado) {
        },
        error: function (error) {
            console.log('Error en la solicitud:', error);
        }
    });
}

//rutas importado
function traer_rutas_importado(numeros, numeros_guardados){

    if (numeros.length === 0) {
        console.log("No hay seguimientos seleccionados. ruta");
        return;
    }

    // Hacer la solicitud AJAX para enviar los IDs al servidor
     const csrftoken = getCookie2('csrftoken');
    $.ajax({
        url: '/exportacion_aerea/source_rutas_importado/',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({ ids: numeros }),
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(response) {
            if (response.data.length > 0) {
                    response.data.forEach(function(item) {
                        numeros_guardados.forEach(function(guardado) {
                            if (item.seguimiento_control === guardado.seguimiento) {
                                // Si coinciden los seguimientos, asignar el numero
                                item.numero = guardado.numero;
                            }
                        });
                    });

                    guardar_ruta_importado(response.data);
            }
        },
        error: function(xhr, status, error) {
            console.error("Error al traer los seguimientos:", error);
        }
    });
}
function guardar_ruta_importado(data){
    miurl = "/exportacion_aerea/add_ruta_importado/";

    $.ajax({
        type: "POST",
        url: miurl,
        contentType: "application/json", // Enviar datos como JSON
        data: JSON.stringify(data),
        headers: { 'X-CSRFToken': csrf_token }, // Enviar token CSRF en el encabezado
        success: function (resultado) {
        },
        error: function (error) {
            console.log('Error en la solicitud:', error);
        }
    });
}
//embarques importado
function traer_embarques_importado(numeros, numeros_guardados){

    if (numeros.length === 0) {
        console.log("No hay seguimientos seleccionados. embarque");
        return;
    }

    // Hacer la solicitud AJAX para enviar los IDs al servidor
     const csrftoken = getCookie2('csrftoken');
    $.ajax({
        url: '/exportacion_aerea/source_embarque_importado/',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({ ids: numeros }),
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(response) {
            if (response.data.length > 0) {
                    response.data.forEach(function(item) {
                        numeros_guardados.forEach(function(guardado) {
                            if (item.seguimiento_control === guardado.seguimiento) {
                                // Si coinciden los seguimientos, asignar el numero
                                item.numero = guardado.numero;
                            }
                        });
                    });

                    guardar_embarque_importado(response.data);
            }
        },
        error: function(xhr, status, error) {
            console.error("Error al traer los seguimientos:", error);
        }
    });
}
function guardar_embarque_importado(data){
    miurl = "/exportacion_aerea/add_embarque_importado/";

    $.ajax({
        type: "POST",
        url: miurl,
        contentType: "application/json", // Enviar datos como JSON
        data: JSON.stringify(data),
        headers: { 'X-CSRFToken': csrf_token }, // Enviar token CSRF en el encabezado
        success: function (resultado) {
        },
        error: function (error) {
            console.log('Error en la solicitud:', error);
        }
    });
}
//archivos importado
function traer_archivos_importado(numeros, numeros_guardados){

    if (numeros.length === 0) {
        console.log("No hay seguimientos seleccionados. archivos");
        return;
    }

    // Hacer la solicitud AJAX para enviar los IDs al servidor
     const csrftoken = getCookie2('csrftoken');
    $.ajax({
        url: '/exportacion_aerea/source_archivos_importado/',
        type: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({ ids: numeros }),
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(response) {
            if (response.data.length > 0) {
                    response.data.forEach(function(item) {
                        numeros_guardados.forEach(function(guardado) {
                            if (item.seguimiento_control === guardado.seguimiento) {
                                // Si coinciden los seguimientos, asignar el numero
                                item.numero = guardado.numero;
                            }
                        });
                    });
                    console.log(response.data);
                    guardar_archivo_importado(response.data);
            }
        },
        error: function(xhr, status, error) {
            console.error("Error al traer los seguimientos:", error);
        }
    });
}
function guardar_archivo_importado(data) {
    const miurl = "/exportacion_aerea/add_archivo_importado/";

        // Enviar los datos como JSON (ruta del archivo, número y detalle)
        $.ajax({
            type: "POST",
            url: miurl,
            contentType: "application/json",
            data: JSON.stringify({data}),
            headers: { 'X-CSRFToken': csrf_token },  // Enviar token CSRF
            success: function (resultado) {
                console.log('Archivo guardado correctamente:', resultado);
            },
            error: function (error) {
                console.log('Error en la solicitud:', error);
            }
        });

}

//eliminar houses de un master
function eliminar_house(){
let tabla = localStorage.getItem('tabla_origen');
        let selectedRowN,url;

        if (tabla.includes('tabla_house_directo')){
         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';
        }else{
         selectedRowN= localStorage.getItem('id_master_editar');
         url='master-detail/';
        }

            $.ajax({
            url: '/exportacion_aerea/'+url,
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    if (localStorage.getItem('lugar_importarhijo') === 'editmaster') {
                        if (confirm('¿Confirma eliminar seleccionado?')) {
                            let row = table_edit_ea.rows('.table-secondary').data();
                            if (row.length === 1) {
                                let master = localStorage.getItem('master_editar');
                                eliminar_agregado(master, row[0][0]);

                                miurl = "/exportacion_aerea/eliminar_house/";
                                var toData = {
                                    'id': row[0][0],
                                    'csrfmiddlewaretoken': csrf_token,
                                };
                                $.ajax({
                                    type: "POST",
                                    url: miurl,
                                    data: toData,
                                    success: function (resultado) {
                                        aux = resultado['resultado'];
                                        if (aux === 'exito') {
                                            //actualizar dependiendo de si es la tabla de editar master o de addmaster
                                            $('#table_edit_ea').DataTable().destroy();
                                            cargar_hauses_master_edit();
                                            alert('Eliminado correctamente');
                                        } else {
                                            alert(aux);
                                        }
                                    }
                                });
                            } else {
                                alert('Debe seleccionar un unico registro');
                            }
                        }
                    } else if (localStorage.getItem('lugar_importarhijo') === 'addmaster') {
                        if (confirm('¿Confirma eliminar seleccionado?')) {
                            let row = table_add_ea.rows('.table-secondary').data();
                            if (row.length === 1) {
                                miurl = "/exportacion_aerea/eliminar_house/";
                                var toData = {
                                    'id': row[0][0],
                                    'csrfmiddlewaretoken': csrf_token,
                                };
                                $.ajax({
                                    type: "POST",
                                    url: miurl,
                                    data: toData,
                                    success: function (resultado) {
                                        aux = resultado['resultado'];
                                        if (aux === 'exito') {
                                            let master = localStorage.getItem('master_editar');
                                            eliminar_agregado(master, row[0][0]);
                                            //actualizar dependiendo de si es la tabla de editar master o de addmaster
                                            $('#table_add_ea').DataTable().destroy();
                                            cargar_hauses_master();
                                            alert('Eliminado correctamente');
                                        } else {
                                            alert(aux);
                                        }
                                    }
                                });
                            } else {
                                alert('Debe seleccionar un unico registro');
                            }
                        }
                    } else {
                        alert('ocurrio error con lugar_importarhijo');
                    }
                }
            });

}
function eliminar_agregado(master,id_house){
        let agregados = JSON.parse(localStorage.getItem('agregados')) || [];
        let csrftoken = getCookie2('csrftoken');
        $.ajax({
        type: "POST",
        url: "/exportacion_aerea/source_embarque_id/",
        data: {
            id: id_house,
            csrfmiddlewaretoken: csrftoken
        },
        success: function(response) {
            $.ajax({
                type: "POST",
                url: "/exportacion_aerea/source_seguimiento_id/",
                data: {
                    id: response.seguimiento,
                    csrfmiddlewaretoken: csrftoken
                },
                success: function(response) {
                    const idBuscado = response.id.toString();
                    agregados.forEach((item, index) => {
                        if (item.master === master) {
                            const idIndex = item.agregados.indexOf(idBuscado);
                            if (idIndex !== -1) {
                                item.agregados.splice(idIndex, 1);
                            }
                        }
                    });
                    localStorage.setItem('agregados', JSON.stringify(agregados));

                },
                error: function(error) {
                    console.log('Error:', error);
                }
            });
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });

}

//gastos master
function get_datos_gastos() {
let numero=localStorage.getItem('numero_master_seleccionado');
    ingresos = 0
    egresos = 0
    diferencia = 0
    $("#tabla_gastos").dataTable().fnDestroy();
    table_gastos = $('#tabla_gastos').DataTable({
        "order": [[1, "desc"], [1, "desc"]],
        "processing": true,
        "serverSide": true,
        "pageLength": 10,
        "language": {
            url: "/static/datatables/es_ES.json"
        },
        "ajax": {
            "url": "/exportacion_aerea/source_gastos/",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "numero": numero,
                });
            }
        }, "columnDefs": [
            {
                "targets": [0],
                "orderable": false,
            },
            {
                "targets": [3],
                "className": 'derecha',
            },
            {
                "targets": [4],
                "className": 'derecha',
            },{
                "targets": [8],
                "className": 'derecha',
            },
            {
                "targets": [11],
                "className": 'derecha',
            },
        ],"rowCallback": function (row, data) {
                // $(row).find('td:eq(3)').css('background-color', '#99cc99');
                // $(row).find('td:eq(4)').css('background-color', '#CC9393');
                console.log(data[3]);
                console.log(data[4]);
                if (parseFloat(data[4]) > 0){
                 //ingresos += parseFloat(data[4]);
                 egresos += parseFloat(data[4]);
                 diferencia += parseFloat(data[4]);
                }
        },"initComplete": function( settings, json ) {
            $('#gastos_form #gastos_ingresos').val(0);
            $('#gastos_form #gastos_egresos').val(egresos.toFixed(2));
            $('#gastos_form #gastos_diferencia').val(0);
        }
    });
    console.log(ingresos.toFixed(2));
    console.log(egresos.toFixed(2));
    console.log(ingresos-egresos.toFixed(2));
}

//gastos house
function get_datos_gastos_house() {
    let numero=localStorage.getItem('num_house_gasto');
    ingresos = 0
    egresos = 0
    diferencia = 0
    $("#tabla_gastos_house").dataTable().fnDestroy();
    table_gastos = $('#tabla_gastos_house').DataTable({
        "order": [[1, "desc"], [1, "desc"]],
        "processing": true,
        "serverSide": true,
        "pageLength": 10,
        "language": {
            url: "/static/datatables/es_ES.json"
        },
        "ajax": {
            "url": "/exportacion_aerea/source_gastos_house/",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "numero": numero,
                });
            }
        }, "columnDefs": [
            {
                "targets": [0],
                "orderable": false,
            },
            {
                "targets": [3],
                "className": 'derecha',
            },
            {
                "targets": [4],
                "className": 'derecha',
            },{
                "targets": [8],
                "className": 'derecha',
            },
            {
                "targets": [11],
                "className": 'derecha',
            },
                        {
                "targets": [0,5,6,8,9,10,11],
                "visible": false,
            },
            {
                "targets": [14],
                "render": function (data, type, row) {
                    return row[18];
                }
            },
        ],"rowCallback": function (row, data) {
                $(row).removeClass('fila-rojo fila-amarillo fila-verde');

                const color = data[17];
                if (color === 'ROJO') {
                    $(row).addClass('fila-rojo');
                } else if (color === 'AMARILLO') {
                    $(row).addClass('fila-amarillo');
                } else if(color === 'VERDE'){
                    $(row).addClass('fila-verde');
                }
                // $(row).find('td:eq(3)').css('background-color', '#99cc99');
                // $(row).find('td:eq(4)').css('background-color', '#CC9393');
                if (parseFloat(data[3]) > 0){
                    ingresos += parseFloat(data[3]);
                    diferencia += parseFloat(data[3]);
                }
        },"initComplete": function( settings, json ) {
            $('#gastos_form_house #gastos_ingresos').val(ingresos.toFixed(2));
            $('#gastos_form_house #gastos_egresos').val(0);
            $('#gastos_form_house #gastos_diferencia').val(0);
        }
    });
}
function gastos_btn_h_click(){
let tabla = localStorage.getItem('tabla_origen');
        let selectedRowN,url;

        if (tabla.includes('tabla_house_directo')){
         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';
        }else{
         selectedRowN= localStorage.getItem('id_master_editar');
         url='master-detail/';
        }

            $.ajax({
            url: '/exportacion_aerea/'+url,
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    $("#id_gasto_id_house").val('');
                    let selectedRowId = localStorage.getItem('id_house_gasto');
                    let selectedRowN = localStorage.getItem('num_house_gasto');
                    let consignatario_code;
                    if ($.fn.dataTable.isDataTable('#table_edit_ea')) {
                        consignatario_code = $('#table_edit_ea').DataTable().row('.table-secondary').data()[18];
                    } else {
                        consignatario_code = $('#tabla_house_directo_ea').DataTable().row('.table-secondary').data()[18];
                    }
                    if (selectedRowN != null) {
                        get_datos_gastos_house();
                        $('#gastos_form_house').trigger("reset");
                        $("#id_socio_h").val(consignatario_code);
                        $("#gastos_modal_house").dialog({
                            autoOpen: true,
                            open: function () {
                                document.getElementById('numero_gasto_house').value = selectedRowN;
                            },
                            modal: true,
                            title: "Gastos para el House N°: " + selectedRowN,
                            height: wHeight * 0.70,
                            width: wWidth * 0.70,
                            class: 'modal fade',
                            buttons: [
                                {
                                    text: "Eliminar",
                                    class: "btn btn-danger",
                                    style: "width:100px",
                                    click: function () {
                                        if (confirm('¿Confirma eliminar el gasto seleccionado?')) {
                                            row = table_gastos.rows('.table-secondary').data();
                                            if (row.length === 1) {
                                                miurl = "/exportacion_aerea/eliminar_gasto_house/";
                                                var toData = {
                                                    'id': row[0][0],
                                                    'csrfmiddlewaretoken': csrf_token,
                                                };
                                                $.ajax({
                                                    type: "POST",
                                                    url: miurl,
                                                    data: toData,
                                                    success: function (resultado) {
                                                        aux = resultado['resultado'];
                                                        if (aux === 'exito') {
                                                            $("#table_gastos_house").dataTable().fnDestroy();
                                                            get_datos_gastos_house();
                                                            alert('Eliminado correctamente');
                                                            if ($.fn.DataTable.isDataTable('#table_add_ea')) {
                                                                $('#table_add_ea').DataTable().ajax.reload(null, false);
                                                            }

                                                            if ($.fn.DataTable.isDataTable('#table_edit_ea')) {
                                                                $('#table_edit_ea').DataTable().ajax.reload(null, false);
                                                            }
                                                            if ($.fn.DataTable.isDataTable('#tabla_house_directo_ea')) {
                                                                $('#tabla_house_directo_ea').DataTable().ajax.reload(null, false);
                                                            }
                                                        } else {
                                                            alert(aux);
                                                        }
                                                    }
                                                });
                                            } else {
                                                alert('Debe seleccionar un unico registro');
                                            }
                                        }
                                    },
                                }, {
                                    text: "Salir",
                                    class: "btn btn-dark",
                                    style: "width:100px",
                                    click: function () {
                                        $(this).dialog("close");
                                    },
                                }],
                            beforeClose: function (event, ui) {
                                //localStorage.removeItem('num_house_gasto');
//                $('#table_add_ea tbody tr').removeClass('table-secondary');
//                $('#table_edit_ea tbody tr').removeClass('table-secondary');
//                $('#tabla_house_directo_ea tbody tr').removeClass('table-secondary');
                                // table.ajax.reload();
                                $("#tabla_gastos").dataTable().fnDestroy();
                            }
                        })

                    } else {
                        alert('Debe seleccionar al menos un registro');
                    }
                }
            });
}

//rutas house
function get_datos_rutas_house() {
    let numero=localStorage.getItem('num_house_gasto');

   $("#tabla_rutas_house").dataTable().fnDestroy();
    table_rutas = $('#tabla_rutas_house').DataTable({
        "order": [[1, "desc"], [1, "desc"]],
        "processing": true,
        "serverSide": true,
        "pageLength": 10,
        "language": {
            url: "/static/datatables/es_ES.json"
        },
        "ajax": {
            "url": "/exportacion_aerea/source_rutas_house/",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "numero": numero,
                });
            }
        },
    });
    get_datos_seguimiento_rutas(numero);
}
function rutas_btn_h_click(){
let tabla = localStorage.getItem('tabla_origen');
        let selectedRowN,url;

        if (tabla.includes('tabla_house_directo')){
         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';
        }else{
         selectedRowN= localStorage.getItem('id_master_editar');
         url='master-detail/';
        }

            $.ajax({
            url: '/exportacion_aerea/'+url,
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    $("#id_house_ruta").val('');
                    let selectedRowId = localStorage.getItem('id_house_gasto');
                    let selectedRowN = localStorage.getItem('num_house_gasto');
                    if (selectedRowN != null) {
                        get_datos_rutas_house();
                        $('#rutas_form_house').trigger("reset");
                        $("#rutas_modal_house").dialog({
                            autoOpen: true,
                            open: function () {
                                document.getElementById('id_ruta_id').value = selectedRowN;
                            },
                            modal: true,
                            title: "Rutas para el House N°: " + selectedRowN,
                            height: 'auto',
                            width: 'auto',
                            position: {my: "top", at: "top+20", of: window},
                            class: 'modal fade',
                            buttons: [
                                {
                                    text: "Eliminar",
                                    class: "btn btn-danger",
                                    style: "width:100px",
                                    click: function () {
                                        if (confirm('¿Confirma eliminar el gasto seleccionado?')) {
                                            var row = $('#tabla_rutas_house').DataTable().rows('.table-secondary').data();
                                            if (row.length === 1) {
                                                miurl = "/exportacion_aerea/eliminar_ruta_house/";
                                                var toData = {
                                                    'id': row[0][0],
                                                    'csrfmiddlewaretoken': csrf_token,
                                                };
                                                $.ajax({
                                                    type: "POST",
                                                    url: miurl,
                                                    data: toData,
                                                    success: function (resultado) {
                                                        aux = resultado['resultado'];
                                                        if (aux === 'exito') {
                                                            $("#tabla_rutas_house").dataTable().fnDestroy();
                                                            get_datos_rutas_house();
                                                            alert('Eliminado correctamente');
                                                            if ($.fn.DataTable.isDataTable('#table_add_ea')) {
                                                                $('#table_add_ea').DataTable().ajax.reload(null, false);
                                                            }

                                                            if ($.fn.DataTable.isDataTable('#table_edit_ea')) {
                                                                $('#table_edit_ea').DataTable().ajax.reload(null, false);
                                                            }
                                                            if ($.fn.DataTable.isDataTable('#tabla_house_directo_ea')) {
                                                                $('#tabla_house_directo_ea').DataTable().ajax.reload(null, false);
                                                            }
                                                        } else {
                                                            alert(aux);
                                                        }
                                                    }
                                                });
                                            } else {
                                                alert('Debe seleccionar un unico registro');
                                            }
                                        }
                                    },
                                }, {
                                    text: "Salir",
                                    class: "btn btn-dark",
                                    style: "width:100px",
                                    click: function () {
                                        $(this).dialog("close");
                                    },
                                }],
                            beforeClose: function (event, ui) {
                                //localStorage.removeItem('num_house_gasto');
                                $("#table_rutas_house").dataTable().fnDestroy();
//                 $('#table_add_ea tbody tr').removeClass('table-secondary');
//                $('#table_edit_ea tbody tr').removeClass('table-secondary');
//                $('#tabla_house_directo_ea tbody tr').removeClass('table-secondary');
                            }
                        })

                    } else {
                        alert('Debe seleccionar al menos un registro');
                    }
                }
            });
}
function get_datos_seguimiento_rutas(numero) {
    $.ajax({
        url: "/exportacion_aerea/datos_embarque_ruta/",  // Asegúrate de que esta URL coincida con tu Django URLConf
        type: "POST",
        data: {
            numero: numero,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() // CSRF Token obligatorio en POST
        },
        dataType: "json",
        success: function (response) {
            if (response.resultado === "exito") {
                // Asignar valores a los inputs si existen en el formulario
                $("#id_salida").val(response.datos.salida || "");
                $("#id_llegada").val(response.datos.llegada || "");
                $("#id_origen").val(response.datos.origen || "");
                $("#id_destino").val(response.datos.destino || "");
                $("#id_modo_ruta").val(response.datos.modo || "");
                $("#id_viaje_ruta").val(response.datos.viaje || "");
                $("#id_vapor").val(response.datos.vapor || "");
            } else {
                console.error("Error en la respuesta:", response.resultado);
                alert("Error: " + response.resultado);
            }
        },
        error: function (xhr, status, error) {
            console.error("Error en la petición AJAX:", error);
            alert("No se pudo obtener la información. Verifica el número e intenta de nuevo.");
        }
    });
}
//rutas master
function get_datos_rutas_master() {
    let numero=localStorage.getItem('numero_master_seleccionado');

   $("#tabla_rutas_master").dataTable().fnDestroy();
    table_rutas = $('#tabla_rutas_master').DataTable({
        "order": [[1, "desc"], [1, "desc"]],
        "processing": true,
        "serverSide": true,
        "pageLength": 10,
        "language": {
            url: "/static/datatables/es_ES.json"
        },
        "ajax": {
            "url": "/exportacion_aerea/source_rutas_master/",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "numero": numero,
                });
            }
        },
    });
    get_datos_seguimiento_rutas_master(numero);
}
function rutas_btn_h_click_master(){
let tabla = localStorage.getItem('tabla_origen');
        let selectedRowN,url;

        if (tabla.includes('tabla_house_directo')){
         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';
        }else{
         selectedRowN= localStorage.getItem('id_master_editar');
         url='master-detail/';
        }

            $.ajax({
            url: '/exportacion_aerea/'+url,
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    $("#id_master_ruta").val('');
                    //let selectedRowId = localStorage.getItem('numero_master_seleccionado');
                    let selectedRowN = localStorage.getItem('numero_master_seleccionado');
                    if (selectedRowN != null) {
                        get_datos_rutas_master();
                        $('#rutas_form_master').trigger("reset");
                        $("#rutas_modal_master").dialog({
                            autoOpen: true,
                            open: function () {
                                document.getElementById('id_ruta_id_master').value = selectedRowN;
                            },
                            modal: true,
                            title: "Rutas para el Master N°: " + selectedRowN,
                            height: wHeight * 0.90,
                            width: wWidth * 0.50,
                            class: 'modal fade',
                            buttons: [
                                {
                                    text: "Eliminar",
                                    class: "btn btn-danger",
                                    style: "width:100px",
                                    click: function () {
                                        if (confirm('¿Confirma eliminar el gasto seleccionado?')) {
                                            var row = $('#tabla_rutas_master').DataTable().rows('.table-secondary').data();
                                            if (row.length === 1) {
                                                miurl = "/exportacion_aerea/eliminar_ruta_master/";
                                                var toData = {
                                                    'id': row[0][0],
                                                    'csrfmiddlewaretoken': csrf_token,
                                                };
                                                $.ajax({
                                                    type: "POST",
                                                    url: miurl,
                                                    data: toData,
                                                    success: function (resultado) {
                                                        aux = resultado['resultado'];
                                                        if (aux === 'exito') {
                                                            $("#tabla_rutas_master").dataTable().fnDestroy();
                                                            get_datos_rutas_master();
                                                            alert('Eliminado correctamente');
                                                            /*
                                                            if ($.fn.DataTable.isDataTable('#table_add_ea')) {
                                                                $('#table_add_ea').DataTable().ajax.reload(null, false);
                                                            }*/
                                                        } else {
                                                            alert(aux);
                                                        }
                                                    }
                                                });
                                            } else {
                                                alert('Debe seleccionar un unico registro');
                                            }
                                        }
                                    },
                                }, {
                                    text: "Salir",
                                    class: "btn btn-dark",
                                    style: "width:100px",
                                    click: function () {
                                        $(this).dialog("close");
                                    },
                                }],
                            beforeClose: function (event, ui) {
                                //localStorage.removeItem('num_house_gasto');
                                $("#table_rutas_master").dataTable().fnDestroy();
                            try {
                                desbloquearDatos();
                            } catch (error) {
                                console.error("⚠️ Error en desbloquearDatos:", error);
                            }
//                $('#table_edit_ea tbody tr').removeClass('table-secondary');
//                $('#tabla_house_directo_ea tbody tr').removeClass('table-secondary');
                            }
                        })

                    } else {
                        alert('Debe seleccionar al menos un registro');
                    }
                }
            });
}
function get_datos_seguimiento_rutas_master(numero) {
    $.ajax({
        url: "/exportacion_aerea/datos_embarque_ruta_master/",  // Asegúrate de que esta URL coincida con tu Django URLConf
        type: "POST",
        data: {
            numero: numero,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() // CSRF Token obligatorio en POST
        },
        dataType: "json",
        success: function (response) {
            if (response.resultado === "exito") {
                // Asignar valores a los inputs si existen en el formulario
                $("#id_salida_master").val(response.datos.salida || "");
                $("#id_origen_master").val(response.datos.origen || "");
                $("#id_destino_master").val(response.datos.destino || "");
                $("#codigo_cia_master").val(response.datos.codigo_cia || "");
            } else {
                console.error("Error en la respuesta:", response.resultado);
                alert("Error: " + response.resultado);
            }
        },
        error: function (xhr, status, error) {
            console.error("Error en la petición AJAX:", error);
            alert("No se pudo obtener la información. Verifica el número e intenta de nuevo.");
        }
    });
}

//embarques house
function get_datos_embarques_house(){
 let numero=localStorage.getItem('num_house_gasto');

   $("#tabla_embarques_house").dataTable().fnDestroy();
    table_embarques = $('#tabla_embarques_house').DataTable({
        "order": [[1, "desc"], [1, "desc"]],
        "processing": true,
        "serverSide": true,
        "pageLength": 10,
        "language": {
            url: "/static/datatables/es_ES.json"
        },
        "ajax": {
            "url": "/exportacion_aerea/source_embarques_house/",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "numero": numero,
                });
            }
        },
        "columnDefs": [
        {
            "targets": 6,  // Índice de la columna a ocultar (empieza en 0)
            "visible": false,
            "searchable": false // También oculta de la búsqueda
        },
        {
            "targets": 0,  // Índice de la columna a ocultar (empieza en 0)
            "visible": false,
            "searchable": false // También oculta de la búsqueda
        }
    ]
    });
}
function embarques_btn_h_click(){
let tabla = localStorage.getItem('tabla_origen');
        let selectedRowN,url;

        if (tabla.includes('tabla_house_directo')){
         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';
        }else{
         selectedRowN= localStorage.getItem('id_master_editar');
         url='master-detail/';
        }

            $.ajax({
            url: '/exportacion_aerea/'+url,
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    $("#id_embarque_id").val('');
                    let selectedRowId = localStorage.getItem('id_house_gasto');
                    let selectedRowN = localStorage.getItem('num_house_gasto');

                    if (selectedRowN != null) {
                        get_datos_embarques_house();
                        $('#embarques_form_house').trigger("reset");
                        $("#embarques_modal_house").dialog({
                            autoOpen: true,
                            open: function () {
                                document.getElementById('numero_embarque').value = selectedRowN;
                            },
                            modal: true,
                            title: "Embarques para el House N°: " + selectedRowN,
                            height: wHeight * 0.60,
                            width: wWidth * 0.50,
                            class: 'modal fade',
                            buttons: [
                                {
                                    text: "Eliminar",
                                    class: "btn btn-danger",
                                    style: "width:100px",
                                    click: function () {
                                        if (confirm('¿Confirma eliminar el embarque seleccionado?')) {
                                            var row = $('#tabla_embarques_house').DataTable().rows('.table-secondary').data();
                                            if (row.length === 1) {
                                                miurl = "/exportacion_aerea/eliminar_embarques_house/";
                                                var toData = {
                                                    'id': row[0][0],
                                                    'csrfmiddlewaretoken': csrf_token,
                                                };
                                                $.ajax({
                                                    type: "POST",
                                                    url: miurl,
                                                    data: toData,
                                                    success: function (resultado) {
                                                        aux = resultado['resultado'];
                                                        if (aux === 'exito') {
                                                            $("#tabla_embarques_house").dataTable().fnDestroy();
                                                            get_datos_embarques_house();
                                                            alert('Eliminado correctamente');
                                                            if ($.fn.DataTable.isDataTable('#table_add_ea')) {
                                                                $('#table_add_ea').DataTable().ajax.reload(null, false);
                                                            }

                                                            if ($.fn.DataTable.isDataTable('#table_edit_ea')) {
                                                                $('#table_edit_ea').DataTable().ajax.reload(null, false);
                                                            }
                                                            if ($.fn.DataTable.isDataTable('#tabla_house_directo_ea')) {
                                                                $('#tabla_house_directo_ea').DataTable().ajax.reload(null, false);
                                                            }
                                                        } else {
                                                            alert(aux);
                                                        }
                                                    }
                                                });
                                            } else {
                                                alert('Debe seleccionar un unico registro');
                                            }
                                        }
                                    },
                                }, {
                                    text: "Salir",
                                    class: "btn btn-dark",
                                    style: "width:100px",
                                    click: function () {
                                        $(this).dialog("close");
                                    },
                                }],
                            beforeClose: function (event, ui) {
                            try {
                                desbloquearDatos();
                            } catch (error) {
                                console.error("⚠️ Error en desbloquearDatos:", error);
                            }
                                $("#tabla_embarques_house").dataTable().fnDestroy();
//                 $('#table_add_ea tbody tr').removeClass('table-secondary');
//                $('#table_edit_ea tbody tr').removeClass('table-secondary');
//                $('#tabla_house_directo_ea tbody tr').removeClass('table-secondary');
                            }
                        })

                    } else {
                        alert('Debe seleccionar al menos un registro');
                    }
                }
            });
}

//acciones mails house
$('.email').click(function () {
        $("#modalSeleccionEmailHouse5").dialog("close");
        let id = localStorage.getItem('id_house_gasto');
        let numero = localStorage.getItem('num_house_gasto');

        let title = this.getAttribute('data-tt');
        var row = $('#table_edit_ea').DataTable().rows('.table-secondary').data();
        $("#id_to").val('');
        $("#id_cc").val('');
        $("#id_cco").val('');
        cco = $("#id_subject").val('');
        $('#email_add_input').summernote('destroy');
        $("#arhivos_adjuntos").html('');
        archivos_adjuntos = {};
        let master=false;
        let gastos = false;
        if(title=='Notificación de llegada de carga'){
            if(confirm('¿Desea informar Máster?')){
                master=true;
            }
            if(confirm('¿Desea informar Gastos?')){
                gastos=true;
            }
        }
        if (row.length === 1) {
             let selectedRowN = localStorage.getItem('id_master_editar');
            $.ajax({
                url: '/exportacion_aerea/master-detail/',
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    get_data_email(row, title, numero, id, master, gastos);
                    //$("#id_to").val(row[0][50]);
                    $("#emails_modal").dialog({
                        autoOpen: true,
                        open: function (event, ui) {
                            $('#email_add_input').summernote('destroy');
                            $('#email_add_input').summernote({
                                placeholder: 'Ingrese su texto aqui',
                                tabsize: 10,
                                height: wHeight * 0.60,
                                width: wWidth * 0.88,
                                toolbar: [
                                    ['style', ['style']],
                                    ['font', ['bold', 'underline', 'clear']],
                                    ['color', ['color']],
                                    ['para', ['ul', 'ol', 'paragraph']],
                                    ['table', ['table']],
                                    ['insert', ['link', 'picture', 'video']],
                                    ['view', ['fullscreen', 'codeview']]
                                ]
                            });
                            $('#email_add_input').focus();
                        },
                        modal: true,
                        title: title + " para el house N°: " + numero,
                        height: wHeight * 0.90,
                        width: wWidth * 0.90,
                        class: 'modal fade',
                        buttons: [
                            {
                                text: "Enviar",
                                class: "btn btn-primary",
                                style: "width:100px",
                                click: function () {
                                    to = $("#id_to").val();
                                    cc = $("#id_cc").val();
                                    cco = $("#id_cco").val();
                                    subject = $("#id_subject").val();
                                    message = $("#email_add_input").summernote('code');
                                    from = $('#id_from').val();
                                    if (!confirm('¿Realmente desea ENVIAR el correo?')) {
                                        return;
                                    }
                                    sendEmail(to, cc, cco, subject, message, title, numero, from);
                                    $(this).dialog("close");
                                },
                            }, {
                                text: "Salir",
                                class: "btn btn-dark",
                                style: "width:100px",
                                click: function () {
                                    $(this).dialog("close");

                                },
                            },],
                        beforeClose: function (event, ui) {
                            // localStorage.removeItem('num_house_gasto');
//                $('#table_add_ea tbody tr').removeClass('table-secondary');
//                $('#table_edit_ea tbody tr').removeClass('table-secondary');
//                $('#tabla_house_directo_ea tbody tr').removeClass('table-secondary');
                        }
                    })
                }
            });
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });

function cerrarDialogo(id) {
    const $dlg = $("#" + id);
    if ($dlg.length && $dlg.hasClass("ui-dialog-content") && $dlg.dialog("isOpen")) {
        $dlg.dialog("close");
    }
}

function get_data_email(row,title,numero,id,master,gastos) {
    let miurl = "/exportacion_aerea/get_data_email/";
    var toData = {
        'title': title,
        'row_number': numero,
        'id':id,
        'csrfmiddlewaretoken': csrf_token,
        'master':master,
        'gastos':gastos
    };
    $.ajax({
        type: "POST",
        url: miurl,
        data: toData,
        async: false,
        success: function (resultado) {
            if (resultado['resultado'] === 'exito') {
                let textarea = document.getElementById("email_add_input");
                textarea.value = resultado['mensaje'];
                $("#id_subject").val(resultado['asunto']);

                let asunto = resultado['asunto'].toLowerCase();
                if (asunto.includes("traspaso a operaciones")) {
                    $("#id_to").val("customerservices@oceanlinkgroup.com;lucas.bocskor@oceanlinkgroup.com;ines.delafuente@oceanlinkgroup.com");
                }else if(asunto.includes("orden de facturacion")){
                    $("#id_to").val("");
                }else if(asunto.includes("instrucción de embarque") || asunto.includes("shipping instruction")){
                $("#id_to").val(resultado['email_agente']);
                } else {
                    $("#id_to").val(resultado['email_cliente']);
                }
                let selectEmails = document.getElementById("id_from");
                if (selectEmails && resultado['emails_disponibles']) {
                    selectEmails.innerHTML = "";

                    resultado['emails_disponibles'].forEach(function(email) {
                        let option = document.createElement("option");
                        option.value = email;
                        option.text = email;
                        selectEmails.appendChild(option);
                    });
                }
            } else {
                alert(resultado['resultado']);
            }
        }
    });
}
function sendEmail(to,cc,cco,subject,message,title,seguimiento,from) {
    let miurl = "/envio_notificacion/EA/";
    var toData = {
        'to': to,
        'cc': cc,
        'cco': cco,
        'from':from,

        'subject': subject,
        'message': message,
        'tipo': title,
        'seguimiento': seguimiento,
        'archivos_adjuntos': JSON.stringify(archivos_adjuntos),
        'csrfmiddlewaretoken': csrf_token,
    };
    $.ajax({
        type: "POST",
        url: miurl,
        data: toData,
        async: false,
        success: function (resultado) {
            if (resultado['resultado'] === 'exito') {
                alert('¡Mensaje enviado con exito!');
                return true;
            } else {
                alert(resultado['resultado']);
            }
        }
    });


}
//adjuntar archivos mails
function get_datos_archivos() {
   let table_archivos = $('#tabla_archivos').DataTable({
        "order": [[1, "desc"], [1, "desc"]],
        "processing": true,
        "serverSide": true,
        "pageLength": 100,
        "language": {
            url: "/static/datatables/es_ES.json"
        },
        "ajax": {
            "url": "/exportacion_aerea/source_archivos/",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "numero": localStorage.getItem('num_house_gasto'),
                });
            }
        }, "columnDefs": [
            {
                "targets": [0],
                "orderable": false,
                "data": null,
                "visible":false,
                "defaultContent": '',
                render: function (data, type, row) {
                }
            },
        ]
    });

}
function eliminar_adjunto(id) {
  // Eliminar el elemento del diccionario
  if(confirm('¿Confirma eliminar archivo adjunto?')){
      delete archivos_adjuntos[id];
      // Eliminar el elemento HTML del DOM
      var elementoHTML = document.getElementById(id);
      if (elementoHTML) {
        elementoHTML.remove();
      }
      mostrarToast('¡Adjunto eliminado con exito!', 'danger');
  }
}

//modificar fechas
function modificar_fecha_retiro(x){
let lugar=localStorage.getItem('lugar');
    let vector = null;
    let master = null;
    let fecha = null;
    const csrftoken = getCookie2('csrftoken');
    if (x == 0) {
        // master
        vector = JSON.parse(localStorage.getItem('fecha_editada_master'));
    } else {
        // house
        vector = JSON.parse(localStorage.getItem('fecha_editada_house'));
    }
    if (vector && vector.length > 0) {
        let objeto = vector[0];
        master = objeto.master;
        fecha = objeto.fecha;
    }
    $.ajax({
        type: "POST",
        url: "/exportacion_aerea/modificar_fecha_retiro/",
        data: JSON.stringify({ master: master, fecha: fecha }),
        contentType: "application/json",
        headers: {
            'X-CSRFToken': csrftoken
        },
        success: function(response) {
            if(lugar==='add_master'){
            table_add_ea.ajax.reload(null, false);
            }else if(lugar==='edit_master'){
            table_edit_ea.ajax.reload(null, false);
            }else if(lugar==='edit_directo'){
            $('#tabla_house_directo_ea').DataTable().ajax.reload(null, false);
            }
            else{
            console.log('error en el lugar '+lugar);
            }
            if (x == 0) {
                localStorage.removeItem('fecha_editada_master');
            } else {
                localStorage.removeItem('fecha_editada_house');
            }

        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
}

//agregar archivo house
function archivos_btn_h_click(){
let tabla = localStorage.getItem('tabla_origen');
        let selectedRowN,url;

        if (tabla.includes('tabla_house_directo')){
         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';
        }else{
         selectedRowN= localStorage.getItem('id_master_editar');
         url='master-detail/';
        }

            $.ajax({
            url: '/exportacion_aerea/'+url,
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    $("#tabla_archivos").dataTable().fnDestroy();
                    row = table.rows('.table-secondary').data();
                    get_datos_archivos();

                    $("#archivos_modal").dialog({
                        autoOpen: true,
                        open: function (event, ui) {

                        },
                        modal: true,
                        title: "Archivos para el House N°: " + localStorage.getItem('num_house_gasto'),
                        height: wHeight * 0.70,
                        width: wWidth * 0.70,
                        class: 'modal fade',
                        buttons: [
                            {
                                text: "Descargar",
                                class: "btn btn-dark",
                                style: "width:100px",
                                click: function () {
                                    if (confirm('¿Confirma descargar el archivo seleccionado?')) {
                                        var url = '/exportacion_aerea/descargar_archivo/' + localStorage.getItem('id_archivo');  // Ruta de la vista que devuelve el archivo
                                        window.open(url, '_blank');
                                    }
                                },
                            }, {
                                text: "Eliminar",
                                class: "btn btn-danger",
                                style: "width:100px",
                                click: function () {
                                    if (confirm('¿Confirma eliminar archivo?')) {
                                        if (localStorage.getItem('id_archivo')) {
                                            miurl = "/exportacion_aerea/eliminar_archivo/";
                                            var toData = {
                                                'id': localStorage.getItem('id_archivo'),
                                                'csrfmiddlewaretoken': csrf_token,
                                            };
                                            $.ajax({
                                                type: "POST",
                                                url: miurl,
                                                data: toData,
                                                success: function (resultado) {
                                                    aux = resultado['resultado'];
                                                    if (aux == 'exito') {
                                                        var idx = table.cell('.table-secondary', 0).index();
                                                        $("#tabla_archivos tr.selected").removeClass('selected');
                                                        $('#tabla_archivos').DataTable().ajax.reload(null, false);
                                                        if ($.fn.DataTable.isDataTable('#table_add_ea')) {
                                                            $('#table_add_ea').DataTable().ajax.reload(null, false);
                                                        }

                                                        if ($.fn.DataTable.isDataTable('#table_edit_ea')) {
                                                            $('#table_edit_ea').DataTable().ajax.reload(null, false);
                                                        }
                                                        if ($.fn.DataTable.isDataTable('#tabla_house_directo_ea')) {
                                                            $('#tabla_house_directo_ea').DataTable().ajax.reload(null, false);
                                                        }
                                                    } else {
                                                        alert(aux);
                                                    }
                                                }
                                            });
                                        } else {
                                            alert('Debe seleccionar un unico registro');
                                        }
                                    }
                                },
                            },
                            {
                                text: "Cerrar",
                                class: "btn btn-info",
                                style: "width:100px",
                                click: function () {
                                    $(this).dialog("close");
                                },
                            },
                        ],
                        beforeClose: function (event, ui) {
                            try {
                                desbloquearDatos();
                            } catch (error) {
                                console.error("⚠️ Error en desbloquearDatos:", error);
                            }
                            $("#tabla_archivos").dataTable().fnDestroy();
//                $('#table_add_ea tbody tr').removeClass('table-secondary');
//                $('#table_edit_ea tbody tr').removeClass('table-secondary');
//                $('#tabla_house_directo_ea tbody tr').removeClass('table-secondary');
                        }
                    })
                }
            });
}


//imprimir caratula house
function pdf_btn_h_click(){
let tabla = localStorage.getItem('tabla_origen');
        let selectedRowN,url;

        if (tabla.includes('tabla_house_directo')){
         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';
        }else{
         selectedRowN= localStorage.getItem('id_master_editar');
         url='master-detail/';
        }

            $.ajax({
            url: '/exportacion_aerea/'+url,
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    let selectedRowN = localStorage.getItem('num_house_gasto');
                    $("#pdf_add_input").html('');
                    $('#pdf_add_input').summernote('destroy');

                    if (selectedRowN != null) {
                        get_datos_pdf();
                        $("#pdf_modal").dialog({
                            autoOpen: true,
                            open: function (event, ui) {
                                $('#pdf_add_input').summernote('destroy');

                                $('#pdf_add_input').summernote({
                                    placeholder: '',
                                    title: 'PDF con el detalle del seguimiento',
                                    tabsize: 10,
                                    fontNames: ['Arial', 'Arial Black', 'Comic Sans MS', 'Courier New', 'Merriweather'],
                                    height: wHeight * 0.65,
                                    width: wWidth * 0.55,
                                    toolbar: [
                                        ['style', ['style']],
                                        ['font', ['bold', 'underline', 'clear']],
                                        ['color', ['color']],
                                        ['para', ['ul', 'ol', 'paragraph']],
                                        ['table', ['table']],
                                        ['insert', ['link', 'picture', 'video']],
                                        ['view', ['fullscreen', 'codeview']]
                                    ]
                                });
                            },
                            modal: true,
                            title: "Carátula del house N°: " + selectedRowN,
                            height: wHeight * 0.70,
                            width: wWidth * 0.60,
                            class: 'modal fade',
                            buttons: [
                                {
                                    // text:"Imprimir",
                                    html: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-printer" viewBox="0 0 16 16">\n' +
                                        '  <path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/>\n' +
                                        '  <path d="M5 1a2 2 0 0 0-2 2v2H2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v1a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1h1a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3a2 2 0 0 0-2-2H5zM4 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2H4V3zm1 5a2 2 0 0 0-2 2v1H2a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v-1a2 2 0 0 0-2-2H5zm7 2v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1z"/>\n' +
                                        '</svg> Imprimir',
                                    class: "btn btn-warning ",
                                    style: "width:100px",
                                    icons: {primary: "bi bi-star"},
                                    click: function () {
                                        imprimirPDF();
                                    },
                                }, {
                                    text: "Salir",
                                    class: "btn btn-dark",
                                    style: "width:100px",
                                    click: function () {
                                        $(this).dialog("close");
                                    },
                                },
                            ],
                            beforeClose: function (event, ui) {
                            try {
                                desbloquearDatos();
                            } catch (error) {
                                console.error("⚠️ Error en desbloquearDatos:", error);
                            }
                            }
                        })
                    } else {
                        alert('Debe seleccionar al menos un registro');
                    }
                }
            });
}
function get_datos_pdf() {
    let selectedRowN = localStorage.getItem('num_house_gasto');
    miurl = "/exportacion_aerea/get_datos_caratula/";
    var toData = {
        'numero': selectedRowN,
        'csrfmiddlewaretoken': csrf_token,
    };
    $.ajax({
        type: "POST",
        url: miurl,
        data: toData,
        async: false,
        success: function (resultado) {
            if (resultado['resultado'] === 'exito') {
                //     LLENAR DATOS
                $("#pdf_add_input").html(resultado['texto']);
            } else {
                alert(resultado['resultado']);
            }
        }
    });
}
//
//traer guia para el master
function guia_master() {

                    let transportista = $('#transportista_i').val();
                    if (transportista) {
                        $.ajax({
                            url: '/obtener-guias/' + transportista + '/',
                            method: 'GET',
                            success: function (data) {
                                // Limpiar las opciones actuales del select
                                $('#id_awb_select').empty();

                                if (data.length > 0) {
                                    // Si hay guías disponibles, agregar las opciones
                                    data.forEach(function (item) {
                                        let optionText = item.prefijo + '-' + item.numero;

                                        // Agregar cada opción al select
                                        $('#id_awb_select').append('<option value="' + optionText + '">' + optionText + '</option>');
                                    });

                                    // Seleccionar por defecto la última guía disponible
                                    if (data.length > 0) {
                                        let lastOptionValue = data[data.length - 1].prefijo + '-' + data[data.length - 1].numero;
                                        $('#id_awb_select').val(lastOptionValue);
                                    }

                                } else {
                                    // Si no hay guías, agregar un mensaje indicando que no hay disponibles
                                    $('#id_awb_select').append('<option value="sin guia">No hay guías disponibles</option>');
                                    $('#id_awb').val('sin guia');

                                }
                            },
                            error: function (error) {
                                console.error('Error al obtener las guías:', error);
                            }
                        });
                    }

}
function guia_master_edit_old(master) {
    let transportista = $('#transportista_ie').val();
    if (transportista) {
        $.ajax({
            url: '/obtener-guias/' + transportista + '/',
            method: 'GET',
            success: function(data) {
                // Limpiar las opciones actuales del select
                $('#id_awb_select_e').empty();

                if (data.length > 0) {
                    // Si hay guías disponibles, agregar las opciones
                    data.forEach(function(item) {
                        let optionText = item.prefijo + '-' + item.numero;

                        // Agregar cada opción al select
                        $('#id_awb_select_e').append('<option value="' + optionText + '">' + optionText + '</option>');
                    });
                /*    if (data.length > 0) {
                        let lastOptionValue = data[data.length - 1].prefijo + '-' + data[data.length - 1].numero;
                    }
                */
                } else {
                    // Si no hay guías, agregar un mensaje indicando que no hay disponibles
                    $('#id_awb_select_e').append('<option value="sin guia">No hay guías disponibles</option>');
                    $('#awd_e').val('sin guia');

                }
            },
            error: function(error) {
                console.error('Error al obtener las guías:', error);
            }
        });
        $('#id_awb_select_e').val(master);
    }


}
function guia_master_edit(master) {

                    let transportista = $('#transportista_ie').val();
                    if (transportista) {
                        $.ajax({
                            url: '/obtener-guias/' + transportista + '/',
                            method: 'GET',
                            success: function (data) {
                                $('#id_awb_select_e').empty();

                                // 👉 Agregar manualmente la guía actual (aunque no esté disponible)
                                if (master && master !== '') {
                                    $('#id_awb_select_e').append(
                                        $('<option>', {
                                            value: master,
                                            text: master + ' (asignada)',
                                            selected: true
                                        })
                                    );
                                }

                                // 👉 Agregar las guías disponibles
                                data.forEach(function (item) {
                                    let optionText = item.prefijo + '-' + item.numero;

                                    // Evitar duplicar si justo coincide con la asignada
                                    if (optionText !== master) {
                                        $('#id_awb_select_e').append(
                                            $('<option>', {
                                                value: optionText,
                                                text: optionText
                                            })
                                        );
                                    }
                                });
                            },
                            error: function (error) {
                                console.error('Error al obtener las guías:', error);
                            }
                        });
                    }

}



//acumulables
function acumulados(master, callback) {
    let peso = 0, volumen = 0,bultos=0;
    let volumen_aux;

    $.ajax({
        url: '/exportacion_aerea/source_embarque_aereo_full/' + master + '/',
        method: 'GET',
        success: function(response) {
                let cant = response.recordsFiltered;
            if (response.data && response.data.length > 0) {

                response.data.forEach(function(item) {
                    peso += item.bruto ? parseFloat(item.bruto) : 0;
                    if (item.medidas && item.medidas.includes('*')) {
                        let medidasArray = item.medidas.split('*');
                        volumen_aux = medidasArray.reduce((total, num) => total * parseFloat(num), 1);
                    }else{
                    volumen_aux=0;
                    }
                    volumen += volumen_aux ? parseFloat(volumen_aux) : 0;
                    bultos += item.bultos ? parseInt(item.bultos) : 0;

                });

                // Llamada al callback con los resultados
                callback({ 'volumen': volumen.toFixed(2), 'peso': peso.toFixed(2), 'cantidad': cant, 'bultos': bultos });

            } else {
                console.log("No se encontraron datos.");
                // Callback con valores por defecto
                callback({ 'volumen': 0, 'peso': 0, 'cantidad': cant,'bultos':0 });

            }
        },
        error: function(error) {
            console.error('Error al obtener las guías:', error);
        }
    });
}

//notas
function notas_house() {
let tabla = localStorage.getItem('tabla_origen');
        let selectedRowN,url;

        if (tabla.includes('tabla_house_directo')){
         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';
        }else{
         selectedRowN= localStorage.getItem('id_master_editar');
         url='master-detail/';
        }

            $.ajax({
            url: '/exportacion_aerea/'+url,
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    let selectedRowN = localStorage.getItem('num_house_gasto');
                    const wHeight = $(window).height();
                    const wWidth = $(window).width();
                    $("#notas_modal").dialog({
                        autoOpen: true,
                        open: function (event, ui) {
                            cargar_notas(selectedRowN);
                        },
                        modal: true,
                        title: "Notas para el House N°: " + selectedRowN,
                        height: wHeight * 0.90,
                        width: wWidth * 0.70,
                        class: 'modal fade',
                        buttons: [
                            {
                                text: "Cancelar",
                                class: "btn btn-dark",
                                style: "width:100px",
                                click: function () {
                                    $(this).dialog("close");
                                }
                            }
                        ],
                        beforeClose: function (event, ui) {
                            try {
                                desbloquearDatos();
                            } catch (error) {
                                console.error("⚠️ Error en desbloquearDatos:", error);
                            }
                            $('#notas_table').DataTable().destroy();
                            $("#notas_form").trigger("reset");
//                 $('#table_add_ea tbody tr').removeClass('table-secondary');
//                $('#table_edit_ea tbody tr').removeClass('table-secondary');
//                $('#tabla_house_directo_ea tbody tr').removeClass('table-secondary');
                        }
                    })
                }
            });
}
function cargar_notas(numero) {
    $('#notas_table').DataTable({
        destroy: true,  // Asegura que se destruya cualquier instancia anterior
        ajax: {
            url: `/exportacion_aerea/source/?numero=${numero}`,  // URL de la vista source
            dataSrc: 'data'
        },
        columns: [
            { data: 'id','visible':false },

            { data: 'fecha' },
            { data: 'asunto' },
            { data: 'tipo' },
            {
                data: null,
                render: function(data, type, row) {
                    return `
                        <button class="btn btn-danger" onclick="eliminarNota(${row.id})">Eliminar</button>
                    `;
                }
            }
        ],
        rowCallback: function(row, data) {
            // Configura el evento de doble clic para cada fila
            $(row).off('dblclick').on('dblclick', function() {

                $("#notas_add_input").val(data.notas);          // ID del registro
                $("#id_fecha_notas").val(formatDateToYYYYMMDD(data.fecha));
                $("#id_nota").val(data.id);      // Notas
                $("#id_asunto").val(data.asunto);    // Asunto
                $("#id_tipo_notas").val(data.tipo);        // Tipo
                $("#guardar_nota").html('Modificar');  // Cambia el botón de guardar a "Modificar"
            });
                $(row).off('click').on('click', function () {
                $('#notas_table tbody tr').removeClass('table-secondary');
                $(this).addClass('table-secondary');
            });

        }
    });
}
function cancelar_nota() {
    const form = document.getElementById('notas_form');
    form.reset(); // limpia los campos
    document.getElementById('id_nota').value = ''; // limpia id oculto
    document.getElementById('guardar_nota').innerHTML = 'Agregar Nota'; // reinicia texto del botón

}
function agregar_nota(event) {
    event.preventDefault();

    // Convierte los datos del formulario en un JSON estructurado
    let formDataArray = $("#notas_form").serializeArray();
    let formData = {};
    formDataArray.forEach(item => {
        formData[item.name] = item.value;
    });

    let numero = localStorage.getItem('num_house_gasto');
    formData.numero = numero;

    // Verifica si estamos editando una nota existente
    const idNota = $("#id_nota").val();
    const url = "/exportacion_aerea/guardar_notas/";

    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify(formData),
        contentType: "application/json",
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function(response) {
            if (response.resultado === 'exito') {
            $("#guardar_nota").html('Agregar');
                alert("Notas guardadas exitosamente");
                //$("#notas_modal").dialog("close");
                $('#notas_table').DataTable().ajax.reload();
                $("#notas_form")[0].reset();  // Limpia el formulario después de guardar
                $("#id_nota").val('');  // Restablece el campo oculto para futuras creaciones
                        if ($.fn.DataTable.isDataTable('#table_add_ea')) {
                            $('#table_add_ea').DataTable().ajax.reload(null, false);
                        }

                        if ($.fn.DataTable.isDataTable('#table_edit_ea')) {
                            $('#table_edit_ea').DataTable().ajax.reload(null, false);
                        }
                        if ($.fn.DataTable.isDataTable('#tabla_house_directo_ea')) {
                            $('#tabla_house_directo_ea').DataTable().ajax.reload(null, false);
                        }
            } else {
                alert("Error al guardar las notas: " + response.errores);
            }
        },
        error: function() {
            alert("Error en la solicitud");
        }
    });
}
function eliminarNota(id) {
    if (confirm("¿Desea eliminar esta nota?")) {
        $.ajax({
            type: "POST",
            url: `/exportacion_aerea/eliminar_nota/`,
            data: {
                id: id,  // Corrige la clave `íd` a `id`
                csrfmiddlewaretoken: csrf_token  // Asegúrate de incluir el token CSRF
            },
            success: function(response) {
                if (response.resultado === 'exito') {
                    alert("Nota eliminada exitosamente");
                    $('#notas_table').DataTable().ajax.reload();
                        if ($.fn.DataTable.isDataTable('#table_add_ea')) {
                            $('#table_add_ea').DataTable().ajax.reload(null, false);
                        }

                        if ($.fn.DataTable.isDataTable('#table_edit_ea')) {
                            $('#table_edit_ea').DataTable().ajax.reload(null, false);
                        }
                        if ($.fn.DataTable.isDataTable('#tabla_house_directo_ea')) {
                            $('#tabla_house_directo_ea').DataTable().ajax.reload(null, false);
                        }
                } else {
                    alert("Error al eliminar la nota");
                }
            },
            error: function() {
                alert("Error en la solicitud");
            }
        });
    }
}

//facturacion preventa
function cargar_gastos_factura(callback){
let tabla = localStorage.getItem('tabla_origen');
        let selectedRowN,url;

        if (tabla.includes('tabla_house_directo')){
         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';
        }else{
         selectedRowN= localStorage.getItem('id_master_editar');
         url='master-detail/';
        }

            $.ajax({
            url: '/exportacion_aerea/'+url,
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    let numero = localStorage.getItem('num_house_gasto');

                    $("#facturar_table").dataTable().fnDestroy();
                    let tabla_factura = $('#facturar_table').DataTable({
                        info: false,        // Oculta "Mostrando X a Y de Z registros"
                        lengthChange: false,
                        "order": [[1, "desc"], [1, "desc"]],
                        "processing": true,
                        "serverSide": true,
                        "pageLength": 10,
                        "language": {
                            url: "/static/datatables/es_ES.json"
                        },
                        "ajax": {
                            "url": "/exportacion_aerea/source_gastos_house_preventa/",
                            'type': 'GET',
                            "data": function (d) {
                                return $.extend({}, d, {
                                    "numero": numero,
                                });
                            }
                        },
                        "columns": [
                            {
                                "data": null,
                                "orderable": false,
                                "className": 'dt-body-center',
                                "render": function (data, type, row) {
                                    const color = row[17]; // el valor que usas para determinar el color
                                    if (color === 'ROJO' || color === 'AMARILLO' || color === 'VERDE') {
                                        return ''; // no muestra checkbox
                                    }
                                    return `<input type="checkbox" class="fila-check" value="${row[0]}">`;
                                }
                            },
                            {
                                "data": 1,    // Concepto - `data[1]`
                                "title": "Concepto"
                            },
                            {
                                "data": 6,    // Tipo - `data[6]`
                                "title": "Tipo"
                            },
                            {
                                "data": null,
                                "title": "Cantidad",
                                "render": function (data, type, row) {
                                    let precio = parseFloat(row[3]) || 0;
                                    let costo = parseFloat(row[4]) || 0;

                                    if (precio !== 0) {
                                        return precio.toFixed(2);
                                    } else if (costo !== 0) {
                                        return costo.toFixed(2);
                                    } else {
                                        return "0.00"; // o "S/I" si preferís
                                    }
                                }
                            },
                            {
                                "data": null, // Facturar a.. - Valor de relleno "S/I"
                                "title": "Facturar a..",
                                "render": function () {
                                    return "S/I";
                                }
                            },
                            {
                                "data": 2,    // Moneda - `data[2]`
                                "title": "Moneda"
                            },
                            {
                                "data": 8,    // Arbitraje - `data[8]`
                                "title": "Arbitraje"
                            },
                            {
                                "data": 5,
                                "title": "Detalle",
                                'visible':false,
                            },

                            {
                                "data": null,
                                'visible':false,
                                "render": function () {
                                    return 'S/I';
                                }
                            },
                            {
                                "data": 18,
                                "title": "Factura"
                            },

                        ],
                        rowCallback: function (row, data) {
                            $(row).removeClass('fila-rojo fila-amarillo fila-verde');

                            const color = data[17];
                            if (color === 'ROJO') {
                                $(row).addClass('fila-rojo');
                            } else if (color === 'AMARILLO') {
                                $(row).addClass('fila-amarillo');
                            } else if(color === 'VERDE'){
                                $(row).addClass('fila-verde');
                            }
                            // Agregar el evento de clic para resaltar la fila seleccionada
                            $(row).off('click').on('click', function () {
                                $('#facturar_table tbody tr').removeClass('table-secondary');
                                $(this).addClass('table-secondary');
                                const valorColumna7 = $(row).find('td').eq(7).text().trim();

                                if (valorColumna7 === 'S/I') {
                                    $('#concepto_detalle').prop('checked', false); // Desmarcar el checkbox
                                } else {
                                    $('#concepto_detalle').prop('checked', true); // Marcar el checkbox
                                }
                            });
                        }
                    });
                    setTimeout(function () {
                        callback();
                    }, 2000);
                }
            });
}
function sumar_ingresos() {
    let totalIngresos = 0;
    const tabla = $('#facturar_table').DataTable();

    // Verifica si DataTable está inicializado
    if (!$.fn.DataTable.isDataTable('#facturar_table')) {
        console.log("DataTable no está inicializado.");
        return;
    }

    // Itera sobre cada fila de la tabla y suma el valor en la columna 3
    tabla.rows().every(function() {
        const data = this.data();
        console.log("Datos de la fila:", data); // Verifica el contenido de cada fila
        const valor = parseFloat(data[3]) || 0;
        totalIngresos += valor;
        console.log("Total acumulado:", totalIngresos);
    });

    // Asigna el resultado total al input con ID #total_ingresos
    $('#total_ingresos').val(totalIngresos.toFixed(2)); // Redondea a 2 decimales si es necesario
}
//autocomplete factura
$("#destinatario").autocomplete({
    source: '/autocomplete_clientes/',
    minLength: 2,
    select: function (event, ui) {
        $(this).attr('data-id', ui.item['id']);
    },
    change: function (event, ui) {
        if (ui.item) {
            $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
             $('#destinatario_input').val(ui.item['id']);
             $('#destinatario_input').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
        } else {
            $(this).val('');
            $('#destinatario_input').val('');
            $(this).css({"border-color": "", 'box-shadow': ''});
            $('#destinatario_input').css({"border-color": "", 'box-shadow': ''});
        }
    }
});

//descargar guias hijas
function descargar_hawb(){
let tabla = localStorage.getItem('tabla_origen');
        let selectedRowN,url;

        if (tabla.includes('tabla_house_directo')){
         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';
        }else{
         selectedRowN= localStorage.getItem('id_master_editar');
         url='master-detail/';
        }

            $.ajax({
            url: '/exportacion_aerea/'+url,
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    let numero_hawb = localStorage.getItem('num_house_gasto');
                    row = table.rows('.table-secondary').data();
                    if (row.length === 1) {
                        window.open('/exportacion_aerea/descargar_hawb/' + numero_hawb, '_blank');
                    } else {
                        alert('Debe seleccionar al menos un registro');
                    }
                }
            });
}
function descargar_hawb_draft(){
    let as_agreed= confirm('¿Desea guia AS AGREED?');
let tabla = localStorage.getItem('tabla_origen');
        let selectedRowN,url;

        if (tabla.includes('tabla_house_directo')){
         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';
        }else{
         selectedRowN= localStorage.getItem('id_master_editar');
         url='master-detail/';
        }

            $.ajax({
            url: '/exportacion_aerea/'+url,
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    let numero_hawb = localStorage.getItem('num_house_gasto');
                    row = table.rows('.table-secondary').data();
                    if (row.length === 1) {
                        let flag = as_agreed ? '1' : '0';
                        window.open(
                          '/exportacion_aerea/descargar_hawb_draft/' + numero_hawb + '/d/' + flag,
                          '_blank'
                        );

                    } else {
                        alert('Debe seleccionar al menos un registro');
                    }
                }
            });
}
function editar_guia() {
let tabla = localStorage.getItem('tabla_origen');
        let selectedRowN,url;

        if (tabla.includes('tabla_house_directo')){
         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';
        }else{
         selectedRowN= localStorage.getItem('id_master_editar');
         url='master-detail/';
        }

            $.ajax({
            url: '/exportacion_aerea/'+url,
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    const rowId = localStorage.getItem('num_house_gasto');
                    if (!rowId) {
                        alert("Debes seleccionar un registro.");
                        return;
                    }

                    window.location.href = `/exportacion_aerea/editar_hawb/${rowId}/`;
                }
            });
}
function guardar_hawb(row_id) {
    const form = document.getElementById('guias_hijas_form');

    // Lista de campos decimales
    const camposDecimales = [
        'total_pesos', 'total_total', 'volumen_total_embarque', 'valppd', 'valcol',
        'prepaid', 'collect', 'taxppd', 'taxcol', 'agentppd', 'agentcol',
        'carrierppd', 'carriercol', 'total_prepaid', 'total_collect'
    ];

    // Sanitizar los campos decimales
    camposDecimales.forEach(campo => {
        const input = form.querySelector(`[name="${campo}"]`);
        if (input && input.value) {
            input.value = input.value.replace(',', '.');
        }
    });

    const mercaderiaCampos = ['peso', 'tarifa', 'total', 'aplicable'];

    mercaderiaCampos.forEach(nombre => {
        const inputs = form.querySelectorAll(`[name^="${nombre}_"]`);
        inputs.forEach(input => {
            if (input.value) {
                const val = input.value.trim();

                if (nombre === 'aplicable') {
                    // Solo reemplazamos si es un número
                    if (!isNaN(val.replace(',', '.'))) {
                        input.value = val.replace(',', '.');
                    }
                } else {
                    input.value = val.replace(',', '.');
                }
            }
        });
    });


    const formData = new FormData(form);

    fetch(`/exportacion_aerea/guardar_hawb/${row_id}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("¡Guía guardada exitosamente!");
        } else {
            alert("Error al guardar: " + (data.mensaje || 'Error desconocido'));
        }
    })
    .catch(err => {
        alert("Error en la solicitud: " + err.message);
    });
}
//guias madre
function editar_guia_madre() {
     let selectedRowN = localStorage.getItem('id_master_editar');
            $.ajax({
                url: '/exportacion_aerea/master-detail/',
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    row = table.rows('.table-secondary').data();
                    if (row.length === 1) {
                        let numero_master = row[0][0];
                        window.location.href = `/exportacion_aerea/editar_awb/${numero_master}/`;
                    } else {
                        alert("Debes seleccionar un registro.");
                        return;
                    }
                }
            });
}


function guardar_awb(row_id) {
    const form = document.getElementById('guias_madres_form');

    // Lista de campos decimales
    const camposDecimales = [
        'total_pesos', 'total_total', 'volumen_total_embarque', 'valppd', 'valcol',
        'prepaid', 'collect', 'taxppd', 'taxcol', 'agentppd', 'agentcol',
        'carrierppd', 'carriercol', 'total_prepaid', 'total_collect'
    ];

    // Sanitizar los campos decimales
    camposDecimales.forEach(campo => {
        const input = form.querySelector(`[name="${campo}"]`);
        if (input && input.value) {
            input.value = input.value.replace(',', '.');
        }
    });

    const mercaderiaCampos = ['peso', 'tarifa', 'total', 'aplicable'];

    mercaderiaCampos.forEach(nombre => {
        const inputs = form.querySelectorAll(`[name^="${nombre}_"]`);
        inputs.forEach(input => {
            if (input.value) {
                const val = input.value.trim();

                if (nombre === 'aplicable') {
                    // Solo reemplazamos si es un número
                    if (!isNaN(val.replace(',', '.'))) {
                        input.value = val.replace(',', '.');
                    }
                } else {
                    input.value = val.replace(',', '.');
                }
            }
        });
    });


    const formData = new FormData(form);


    fetch(`/exportacion_aerea/guardar_awb/${row_id}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("¡Guía guardada exitosamente!");
        } else {
            alert("Error al guardar: " + (data.mensaje || 'Error desconocido'));
        }
    })
    .catch(err => {
        alert("Error en la solicitud: " + err.message);
    });
}

//modal para buscar
function modal_buscar(){
$("#searchModal").dialog({
        autoOpen: true,
        modal: true,
        width: 400,
        buttons: [
            {
                text: "Buscar",
                class: "btn btn-success",
                click: function(e) {
                    let formData = $("#searchForm").serialize();
                    filtrar_tabla_master(formData,e);
                    $(this).dialog("close");
                }
            },
            {
                text: "Cerrar",
                class: "btn btn-dark",
                click: function() {
                    $(this).dialog("close");
                }
            }
        ]
    });
    $("#origen").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                //$(this).val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
}
function filtrar_tabla_master(data, e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: '/exportacion_aerea/buscar_registros/',
        data: $("#searchForm").serialize(),
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function(response) {
            let awbList = response.resultados;
            // if (awbList && awbList.length > 0) {
            //     // Eliminar duplicados y construir la regex
            //     let uniqueAwbs = [...new Set(awbList)];
            //     awbRegex = uniqueAwbs.map(function(item) {
            //         return '.*' + $.trim(item) + '.*';
            //     }).join('|');
            //     awbRegex=uniqueAwbs;
            // } else {
            //     awbRegex = "";
            // }
            // Recargar la tabla para enviar el nuevo parámetro al servidor
            table.ajax.reload();
        },
        error: function(xhr, status, error) {
            console.error("Error al obtener AWB:", error);
        }
    });
}

//acumulados comprobacion:
function validarCoincidenciaAcumulados() {
    const kilosMadre = parseFloat(document.getElementById("id_kilos_e").value) || 0;
    const pesoAcumulado = parseFloat(document.getElementById("peso_acumulados").value) || 0;


    const difPeso = Math.abs(kilosMadre - pesoAcumulado);

    if (difPeso > 0.01) {
        alert("⚠️ Los valores ingresados en el máster no coinciden con los acumulados de los hijos.\n\n" +
              `Peso máster: ${kilosMadre.toFixed(2)} / Acumulado: ${pesoAcumulado.toFixed(2)}\n` );
        return false;
    }

    return true;
}

//mails
function abrir_modal_mails(e){
    e.preventDefault();

    let row = table_edit_ea.rows('.table-secondary').data();
    if (row.length !== 1) {
        alert('Debe seleccionar un embarque primero.');
        return;
    }

    $("#modalSeleccionEmailHouse5").dialog('open');
}

//mostrar logs
function get_datos_logs() {
let tabla = localStorage.getItem('tabla_origen');
        let selectedRowN,url;

        if (tabla.includes('tabla_house_directo')){
         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';
        }else{
         selectedRowN= localStorage.getItem('id_master_editar');
         url='master-detail/';
        }

            $.ajax({
            url: '/exportacion_aerea/'+url,
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    row = table_edit_ea.rows('.table-secondary').data();
                    if (row.length === 1) {
                        $("#logs_modal").dialog({
                            autoOpen: true,
                            open: function () {

                            },
                            modal: true,
                            title: "Log de interacciones para en el embarque N°: " + row[0][3],
                            height: wHeight * 0.90,
                            width: wWidth * 0.90,
                            class: 'modal fade',
                            buttons: [{
                                text: "Salir",
                                class: "btn btn-dark",
                                style: "width:100px",
                                click: function () {
                                    $(this).dialog("close");
                                },
                            },],
                            beforeClose: function (event, ui) {

                            }
                        });
                        $("#tabla_logs").dataTable().fnDestroy();
                        table_logs = $('#tabla_logs').DataTable({
                            "order": [[2, "desc"], [1, "desc"]],
                            "columnDefs": [
                                {
                                    "targets": [0],
                                    "orderable": false,
                                },
                            ],
                            "processing": true,
                            "serverSide": true,
                            "dom": 'Btlipr',
                            "scrollX": true,
                            "pageLength": 100,
                            "language": {
                                url: "/static/datatables/es_ES.json"
                            },
                            "ajax": {
                                "url": "/exportacion_aerea/source_logs/",
                                'type': 'GET',
                                "data": function (d) {
                                    return $.extend({}, d, {
                                        "id": row[0][0], 'numero': row[0][3]
                                    });
                                }
                            },
                            "rowCallback": function (row, data, index) {
                                // data[3] es la columna 'Acción' => Created / Updated / Deleted
                                var accion = data[3].toLowerCase();

                                // Limpiar clases anteriores
                                $(row).removeClass('table-success table-warning table-danger');

                                if (accion === 'create') {
                                    $(row).addClass('table-success');
                                } else if (accion === 'update') {
                                    $(row).addClass('table-warning');
                                } else if (accion === 'delete') {
                                    $(row).addClass('table-danger');
                                }
                            }
                        });
                    } else {
                        alert('Debe seleccionar al menos un registro');
                    }
                }
            });
}