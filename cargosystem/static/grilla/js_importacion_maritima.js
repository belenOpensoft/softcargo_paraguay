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

let table_add_im;

$(document).ready(function () {


    /* COLLAPSE NAVBAR 5 SECONDS AFTER LOADING THE PAGE */
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

    $('#tabla_importmarit tfoot th').each(function () {
        let title = $(this).text();
        if (title !== '') {
            $(this).html('<input type="text" class="form-control"  autocomplete="off" id="buscoid_' + contador + '" type="text" placeholder="Buscar ' + title + '"  autocomplete="off" />');
            contador++;
        } else {
            $(this).html('<button class="btn" title="Borrar filtros" id="clear" ><span class="glyphicon glyphicon-erase"></span></button> ');
        }
    });

    //tabla general
    table = $('#tabla_importmarit').DataTable({
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
            {
                "targets": [8],
            },
            {
                "targets": [9],
            },
            {
                "targets": [10],
            },
            {
                "targets": [11],
            },
        ],
        "order": [[1, "desc"],],
        "processing": true,
        "serverSide": true,
        "pageLength": 100,
        "ajax": {
            "url": "/importacion_maritima/source_master",
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
            var api = this.api();
            api.columns().every(function () {
                var that = this;
                $('input', this.footer()).on('keyup change', function () {
                    if (that.search() !== this.value) {
                        that
                            .search(this.value)
                            .draw();
                    }
                });
            });
        },
        "rowCallback": function (row, data) {
            texto = ''
            if (data[8].length > 0 && data[8] !== 'S/I') {
                texto += ' <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-clipboard2-check-fill" viewBox="0 0 16 16">\n' +
'                          <path d="M10 .5a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5.5.5 0 0 1-.5.5.5.5 0 0 0-.5.5V2a.5.5 0 0 0 .5.5h5A.5.5 0 0 0 11 2v-.5a.5.5 0 0 0-.5-.5.5.5 0 0 1-.5-.5Z"/>\n' +
'                          <path d="M4.085 1H3.5A1.5 1.5 0 0 0 2 2.5v12A1.5 1.5 0 0 0 3.5 16h9a1.5 1.5 0 0 0 1.5-1.5v-12A1.5 1.5 0 0 0 12.5 1h-.585c.055.156.085.325.085.5V2a1.5 1.5 0 0 1-1.5 1.5h-5A1.5 1.5 0 0 1 4 2v-.5c0-.175.03-.344.085-.5Zm6.769 6.854-3 3a.5.5 0 0 1-.708 0l-1.5-1.5a.5.5 0 1 1 .708-.708L7.5 9.793l2.646-2.647a.5.5 0 0 1 .708.708Z"/>\n' +
'                          </svg>';
            }
            if (data[44] > 0) {
                texto += ' <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-filetype-docx" viewBox="0 0 16 16"' +
                            '><path fill-rule="evenodd" d="M14 4.5V11h-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5L14 4.5Zm-6.839 9.688v-.522a1.54 1.54 0 0 0-.117-.641.861.861 0 0 0-.322-.387.862.862 0 0 0-.469-.129.868.868 0 0 0-.471.13.868.868 0 0 0-.32.386 1.54 1.54 0 0 0-.117.641v.522c0 .256.04.47.117.641a.868.868 0 0 0 .32.387.883.883 0 0 0 .471.126.877.877 0 0 0 .469-.126.861.861 0 0 0 .322-.386 1.55 1.55 0 0 0 .117-.642Zm.803-.516v.513c0 .375-.068.7-.205.973a1.47 1.47 0 0 1-.589.627c-.254.144-.56.216-.917.216a1.86 1.86 0 0 1-.92-.216 1.463 1.463 0 0 1-.589-.627 2.151 2.151 0 0 1-.205-.973v-.513c0-.379.069-.704.205-.975.137-.274.333-.483.59-.627.257-.147.564-.22.92-.22.357 0 .662.073.916.22.256.146.452.356.59.63.136.271.204.595.204.972ZM1 15.925v-3.999h1.459c.406 0 .741.078 1.005.235.264.156.46.382.589.68.13.296.196.655.196 1.074 0 .422-.065.784-.196 1.084-.131.301-.33.53-.595.689-.264.158-.597.237-.999.237H1Zm1.354-3.354H1.79v2.707h.563c.185 0 .346-.028.483-.082a.8.8 0 0 0 .334-.252c.088-.114.153-.254.196-.422a2.3 2.3 0 0 0 .068-.592c0-.3-.04-.552-.118-.753a.89.89 0 0 0-.354-.454c-.158-.102-.361-.152-.61-.152Zm6.756 1.116c0-.248.034-.46.103-.633a.868.868 0 0 1 .301-.398.814.814 0 0 1 .475-.138c.15 0 .283.032.398.097a.7.7 0 0 1 .273.26.85.85 0 0 1 .12.381h.765v-.073a1.33 1.33 0 0 0-.466-.964 1.44 1.44 0 0 0-.49-.272 1.836 1.836 0 0 0-.606-.097c-.355 0-.66.074-.911.223-.25.148-.44.359-.571.633-.131.273-.197.6-.197.978v.498c0 .379.065.704.194.976.13.271.321.48.571.627.25.144.555.216.914.216.293 0 .555-.054.785-.164.23-.11.414-.26.551-.454a1.27 1.27 0 0 0 .226-.674v-.076h-.765a.8.8 0 0 1-.117.364.699.699 0 0 1-.273.248.874.874 0 0 1-.401.088.845.845 0 0 1-.478-.131.834.834 0 0 1-.298-.393 1.7 1.7 0 0 1-.103-.627v-.495Zm5.092-1.76h.894l-1.275 2.006 1.254 1.992h-.908l-.85-1.415h-.035l-.852 1.415h-.862l1.24-2.015-1.228-1.984h.932l.832 1.439h.035l.823-1.439Z"' +
                            '/></svg>';
            }
            if (data[45] > 0) {
                texto += '  <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-h-circle" viewBox="0 0 16 16"' +
                            '><path d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8Zm15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0Zm-5-3.998V12H9.67V8.455H6.33V12H5V4.002h1.33v3.322h3.34V4.002H11Z"/></svg>';
            }
            if (data[46] > 0) {
                texto += ' <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-box-seam" viewBox="0 0 16 16"' +
                            '><path d="M8.186 1.113a.5.5 0 0 0-.372 0L1.846 3.5l2.404.961L10.404 2l-2.218-.887zm3.564 1.426L5.596 5 8 5.961 14.154 3.5l-2.404-.' +
                            '961zm3.25 1.7-6.5 2.6v7.922l6.5-2.6V4.24zM7.5 14.762V6.838L1 4.239v7.923l6.5 2.6zM7.443.184a1.5 1.5 0 0 1 1.114 0l7.129 2.852A.5.5 0 0 1 16' +
                            ' 3.5v8.662a1 1 0 0 1-.629.928l-7.185 2.874a.5.5 0 0 1-.372 0L.63 13.09a1 1 0 0 1-.63-.928V3.5a.5.5 0 0 1 .314-.464L7.443.184z"/> </svg>';
            }
            if (data[47] > 0) {
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
            if (data[49]) {
                texto += '<svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-geo-alt" viewBox="0 0 16 16"' +
                    '><path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.' +
                    '008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"/' +
                    '><path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>SSSS</svg>';
            }
            $('td:eq(1)', row).html(texto + " " +  data[1] + " ");
            if (data[0] === row_selected) {
                row_number = data[1];
                $(row).addClass('table-secondary');
            }
        },
    });
    let state = table.state.loaded();
    $('#tabla_importmarit tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        alert('Abro edicion del formulario');
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
    $('#tabla_importmarit tbody').on('click', 'tr', function () {
        if ($(this).hasClass('table-secondary')) {
            $(this).removeClass('table-secondary');
        } else {
            let row = table.row($(this).closest('tr')).data();
            row_selected = row[0];
            row_number = row[1];
            setCookie(row_selected);
            table.$('tr.table-secondary').removeClass('table-secondary');
            $(this).addClass('table-secondary');
        }
    });


    //autocompletes add master form
    $("#vapor_add").autocomplete({
        source: '/autocomplete_vapores/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['codigo']);
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
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#transportista_i').val(ui.item['id']);
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
    $("#armador_add").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#armador_i').val(ui.item['id']);
                 $('#armador_i').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#armador_i').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#armador_i').css({"border-color": "", 'box-shadow': ''});
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
                 $('#agecompras_ih').val(ui.item['id']);
                 $('#agecompras_ih').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#agecompras_ih').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#agecompras_ih').css({"border-color": "", 'box-shadow': ''});
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
                 $('#ageventas_ih').val(ui.item['id']);
                 $('#ageventas_ih').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#ageventas_ih').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#ageventas_ih').css({"border-color": "", 'box-shadow': ''});
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


    //botones funcionalidades

    //form addmaster
    $('#add_btn').click(function () {
        //generar_posicion();
        $("#add_master_modal").dialog({
                    autoOpen: true,
                    open: function (event, ui) {
                    },
                    modal: true,
                    title: "Ingresar un nuevo máster",
                     width: 'auto',  // Ajusta el ancho al contenido
                     height: 'auto', // Ajusta la altura al contenido
                     position: { my: "center", at: "center", of: window },
                    buttons: [
                        {
                           text: "Salir",
                           class: "btn btn-dark",
                           style: "width:100px",
                           click: function () {
                                $('#agregar_hijo').css({'visibility':'hidden'});
                                $('#segment_response').css({'visibility':'hidden'});
                               $(this).dialog("close");
                           },
                       },

                    ],
                    beforeClose: function (event, ui) {

                    }
                });
        });
    $('#add_master_form').submit(function(e){

    e.preventDefault();
    e.stopPropagation();
    let formData = $(this).serialize();
    formData += '&csrfmiddlewaretoken=' + csrf_token;
    $.ajax({
        type: "POST",
        url: "/importacion_maritima/add_master/",
        data: formData,
        success: function(response) {
            if (response.success) {
            $('#agregar_hijo').css({'visibility':'visible'});
            cargar_hauses_master();
            table.ajax.reload(null, false);
                 //$('#add_master_modal').dialog('close');
                 //guardar master en la sesion
                 let master = document.getElementById('id_awb').value;
                 localStorage.setItem('master',master );
                document.getElementById("add_master_form").reset();
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
                console.log(response.errors);
            }
        },
        error: function(xhr, status, error) {
            alert('Ocurrió un error al agregar el master: ' + error);
        }
    });
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
//                                $('#agregar_hijo').css({'visibility':'hidden'});
//                                $('#segment_response').css({'visibility':'hidden'});
                               $(this).dialog("close");
                           },
                       },

                    ],
                    beforeClose: function (event, ui) {

                    }
                });
                //cargar con la id desde la sesion
                let master = localStorage.getItem('master');
                $('#id_awbhijo').val(master);

                $('#cliente_addh').addClass('input-sobrepasar');
                $('#embarcador_addh').addClass('input-sobrepasar');
                $('#consignatario_addh').addClass('input-sobrepasar');
                $('#agente_addh').addClass('input-sobrepasar');
                $('#transportista_addh').addClass('input-sobrepasar');
                $('#armador_addh').addClass('input-sobrepasar');
                $('#agecompras_addh').addClass('input-sobrepasar');
                $('#ageventas_addh').addClass('input-sobrepasar');



        });
    $('#add_house_form').submit(function(e){
    e.preventDefault();
    e.stopPropagation();
    let formData = $(this).serialize();
    formData += '&csrfmiddlewaretoken=' + csrf_token;
    $.ajax({
        type: "POST",
        url: "/importacion_maritima/add_house/",
        data: formData,
        success: function(response) {
            if (response.success) {
//            $('#agregar_hijo').css({'visibility':'visible'});
//            cargar_hauses_master();
               table_add_im.ajax.reload(null, false);
              // let master = document.getElementById('id_awb').value;
               // $('#id_awbhijo').val(master);
                 $('#add_houses_modal').dialog('close');
                 document.getElementById("add_houses_form").reset();

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
                console.log(response.errors);
            }
        },
        error: function(xhr, status, error) {
            alert('Ocurrió un error al agregar el house: ' + error);
        }
    });
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
//tabla dentro del add-master form
let master = localStorage.getItem('master');
//let master='MOLU13000250048';
let csrftoken = getCookie2('csrftoken');
table_add_im = $('#table_add_im').DataTable({
    "stateSave": true,
    "dom": 'Btlipr',
    "scrollX": true,
     "autoWidth": true,  // Permitir ajuste automático de las columnas
    "bAutoWidth": true,
    "scrollY": wHeight * 0.60,
    "columnDefs": [
    {
        "targets": [0],  // Fecha
        "className": 'details-control',  // Clase similar a la segunda tabla
        "orderable": false,
        "data": null,
        "defaultContent": '',  // Permitir contenido por defecto
        "render": function (data, type, row) {
            // Aquí puedes definir el contenido que debe aparecer en la columna
        }
    },
    {
        "targets": [1],  // N° Seguimiento
        "className": 'derecha archivos',  // Mismo estilo que la segunda tabla
    },
    {
        "targets": [2],  // Cliente
    },
    {
        "targets": [3],  // Origen
    },
    {
        "targets": [4],  // Destino
    },
    {
        "targets": [5],  // Estado
    }
],
    "order": [[0, "desc"]],
    "processing": true,
    "serverSide": true,
    "pageLength": 100,
    "ajax": {
        "url": `/importacion_maritima/source_embarque_aereo/${master}/`,
        "type": 'POST',
        "headers": {
            "X-CSRFToken": csrftoken
        },
        "dataSrc": function (json) {
         $('#table_add_im th').css({'width':'auto'});
         $('#table_add_im_wrapper .dataTables_scrollBody').css({
        'height': 'fit-content',
        });

         if (json.data.length === 0) {
            console.log('No se encontraron datos.');
            $('#segment_response').text('No se encontraron datos.');
        } else {
      $('#segment_response').css({'visibility':'visible'});
        }

        return json.data;
        },
        "error": function(xhr, status, error) {
            console.error('Error en la llamada AJAX:', error);
        }
    },
    "language": {
        "url": "/static/datatables/es_ES.json"
    }
});

}

document.getElementById('posicion_g').addEventListener('focus', function() {
    generar_posicion();
});

function generar_posicion(){
posicion=document.getElementById('posicion_g');
//IM09-00237-2024
posicion.value=12345;
}

