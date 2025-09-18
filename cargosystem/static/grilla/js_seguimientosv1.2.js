// INICIO CONTROL PAGINA
var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;
// FIN CONTROL PAGINA

// INICIO TABLAS
var table = false;
var table_envases = false;
var table_logs = false;
var table_embarques = false;
var table_gastos = false;
var table_archivos = false;
var row_selected = 0;
var row_selected_envase = 0;
var row_selected_embarque = 0;
var row_selected_archivo = 0;
var row_selected_ruta = 0;
// var row_number = 0;
var row_id = 0;
var row_number_embarque = 0;
var row_number_archivo = 0;
var row_number_envase = 0;
var row_number_ruta = 0;
var nombre_form = 'Nuevo'
// FIN TABLAS

// INICIO GASTOS
var ingresos = 0;
var egresos = 0;
var diferencia = 0;
// FIN GASTOS

// DATOS
var tipo_seguimiento = '';
var archivos_adjuntos = {};
var buscar = '';
var que_buscar = '';
// FIN DATOS


$(document).ready(function () {


    setTimeout(function () {
        $('.navbar-collapse').collapse('hide');
    }, 5000);

    getCookie('row_selected_seguimiento');
    var contador = 0;
    /* DATATABLES */
    $('#tabla_seguimiento tfoot th').each(function (index) {
        let title = $('#tabla_seguimiento thead th').eq(index).text();

        if (index === 0) {
            // Si es la primera columna, colocar el botón de limpiar filtros
            $(this).html('<button class="btn btn-danger" title="Borrar filtros" id="clear"><span class="glyphicon glyphicon-erase"></span> Limpiar</button>');
        } else if (title !== '') {
            // Agregar inputs de búsqueda en las demás columnas
            $(this).html('<input type="text" class="form-control filter-input" autocomplete="off" id="buscoid_' + index + '" placeholder="Buscar ' + title + '" />');
        }
    });
    table = $('#tabla_seguimiento').DataTable({
        "stateSave": true,
        "dom": 'Btlipr',
        "scrollX": true,
        "bAutoWidth": false,
        "scrollY": wHeight * 0.60,
        "columnDefs": [
            {
                "targets": [0], //boton de mas
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": '',
                render: function (data, type, row) {

                }
            },
            {
                "targets": [1], //numero
                "className": 'derecha archivos',
            },
            {
                "targets": [2], //modo

            },
            {
                "targets": [3],
                "render": function (data, type, row, meta) {
                    return row[56]; // Toma el índice 5 para la columna 6
                }
            },
            {
                "targets": [4],
                "render": function (data, type, row, meta) {
                    return row[55]; // Toma el índice 5 para la columna 6
                }
            },
            {
                "targets": [5],
                "render": function (data, type, row, meta) {
                    return row[57]; // Toma el índice 5 para la columna 6
                }
            },
            {
                "targets": [6],
                "render": function (data, type, row, meta) {
                    return row[25]; // Toma el índice 5 para la columna 6
                }
            },
            {
                "targets": [7],
                "render": function (data, type, row, meta) {
                    return row[26]; // Toma el índice 5 para la columna 6
                }
            },
            {
                "targets": [8],
                "render": function (data, type, row, meta) {
                    return row[10]; // Toma el índice 5 para la columna 6
                }
            },
            {
                "targets": [9],
                "render": function (data, type, row, meta) {
                    return row[11]; // Toma el índice 5 para la columna 6
                }
            },
            {
                "targets": [10],
                "render": function (data, type, row, meta) {
                    return row[4]; // Toma el índice 5 para la columna 6
                }
            },
            {
                "targets": [11],
                "render": function (data, type, row, meta) {
                    return row[5]; // Toma el índice 5 para la columna 6
                }
            },
            {
                "targets": [12],
                "render": function (data, type, row, meta) {
                    return row[31]; // Toma el índice 5 para la columna 6
                }
            },
        ],
        "order": [[1, "desc"],],
        "processing": true,
        "serverSide": true,
        "pageLength": 100,
        "ajax": {
            "url": "/source_seguimientos",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "buscar": buscar,
                    "que_buscar": que_buscar,
                });
            }
        },
        "language": {
            url: "/static/datatables/es_ES.json"
        },
        initComplete: function () {
            let api = this.api();

            // Cargar estado guardado
            let state = table.state.loaded();
            if (state) {
                // Restaurar filtros en los inputs y aplicar clase si tienen valor
                api.columns().every(function (index) {
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
            $(document).on("input", ".filter-input", function () {
                if ($(this).val().trim() !== "") {
                    $(this).addClass("is-invalid"); // Se pone en rojo
                } else {
                    $(this).removeClass("is-invalid"); // Se quita el rojo si se vacía
                }
            });

            // Agregar funcionalidad de filtrado
            api.columns().every(function () {
                let that = this;
                $('input', this.footer()).on('keyup change', function () {
                    if (that.search() !== this.value) {
                        that.search(this.value).draw();
                    }
                });
            });
        },
        "rowCallback": function (row, data) {
            $('td:eq(1)', row).html('');
            let texto = ''
            if (data[8].length > 0 && data[8] !== 'S/I') {
                //notas
                texto += '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-sticky" viewBox="0 0 16 16">\n' +
                    '<path d="M2.5 1A1.5 1.5 0 0 0 1 2.5v11A1.5 1.5 0 0 0 2.5 15h6.086a1.5 1.5 0 0 0 1.06-.44l4.915-4.914A1.5 1.5 0 0 0 15 8.586V2.5A1.5 1.5 0 0 0 13.5 1zM2 2.5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 .5.5V8H9.5A1.5 1.5 0 0 0 8 9.5V14H2.5a.5.5 0 0 1-.5-.5zm7 11.293V9.5a.5.5 0 0 1 .5-.5h4.293z"/>\n' +
                    '</svg>';

            }
            if (data[44] > 0) {
                //archivo
                texto += ' <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-filetype-docx" viewBox="0 0 16 16"' +
                    '><path fill-rule="evenodd" d="M14 4.5V11h-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5L14 4.5Zm-6.839 9.688v-.522a1.54 1.54 0 0 0-.117-.641.861.861 0 0 0-.322-.387.862.862 0 0 0-.469-.129.868.868 0 0 0-.471.13.868.868 0 0 0-.32.386 1.54 1.54 0 0 0-.117.641v.522c0 .256.04.47.117.641a.868.868 0 0 0 .32.387.883.883 0 0 0 .471.126.877.877 0 0 0 .469-.126.861.861 0 0 0 .322-.386 1.55 1.55 0 0 0 .117-.642Zm.803-.516v.513c0 .375-.068.7-.205.973a1.47 1.47 0 0 1-.589.627c-.254.144-.56.216-.917.216a1.86 1.86 0 0 1-.92-.216 1.463 1.463 0 0 1-.589-.627 2.151 2.151 0 0 1-.205-.973v-.513c0-.379.069-.704.205-.975.137-.274.333-.483.59-.627.257-.147.564-.22.92-.22.357 0 .662.073.916.22.256.146.452.356.59.63.136.271.204.595.204.972ZM1 15.925v-3.999h1.459c.406 0 .741.078 1.005.235.264.156.46.382.589.68.13.296.196.655.196 1.074 0 .422-.065.784-.196 1.084-.131.301-.33.53-.595.689-.264.158-.597.237-.999.237H1Zm1.354-3.354H1.79v2.707h.563c.185 0 .346-.028.483-.082a.8.8 0 0 0 .334-.252c.088-.114.153-.254.196-.422a2.3 2.3 0 0 0 .068-.592c0-.3-.04-.552-.118-.753a.89.89 0 0 0-.354-.454c-.158-.102-.361-.152-.61-.152Zm6.756 1.116c0-.248.034-.46.103-.633a.868.868 0 0 1 .301-.398.814.814 0 0 1 .475-.138c.15 0 .283.032.398.097a.7.7 0 0 1 .273.26.85.85 0 0 1 .12.381h.765v-.073a1.33 1.33 0 0 0-.466-.964 1.44 1.44 0 0 0-.49-.272 1.836 1.836 0 0 0-.606-.097c-.355 0-.66.074-.911.223-.25.148-.44.359-.571.633-.131.273-.197.6-.197.978v.498c0 .379.065.704.194.976.13.271.321.48.571.627.25.144.555.216.914.216.293 0 .555-.054.785-.164.23-.11.414-.26.551-.454a1.27 1.27 0 0 0 .226-.674v-.076h-.765a.8.8 0 0 1-.117.364.699.699 0 0 1-.273.248.874.874 0 0 1-.401.088.845.845 0 0 1-.478-.131.834.834 0 0 1-.298-.393 1.7 1.7 0 0 1-.103-.627v-.495Zm5.092-1.76h.894l-1.275 2.006 1.254 1.992h-.908l-.85-1.415h-.035l-.852 1.415h-.862l1.24-2.015-1.228-1.984h.932l.832 1.439h.035l.823-1.439Z"' +
                    '/></svg>';
            }
            if (data[45] > 0) {
                //embarque
                texto += '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-truck" viewBox="0 0 16 16">\n' +
                    '<path d="M0 3.5A1.5 1.5 0 0 1 1.5 2h9A1.5 1.5 0 0 1 12 3.5V5h1.02a1.5 1.5 0 0 1 1.17.563l1.481 1.85a1.5 1.5 0 0 1 .329.938V10.5a1.5 1.5 0 0 1-1.5 1.5H14a2 2 0 1 1-4 0H5a2 2 0 1 1-3.998-.085A1.5 1.5 0 0 1 0 10.5zm1.294 7.456A2 2 0 0 1 4.732 11h5.536a2 2 0 0 1 .732-.732V3.5a.5.5 0 0 0-.5-.5h-9a.5.5 0 0 0-.5.5v7a.5.5 0 0 0 .294.456M12 10a2 2 0 0 1 1.732 1h.768a.5.5 0 0 0 .5-.5V8.35a.5.5 0 0 0-.11-.312l-1.48-1.85A.5.5 0 0 0 13.02 6H12zm-9 1a1 1 0 1 0 0 2 1 1 0 0 0 0-2m9 0a1 1 0 1 0 0 2 1 1 0 0 0 0-2"/>\n' +
                    '</svg>';


            }
            if (data[46] > 0) {
                //envase
                texto += ' <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-box-seam" viewBox="0 0 16 16"' +
                    '><path d="M8.186 1.113a.5.5 0 0 0-.372 0L1.846 3.5l2.404.961L10.404 2l-2.218-.887zm3.564 1.426L5.596 5 8 5.961 14.154 3.5l-2.404-.' +
                    '961zm3.25 1.7-6.5 2.6v7.922l6.5-2.6V4.24zM7.5 14.762V6.838L1 4.239v7.923l6.5 2.6zM7.443.184a1.5 1.5 0 0 1 1.114 0l7.129 2.852A.5.5 0 0 1 16' +
                    ' 3.5v8.662a1 1 0 0 1-.629.928l-7.185 2.874a.5.5 0 0 1-.372 0L.63 13.09a1 1 0 0 1-.63-.928V3.5a.5.5 0 0 1 .314-.464L7.443.184z"/> </svg>';
            }
            if (data[47] > 0) {
                //gastos
                texto += '   <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-currency-dollar" viewBox="0 0 16 16"' +
                    '><path d="M4 10.781c.148 1.667 1.513 2.85 3.591 3.003V15h1.043v-1.216c2.27-.179 3.678-1.438 3.678-3.3 0-1.59-.947-2.51-2.956-3.028l-.722-.18' +
                    '7V3.467c1.122.11 1.879.714 2.07 1.616h1.47c-.166-1.6-1.54-2.748-3.54-2.875V1H7.591v1.233c-1.939.23-3.27 1.472-3.27 3.156 0 1.454.966 2.483 2.' +
                    '661 2.917l.61.162v4.031c-1.149-.17-1.94-.8-2.131-1.718H4zm3.391-3.836c-1.043-.263-1.6-.825-1.6-1.616 0-.944.704-1.641 1.8-1.828v3.495l-.2-.05z' +
                    'm1.591 1.872c1.287.323 1.852.859 1.852 1.769 0 1.097-.826 1.828-2.2 1.939V8.73l.348.086z"/>sss</svg>';
            }
            if (data[48]) {
                texto += ' <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-calendar3" viewBox="0 0 16 16"' +
                    '><path d="M14 0H2a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2zM1 3.857C1 3.384 1.448 3 2 3h12c.552 0 1 .384 1 .' +
                    '857v10.286c0 .473-.448.857-1 .857H2c-.552 0-1-.384-1-.857V3.857z"/><path d="M6.5 7a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 ' +
                    '0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm-9 3a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 ' +
                    '0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm-9 3a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm3 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/></svg>';
            }
            if (data[51]) {
                //historial
                texto += '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-clock-history" viewBox="0 0 16 16">\n' +
                    '<path d="M8.515 1.019A7 7 0 0 0 8 1V0a8 8 0 0 1 .589.022zm2.004.45a7 7 0 0 0-.985-.299l.219-.976q.576.129 1.126.342zm1.37.71a7 7 0 0 0-.439-.27l.493-.87a8 8 0 0 1 .979.654l-.615.789a7 7 0 0 0-.418-.302zm1.834 1.79a7 7 0 0 0-.653-.796l.724-.69q.406.429.747.91zm.744 1.352a7 7 0 0 0-.214-.468l.893-.45a8 8 0 0 1 .45 1.088l-.95.313a7 7 0 0 0-.179-.483m.53 2.507a7 7 0 0 0-.1-1.025l.985-.17q.1.58.116 1.17zm-.131 1.538q.05-.254.081-.51l.993.123a8 8 0 0 1-.23 1.155l-.964-.267q.069-.247.12-.501m-.952 2.379q.276-.436.486-.908l.914.405q-.24.54-.555 1.038zm-.964 1.205q.183-.183.35-.378l.758.653a8 8 0 0 1-.401.432z"/>\n' +
                    '<path d="M8 1a7 7 0 1 0 4.95 11.95l.707.707A8.001 8.001 0 1 1 8 0z"/>\n' +
                    '<path d="M7.5 3a.5.5 0 0 1 .5.5v5.21l3.248 1.856a.5.5 0 0 1-.496.868l-3.5-2A.5.5 0 0 1 7 9V3.5a.5.5 0 0 1 .5-.5"/>\n' +
                    '</svg>';

            }
            if (data[49]) {
                //rutas
                texto += '   <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-geo-alt" viewBox="0 0 16 16">\n' +
                    '<path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"/>\n' +
                    '<path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>\n' +
                    '</svg>';
            }
            if (data[52] > 0) {
                //notas
                texto += '   <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-sticky" viewBox="0 0 16 16">\n' +
                    '<path d="M2.5 1A1.5 1.5 0 0 0 1 2.5v11A1.5 1.5 0 0 0 2.5 15h6.086a1.5 1.5 0 0 0 1.06-.44l4.915-4.914A1.5 1.5 0 0 0 15 8.586V2.5A1.5 1.5 0 0 0 13.5 1zM2 2.5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 .5.5V8H9.5A1.5 1.5 0 0 0 8 9.5V14H2.5a.5.5 0 0 1-.5-.5zm7 11.293V9.5a.5.5 0 0 1 .5-.5h4.293z"/>\n' +
                    '</svg>';

            }
            if (data[53]) {
                //aplicable
                texto += ' <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-coin" viewBox="0 0 16 16">\n' +
                    '                      <path d="M5.5 9.511c.076.954.83 1.697 2.182 1.785V12h.6v-.709c1.4-.098 2.218-.846 2.218-1.932 0-.987-.626-1.496-1.745-1.76l-.473-.112V5.57c.6.068.982.396 1.074.85h1.052c-.076-.919-.864-1.638-2.126-1.716V4h-.6v.719c-1.195.117-2.01.836-2.01 1.853 0 .9.606 1.472 1.613 1.707l.397.098v2.034c-.615-.093-1.022-.43-1.114-.9zm2.177-2.166c-.59-.137-.91-.416-.91-.836 0-.47.345-.822.915-.925v1.76h-.005zm.692 1.193c.717.166 1.048.435 1.048.91 0 .542-.412.914-1.135.982V8.518z"/>\n' +
                    '                      <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16"/>\n' +
                    '                      <path d="M8 13.5a5.5 5.5 0 1 1 0-11 5.5 5.5 0 0 1 0 11m0 .5A6 6 0 1 0 8 2a6 6 0 0 0 0 12"/>\n' +
                    '                    </svg>';

            }
            $('td:eq(1)', row).html(texto + " " + data[1] + " ");
            if (data[0] === row_selected) {
                window.row_number = data[1];
                row_id = data[0];
                $(row).addClass('table-secondary');
            }
        },
    });
    $('#tabla_seguimiento tbody').on('dblclick', 'tr', function () {
        // Remover selección previa y marcar esta fila como seleccionada
        $('#tabla_seguimiento tbody tr').removeClass('table-secondary');
        $(this).addClass('table-secondary');
        // Ejecutar la misma lógica que el botón Editar
        $('#editar_btn').trigger('click');
    });
    $('input.autocomplete').on('keydown', function (event) {
        var keyCode = event.keyCode || event.which;

        if (keyCode === 13 || keyCode === 9) { // 'Enter' (13) o 'Tab' (9)
            var activeItem = $(".ui-menu-item:hover");
            if (activeItem.length > 0) {
                var selectedValue = activeItem.find("a").text();
                $(this).val(selectedValue);  // Establece el valor automáticamente
            }
        }
    });
    // Evento para limpiar todos los filtros
    $(document).on("click", "#clear", function () {
        awbRegex = '';
        $(".filter-input").val("").trigger("keyup"); // Limpia los inputs y activa la búsqueda
        $(".filter-input").removeClass("is-invalid"); // Se quita el rojo si se vacía
        table.ajax.reload();
    });
    // Evento para resaltar los inputs cuando tienen contenido
    $(document).on("input", ".filter-input", function () {
        if ($(this).val().trim() !== "") {
            $(this).addClass("is-invalid"); // Se pone en rojo
        } else {
            $(this).removeClass("is-invalid"); // Se quita el rojo si se vacía
        }
    });

    $('#tabla_seguimiento tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        if (row.child.isShown()) {
            row.child.hide();
            tr.removeClass('shown');
        } else {
            table.row(".shown").child.hide();
            $("#tabla_seguimiento tr").removeClass("shown");
            if (row.child.isShown()) {
            } else {
                console.log(row.data());
                row.child(format(row.data()), 'addinfowrapper').show();
                tr.addClass('shown');
            }
        }
    });
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
    var state = table.state.loaded();
    $('#id_medidas, #id_bultos_embarque').on('change', function () {
        let m = $('#id_medidas').val(); // Valor del primer input
        let b = $('#id_bultos_embarque').val(); // Valor del segundo input

        let resultado = calcular_volumen(m, b)
        $('#id_cbm').val(resultado); // Mostrar resultado en el div
    });

    $('#tabla_seguimiento tbody').on('click', 'tr', function () {
        if ($(this).hasClass('table-secondary')) {
            $(this).removeClass('table-secondary');
        } else {
            var row = table.row($(this).closest('tr')).data();
            row_selected = row[0];
            window.row_number = row[1];
            setCookie(row_selected);
            table.$('tr.table-secondary').removeClass('table-secondary');
            localStorage.setItem('id_seguimiento_seleccionado', row[0]);
            $(this).addClass('table-secondary');
        }
    });
    $('#tabla_envases tbody').on('click', 'tr', function () {
        if ($(this).hasClass('table-secondary')) {
            $(this).removeClass('table-secondary');
        } else {
            var row = table_envases.row($(this).closest('tr')).data();
            row_selected_envase = row[0];
            row_number_envase = row[1];
            table_envases.$('tr.table-secondary').removeClass('table-secondary');
            $(this).addClass('table-secondary');
        }
    });
    $('#tabla_embarques tbody').on('click', 'tr', function () {
        if ($(this).hasClass('table-secondary')) {
            $(this).removeClass('table-secondary');
        } else {
            var row = table_embarques.row($(this).closest('tr')).data();
            row_selected_embarque = row[0];
            row_number_embarque = row[1];
            table_embarques.$('tr.table-secondary').removeClass('table-secondary');
            $(this).addClass('table-secondary');
        }
    });
    $('#tabla_archivos tbody').on('click', 'tr', function () {
        if ($(this).hasClass('table-secondary')) {
            $(this).removeClass('table-secondary');
        } else {
            var row = table_archivos.row($(this).closest('tr')).data();
            row_selected_archivo = row[0];
            row_number_archivo = row[1];
            table_archivos.$('tr.table-secondary').removeClass('table-secondary');
            $(this).addClass('table-secondary');
        }
    });
    $('#tabla_gastos tbody').on('click', 'tr', function () {
        if ($(this).hasClass('table-secondary')) {
            $(this).removeClass('table-secondary');
        } else {
            var row = table_gastos.row($(this).closest('tr')).data();
            row_selected_gasto = row[0];
            row_number_archivo = row[1];
            table_gastos.$('tr.table-secondary').removeClass('table-secondary');
            $(this).addClass('table-secondary');
        }
    });
    $('#tabla_rutas tbody').on('click', 'tr', function () {
        if ($(this).hasClass('table-secondary')) {
            $(this).removeClass('table-secondary');
        } else {
            var row = table_rutas.row($(this).closest('tr')).data();
            row_selected_ruta = row[0];
            row_number_ruta = row[1];
            table_rutas.$('tr.table-secondary').removeClass('table-secondary');
            $(this).addClass('table-secondary');
        }
    });
    /* FIN DE TABLA DATATABLES*/

    // MODALES
    $('#id_operacion').on('change', function () {
        if (this.value != '') {
            $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
        } else {
            $(this).css({"border-color": "", 'box-shadow': ''});
        }
    });
    $('#id_moneda').on('change', function () {
        if (this.value != '') {
            $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
        } else {
            $(this).css({"border-color": "", 'box-shadow': ''});
        }
    });
    $('#id_status').on('change', function () {
        if (this.value != '') {
            $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
        } else {
            $(this).css({"border-color": "", 'box-shadow': ''});
        }
    });
    $('#id_pago').on('change', function () {
        if (this.value != '') {
            $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
        } else {
            $(this).css({"border-color": "", 'box-shadow': ''});
        }
    });

    /* FUNCIONES MODALES */
    $('#ingresar_envase').click(function (event) {
        event.preventDefault();
        if (document.getElementById('id_profit').value < 0 || document.getElementById('id_volumen').value < 0 || document.getElementById('id_precio').value < 0 || document.getElementById('id_peso').value < 0 || document.getElementById('id_cantidad').value < 0 || document.getElementById('id_bonifcli').value < 0 || document.getElementById('id_bultos').value < 0 || document.getElementById('id_tara').value < 0) {
            alert('No se admiten valores negativos en los campos numéricos.')
        } else {
            if (confirm("¿Confirma guardar datos?")) {
                var form = $('#envases_form');
                var formData = new FormData(form[0]);
                if (form[0].checkValidity()) {
                    row = table.rows('.table-secondary').data();
                    let formData = $("#envases_form").serializeArray();
                    let data = JSON.stringify(formData);
                    miurl = "/guardar_envases/";
                    const numero = (window.wizardMode && window.wizCtx && window.wizCtx.numero)
                        ? window.wizCtx.numero
                        : row[0][1];
                    var toData = {
                        'numero': numero,
                        'data': data,
                        'csrfmiddlewaretoken': csrf_token,
                    };
                    $.ajax({
                        type: "POST",
                        url: miurl,
                        data: toData,
                        async: false,
                        // SUCCESS de tu AJAX de guardar envase:
                        success: function (resultado) {
                            if (resultado['resultado'] === 'exito') {

                                if (window.wizardMode) {
                                    // ✅ wizard: no cierres ni destruyas el modal; no re-abrir via botón
                                    $('#envases_form')[0].reset();
                                    mostrarToast('¡Envase guardado con éxito!', 'success');

                                    try {
                                        $('#tabla_envases').DataTable().ajax.reload(null, false);
                                    } catch (e) {
                                    }
                                    try {
                                        table.ajax.reload(null, false);
                                    } catch (e) {
                                    }

                                    // avisar al wizard y refrescar la barra (si Envases es último → se verá "Finalizar")
                                    $(document).trigger('envases:guardado');
                                    refreshCurrentToolbar();

                                } else {
                                    // 🔁 comportamiento legacy fuera del wizard (lo que ya hacías)
                                    $('#ingresar_envase').html('Agregar');
                                    $("#tabla_envases").dataTable().fnDestroy();
                                    $('#envases_btn').addClass('triggered').trigger('click'); // reabría el modal
                                    $("#id_envase_id").val && $("#id_envase_id").val('');
                                    table.ajax.reload();
                                    mostrarToast('¡Envase guardado con éxito!', 'success');
                                }

                            } else {
                                alert(resultado['resultado']);
                            }
                        }

                    });
                } else {
                    const invalidFields = form[0].querySelectorAll(':invalid'); // Selecciona los campos no válidos
                    invalidFields.forEach(field => {
                        console.log('Campo no válido:', field.name); // Muestra los campos no válidos
                    });

                    alert('Debe completar todos los campos.');
                }
            }
        }

    });
    $('#ingresar_ruta').click(function (event) {
        event.preventDefault();
        if (confirm("¿Confirma guardar datos?")) {
            var form = $('#rutas_form');
            if (form[0].checkValidity()) {
                row = table.rows('.table-secondary').data();
                let formData = $("#rutas_form").serializeArray();
                let data = JSON.stringify(formData);
                miurl = "/guardar_ruta/";
                const numero = (window.wizardMode && window.wizCtx && window.wizCtx.numero)
                    ? window.wizCtx.numero
                    : row[0][1];

                var toData = {
                    numero: numero,
                    data: data,
                    csrfmiddlewaretoken: csrf_token,
                };

                $.ajax({
                    type: "POST",
                    url: miurl,
                    data: toData,
                    async: false,
                    success: function (resultado) {
                        if (resultado['resultado'] === 'exito') {

                            if (window.wizardMode) {
                                // ✅ Comportamiento SOLO cuando viene del wizard:
                                $('#rutas_form')[0].reset();                 // limpiar el form si querés cargar otra
                                mostrarToast('¡Ruta guardada con éxito!', 'success');
                                $(".alert").delay(4000).slideUp(200, function () {
                                    $(this).alert('close');
                                });

                                // refrescá tus tablas sin destruir/recrear el modal
                                try {
                                    $('#tabla_rutas').DataTable().ajax.reload(null, false);
                                } catch (e) {
                                }
                                try {
                                    table.ajax.reload(null, false);
                                } catch (e) {
                                }

                                // limpiá estilos de validación si aplica
                                $("#id_origen, #id_destino").css({"border-color": "", 'box-shadow': ''});
                                $("#id_ruta_id").val('');

                                // 🔔 Notificar al wizard y refrescar la barra (para mostrar "Finalizar")
                                $(document).trigger('rutas:guardada');
                                refreshCurrentToolbar();  // asegura que se vea "Finalizar" si Rutas es el último paso

                            } else {
                                // 🔁 Tu comportamiento actual (fuera del wizard) — lo dejamos igual:
                                $('#rutas_form')[0].reset();
                                mostrarToast('¡Ruta guardado con exito!', 'success');
                                $(".alert").delay(4000).slideUp(200, function () {
                                    $(this).alert('close');
                                });
                                $("#tabla_rutas").dataTable().fnDestroy();
                                $("#ingresar_ruta").html('Agregar');
                                $('#rutas_btn').addClass('triggered').trigger('click'); // reabre modal de rutas
                                $("#id_ruta_id").val('');
                                table.ajax.reload();
                                $("#id_origen, #id_destino").css({"border-color": "", 'box-shadow': ''});
                            }

                        } else {
                            alert(resultado['resultado']);
                        }
                    }
                });
            } else {
                const invalidFields = form[0].querySelectorAll(':invalid'); // Selecciona los campos no válidos
                invalidFields.forEach(field => {
                    console.log('Campo no válido:', field.name); // Muestra los campos no válidos
                });
                alert("Error: " + campo.validationMessage);
            }
        }
    });
    $('#ingresar_gasto').click(function (event) {
        event.preventDefault();
        if (document.getElementById('id_pinformar').value < 0 || document.getElementById('id_arbitraje').value < 0 || document.getElementById('id_precio').value < 0) {
            alert('No se admiten valores negativos en los campos numéricos.')
        } else {
            if (confirm("¿Confirma guardar el gasto?")) {
                var form = $('#gastos_form');
                var formData = new FormData(form[0]);
                if (form[0].checkValidity()) {
                    row = table.rows('.table-secondary').data();
                    let formData = $("#gastos_form").serializeArray();
                    let data = JSON.stringify(formData);
                    miurl = "/guardar_gasto/";
                    const numero = (window.wizardMode && window.wizCtx && window.wizCtx.numero)
                        ? window.wizCtx.numero
                        : row[0][1];
                    var toData = {
                        'numero': numero,
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
                                mostrarToast('¡Gasto guardado con éxito!', 'success');
                                $(".alert").delay(4000).slideUp(200, function () {
                                    $(this).alert('close');
                                });

                                if (window.wizardMode) {
                                    // ✅ En wizard: NO destruir DataTables ni reabrir el modal
                                    try {
                                        $('#tabla_gastos').DataTable().ajax.reload(null, false);
                                    } catch (e) {
                                    }
                                    try {
                                        $('#tabla_seguimiento').DataTable().ajax.reload(null, false);
                                    } catch (e) {
                                    }
                                    try {
                                        table.ajax.reload(null, false);
                                    } catch (e) {
                                    }

                                    $("#ingresar_gasto").html('Agregar');
                                    $("#id_gasto_id").val('');
                                    $('#gastos_form')[0].reset();

                                    // 🔔 Notificar al wizard y refrescar la barra
                                    $(document).trigger('gastos:guardado');
                                    refreshCurrentToolbar();

                                } else {
                                    // 🔁 Flujo legacy fuera del wizard (tu comportamiento actual)
                                    $("#ingresar_gasto").html('Agregar');
                                    $('#gastos_btn').addClass('triggered').trigger('click'); // reabrir por botón
                                    $('#id_socio').val(row[0][54]);
                                    $("#id_gasto_id").val('');
                                    try {
                                        $('#tabla_gastos').DataTable().ajax.reload(null, false);
                                    } catch (e) {
                                    }
                                    try {
                                        $('#tabla_seguimiento').DataTable().ajax.reload(null, false);
                                    } catch (e) {
                                    }
                                }
                            } else {
                                alert(resultado['resultado']);
                            }
                        }
                    });
                } else {
                    const invalidFields = form[0].querySelectorAll(':invalid'); // Selecciona los campos no válidos
                    invalidFields.forEach(field => {
                        console.log('Campo no válido:', field.name); // Muestra los campos no válidos
                    });

                    alert('Debe completar todos los campos.');
                }
            }
        }
    });
    $('#ingresar_embarque').click(function (event) {
        event.preventDefault();
        if (document.getElementById('id_bruto_embarque').value < 0 || document.getElementById('id_cbm').value < 0 || document.getElementById('id_bruto_embarque').value < 0) {
            alert('No se admiten valores negativos en los campos numéricos.')
        } else {
            if (confirm("¿Confirma guardar datos?")) {
                var form = $('#embarques_form');
                var formData = new FormData(form[0]);
                if (form[0].checkValidity()) {
                    row = table.rows('.table-secondary').data();
                    let formData = $("#embarques_form").serializeArray();
                    let formDataExtra = $("#embarques_extra_form").serializeArray();
                    let data = JSON.stringify(formData);
                    let data_extra = JSON.stringify(formDataExtra);
                    miurl = "/guardar_embarques/";
                    const numero = (window.wizardMode && window.wizCtx && window.wizCtx.numero)
                        ? window.wizCtx.numero
                        : row[0][1];
                    localStorage.setItem('numero_embarque', numero);
                    var toData = {
                        'numero': numero,
                        'data': data,
                        'data_extra': data_extra,
                        'csrfmiddlewaretoken': csrf_token,
                    };
                    $.ajax({
                        type: "POST",
                        url: miurl,
                        data: toData,
                        async: false,
                        success: function (resultado) {
                            mostrarToast('¡Embarque guardado con exito!', 'success');
                            $(".alert").delay(4000).slideUp(200, function () {
                                $(this).alert('close');
                            });

                            if (window.wizardMode) {
                                // ✅ En wizard: NO destruir ni re-abrir el modal
                                try {
                                    $('#tabla_embarques').DataTable().ajax.reload(null, false);
                                } catch (e) {
                                }
                                try {
                                    table.ajax.reload(null, false);
                                } catch (e) {
                                }
                                $('#embarques_form')[0].reset();
                                $('#id_embarque_id').val && $('#id_embarque_id').val("");

                                // avisar al wizard y refrescar la barra (si es el último paso → “Finalizar”)
                                $(document).trigger('embarques:guardado');
                                refreshCurrentToolbar();

                            } else {
                                // 🔁 Flujo legacy fuera del wizard (lo que ya hacías)
                                try {
                                    $("#tabla_embarques").dataTable().fnDestroy();
                                } catch (e) {
                                }
                                $("#ingresar_embarque").html('Agregar');
                                $('#embarques_btn').addClass('triggered').trigger('click'); // reabría el modal
                                $('#id_embarque_id').val("");
                                try {
                                    table.ajax.reload(function (json) {
                                    });
                                } catch (e) {
                                }
                            }

                            console.log(resultado['resultado']);
                        }
                    });
                } else {
                    const invalidFields = form[0].querySelectorAll(':invalid'); // Selecciona los campos no válidos
                    invalidFields.forEach(field => {
                        console.log('Campo no válido:', field.name); // Muestra los campos no válidos
                    });

                    alert('Debe completar todos los campos.');
                }
            }
        }
    });
    $('#cancelar_envase').click(function (event) {
        event.preventDefault();

        if (confirm('¿Desea cancelar la modificacion?')) {
            $("#ingresar_envase").html('Agregar');
            $("#tabla_envases").dataTable().fnDestroy();
            $('#envases_btn').addClass('triggered').trigger('click');
        }


    })
    $('#cancelar_gasto').click(function (event) {
        event.preventDefault();
        if (confirm('¿Desea cancelar la modificacion?')) {
            $("#ingresar_gasto").html('Agregar');
            $("#tabla_gastos").dataTable().fnDestroy();
            $('#gastos_btn').addClass('triggered').trigger('click');
            $("#id_gasto_id").val('');
        }
    })
    $('#cancelar_ruta').click(function (event) {
        event.preventDefault();

        if (confirm('¿Desea cancelar la modificacion?')) {
            $("#ingresar_ruta").html('Agregar');
            $("#tabla_rutas").dataTable().fnDestroy();
            $('#rutas_btn').addClass('triggered').trigger('click');
        }

    })
    $('#busqueda_manual').click(function () {
        buscar = $("#buscar").val();
        que_buscar = $("#que_buscar").val();
        table.ajax.reload();
    })
    $('#cancelar_embarque').click(function (event) {
        event.preventDefault();

        if (confirm('¿Desea cancelar la modificacion?')) {
            $("#ingresar_embarque").html('Agregar');
            $("#tabla_embarques").dataTable().fnDestroy();
            $('#embarques_btn').addClass('triggered').trigger('click');
        }

    })
    $('#guardar_archivo').click(function (event) {
        event.preventDefault();
        if (confirm("¿Confirma guardar archivo?")) {
            row = table.rows('.table-secondary').data();
            var formData = new FormData(document.getElementById("archivos_form"));
            formData.append('numero', row[0][1]);
            miurl = "/guardar_archivo/";
            $.ajax({
                type: "POST",
                url: miurl,
                data: formData,
                processData: false,
                contentType: false,
                async: false,
                success: function (resultado) {
                    if (resultado['resultado'] === 'exito') {
                        mostrarToast('¡Archivo guardado con exito!', 'success');
                        $(".alert").delay(4000).slideUp(200, function () {
                            $(this).alert('close');
                        });
                        table_archivos.ajax.reload();
                        table.ajax.reload();
                    } else {
                        alert(resultado['resultado']);
                    }
                }, error: function (xhr, status, error) {
                    // Manejar el error en caso de que ocurra
                }
            });

        }
    })

    /* FIN FUNCIONES MODALES */


    /* BOTONES ACCIONES */
    $('#notas_btn').click(function () {
        row = table.rows('.table-secondary').data();
        $("#notas_add_input").val(row[0][8]);
        if (row.length === 1) {
            $.ajax({
                url: '/get_data_seguimiento/' + row[0][0] + '/',
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    $("#notas_modal").dialog({
                        autoOpen: true,
                        open: function (event, ui) {
                            cargar_notas(row[0][1]);
                        },
                        modal: true,
                        title: "Notas para el Seguimiento N°: " + row[0][1],
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
                            // localStorage.removeItem('num_house_gasto');
                            $('#notas_table').DataTable().destroy();
                            $("#notas_form").trigger("reset");
                            try {
                                desbloquearDatos();
                            } catch (error) {
                                console.error("⚠️ Error en desbloquearDatos:", error);
                            }

                            //                 $('#table_add_im tbody tr').removeClass('table-secondary');
                            //                $('#table_edit_im tbody tr').removeClass('table-secondary');
                            //                $('#tabla_house_directo tbody tr').removeClass('table-secondary');
                        }
                    })

                }
            });
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    }); // falta este
    $('.email').click(function () {
        let title = this.getAttribute('data-tt');
        let mail_to = this.getAttribute('data-to');
        let row = table.rows('.table-secondary').data();
        $("#id_to").val('');
        $("#id_cc").val('');
        $("#id_cco").val('');
        cco = $("#id_subject").val('');
        $('#email_add_input').summernote('destroy');
        $("#arhivos_adjuntos").html('');
        archivos_adjuntos = {};
        let transportista = false;
        let master = false;
        let gastos = false;
        let directo = false;
        if (title == 'Notificacion llegada de carga') {
            if (confirm('¿Desea informar Máster?')) {
                master = true;
            }
            if (confirm('¿Desea informar Gastos?')) {
                gastos = true;
            }
        }
        if (title == 'Aviso de embarque') {
            if (confirm('¿Desea informar Transportista?')) {
                transportista = true;
            }
            if (confirm('¿Desea informar Máster?')) {
                master = true;
            }
            if (confirm('¿Desea informar Gastos?')) {
                gastos = true;
            }
        }

        if (title == 'Instruccion de embarque') {
            if (confirm('¿Desea informar Transportista?')) {
                transportista = true;
            }
            if (confirm('¿Desea una instrucción Completa o Directa? Directa=Cancelar, Completa=Aceptar')) {
                directo = true;
            }
        }

        if (title == 'Shipping instruction') {
            if (confirm('¿Desea informar Transportista?')) {
                transportista = true;
            }
            if (confirm('¿Desea una instrucción Completa o Directa? Directa=Cancelar, Completa=Aceptar')) {
                directo = true;
            }
        }

        if (row.length === 1) {
            $.ajax({
                url: '/get_data_seguimiento/' + row[0][0] + '/',
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }

                    get_data_email(row, title, row_number, transportista, master, gastos, directo);
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
                        title: title + " para el seguimiento N°: " + window.row_number,
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
                                    sendEmail(to, cc, cco, subject, message, title, window.row_number, from);
                                    $(this).dialog("close");
                                },
                            }, {
                                text: "Salir",
                                class: "btn btn-dark",
                                style: "width:100px",
                                click: function () {
                                    $(this).dialog("close");
                                    $('#modalSeleccionEmail').dialog("close");
                                },
                            },],
                        beforeClose: function (event, ui) {
                            try {
                                desbloquearDatos();
                            } catch (error) {
                                console.error("⚠️ Error en desbloquearDatos:", error);
                            }// table.ajax.reload();
                        }
                    })
                }
            });
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#pdf_btn').click(function () {
        row = table.rows('.table-secondary').data();
        $("#pdf_add_input").html('');
        $('#pdf_add_input').summernote('destroy');

        if (row.length === 1) {
            $.ajax({
                url: '/get_data_seguimiento/' + row[0][0] + '/',
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
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
                                height: wHeight * 0.90,
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
                        },
                        modal: true,
                        title: "Archivo para imprimir seguimiento N°: " + row[0][1],
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

                }
            });
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });

    $('#buscadorEmails').on('keyup', function () {
        let valor = $(this).val().toLowerCase();
        $("#listaEmails tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(valor) > -1);
        });
    });
    $('#btnAbrirModalEmail').click(function (e) {
        e.preventDefault();

        let row = table.rows('.table-secondary').data();  // Obtenemos la fila seleccionada
        if (row.length !== 1) {
            alert('Debe seleccionar un seguimiento primero.');
            return; // No sigue, no abre el modal
        }

        $("#modalSeleccionEmail").dialog({
            autoOpen: true,
            modal: true,
            width: 400,
            height: 400,
            resizable: false,
            draggable: false,
            title: 'Seleccione el tipo de aviso',
            open: function (event, ui) {
                $(this).parent().css('overflow', 'hidden'); // Quita scroll del modal
                $('#buscadorEmails').val('');
                $("#listaEmails tr").show();
            }
        });
    });

    $('#archivos_btn').click(function () {
        $("#tabla_archivos").dataTable().fnDestroy();
        row = table.rows('.table-secondary').data();
        if (row.length === 1) {
            $.ajax({
                url: '/get_data_seguimiento/' + row[0][0] + '/',
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    get_datos_archivos();
                    $("#archivos_modal").dialog({
                        autoOpen: true,
                        open: function (event, ui) {

                        },
                        modal: true,
                        title: "Archivos para el seguimiento N°: " + row[0][1],
                        height: wHeight * 0.90,
                        width: wWidth * 0.90,
                        class: 'modal fade',
                        buttons: [
                            {
                                text: "Descargar",
                                class: "btn btn-warning",
                                style: "width:100px",
                                click: function () {
                                    if (confirm('¿Confirma descargar el archivo seleccionado?')) {
                                        row = table_archivos.rows('.table-secondary').data();
                                        var url = '/descargar_archivo/' + row[0][0];  // Ruta de la vista que devuelve el archivo
                                        window.open(url, '_blank');
                                    }
                                },
                            }, {
                                text: "Eliminar",
                                class: "btn btn-danger",
                                style: "width:100px",
                                click: function () {
                                    if (confirm('¿Confirma eliminar archivo?')) {
                                        row = table_archivos.rows('.table-secondary').data();
                                        if (row.length === 1) {
                                            miurl = "/eliminar_archivo/";
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
                                                    if (aux == 'exito') {
                                                        var idx = table.cell('.table-secondary', 0).index();
                                                        table_archivos.$("tr.table-secondary").removeClass('table-secondary');
                                                        table_archivos.row(idx).remove().draw(true);
                                                        mostrarToast('¡Archivo eliminado correctamente!', 'success');
                                                        table.ajax.reload();
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
                            $("#tabla_archivos").dataTable().fnDestroy();
                        }
                    })

                }
            });
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    }); //falta este
    $('#adjuntar_btn').click(function () {
        $("#tabla_archivos").dataTable().fnDestroy();
        row = table.rows('.table-secondary').data();
        if (row.length === 1) {

            get_datos_archivos();
            $("#archivos_modal").dialog({
                autoOpen: true,
                open: function (event, ui) {

                },
                modal: true,
                title: "Archivos para el seguimiento N°: " + row[0][1],
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
                                row = table_archivos.rows('.table-secondary').data();
                                let nombre = row[0][2].split("/")[1];
                                let id = row[0][0];
                                if (id in archivos_adjuntos) {
                                    alert('El archivo adjunto ya se encuentra seleccionado');
                                } else {
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
                    }, {
                        text: "Descargar",
                        class: "btn btn-dark",
                        style: "width:100px",
                        click: function () {
                            if (confirm('¿Confirma descargar el archivo seleccionado?')) {
                                row = table_archivos.rows('.table-secondary').data();
                                var url = '/descargar_archivo/' + row[0][0];  // Ruta de la vista que devuelve el archivo
                                window.open(url, '_blank');
                            }
                        },
                    }, {
                        text: "Eliminar",
                        class: "btn btn-danger",
                        style: "width:100px",
                        click: function () {
                            if (confirm('¿Confirma eliminar archivo?')) {
                                row = table_archivos.rows('.table-secondary').data();
                                if (row.length === 1) {
                                    miurl = "/eliminar_archivo/";
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
                                            if (aux == 'exito') {
                                                var idx = table.cell('.table-secondary', 0).index();
                                                table_archivos.$("tr.table-secondary").removeClass('table-secondary');
                                                table_archivos.row(idx).remove().draw(true);
                                                mostrarToast('¡Archivo eliminado correctamente!', 'success');
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
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#editar_btn').click(function () {
        $('#impo_marit_form').trigger('reset');
        row = table.rows('.table-secondary').data();
        if (row.length === 1) {
            let tipo = row[0][2];
            tipo_seguimiento = 'IMPOMARIT';
            let boton_guardar = true;
            get_datos_seguimiento(row[0][0], function (datos) {
                if (!datos) return;

                let boton_guardar = !datos.bloqueado;

                nombre_form = 'Modificar'
                if (tipo == 'IMPORT MARITIMO') {
                    $('#seguimiento_im').addClass('triggered').trigger('click', [boton_guardar]);
                } else if (tipo === 'EXPORT MARITIMO') {
                    $('#seguimiento_em').addClass('triggered').trigger('click', [boton_guardar]);
                } else if (tipo === 'IMPORT TERRESTRE') {
                    $('#seguimiento_it').addClass('triggered').trigger('click', [boton_guardar]);
                } else if (tipo === 'EXPORT TERRESTRE') {
                    $('#seguimiento_et').addClass('triggered').trigger('click', [boton_guardar]);
                } else if (tipo === 'EXPORT AEREO') {
                    $('#seguimiento_ea').addClass('triggered').trigger('click', [boton_guardar]);
                } else if (tipo === 'IMPORT AEREO') {
                    $('#seguimiento_ia').addClass('triggered').trigger('click', [boton_guardar]);
                }

            });
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#eliminar_btn').click(function () {
        row = table.rows('.table-secondary').data();
        if (row.length === 1) {
            let id = row[0][0];
            if (confirm('¿Realmente desea cancelar el seguimiento: ' + row[0][1] + '?')) {
                eliminar_seguimiento(id);
            }
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#cronologia_btn').click(function () {
        row = table.rows('.table-secondary').data();
        if (row.length === 1) {
            $('#cronologia_form').trigger("reset");
            get_datos_cronologia(row[0][0], function (ok) {
                if (!ok) return;
                $("#cronologia_modal").dialog({
                    autoOpen: true,
                    open: function () {

                    },
                    modal: true,
                    title: "Fechas de cronologia para el seguimiento N°: " + row[0][1],
                    height: wHeight * 0.50,
                    width: wWidth * 0.40,
                    class: 'modal fade',
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
                            text: "Guardar",
                            class: "btn btn-primary",
                            style: "width:100px",
                            click: function () {

                                let formData = $("#cronologia_form").serializeArray();
                                let data = JSON.stringify(formData);
                                miurl = "/guardar_cronologia/";
                                var toData = {
                                    'id': row[0][0],
                                    'data': data,
                                    'csrfmiddlewaretoken': csrf_token,
                                };
                                $.ajax({
                                    type: "POST",
                                    url: miurl,
                                    data: toData,
                                    async: true,
                                    success: function (resultado) {
                                        if (resultado['resultado'] === 'exito') {
                                            mostrarToast("¡Cronologia guardada correctamente.!", 'success')
                                            table.ajax.reload();
                                        } else {
                                            alert(resultado['resultado']);
                                        }
                                    }
                                });
                                $(this).dialog("close");

                            },
                        }],
                    beforeClose: function (event, ui) {
                        try {
                            desbloquearDatos();
                        } catch (error) {
                            console.error("⚠️ Error en desbloquearDatos:", error);
                        }
                    }
                })
            });
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#envases_btn').click(function () {
        row = table.rows('.table-secondary').data();
        if (row.length === 1) {
            if (row[0][2] == 'IMPORT AEREO' || row[0][2] == 'EXPORT AEREO') {
                alert('No puede agregar envases a las operaciones aereas.');
                return;
            }
            $.ajax({
                url: '/get_data_seguimiento/' + row[0][0] + '/',
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    get_datos_envases();
                }
            });
            $('#envases_form').trigger("reset");

            $("#envases_modal").dialog({
                autoOpen: true,
                open: function () {

                },
                modal: true,
                title: "Envases para el seguimiento N°: " + row[0][1],
                height: wHeight * 0.80,
                width: wWidth * 0.80,
                class: 'modal fade',
                buttons: [
                    {
                        text: "Eliminar",
                        class: "btn btn-danger",
                        style: "width:100px",
                        click: function () {
                            if (confirm('¿Confirma eliminar?')) {
                                row = table_envases.rows('.table-secondary').data();
                                if (row.length === 1) {
                                    miurl = "/eliminar_envase/";
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
                                            if (aux == 'exito') {
                                                var idx = table.cell('.table-secondary', 0).index();
                                                table_envases.$("tr.table-secondary").removeClass('table-secondary');
                                                table_envases.row(idx).remove().draw(true);
                                                $('#tabla_seguimiento').DataTable().ajax.reload();
                                                mostrarToast('¡Envase eliminado correctamente!', 'success');
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

                }
            })
            get_sugerencias_envases(window.row_number);
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#clonar_btn').click(function () {
        row = table.rows('.table-secondary').data();
        if (row.length === 1) {
            $('#clonar_form').trigger("reset");
            $("#clonar_modal").dialog({
                autoOpen: true,
                open: function () {

                },
                modal: true,
                title: "Clonar el seguimiento N°: " + row[0][1],
                height: wHeight * 0.50,
                width: wWidth * 0.40,
                class: 'modal fade',
                buttons: [
                    {
                        text: "Clonar",
                        class: "btn btn-success",
                        style: "width:100px",
                        click: function () {
                            if (confirm('¿Confirma clonar el seguimiento?')) {
                                if (row.length === 1) {
                                    let formData = $("#clonar_form").serializeArray();
                                    let dataForm = JSON.stringify(formData);
                                    $.ajax({
                                        url: '/get_data_seguimiento/' + row[0][0] + '/',
                                        type: 'GET',
                                        success: function (data) {
                                            if (data.bloqueado) {
                                                alert(data.mensaje);
                                                return;
                                            }

                                            miurl = "/clonar_seguimiento/";
                                            var toData = {
                                                'id': row[0][0],
                                                'data': dataForm,
                                                'csrfmiddlewaretoken': csrf_token,
                                            };
                                            $.ajax({
                                                type: "POST",
                                                url: miurl,
                                                data: toData,
                                                success: function (resultado) {
                                                    aux = resultado['resultado'];
                                                    if (aux == 'exito') {
                                                        $("#clonar_modal").dialog("close");
                                                        var idx = table.cell('.table-secondary', 0).index();
                                                        alert('Seguimiento clonardo N° ' + resultado['numero'])
                                                        mostrarToast('¡Seguimiento clonado correctamente!', 'success');
                                                        table.ajax.reload();

                                                    } else {
                                                        alert(aux);
                                                    }
                                                }
                                            });
                                        }
                                    });
                                } else {
                                    alert('Debe seleccionar un unico registro a clonar');
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

                }
            })
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#rutas_btn').click(function () {
        row = table.rows('.table-secondary').data();

        if (row.length === 1) {
            $.ajax({
                url: '/get_data_seguimiento/' + row[0][0] + '/',
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    get_datos_rutas();

                    $('#rutas_form').trigger("reset");
                    $("#id_origen").val(row[0][5]);
                    $("#id_destino").val(row[0][5]);
                    $("#id_cia").val(row[0][14]);
                    $("#id_viaje").val(row[0][24]);
                    $("#id_vapor").val(row[0][23]);
                    $("#rutas_modal").dialog({
                        autoOpen: true,
                        open: function () {
                            $('#rutas_form')[0].reset();
                        },
                        modal: true,
                        title: "Ingreso de datos para transbordos en el seguimiento N°: " + row[0][1],
                        height: 'auto',
                        width: 'auto',
                        position: {my: "center", at: "center", of: window},
                        class: 'modal fade',
                        buttons: [
                            {
                                text: "Eliminar",
                                class: "btn btn-danger",
                                style: "width:100px",
                                click: function () {
                                    if (confirm('¿Confirma eliminar?')) {
                                        row = table_rutas.rows('.table-secondary').data();
                                        if (row.length === 1) {
                                            miurl = "/eliminar_ruta/";
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
                                                        var idx = table.cell('.table-secondary', 0).index();
                                                        table_rutas.$("tr.table-secondary").removeClass('table-secondary');
                                                        table_rutas.row(idx).remove().draw(true);
                                                        $('#tabla_rutas').DataTable().ajax.reload();
                                                        $('#tabla_seguimiento').DataTable().ajax.reload();
                                                        mostrarToast('¡Ruta eliminada correctamente!', 'success');
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
                            const $ciaInput = $("#id_cia");

                            // Solo destruimos si estaba inicializado
                            if ($ciaInput.data("autocomplete-initialized")) {
                                $ciaInput.autocomplete("destroy");
                                $ciaInput.removeData("autocomplete-initialized");
                            }
                        }

                    });
                    if (row[0][2] != 'IMPORT AEREO' && row[0][2] != 'EXPORT AEREO') {
                        const $ciaInput = $("#id_cia");

                        // Verificamos si ya fue inicializado antes
                        if (!$ciaInput.data("autocomplete-initialized")) {
                            $ciaInput.autocomplete({
                                source: '/autocomplete_clientes/',
                                minLength: 2,
                                select: function (event, ui) {
                                    $(this).attr('data-id', ui.item['id']);
                                },
                                change: function (event, ui) {
                                    if (ui.item) {
                                        $(this).css({
                                            "border-color": "#3D9A37",
                                            'box-shadow': '0 0 0 0.1rem #3D9A37'
                                        });
                                        $('#id_cia').val(ui.item['value']);
                                        $('#id_cia').css({
                                            "border-color": "#3D9A37",
                                            'box-shadow': '0 0 0 0.1rem #3D9A37'
                                        });
                                    } else {
                                        $(this).val('');
                                        $('#id_cia').val('');
                                        $(this).css({
                                            "border-color": "",
                                            'box-shadow': ''
                                        });
                                        $('#id_cia').css({
                                            "border-color": "",
                                            'box-shadow': ''
                                        });
                                    }
                                }
                            });

                            // Marcamos que ya fue inicializado
                            $ciaInput.data("autocomplete-initialized", true);
                        }
                    }

                }
            });
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#logs_btn').click(function () {
        row = table.rows('.table-secondary').data();
        if (row.length === 1) {
            $.ajax({
                url: '/get_data_seguimiento/' + row[0][0] + '/',
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    get_datos_logs();
                    $("#logs_modal").dialog({
                        autoOpen: true,
                        open: function () {

                        },
                        modal: true,
                        title: "Log de interacciones para en el seguimiento N°: " + row[0][1],
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
                            try {
                                desbloquearDatos();
                            } catch (error) {
                                console.error("⚠️ Error en desbloquearDatos:", error);
                            }
                        }
                    })
                }
            });

        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#gastos_btn').click(function () {
        row = table.rows('.table-secondary').data();

        if (row.length === 1) {
            $.ajax({
                url: '/get_data_seguimiento/' + row[0][0] + '/',
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
                            $('#id_socio').val(row[0][54]);
                        },
                        modal: true,
                        title: "Gastos para el seguimiento N°: " + row[0][1],
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
                                        row_g = table_gastos.rows('.table-secondary').data();
                                        if (row_g.length === 1) {
                                            miurl = "/eliminar_gasto/";
                                            var toData = {
                                                'id': row_g[0][0],
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
                                                        $('#gastos_btn').addClass('triggered').trigger('click');
                                                        $('#tabla_seguimiento').DataTable().ajax.reload();
                                                        mostrarToast('¡Gasto eliminado correctamente!', 'success');
                                                        $('#id_socio').val(row[0][54]);

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
                        }
                    })
                }
            });
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#descargar_guia').click(function () {
        row = table.rows('.table-secondary').data();
        if (row.length === 1) {
            if (row[0][2] == 'EXPORT AEREO') {
                $.ajax({
                    url: '/get_data_seguimiento/' + row[0][0] + '/',
                    type: 'GET',
                    success: function (data) {
                        if (data.bloqueado) {
                            alert(data.mensaje);
                            return;
                        }

                        window.open('/descargar_awb_seguimientos/' + row[0][0], '_blank');
                    }
                });
            } else {
                alert('La guias solo pueden ser asignadas a EXPORTACION AEREA');
            }

        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#descargar_guia_draft').click(function () {
        row = table.rows('.table-secondary').data();
        if (row.length === 1) {
            if (row[0][2] == 'EXPORT AEREO') {
                $.ajax({
                    url: '/get_data_seguimiento/' + row[0][0] + '/',
                    type: 'GET',
                    success: function (data) {
                        if (data.bloqueado) {
                            alert(data.mensaje);
                            return;
                        }
                        window.open('/descargar_awb_seguimientos_draft/' + row[0][0] + '/d', '_blank');
                    }
                });
            } else {
                alert('La guias solo pueden ser asignadas a EXPORTACION AEREA');
            }

        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    /* FIN BOTONES ACCIONES */

    /* ACCIONES DE LAS TABLAS AUXILIARES */
    $('#tabla_envases tbody').on('dblclick', 'tr', function () {
        var data = table_envases.row(this).data();

        $("#id_envase_id").val(data[0]);         // ID del registro
        $("#id_unidad").val(data[2]);                // Unidad
        $("#id_tipo").val(data[3]);                  // Tipo
        $("#id_movimiento").val(data[4]);            // Movimiento
        $("#id_terminos").val(data[5]);              // Términos
        $("#id_cantidad").val(data[6]);              // Cantidad
        $("#id_precio").val(data[7]);                // Precio
        $("#id_marcas").val(data[8]);                // Marcas
        $("#id_precinto").val(data[9]);             // Precinto
        $("#id_tara").val(data[10]);                 // Tara
        $("#envases_form #id_bonifcli").val(data[11]);             // Bonificación cliente
        $("#id_envase").val(data[12]);               // Envase
        $("#id_bultos").val(data[13]);               // Bultos
        $("#id_peso").val(data[14]);                 // Peso
        $("#id_profit").val(data[15]);               // Profit
        $("#id_nrocontenedor").val(data[16]);        // Número de contenedor
        $("#id_volumen").val(data[17]);

        $("#ingresar_envase").html('Modificar');
        $("#cancelar_envase").show();
    });
    $('#tabla_gastos tbody').on('dblclick', 'tr', function () {
        var data = table_gastos.row(this).data();
        $("#id_gasto_id").val(data[0]);
        if (data[3] > 0) {
            $("#id_compra_venta").val('C');
            $("#id_importe").val(data[3]);
        } else {
            $("#id_compra_venta").val('V');
            $("#id_importe").val(data[4]);
        }
        //$("#id_detalle").val(data[5]);
        if (data[6] === 'Collect') {
            $("#id_modo_id").val('C');
        } else {
            $("#id_modo_id").val('P');
        }
        $("#id_tipogasto").val(data[7]);
        $("#id_arbitraje_id").val(data[8]);
        if (data[9] === 'SI') {
            $("#id_notomaprofit").prop("checked", true);
        } else {
            $("#id_notomaprofit").prop("checked", false);
        }
        $("#id_secomparte").val(data[10].substr(0, 1));
        $("#id_pinformar").val(data[11]);
        $("#id_servicio").val(data[14]);
        $("#id_moneda_id").val(data[15]);
        $("#id_socio").val(data[16]);
        $("#ingresar_gasto").html('Modificar');
        $("#cancelar_gasto").show();
    });
    $('#tabla_embarques tbody').on('dblclick', 'tr', function () {
        var data = table_embarques.row(this).data();
        $("#id_embarque_id").val(data[0]);
        $("#id_producto").val(data[1]);
        $("#cod_producto").val(data[9]);
        $("#id_bultos_embarque").val(data[2]);
        $("#id_tipo_embarque").val(data[3]);
        $("#id_bruto_embarque").val(data[4]);
        $("#id_terminos").val(data[4]);
        $("#id_medidas").val(data[5]);
        $("#id_cbm").val(data[6]);
        $("#id_materialreceipt").val(data[7]);
        $("#id_mercaderia").val(data[8]);
        $("#ingresar_embarque").html('Modificar');
        $("#cancelar_embarque").show();
    });
    $('#tabla_rutas tbody').on('dblclick', 'tr', function () {
        var data = table_rutas.row(this).data();
        $("#id_ruta_id").val(data[0]);
        $("#id_origen").val(data[1]);
        $("#id_destino").val(data[2]);
        $("#id_vapor").val(data[3]);
        $("#id_salida").val(data[4]);
        $("#id_llegada").val(data[5]);
        $("#id_viaje_ruta").val(data[6]);
        $("#id_cia").val(data[7]);
        $("#id_modo_ruta").val(data[8]);
        $("#id_accion").val(data[9]);
        $("#ingresar_ruta").html('Modificar');
        $("#cancelar_ruta").show();
    });
    /* FIN ACCIONES TABLAS AUXILIARES */
    //calculo de aplicables del embarque
    $('#btn_aplicable').click(function () {
        row = table.rows('.table-secondary').data(); // Asumimos que seleccionás una fila

        if (row.length === 1) {

            if (row[0][2] == 'IMPORT MARITIMO' || row[0][2] == 'EXPORT MARITIMO') {
                alert('No puede asignar un aplicable a las operaciones maritimas.');
                return;
            }
            $('#form_aplicable').trigger("reset");
            $.ajax({
                url: '/get_data_seguimiento/' + row[0][0] + '/',
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    cargar_datos_aplicables(row[0][1]);
                    $("#aplicable_modal").dialog({
                        autoOpen: true,
                        modal: true,
                        title: "Editar datos aplicables del seguimiento N°: " + row[0][1],
                        height: 'auto',
                        width: wWidth * 0.50,
                        buttons: [
                            {
                                text: "Guardar",
                                class: "btn btn-primary",
                                click: function () {
                                    guardar_aplicable(window.row_number);
                                    table.ajax.reload();
                                    $(this).dialog("close");
                                }
                            },
                            {
                                text: "Cancelar",
                                class: "btn btn-dark",
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
                        }
                    });
                }
            });
        } else {
            alert('Debe seleccionar un único registro');
        }
    });

    $('#embarques_btn').click(function () {
        row = table.rows('.table-secondary').data();

        if (row.length === 1) {
            $.ajax({
                url: '/get_data_seguimiento/' + row[0][0] + '/',
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    get_datos_embarques();
                    $('#embarques_form').trigger("reset");
                    // get_datos_cronologia(row[0][0]);
                    $("#embarques_modal").dialog({
                        autoOpen: true,
                        open: function () {

                        },
                        modal: true,
                        title: "Embarques para el seguimiento N°: " + row[0][1],
                        height: wHeight * 0.80,
                        width: wWidth * 0.80,
                        class: 'modal fade',
                        buttons: [
                            {
                                text: "Eliminar",
                                class: "btn btn-danger",
                                style: "width:100px",
                                click: function () {
                                    if (confirm('¿Confirma eliminar?')) {
                                        row = table_embarques.rows('.table-secondary').data();
                                        let formDataExtra = $("#embarques_extra_form").serializeArray();
                                        let data_extra = JSON.stringify(formDataExtra);
                                        if (row.length === 1) {
                                            miurl = "/eliminar_embarque/";
                                            var toData = {
                                                'id': row[0][0],
                                                'data_extra': data_extra,
                                                'csrfmiddlewaretoken': csrf_token,
                                            };
                                            $.ajax({
                                                type: "POST",
                                                url: miurl,
                                                data: toData,
                                                success: function (resultado) {
                                                    aux = resultado['resultado'];

                                                    mostrarToast('¡Embarque eliminado correctamente!', 'success');
                                                    $("#tabla_embarques").dataTable().fnDestroy();
                                                    $("#ingresar_embarque").html('Agregar');
                                                    $('#embarques_btn').addClass('triggered').trigger('click');
                                                    $('#id_embarque_id').val("");
                                                    table.ajax.reload(function (json) {
                                                        // Callback function to handle the response data


                                                    });
                                                    $('#tabla_embarques').DataTable().ajax.reload();
                                                    $('#tabla_seguimiento').DataTable().ajax.reload();


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
                                    miurl = "/actualizo_datos_embarque/";
                                    let formDataExtra = $("#embarques_extra_form").serializeArray();
                                    let data_extra = JSON.stringify(formDataExtra);
                                    let numero = localStorage.getItem('numero_embarque');
                                    var toData = {
                                        'numero': numero, //row[0][1]
                                        'data': data_extra,
                                        'csrfmiddlewaretoken': csrf_token,
                                    };
                                    $.ajax({
                                        type: "POST",
                                        url: miurl,
                                        data: toData,
                                        async: false,
                                        success: function (resultado) {
                                            if (resultado['resultado'] === 'exito') {
                                                mostrarToast('¡Datos de embarques actualizados con exito!', 'success');
                                                table.ajax.reload();
                                            } else {
                                                console.log(resultado['resultado']);
                                                //alert(resultado['resultado']);
                                            }
                                        }
                                    });
                                    $(this).dialog("close");
                                },
                            }],
                        beforeClose: function (event, ui) {
                            try {
                                desbloquearDatos();
                            } catch (error) {
                                console.error("⚠️ Error en desbloquearDatos:", error);
                            }
                            $("#tabla_embarques").dataTable().fnDestroy();
                        }
                    })
                }
            });
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('.nuevo_seguimiento_old ').click(function (event, boton_guardar = true) {
        tipo_seguimiento = this.getAttribute('data-tp');
        var titulo = this.getAttribute('data-tt');
        var tipo = this.getAttribute('data-tipo');
        if (!event.target.classList.contains('triggered')) {
            var titulo = "Nuevo seguimiento de " + titulo;
            $('#impo_marit_form').trigger("reset");
            $('.form-control').css({"border-color": "", 'box-shadow': ''});
        } else {
            var titulo = "Modificar seguimiento de " + titulo + " N° " + window.row_number;
            $('.nuevo_seguimiento').removeClass('triggered');
        }
        $("#impo_marit_modal").dialog({
            autoOpen: true,
            open: function () {
                $('#id_modo').val(tipo);
                if (!boton_guardar) {
                    $(".btn-guardar-seguimiento").prop("disabled", true);
                } else {
                    $(".btn-guardar-seguimiento").prop("disabled", false);
                }
            },
            modal: true,
            title: titulo,
            height: wHeight * 0.95,
            width: wWidth * 0.75,
            class: 'modal fade',
            buttons: [
                {
                    text: "Guardar",
                    class: "btn btn-primary btn-guardar-seguimiento",
                    style: "width:100px",
                    click: function () {
                        var form = $('#impo_marit_form');
                        var formData = new FormData(form[0]);
                        if (form[0].checkValidity()) {
                            // let formData = $("#impo_marit_form").serializeArray();

                            $("#impo_marit_form").find(':input').each(function () {
                                var dataId = $(this).data('id');
                                var value = $(this).val();
                                var name = $(this).attr('name');
                                formData[name] = [value, dataId];
                            });
                            let data = JSON.stringify(formData);
                            miurl = "/guardar_seguimiento/";
                            var toData = {
                                'tipo': tipo,
                                'form': data,
                                'csrfmiddlewaretoken': csrf_token,
                            };
                            $.ajax({
                                type: "POST",
                                url: miurl,
                                data: toData,
                                async: false,
                                success: function (resultado) {
                                    if (resultado['resultado'] === 'exito') {
                                        if (resultado['tipo'] === 'nuevo') {
                                            mostrarToast("!Seguimiento GUARDADO con exito¡", 'success');
                                            alert('Número de seguimiento: ' + resultado['numero']);
                                        } else {
                                            //mostrarToast("!Seguimiento MODIFICADO con exito¡", 'success');
                                            alert("!Seguimiento MODIFICADO con exito¡");
                                        }
                                        table.ajax.reload();
                                        $('#impo_marit_modal').dialog("close");
                                    } else {
                                        alert(resultado['resultado']);
                                        //console.log(resultado['resultado']);
                                    }
                                },
                                error: function (e) {
                                    alert(e);
                                }
                            });

                        } else {
                            var isValid = document.querySelector('#impo_marit_form').reportValidity();
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
                $("#id_id").val('');
                try {
                    desbloquearDatos();
                } catch (error) {
                    console.error("⚠️ Error en desbloquearDatos:", error);
                }
            }
        })
    });

    $('.nuevo_seguimiento').click(function (event, boton_guardar = true) {
        tipo_seguimiento = this.getAttribute('data-tp');
        var titulo = this.getAttribute('data-tt');
        var tipo = this.getAttribute('data-tipo');
        var esCreacion = false;
        if (!event.target.classList.contains('triggered')) {
            esCreacion = true;
            var titulo = "Nuevo seguimiento de " + titulo;
            $('#impo_marit_form').trigger("reset");
            $('.form-control').css({"border-color": "", 'box-shadow': ''});
        } else {
            esCreacion = false;
            var titulo = "Modificar seguimiento de " + titulo + " N° " + window.row_number;
            $('.nuevo_seguimiento').removeClass('triggered');
        }

        $("#impo_marit_modal").dialog({
            autoOpen: true,
            open: function () {
                $('#id_modo').val(tipo);
                $(".btn-guardar-seguimiento").prop("disabled", !boton_guardar);

                if (esCreacion) {
                    // ✅ CREACIÓN → activar wizard
                    window.wizardMode = true;
                    window.wizardStep = 0;
                    firstStepSaved = false;

                    // si ya sabés el modo ahora, lo dejás en contexto
                    window.wizCtx = window.wizCtx || {};
                    window.wizCtx.modo = $('#id_modo').val() || null;

                    // adjuntar barra a ESTA instancia del diálogo
                    setTimeout(() => attachWizardToolbarToDialog($(this)), 0);

                    // evitar cierres accidentales
                    $(this).dialog('option', 'closeOnEscape', false);
                    $('.ui-widget-overlay').off('click'); // por si lo habías atado antes
                } else {
                    // ✅ EDICIÓN → asegurar que NO quede nada del wizard viejo
                    // limpia barra, flags, etc. y re-habilita cierre normal
                    if (typeof wizardReset === 'function') {
                        wizardReset({restoreRowNumber: true}); // o false, como prefieras
                    } else {
                        window.wizardMode = false;
                    }
                    $(this).dialog('option', 'closeOnEscape', true);
                    // (no toques overlay aquí; por defecto jQuery UI no cierra al click)
                }
            },
            modal: true,
            title: titulo,
            height: wHeight * 0.95,
            width: wWidth * 0.75,
            class: 'modal fade',
            buttons: [
                {
                    text: "Guardar",
                    class: "btn btn-primary btn-guardar-seguimiento",
                    style: "width:100px",
                    click: function () {
                        var form = $('#impo_marit_form');
                        var formData = new FormData(form[0]);
                        if (form[0].checkValidity()) {
                            // let formData = $("#impo_marit_form").serializeArray();

                            $("#impo_marit_form").find(':input').each(function () {
                                var dataId = $(this).data('id');
                                var value = $(this).val();
                                var name = $(this).attr('name');
                                formData[name] = [value, dataId];
                            });
                            let data = JSON.stringify(formData);
                            miurl = "/guardar_seguimiento/";
                            var toData = {
                                'tipo': tipo,
                                'form': data,
                                'csrfmiddlewaretoken': csrf_token,
                            };
                            $.ajax({
                                type: "POST",
                                url: miurl,
                                data: toData,
                                async: false,
                                success: function (resultado) {
                                    if (resultado['resultado'] !== 'exito') {
                                        alert(resultado['resultado']);
                                        $(document).trigger('seguimiento:error', resultado['resultado']);
                                        return;
                                    }

                                    table.ajax.reload();

                                    if (resultado['tipo'] === 'nuevo') {
                                        mostrarToast("¡Seguimiento GUARDADO con éxito!", 'success');
                                        alert('Número de seguimiento: ' + resultado['numero']);

                                        if (window.wizardMode) {
                                            // ✅ Sólo si el wizard está activo, actualizamos contexto y disparamos evento
                                            window.wizCtx.id = resultado['id'] || null;
                                            window.wizCtx.numero = resultado['numero'] || null;
                                            window.wizCtx.modo = $('#id_modo').val() || window.wizCtx.modo || null;

                                            firstStepSaved = true;

                                            // Disparar UNA sola vez este evento (sacá el duplicado de abajo)
                                            $(document).trigger('seguimiento:guardado', {
                                                id: window.wizCtx.id,
                                                numero: window.wizCtx.numero,
                                                modo: window.wizCtx.modo
                                            });

                                            refreshCurrentToolbar();
                                            // OJO: no cierres el modal aquí si vas a usar “Siguiente”
                                        } else {
                                            // Flujo tradicional (edición o creacion sin wizard)
                                            $('#impo_marit_modal').dialog("close");
                                        }
                                    } else {
                                        // edición
                                        alert("¡Seguimiento MODIFICADO con éxito!");
                                        $('#impo_marit_modal').dialog("close");
                                    }
                                },
                                error: function (e) {
                                    alert(e);
                                    $(document).trigger('seguimiento:error', e); // NUEVO
                                }
                            });

                        } else {
                            var isValid = document.querySelector('#impo_marit_form').reportValidity();
                        }
                    },
                }, {
                    text: "Salir",
                    class: "btn btn-dark",
                    style: "width:100px",
                    click: function () {
                        $(this).dialog("close");
                        if (window.wizardMode && typeof wizardReset === 'function') {
                            wizardReset({restoreRowNumber: true});
                        }
                    },
                }],
            beforeClose: function (event, ui) {
                $("#id_id").val('');
                try {
                    desbloquearDatos();
                } catch (error) {
                    console.error("⚠️ Error en desbloquearDatos:", error);
                }
            }
        })
    });


    /* FIN MODALES */

    // ESCONDER MENSAJES
    $(".alert").delay(4000).slideUp(200, function () {
        $(this).alert('close');
    });

    // AUTOCOMPLETES


    // $(".autocomplete-validable").on("blur", function () {
    //     const inputVal = $(this).val().trim();
    //     const expectedVal = $(this).attr('data-label') || '';
    //
    //     // Si el valor fue modificado y no coincide con la selección, limpiar
    //     if (inputVal !== expectedVal) {
    //         $(this).val('');
    //         $(this).attr('data-id', '');
    //         $(this).attr('data-label', '');
    //         $(this).css({
    //             "border-color": "",
    //             "box-shadow": ""
    //         });
    //     }
    // });

    $(".autocomplete-validable").on("blur", function () {
        const input = $(this);

        // Si se está forzando desde autocomplete.change, no limpiar
        if (input.attr('data-forzando') === '1') return;

        const inputVal = input.val().trim();
        const expectedVal = input.attr('data-label') || '';

        if (inputVal !== expectedVal) {
            input.val('');
            input.attr('data-id', '');
            input.attr('data-label', '');
            input.css({
                "border-color": "",
                "box-shadow": ""
            });
        }
    });


    $("#cliente_add").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
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
    $("#despachante_add").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });

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
    $("#embarcador_add").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
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
    $("#consignatario_add").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
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
    $("#notificar_add").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
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
    $("#agente_add").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
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
    $("#transportista_add").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
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
    $("#armador_add").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
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
    $("#agecompras_add").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
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
    $("#ageventas_add").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
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
        source: '/autocomplete_ciudades/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
            $('#loading_add').val(ui.item['id']);
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
    $("#deposito_add").autocomplete({
        source: '/autocomplete_depositos/',
        minLength: 0,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
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
        source: '/autocomplete_ciudades/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
            $('#discharge_add').val(ui.item['id']);
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
    $("#vendedor_add").autocomplete({
        source: '/autocomplete_vendedores/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
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
    $("#loading_add").autocomplete({
        source: '/autocomplete_ciudades/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
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
        source: '/autocomplete_ciudades/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
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

    $("#vapor_add").autocomplete({
        source: function (request, response) {
            $.getJSON('/autocomplete_vapores/', {term: request.term}, response);
        },
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['label']);  // Guarda el ID si es un item de la lista
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
        },
        change: function (event, ui) {
            var input = $(this);
            var valorIngresado = input.val();

            if (ui.item) {
                input.css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
            } else {
                if (valorIngresado.trim() !== '') {
                    $.ajax({
                        url: '/agregar_buque/',
                        method: 'POST',
                        data: {
                            nombre: valorIngresado,
                            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                        },
                        success: function (data) {
                            if (data.success) {
                                input.attr('data-id', valorIngresado);
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

    //autocomplete rutas
    $("#id_origen").autocomplete({
        source: '/autocomplete_ciudades_codigo/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
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
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
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
    // FIN AUTOCOMPLETES
    //productos para el embarque
    $("#id_producto").autocomplete({
        source: function (request, response) {
            $.getJSON('/autocomplete_productos/', {term: request.term}, response);
        },
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $(this).attr('data-label', ui.item['label']);
            $(this).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.1rem #3D9A37"
            });
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


    const campoPrecio = document.getElementById("id_importe");
    const campoInformar = document.getElementById("id_pinformar");

    campoInformar.addEventListener("keydown", function (event) {
        if (event.key === "Tab" && !event.shiftKey) {
            // Buscar valores
            let valor = campoPrecio.value;

            if (valor) {
                campoInformar.value = valor;
            }
        }
    });

});

function format(d) {
    // `d` is the original data object for the row
    let aux = '<table class="table table-sm table-responsive   " cellpadding="5" cellspacing="0" border="0" style="padding-left:30px;">' +
        '<tbody>' +
        '<tr>' +
        '<th class="derecha">Cliente:</th>' +
        '<td colspan="5">' + d[9] + '</td>' +
        '<th class="derecha">Origen:</th>' +
        '<td colspan="5">' + d[4] + '</td>' +
        '<th class="derecha">Carga:</th>' +
        '<td colspan="5">' + d[29] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha">Embarcador:</th>' +
        '<td colspan="5">' + d[10] + '</td>' +
        '<th class="derecha">Destino:</th>' +
        '<td colspan="5">' + d[5] + '</td>' +
        '<th class="derecha">Descarga:</th>' +
        '<td colspan="5">' + d[30] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha">Consignatario:</th>' +
        '<td colspan="5">' + d[11] + '</td>' +
        '<th class="derecha">Status:</th>' +
        '<td colspan="5">' + d[7] + '</td>' +
        '<th class="derecha">Posicion:</th>' +
        '<td colspan="5">' + d[31] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha">Notificar:</th>' +
        '<td colspan="5">' + d[12] + '</td>' +
        '<th class="derecha">Enlace:</th>' +
        '<td colspan="5">' + d[19] + '</td>' +
        '<th class="derecha">Tipo flete:</th>' +
        '<td colspan="5">' + d[32] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha">Agente:</th>' +
        '<td colspan="5">' + d[13] + '</td>' +
        '<th class="derecha">Moneda:</th>' +
        '<td colspan="5">' + d[20] + '</td>' +
        '<th class="derecha">Arbitraje:</th>' +
        '<td colspan="5">' + d[33] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha">Transportista:</th>' +
        '<td colspan="5">' + d[14] + '</td>' +
        '<th class="derecha">Vendedor:</th>' +
        '<td colspan="5">' + d[21] + '</td>' +
        '<th class="derecha">Ubicacion:</th>' +
        '<td colspan="5">' + d[34] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha">Armador:</th>' +
        '<td colspan="5">' + d[15] + '</td>' +
        '<th class="derecha">Deposito:</th>' +
        '<td colspan="5">' + d[22] + '</td>' +
        '<th class="derecha">Booking:</th>' +
        '<td colspan="5">' + d[35] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha">Viaje:</th>' +
        '<td colspan="5">' + d[24] + '</td>' +
        '<th class="derecha">Vapor:</th>' +
        '<td colspan="5">' + d[23] + '</td>' +
        '<th class="derecha">Track ID:</th>' +
        '<td colspan="5">' + d[36] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha">Master:</th>' +
        '<td colspan="5">' + d[25] + '</td>' +
        '<th class="derecha">Trafico:</th>' +
        '<td colspan="5">' + d[38] + '</td>' +
        '<th class="derecha">Proyecto:</th>' +
        '<td colspan="5">' + d[37] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha">Dias demora:</th>' +
        '<td colspan="5">' + d[40] + '</td>' +
        '<th class="derecha">House:</th>' +
        '<td colspan="5">' + d[26] + '</td>' +
        '<th class="derecha">Actividad:</th>' +
        '<td colspan="5">' + d[39] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha">Operacion:</th>' +
        '<td colspan="5">' + d[27] + '</td>' +
        '<th class="derecha">Orden cliente:</th>' +
        '<td colspan="5">' + d[28] + '</td>' +
        '<th class="derecha">Dias almacenaje:</th>' +
        '<td colspan="5">' + d[41] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha" colspan="12"></th>' +
        '<th class="derecha">WR:</th>' +
        '<td colspan="">' + d[42] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha" colspan="12"></th>' +
        '<th class="derecha">Valor:</th>' +
        '<td colspan="">' + d[43] + '</td>' +
        '</tr>' +
        '</tbody>' +
        '</table>';

    return aux;
}

function setCookie(row_selected) {
    select_row = row_selected;
    document.cookie = 'row_selected_seguimiento' + "=" + select_row + "; path=/";
}

function getCookie(name) {
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        row_selected = c.split('=')[1];
    }
    return null;
}

function get_datos_cronologia(id, callback) {
    $("#id_originales").val("S");
    $.ajax({
        url: '/get_data_cronologia/' + id + '/',
        type: 'GET',
        async: false,
        success: function (data) {
            if (data.bloqueado) {
                alert(data.mensaje);
                callback(false);
                return;
            }

            var datos = data.datos[0];
            // Establece los valores en los campos del formulario
            if (datos['fecha'] !== null) {
                $("#id_fecha_crono").val(datos['fecha']);
            }
            if (datos['loadingdate'] !== null) {
                $("#id_loadingdate").val(datos['loadingdate']);
            }
            if (datos['estimadorecepcion'] !== null) {
                $("#id_estimadorecepcion").val(datos['estimadorecepcion'].substring(0, 10))
            }
            if (datos['recepcion'] !== null) {
                $("#id_recepcion").val(datos['recepcion'].substring(0, 10))
            }
            if (datos['fecemision'] !== null) {
                $("#id_fecemision").val(datos['fecemision'].substring(0, 10))
            }
            if (datos['fecseguro'] !== null) {
                $("#id_fecseguro").val(datos['fecseguro'].substring(0, 10))
            }
            if (datos['fecdocage'] !== null) {
                $("#id_fecdocage").val(datos['fecdocage'].substring(0, 10))
            }
            if (datos['loadingdate'] !== null) {
                $("#id_loadingdate").val(datos['loadingdate'].substring(0, 10))
            }
            if (datos['arriboreal'] !== null) {
                $("#id_arriboreal").val(datos['arriboreal'].substring(0, 10))
            }
            if (datos['fecaduana'] !== null) {
                $("#id_fecaduana").val(datos['fecaduana'].substring(0, 10))
            }
            if (datos['pagoenfirme'] !== null) {
                $("#id_pagoenfirme").val(datos['pagoenfirme'].substring(0, 10))
            }
            if (datos['vencimiento'] !== null) {
                $("#id_vencimiento").val(datos['vencimiento'].substring(0, 10))
            }
            if (datos['etd'] !== null) {
                $("#id_etd").val(datos['etd'].substring(0, 10))
            }
            if (datos['eta'] !== null) {
                $("#id_eta").val(datos['eta'].substring(0, 10))
            }
            if (datos['fechaonhand'] !== null) {
                $("#id_fechaonhand").val(datos['fechaonhand'].substring(0, 10))
            }
            if (datos['fecrecdoc'] !== null) {
                $("#id_fecrecdoc").val(datos['fecrecdoc'].substring(0, 10))
            }
            if (datos['recepcionprealert'] !== null) {
                $("#id_recepcionprealert").val(datos['recepcionprealert'].substring(0, 10))
            }
            // campos sin fecha
            if (datos['lugar'] !== null) {
                $("#id_lugar").val(datos['lugar'])
            }
            if (datos['nroseguro'] !== null) {
                $("#id_nroseguro").val(datos['nroseguro'])
            }
            if (datos['bltipo'] !== null) {
                $("#id_bltipo").val(datos['bltipo'])
            }
            if (datos['lugar'] !== null) {
                $("#id_lugar").val(datos['lugar'])
            }
            if (datos['manifiesto'] !== null) {
                $("#id_manifiesto").val(datos['manifiesto'])
            }
            if (datos['credito'] !== null) {
                $("#id_credito").val(datos['credito'])
            }
            if (datos['prima'] !== null) {
                $("#id_prima").val(datos['prima'])
            }
            if (datos['originales'] !== null) {
                $("#id_originales").val(datos['originales'])
            }
            callback(true);
        },
        error: function (xhr, status, error) {
            alert(error);
            callback(true);
        }

    });
}

function get_datos_seguimiento(id, callback) {
    $("#id_originales").val("S");
    $.ajax({
        url: '/get_data_seguimiento/' + id + '/',
        type: 'GET',
        success: function (datos) {
            if (datos.bloqueado) {
                alert(datos.mensaje);
            }
            if (datos['fecha'] !== null) {
                $("#id_fecha").val(datos['fecha']);
            }
            if (datos['loadingdate'] !== null) {
                $("#id_loadingdate").val(datos['loadingdate']);
            }
            if (datos['vencimiento'] !== null) {
                $("#id_vencimiento").val(datos['vencimiento']);
            }

            if (datos['cliente']) {
                $("#cliente_add").val(datos['cliente']);
                $("#cliente_add").attr('data-id', datos['cliente_codigo']);
                $("#cliente_add").attr('data-label', datos['cliente']);
                $("#cliente_add").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['deposito']) {
                $("#deposito_add").val(datos['deposito']);
                $("#deposito_add").attr('data-id', datos['deposito_codigo']);
                $("#deposito_add").attr('data-label', datos['deposito']);
                $("#deposito_add").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['embarcador']) {
                $("#embarcador_add").val(datos['embarcador']);
                $("#embarcador_add").attr('data-id', datos['embarcador_codigo']);
                $("#embarcador_add").attr('data-label', datos['embarcador']);
                $("#embarcador_add").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['consignatario']) {
                $("#consignatario_add").val(datos['consignatario']);
                $("#consignatario_add").attr('data-id', datos['consignatario_codigo']);
                $("#consignatario_add").attr('data-label', datos['consignatario']);
                $("#consignatario_add").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['notificar']) {
                $("#notificar_add").val(datos['notificar']);
                $("#notificar_add").attr('data-id', datos['notificar_codigo']);
                $("#notificar_add").attr('data-label', datos['notificar']);
                $("#notificar_add").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['agente']) {
                $("#agente_add").val(datos['agente']);
                $("#agente_add").attr('data-id', datos['agente_codigo']);
                $("#agente_add").attr('data-label', datos['agente']);
                $("#agente_add").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['transportista']) {
                $("#transportista_add").val(datos['transportista']);
                $("#transportista_add").attr('data-id', datos['transportista_codigo']);
                $("#transportista_add").attr('data-label', datos['transportista']);
                $("#transportista_add").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['armador']) {
                $("#armador_add").val(datos['armador']);
                $("#armador_add").attr('data-id', datos['armador_codigo']);
                $("#armador_add").attr('data-label', datos['armador']);
                $("#armador_add").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['agecompras']) {
                $("#agecompras_add").val(datos['agecompras']);
                $("#agecompras_add").attr('data-id', datos['agecompras_codigo']);
                $("#agecompras_add").attr('data-label', datos['agecompras']);
                $("#agecompras_add").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['ageventas']) {
                $("#ageventas_add").val(datos['ageventas']);
                $("#ageventas_add").attr('data-id', datos['ageventas_codigo']);
                $("#ageventas_add").attr('data-label', datos['ageventas']);
                $("#ageventas_add").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['origen']) {
                $("#origen_add").val(datos['origen_text']);
                $("#origen_add").attr('data-id', datos['origen']);
                $("#origen_add").attr('data-label', datos['origen_text']);
                $("#origen_add").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['destino']) {
                $("#destino_add").val(datos['destino_text']);
                $("#destino_add").attr('data-id', datos['destino']);
                $("#destino_add").attr('data-label', datos['destino_text']);
                $("#destino_add").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['operacion']) {
                $("#id_operacion_seg").val(datos['operacion']);
                $("#id_operacion_seg").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['moneda']) {
                $("#id_moneda").val(datos['moneda']);
                $("#id_moneda").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['vendedor']) {
                $("#vendedor_add").val(datos['vendedor']);
                $("#vendedor_add").attr('data-id', datos['vendedor_codigo']);
                $("#vendedor_add").attr('data-label', datos['vendedor']);
                $("#vendedor_add").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['vapor']) {
                $("#vapor_add").val(datos['vapor']);
                $("#vapor_add").attr('data-id', datos['vapor_codigo']);
                $("#vapor_add").attr('data-label', datos['vapor']);
                $("#vapor_add").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['loading']) {
                $("#loading_add").val(datos['loading']);
                $("#loading_add").attr('data-id', datos['loading_codigo']);
                $("#loading_add").attr('data-label', datos['loading']);
                $("#loading_add").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }
            if (datos['discharge']) {
                $("#discharge_add").val(datos['discharge']);
                $("#discharge_add").attr('data-id', datos['discharge_codigo']);
                $("#discharge_add").attr('data-label', datos['discharge']);
                $("#discharge_add").css({"border-color": "#3D9A37", "box-shadow": "0 0 0 0.07rem #3D9A37"});
            }

            if (datos['proyecto']) $("#proyecto_add").val(datos['proyecto']).attr('data-id', datos['proyecto_codigo']).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.07rem #3D9A37"
            });
            if (datos['actividad']) $("#actividad_add").val(datos['actividad']).attr('data-id', datos['actividad_codigo']).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.07rem #3D9A37"
            });
            if (datos['desposito']) $("#id_desposito").val(datos['desposito']).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.07rem #3D9A37"
            });
            if (datos['status']) $("#id_status").val(datos['status']).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.07rem #3D9A37"
            });
            if (datos['pago']) $("#id_pago").val(datos['pago']).css({
                "border-color": "#3D9A37",
                "box-shadow": "0 0 0 0.07rem #3D9A37"
            });
            if (datos['awb']) $("#id_awb").val(datos['awb']);
            if (datos['hawb']) $("#id_hawb").val(datos['hawb']);
            if (datos['wreceipt']) $("#id_wreceipt").val(datos['wreceipt']);
            if (datos['valor']) $("#id_valor").val(datos['valor']);
            if (datos['notas']) $("#notas_seguimiento").val(datos['notas']);
            if (datos['posicion']) $("#id_posicion").val(datos['posicion']);
            if (datos['arbitraje']) $("#id_arbitraje").val(datos['arbitraje']);
            if (datos['viaje']) $("#id_viaje").val(datos['viaje']);
            if (datos['ubicacion']) $("#id_ubicacion").val(datos['ubicacion']);
            if (datos['booking']) $("#id_booking").val(datos['booking']);
            if (datos['trackid']) $("#id_trackid").val(datos['trackid']);
            if (datos['diasalmacenaje']) $("#id_diasalmacenaje").val(datos['diasalmacenaje']);
            if (datos['demora']) $("#id_demora").val(datos['demora']);
            if (datos['id']) $("#id_id").val(datos['id']);
            if (datos['modo']) $("#id_modo").val(datos['modo']);
            if (datos['refcliente']) $("#id_refcliente").val(datos['refcliente']);
            if (datos['refproveedor']) $("#id_refproveedor").val(datos['refproveedor']);
            if (datos['terminos']) $("#terminos").val(datos['terminos']);
            if (datos['volumen']) $("#id_volumen_seg").val(datos['volumen']);
            if (datos['trafico']) $("#id_trafico_seg").val(datos['trafico']);
            if (datos['contratotra']) $("#id_contratotra").val(datos['contratotra']);

            //return datos;}
            callback(datos);
        },
        error: function (xhr, status, error) {
            alert(error);
            callback(null);
        }
    });
}

function eliminar_seguimiento_old(id) {

    miurl = "/eliminar_seguimiento/";
    var toData = {
        'id': id,
        'csrfmiddlewaretoken': csrf_token,
    };
    $.ajax({
        type: "POST",
        url: miurl,
        data: toData,
        success: function (resultado) {
            let aux = resultado['resultado'];
            if (aux === 'exito') {
                table.ajax.reload();
            } else {
                alert(aux);
            }
        }
    });
}

function eliminar_seguimiento(id) {
    $.ajax({
        url: '/get_data_seguimiento/' + id + '/',
        type: 'GET',
        success: function (data) {
            if (data.bloqueado) {
                alert(data.mensaje);
                return;
            }

            // Si no está bloqueado, seguimos con la eliminación
            $.ajax({
                type: "POST",
                url: "/eliminar_seguimiento/",
                data: {
                    'id': id,
                    'csrfmiddlewaretoken': csrf_token,
                },
                success: function (resultado) {
                    if (resultado['resultado'] === 'exito') {
                        table.ajax.reload();
                    } else {
                        alert(resultado['resultado']);
                    }
                },
                error: function (xhr, status, error) {
                    alert("Error al eliminar: " + error);
                }
            });
        },
        error: function (xhr, status, error) {
            alert("Error al verificar bloqueo: " + error);
        }
    });
}

function get_datos_envases() {
    $("#tabla_envases").dataTable().fnDestroy();
    table_envases = $('#tabla_envases').DataTable({
        "order": [[6, "desc"], [1, "desc"]],
        "processing": true,
        "serverSide": true,
        "pageLength": 100,
        "language": {
            url: "/static/datatables/es_ES.json"
        },
        "ajax": {
            "url": "/source_envases",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "numero": window.row_number,
                });
            }
        }, "columnDefs": [
            {
                "targets": [0],
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": '',
                render: function (data, type, row) {

                }
            },
        ]
    });

}

function get_datos_rutas() {
    $("#tabla_rutas").dataTable().fnDestroy();
    table_rutas = $('#tabla_rutas').DataTable({
        "order": [[2, "desc"], [1, "desc"]],
        "processing": true,
        "serverSide": true,
        "pageLength": 100,
        "language": {
            url: "/static/datatables/es_ES.json"
        },
        "ajax": {
            "url": "/source_rutas",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "numero": window.row_number,
                });
            }
        }, "columnDefs": [
            {
                "targets": [0],
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": '',
                render: function (data, type, row) {

                }
            },
        ]
    });

    get_datos_seguimiento_rutas(window.row_number);
}

function get_datos_seguimiento_rutas(numero) {
    $.ajax({
        url: "/datos_seguimiento",  // Asegúrate de que esta URL coincida con tu Django URLConf
        type: "POST",
        data: {
            numero: numero,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() // CSRF Token obligatorio en POST
        },
        dataType: "json",
        success: function (response) {
            if (response.resultado === "exito") {
                let modo = response.datos.modo.split(' ');

                // Asignar valores a los inputs si existen en el formulario
                $("#id_salida").val(response.datos.salida || "");
                $("#id_llegada").val(response.datos.llegada || "");
                $("#id_origen").val(response.datos.origen || "");
                $("#id_destino").val(response.datos.destino || "");
                $("#id_modo_ruta").val(modo[1] || "");
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

function get_datos_logs() {
    row = table.rows('.table-secondary').data();
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
            "url": "/source_logs_seguimiento",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "id": row[0][0], 'numero': window.row_number
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

}

function get_datos_embarques() {
    table_embarques = $('#tabla_embarques').DataTable({
        "order": [[1, "desc"], [1, "desc"]],
        "processing": true,
        "serverSide": true,
        "pageLength": 100,
        "language": {
            url: "/static/datatables/es_ES.json"
        },
        "ajax": {
            "url": "/source_embarques",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "numero": window.row_number,
                });
            }
        }, "columnDefs": [
            {
                "targets": [0],
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": '',
                render: function (data, type, row) {
                }
            },
        ], "initComplete": function (settings, json) {
            $("#id_aplicable").val(json['data_extra']['aplicable']);
            $("#id_tarifaprofit").val(json['data_extra']['tarifaprofit']);
            $("#id_tarifaventa").val(json['data_extra']['tarifaventa']);
            $("#id_tarifacompra").val(json['data_extra']['tarifacompra']);
            $("#id_muestroflete").val(json['data_extra']['muestroflete']);
            $("#volumen").val(json['data_extra']['volumen']);
            $("input[type='radio'][value='" + json['data_extra']['tomopeso'] + "'][id^='id_tomopeso_']").prop("checked", true);
            $("input[type='radio'][value='" + json['data_extra']['tipobonifcli'] + "'][id^='id_tipobonifcli_']").prop("checked", true);
            if (json['data_extra']['tarifafija'] == 'S') {
                $("#id_tarifafija").prop("checked", true);
            } else {
                $("#id_tarifafija").prop("checked", false);
            }

        }
    });

}

function get_datos_gastos() {
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
            "url": "/source_gastos",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "numero": window.row_number,
                });
            }
        }, "columnDefs": [
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
                "targets": [3],
                "className": 'derecha',
            },
            {
                "targets": [4],
                "className": 'derecha',
            }, {
                "targets": [8],
                "className": 'derecha',
            },
            {
                "targets": [11],
                "className": 'derecha',
            },
            {
                "targets": [5, 8, 9, 10],
                "visible": false
            },
        ], "rowCallback": function (row, data) {
            // $(row).find('td:eq(3)').css('background-color', '#99cc99');
            // $(row).find('td:eq(4)').css('background-color', '#CC9393');
            if (parseFloat(data[3]) > 0) {
                ingresos += parseFloat(data[3]);
                diferencia += parseFloat(data[3]);
            } else {
                egresos += parseFloat(data[4]);
                diferencia -= parseFloat(data[3]);
            }
        }, "initComplete": function (settings, json) {
            $('#gastos_ingresos').val(ingresos.toFixed(2));
            $('#gastos_egresos').val(egresos.toFixed(2));
            $('#gastos_diferencia').val((ingresos - egresos).toFixed(2));
        }
    });

}

function get_datos_pdf() {
    row = table.rows('.table-secondary').data();
    miurl = "/get_datos_caratula/";
    var toData = {
        'numero': row[0][1],
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

function mostrarToast(mensaje, tipo) {
    var toast = $('<div class="toast toast-lg"  role="alert" aria-live="assertive" aria-atomic="true">')
        .addClass('bg-' + tipo + ' text-white')
        .text(mensaje);

    var toastContainer = $('#toast-container');
    toastContainer.append(toast);

    var toastObj = new bootstrap.Toast(toast[0]);
    toastObj.show();

    setTimeout(function () {
        toast.remove();
    }, 5000);
}

function get_datos_archivos() {
    table_archivos = $('#tabla_archivos').DataTable({
        "order": [[1, "desc"], [1, "desc"]],
        "processing": true,
        "serverSide": true,
        "pageLength": 100,
        "language": {
            url: "/static/datatables/es_ES.json"
        },
        "ajax": {
            "url": "/source_archivos",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "numero": window.row_number,
                });
            }
        }, "columnDefs": [
            {
                "targets": [0],
                "orderable": false,
                "data": null,
                "visible": false,
                "defaultContent": '',
                render: function (data, type, row) {
                }
            },
        ]
    });

}

function sendEmail(to, cc, cco, subject, message, title, seguimiento, from) {
    let miurl = "/envio_notificacion/SG/";
    var toData = {
        'to': to,
        'cc': cc,
        'cco': cco,
        'from': from,
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
                mostrarToast('¡Mensaje enviado con exito!', 'success');
                return true;
            } else {
                alert(resultado['resultado']);
            }
        }
    });


}

function get_data_email(row, title, row_number, transportista, master, gastos, directo) {
    let miurl = "/get_data_email/";
    var toData = {
        'title': title,
        'row_number': window.row_number,
        'csrfmiddlewaretoken': csrf_token,
        'transportista': transportista,
        'master': master,
        'gastos': gastos,
        'directo': directo,
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
                } else if (asunto.includes("orden de facturacion")) {
                    $("#id_to").val("");
                } else if (asunto.includes("instrucción de embarque") || asunto.includes("shipping instruction")) {
                    $("#id_to").val(resultado['email_agente']);
                } else {
                    $("#id_to").val(resultado['email_cliente']);
                }
                let selectEmails = document.getElementById("id_from");
                if (selectEmails && resultado['emails_disponibles']) {
                    selectEmails.innerHTML = "";

                    resultado['emails_disponibles'].forEach(function (email) {
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

function eliminar_adjunto(id) {
    // Eliminar el elemento del diccionario
    if (confirm('¿Confirma eliminar archivo adjunto?')) {
        delete archivos_adjuntos[id];
        // Eliminar el elemento HTML del DOM
        var elementoHTML = document.getElementById(id);
        if (elementoHTML) {
            elementoHTML.remove();
        }
        mostrarToast('¡Adjunto eliminado con exito!', 'danger');
    }
}

function calcular_volumen(medidas, bultos) {
    let volumen_aux = 0;
    let total = 0;
    if (medidas != null && bultos != null) {
        let medidasArray = medidas.split('*');
        volumen_aux = medidasArray.reduce((total, num) => total * parseFloat(num), 1);
        total = volumen_aux * bultos;
    }
    return total;
}

function get_sugerencias_envases(numero) {

    if (numero.trim() === "") {
        alert("Por favor ingrese un número válido.");
        return;
    }

    $.ajax({
        type: "GET",
        url: "get_sugerencias_envases/" + numero,
        success: function (response) {
            if (response.status === "success") {
                if (response.data.bultos !== null && response.data.bultos !== undefined && response.data.bultos !== "") {
                    $("#id_bultos").val(response.data.bultos);
                }
                if (response.data.bruto !== null && response.data.bruto !== undefined && response.data.bruto !== "") {
                    $("#id_peso").val(response.data.bruto);
                }
                if (response.data.nrocontenedor !== null && response.data.nrocontenedor !== undefined && response.data.nrocontenedor !== "") {
                    $("#id_nrocontenedor").val(response.data.nrocontenedor);
                }
                if (response.data.cbm !== null && response.data.cbm !== undefined && response.data.cbm !== "") {
                    $("#id_volumen").val(response.data.cbm);
                }
            }
        },
        error: function () {
        }
    });
}

function cargar_notas(numero) {
    $('#notas_table').DataTable({
        destroy: true,  // Asegura que se destruya cualquier instancia anterior
        ajax: {
            url: `/source/?numero=${numero}`,  // URL de la vista source
            dataSrc: 'data'
        },
        columns: [
            {data: 'id', 'visible': false},
            {data: 'fecha'},
            {data: 'asunto'},
            {data: 'tipo'},
            {
                data: null,
                render: function (data, type, row) {
                    return `
                        <button class="btn btn-danger" onclick="eliminarNota(${row.id})">Eliminar</button>
                    `;
                }
            }
        ],
        rowCallback: function (row, data) {
            // Configura el evento de doble clic para cada fila
            $(row).off('dblclick').on('dblclick', function () {
                console.log(data.notas);
                $("#notas_add_input").val(data.notas);
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
    row = table.rows('.table-secondary').data();
    let numero = row[0][1]
    formData.numero = numero;

    // Verifica si estamos editando una nota existente
    const idNota = $("#id_nota").val();
    const url = "/guardar_notas/";

    $.ajax({
        type: 'POST',
        url: url,
        data: JSON.stringify(formData),
        contentType: "application/json",
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (response) {
            if (response.resultado === 'exito') {
                $("#guardar_nota").html('Agregar');
                alert("Notas guardadas exitosamente");
                //$("#notas_modal").dialog("close");
                $('#notas_table').DataTable().ajax.reload();
                $("#notas_form")[0].reset();  // Limpia el formulario después de guardar
                $("#id_nota").val('');  // Restablece el campo oculto para futuras creaciones
                table.ajax.reload();
            } else {
                alert("Error al guardar las notas: " + response.errores);
            }
        },
        error: function () {
            alert("Error en la solicitud");
        }
    });
}

function eliminarNota(id) {
    if (confirm("¿Desea eliminar esta nota?")) {
        $.ajax({
            type: "POST",
            url: `/eliminar_nota/`,
            data: {
                id: id,  // Corrige la clave `íd` a `id`
                csrfmiddlewaretoken: csrf_token  // Asegúrate de incluir el token CSRF
            },
            success: function (response) {
                if (response.resultado === 'exito') {
                    alert("Nota eliminada exitosamente");
                    $('#notas_table').DataTable().ajax.reload();
                    table.ajax.reload();
                } else {
                    alert("Error al eliminar la nota");
                }
            },
            error: function () {
                alert("Error en la solicitud");
            }
        });
    }
}

//calculo de aplicable
function cargar_datos_aplicables(numero) {
    $.ajax({
        url: '/get_datos_aplicables/',
        data: {
            'numero': numero
        },
        type: 'GET',
        success: function (data) {
            if (data.status === 'ok' || data.status === 'parcial') {
                $('#id_tarifacompra_ap').val(data.tarifacompra.toFixed(2));
                $('#id_tarifaventa_ap').val(data.tarifaventa.toFixed(2));
                $('#id_bruto_ap').val(data.bruto.toFixed(2));
                $('#id_volumen_ap').val(data.volumen.toFixed(2));
                $('#id_muestroflete_ap').val(data.muestroflete.toFixed(2));
                $('#id_aplicable_ap').val(data.aplicable.toFixed(2));

                if (data.status === 'parcial') {
                    mostrarToast(data.mensaje, 'warning');
                }
            } else {
                mostrarToast(data.mensaje, 'danger');
            }
        },
        error: function (xhr) {
            alert('Error al obtener los datos del seguimiento');
        }
    });
}

function recalculo_embarques() {
    const coef = 166.67;

    let tipo = null;
    if ($('#id_tomopeso_ap_0').is(':checked')) {
        tipo = '1';
    } else if ($('#id_tomopeso_ap_1').is(':checked')) {
        tipo = '2';
    } else if ($('#id_tomopeso_ap_2').is(':checked')) {
        tipo = '3';
    }

    const bruto = parseFloat($('#id_bruto_ap').val()) || 0;
    const volumen = parseFloat($('#id_volumen_ap').val()) || 0;
    const tarifa_venta = parseFloat($('#id_tarifaventa_ap').val()) || 0;
    //const tarifa_compra = parseFloat($('#id_tarifacompra_ap').val()) || 0;
    let tarifa = tarifa_venta;

    let aplicable = 0;
    let flete = 0;

    if (tipo === '1') {
        $('#id_aplicable_ap').val(0);
        $('#id_muestroflete_ap').val(0);
        // Usar el bruto directamente
        aplicable = redondear_a_05_o_0(bruto);
        flete = aplicable * tarifa;
    } else if (tipo === '2') {
        $('#id_aplicable_ap').val(0);
        $('#id_muestroflete_ap').val(0);
        // Calcular aplicable como volumen * coef
        aplicable = redondear_a_05_o_0(volumen * coef);
        flete = aplicable * tarifa;
    } else if (tipo === '3') {
        aplicable = parseFloat($('#id_aplicable_ap').val()) || 0;
        flete = aplicable * tarifa;
    }

    $('#id_aplicable_ap').val(aplicable.toFixed(2));
    $('#id_muestroflete_ap').val(flete ? flete.toFixed(2) : '');
}

function redondear_a_05_o_0(numero) {
    let redondeado = parseFloat(numero.toFixed(1));
    let decimal = redondeado - Math.floor(redondeado);

    if (decimal < 0.25) {
        return Math.floor(redondeado);
    } else if (decimal < 0.75) {
        return Math.floor(redondeado) + 0.5;
    } else {
        return Math.ceil(redondeado);
    }
}

function guardar_aplicable(numero) {
    const data = {
        bruto: $('#id_bruto_ap').val(),
        volumen: $('#id_volumen_ap').val(),
        tarifacompra: $('#id_tarifacompra_ap').val(),
        tarifaventa: $('#id_tarifaventa_ap').val(),
        aplicable: $('#id_aplicable_ap').val(),
        muestroflete: $('#id_muestroflete_ap').val(),
        tomopeso: $('input[name="tomopeso_ap"]:checked').val(),
        numero: numero,
        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
    };

    $.ajax({
        url: '/guardar_aplicable/',
        method: 'POST',
        data: JSON.stringify(data),
        contentType: "application/json",
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (resp) {
            if (resp.status === 'ok') {
                // ✅ notificación y refrescos
                try {
                    mostrarToast('¡Datos aplicables guardados!', 'success');
                } catch (e) {
                    alert('Datos guardados correctamente.');
                }
                try {
                    table.ajax.reload(null, false);
                } catch (e) {
                }

                if (window.wizardMode) {
                    // 👉 en wizard: NO cerrar; avisar y refrescar la botonera
                    $(document).trigger('aplicable:guardado');
                    if (typeof refreshCurrentToolbar === 'function') refreshCurrentToolbar();
                } else {
                    // 👉 flujo normal
                    $('#aplicable_modal').dialog('close');
                }
            } else {
                alert('Error: ' + (resp.mensaje || 'No se pudo guardar.'));
            }
        },
        error: function (xhr) {
            alert('Error en el servidor: ' + xhr.status);
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