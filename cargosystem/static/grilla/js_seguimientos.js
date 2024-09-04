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
var row_number = 0;
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

    setTimeout(function(){
        $('.navbar-collapse').collapse('hide');
    }, 5000);

    getCookie('row_selected_seguimiento');
    var contador = 0;
    /* DATATABLES */
    $('#tabla_seguimiento tfoot th').each(function () {
        var title = $(this).text();
        if (title !== '') {
            $(this).html('<input type="text" class="form-control"  autocomplete="off" id="buscoid_' + contador + '" type="text" placeholder="Buscar ' + title + '"  autocomplete="off" />');
            contador++;
        } else {
            var aux2 = 'Borrar';
            $(this).html('<button class="btn" title="Borrar filtros" id="clear" ><span class="glyphicon glyphicon-erase"></span></button> ');
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
            let texto = ''
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
//    if (state) {
//        table.columns().eq(0).each(function (colIdx) {
//            var colSearch = state.columns[colIdx].search;
//            if (colSearch.search) {
//                var aux = colSearch.search;
//                document.getElementById('buscoid_' + colIdx).value = aux;
//            }
//        });
//        table.draw();
//    }
    ;

    $('#tabla_seguimiento tbody').on('click', 'tr', function () {
        if ($(this).hasClass('table-secondary')) {
            $(this).removeClass('table-secondary');
        } else {
            var row = table.row($(this).closest('tr')).data();
            row_selected = row[0];
            row_number = row[1];
            setCookie(row_selected);
            table.$('tr.table-secondary').removeClass('table-secondary');
            $(this).addClass('table-secondary');
        }
    });
    $('#tabla_envases tbody').on('click', 'tr', function () {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        } else {
            var row = table_envases.row($(this).closest('tr')).data();
            row_selected_envase = row[0];
            row_number_envase = row[1];
            table_envases.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });
    $('#tabla_embarques tbody').on('click', 'tr', function () {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        } else {
            var row = table_embarques.row($(this).closest('tr')).data();
            row_selected_embarque = row[0];
            row_number_embarque = row[1];
            table_embarques.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });
    $('#tabla_archivos tbody').on('click', 'tr', function () {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        } else {
            var row = table_archivos.row($(this).closest('tr')).data();
            row_selected_archivo = row[0];
            row_number_archivo = row[1];
            table_archivos.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });
    $('#tabla_gastos tbody').on('click', 'tr', function () {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        } else {
            var row = table_gastos.row($(this).closest('tr')).data();
            row_selected_gasto = row[0];
            row_number_archivo = row[1];
            table_gastos.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    });
    $('#tabla_rutas tbody').on('click', 'tr', function () {
        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');
        } else {
            var row = table_rutas.row($(this).closest('tr')).data();
            row_selected_ruta = row[0];
            row_number_ruta = row[1];
            table_rutas.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
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
    $('#ingresar_envase').click(function () {
        if (confirm("¿Confirma guardar datos?")) {
            var form = $('#envases_form');
            var formData = new FormData(form[0]);
            if (form[0].checkValidity()) {
                row = table.rows('.table-secondary').data();
                let formData = $("#envases_form").serializeArray();
                let data = JSON.stringify(formData);
                miurl = "/guardar_envases/";
                var toData = {
                    'numero': row[0][1],
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
                            mostrarToast('¡Envase guardado con exito!', 'success');
                            $(".alert").delay(4000).slideUp(200, function () {
                                $(this).alert('close');
                            });
                            $("#tabla_envases").dataTable().fnDestroy();
                            $("#ingresar_envase").html('Agregar');
                            $('#envases_btn').addClass('triggered').trigger('click');
                            $("#id_envase_id").val('');
                            table.ajax.reload();
                        } else {
                            alert(resultado['resultado']);
                        }
                    }
                });
            }
        }
    });
    $('#ingresar_ruta').click(function () {
        if (confirm("¿Confirma guardar datos?")) {
            var form = $('#rutas_form');
            if (form[0].checkValidity()) {
                row = table.rows('.table-secondary').data();
                let formData = $("#rutas_form").serializeArray();
                let data = JSON.stringify(formData);
                miurl = "/guardar_ruta/";
                var toData = {
                    'numero': row[0][1],
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
                            mostrarToast('¡Ruta guardado con exito!', 'success');
                            $(".alert").delay(4000).slideUp(200, function () {
                                $(this).alert('close');
                            });
                            $("#tabla_rutas").dataTable().fnDestroy();
                            $("#ingresar_ruta").html('Agregar');
                            $('#rutas_btn').addClass('triggered').trigger('click');
                            $("#id_ruta_id").val('');
                            table.ajax.reload();
                        } else {
                            alert(resultado['resultado']);
                        }
                    }
                });
            }
        }
    });
    $('#ingresar_gasto').click(function () {
        if (confirm("¿Confirma guardar el gasto?")) {
            var form = $('#gastos_form');
            var formData = new FormData(form[0]);
            if (form[0].checkValidity()) {
                row = table.rows('.table-secondary').data();
                let formData = $("#gastos_form").serializeArray();
                let data = JSON.stringify(formData);
                miurl = "/guardar_gasto/";
                var toData = {
                    'numero': row[0][1],
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
                            mostrarToast('¡Gasto guardado con exito!', 'success');
                            $(".alert").delay(4000).slideUp(200, function () {
                                $(this).alert('close');
                            });
                            $("#tabla_gastos").dataTable().fnDestroy();
                            $("#ingresar_gasto").html('Agregar');
                            $('#gastos_btn').addClass('triggered').trigger('click');
                            $("#id_gasto_id").val('');
                            table_gastos.ajax.reload();
                            table.ajax.reload();
                        } else {
                            alert(resultado['resultado']);
                        }
                    }
                });
            }
        }
    });
    $('#ingresar_embarque').click(function () {
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
                var toData = {
                    'numero': row[0][1],
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
                        if (resultado['resultado'] === 'exito') {
                            mostrarToast('¡Embarque guardado con exito!', 'success');
                            $(".alert").delay(4000).slideUp(200, function () {
                                $(this).alert('close');
                            });
                            $("#tabla_embarques").dataTable().fnDestroy();
                            $("#ingresar_embarque").html('Agregar');
                            $('#embarques_btn').addClass('triggered').trigger('click');
                            $('#id_embarque_id').val("");
                            table.ajax.reload(function(json) {
                                // Callback function to handle the response data
                                console.log('Data reloaded:', json);

                            });
                        } else {
                            alert(resultado['resultado']);
                        }
                    }
                });
            }
        }
    });
    $('#cancelar_envase').click(function () {
        if (confirm('¿Desea cancelar la modificacion?')) {
            $("#ingresar_envase").html('Agregar');
            $("#tabla_envases").dataTable().fnDestroy();
            $('#envases_btn').addClass('triggered').trigger('click');
        }
    })
    $('#cancelar_gasto').click(function () {
        if (confirm('¿Desea cancelar la modificacion?')) {
            $("#ingresar_gasto").html('Agregar');
            $("#tabla_gastos").dataTable().fnDestroy();
            $('#gastos_btn').addClass('triggered').trigger('click');
        }
    })
    $('#cancelar_ruta').click(function () {
        if (confirm('¿Desea cancelar la modificacion?')) {
            $("#ingresar_ruta").html('Agregar');
            $("#tabla_rutas").dataTable().fnDestroy();
            $('#rutas_btn').addClass('triggered').trigger('click');
        }
    })
    $('#busqueda_manual').click(function () {
        buscar =  $("#buscar").val();
        que_buscar =  $("#que_buscar").val();
        table.ajax.reload();
    })
    $('#cancelar_embarque').click(function () {
        if (confirm('¿Desea cancelar la modificacion?')) {
            $("#ingresar_embarque").html('Agregar');
            $("#tabla_embarques").dataTable().fnDestroy();
            $('#embarques_btn').addClass('triggered').trigger('click');
        }
    })
    $('#guardar_archivo').click(function () {
        if (confirm("¿Confirma guardar archivo?")) {
            row = table.rows('.table-secondary').data();
            var formData = new FormData(document.getElementById("archivos_form"));
            formData.append('numero',row[0][1]);
            miurl = "/guardar_archivo/";
            $.ajax({
                type: "POST",
                url: miurl,
                data: formData,
                processData: false,
                contentType: false,
                async:false,
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
            $("#notas_modal").dialog({
                autoOpen: true,
                open: function (event, ui) {
                    $('#notas_add_input').summernote('destroy');

                    $('#notas_add_input').summernote({
                        placeholder: 'Ingrese sus notas aqui',
                        tabsize: 10,
                        height: wHeight * 0.78,
                        width: wWidth * 0.48,
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
                    $('#notas_add_input').focus();
                },
                modal: true,
                title: "Notas para el seguimiento N°: " + row[0][1],
                height: wHeight * 0.80,
                width: wWidth * 0.50,
                class: 'modal fade',
                buttons: [
                    {
                        text: "Guardar",
                        class: "btn btn-primary",
                        style: "width:100px",
                        click: function () {
                            let formData = $("#notas_form").serializeArray();
                            let data = JSON.stringify(formData);
                            miurl = "/guardar_notas/";
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
                                        mostrarToast('¡Notas actualizadas con exito!', 'success');
                                        $(".alert").delay(4000).slideUp(200, function () {
                                            $(this).alert('close');
                                        });
                                        table.ajax.reload();
                                    } else {
                                        alert(resultado['resultado']);
                                    }
                                }
                            });
                            $(this).dialog("close");
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
                    // table.ajax.reload();
                }
            })
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('.email').click(function () {
        title = this.getAttribute('data-tt');
        row = table.rows('.table-secondary').data();
        $("#id_to").val('');
        $("#id_cc").val('');
        $("#id_cco").val('');
        cco = $("#id_subject").val('');
        $('#email_add_input').summernote('destroy');
        $("#arhivos_adjuntos").html('');
        archivos_adjuntos = {};
        if (row.length === 1) {
            get_data_email(row,title,row_number);
            $("#id_to").val(row[0][50]);
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
                title:   title  + " para el seguimiento N°: " + row_number,
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
                            sendEmail(to,cc,cco,subject,message,title,row_number);
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
                    // table.ajax.reload();
                }
            })
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#pdf_btn').click(function () {
        row = table.rows('.table-secondary').data();
        $("#pdf_add_input").html('');
        $('#pdf_add_input').summernote('destroy');
        get_datos_pdf();
        if (row.length === 1) {
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
                height: wHeight * 0.90,
                width: wWidth * 0.90,
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
                    // table.ajax.reload();
                }
            })
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#archivos_btn').click(function () {
        $("#tabla_archivos").dataTable().fnDestroy();
        row = table.rows('.table-secondary').data();
        get_datos_archivos();
        if (row.length === 1) {
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
                                row = table_archivos.rows('.selected').data();
                                var url = '/descargar_archivo/' + row[0][0];  // Ruta de la vista que devuelve el archivo
                                window.open(url, '_blank');
                            }
                        },
                    },{
                        text: "Eliminar",
                        class: "btn btn-danger",
                        style: "width:100px",
                        click: function () {
                            if (confirm('¿Confirma eliminar archivo?')) {
                                row = table_archivos.rows('.selected').data();
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
                                                var idx = table.cell('.selected', 0).index();
                                                table_archivos.$("tr.selected").removeClass('selected');
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
                    // table.ajax.reload();
                    $("#tabla_archivos").dataTable().fnDestroy();
                }
            })
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#adjuntar_btn').click(function () {
        $("#tabla_archivos").dataTable().fnDestroy();
        row = table.rows('.table-secondary').data();
        get_datos_archivos();
        if (row.length === 1) {
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
                                row = table_archivos.rows('.selected').data();
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
                    },{
                        text: "Descargar",
                        class: "btn btn-dark",
                        style: "width:100px",
                        click: function () {
                            if (confirm('¿Confirma descargar el archivo seleccionado?')) {
                                row = table_archivos.rows('.selected').data();
                                var url = '/descargar_archivo/' + row[0][0];  // Ruta de la vista que devuelve el archivo
                                window.open(url, '_blank');
                            }
                        },
                    },{
                        text: "Eliminar",
                        class: "btn btn-danger",
                        style: "width:100px",
                        click: function () {
                            if (confirm('¿Confirma eliminar archivo?')) {
                                row = table_archivos.rows('.selected').data();
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
                                                var idx = table.cell('.selected', 0).index();
                                                table_archivos.$("tr.selected").removeClass('selected');
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
        row = table.rows('.table-secondary').data();
        if (row.length === 1) {
            let tipo = row[0][2];
            tipo_seguimiento = 'IMPOMARIT';
            get_datos_seguimiento(row[0][0]);
            nombre_form = 'Modificar'
            if(tipo == 'IMPORT MARITIMO'){
                $('#seguimiento_im').addClass('triggered').trigger('click');
            }else if(tipo === 'EXPORT MARITIMO'){
                $('#seguimiento_em').addClass('triggered').trigger('click');
            }else if(tipo === 'IMPORT TERRESTRE'){
                $('#seguimiento_it').addClass('triggered').trigger('click');
            }else if(tipo === 'EXPORT TERRESTRE'){
                $('#seguimiento_et').addClass('triggered').trigger('click');
            }else if(tipo === 'EXPORT AEREO'){
                $('#seguimiento_ea').addClass('triggered').trigger('click');
            }else if(tipo === 'IMPORT AEREO'){
                $('#seguimiento_ia').addClass('triggered').trigger('click');
            }
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#cronologia_btn').click(function () {
        row = table.rows('.table-secondary').data();
        if (row.length === 1) {
            $('#cronologia_form').trigger("reset");
            get_datos_cronologia(row[0][0]);
            $("#cronologia_modal").dialog({
                autoOpen: true,
                open: function () {

                },
                modal: true,
                title: "Fechas de cronologia para el seguimiento N°: " + row[0][1],
                height: wHeight * 0.80,
                width: wWidth * 0.80,
                class: 'modal fade',
                buttons: [
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
                    }, {
                        text: "Salir",
                        class: "btn btn-dark",
                        style: "width:100px",
                        click: function () {
                            $(this).dialog("close");
                        },
                    }],
                beforeClose: function (event, ui) {
                    // table.ajax.reload();
                }
            })
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#envases_btn').click(function () {
        row = table.rows('.table-secondary').data();
        get_datos_envases();
        if (row.length === 1) {
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
                                row = table_envases.rows('.selected').data();
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
                                                var idx = table.cell('.selected', 0).index();
                                                table_envases.$("tr.selected").removeClass('selected');
                                                table_envases.row(idx).remove().draw(true);
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
                    // table.ajax.reload();

                }
            })
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
                height: wHeight * 0.40,
                width: wWidth * 0.30,
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
                                    let data = JSON.stringify(formData);
                                    miurl = "/clonar_seguimiento/";
                                    var toData = {
                                        'id': row[0][0],
                                        'data': data,
                                        'csrfmiddlewaretoken': csrf_token,
                                    };
                                    $.ajax({
                                        type: "POST",
                                        url: miurl,
                                        data: toData,
                                        success: function (resultado) {
                                            aux = resultado['resultado'];
                                            if (aux == 'exito') {
                                                var idx = table.cell('.selected', 0).index();
                                                alert('Seguimiento clonardo N° ' + resultado['numero'] )
                                                mostrarToast('¡Seguimiento clonado correctamente!', 'success');
                                                table.ajax.reload();
                                            } else {
                                                alert(aux);
                                            }
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
                    // table.ajax.reload();

                }
            })
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#rutas_btn').click(function () {
        row = table.rows('.table-secondary').data();
        get_datos_rutas();
        if (row.length === 1) {
            $('#rutas_form').trigger("reset");
            $("#id_origen").val(row[0][5]);
            $("#id_destino").val(row[0][5]);
            $("#id_cia").val(row[0][14]);
            $("#id_viaje").val(row[0][24]);
            $("#id_vapor").val(row[0][23]);
            $("#rutas_modal").dialog({
                autoOpen: true,
                open: function () {

                },
                modal: true,
                title: "Ingreso de datos para transbordos en el seguimiento N°: " + row[0][1],
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
                                row = table_rutas.rows('.selected').data();
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
                                                var idx = table.cell('.selected', 0).index();
                                                table_rutas.$("tr.selected").removeClass('selected');
                                                table_rutas.row(idx).remove().draw(true);
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

                }
            })
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#logs_btn').click(function () {
        row = table.rows('.table-secondary').data();
        get_datos_logs();
        if (row.length === 1) {
            $("#logs_modal").dialog({
                autoOpen: true,
                open: function () {

                },
                modal: true,
                title: "Log de interacciones para en el seguimiento N°: " + row[0][1],
                height: wHeight * 0.90,
                width: wWidth * 0.90,
                class: 'modal fade',
                buttons: [ {
                        text: "Salir",
                        class: "btn btn-dark",
                        style: "width:100px",
                        click: function () {
                            $(this).dialog("close");
                        },
                    },],
                beforeClose: function (event, ui) {

                }
            })
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#gastos_btn').click(function () {
        row = table.rows('.table-secondary').data();
        get_datos_gastos();
        if (row.length === 1) {
            $('#gastos_form').trigger("reset");
            $("#gastos_modal").dialog({
                autoOpen: true,
                open: function () {

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
                                row = table_gastos.rows('.selected').data();
                                if (row.length === 1) {
                                    miurl = "/eliminar_gasto/";
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
                                                // table_gastos.ajax.reload();
                                                // if (parseFloat(data[3]) > 0){
                                                //     ingresos += parseFloat(data[3]);
                                                //     diferencia += parseFloat(data[3]);
                                                // }else{
                                                //     egresos += parseFloat(data[4]);
                                                //     diferencia -= parseFloat(data[3]);
                                                // }
                                                // var idx = table.cell('.selected', 0).index();
                                                // table_gastos.$("tr.selected").removeClass('selected');
                                                // table_gastos.row(idx).remove().draw(true);
                                                $("#table_gastos").dataTable().fnDestroy();
                                                $('#gastos_btn').addClass('triggered').trigger('click');
                                                mostrarToast('¡Gasto eliminado correctamente!', 'success');
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
                    // table.ajax.reload();
                    // $("#tabla_gastos").dataTable().fnDestroy();
                }
            })
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#asignar_guia').click(function () {
        if(confirm('¿Confirma asignar guia aerea?')){
            row = table.rows('.table-secondary').data();
            if (row.length === 1) {
                if(row[0][2] == 'EXPORT AEREO'){
                    miurl = "/asignar_guia_aerea/";
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
                                alert('Guian asignada N°' + resultado['numero']);
                                mostrarToast('¡Guia asignada correctamente!', 'success');
                            } else {
                                alert(aux);
                            }
                        }
                    });
                }else{
                    alert('La guias solo pueden ser asignadas a EXPORTACION AEREA');
                }

            } else {
                alert('Debe seleccionar al menos un registro');
            }
        }
    });
    $('#descargar_guia').click(function () {
        row = table.rows('.table-secondary').data();
        if (row.length === 1) {
            if(row[0][2] == 'EXPORT AEREO'){
                   window.open('/descargar_hawb/' + row[0][0], '_blank');

            }else{
                alert('La guias solo pueden ser asignadas a EXPORTACION AEREA');
            }

        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('#descargar_guia_draft').click(function () {
        row = table.rows('.table-secondary').data();
        if (row.length === 1) {
            if(row[0][2] == 'EXPORT AEREO'){
                   window.open('/descargar_hawb_draft/' + row[0][0] + '/d' ,'_blank');

            }else{
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
        $("#id_envase_id").val(data[0]);
        $("#id_unidad").val(data[1]);
        $("#id_tipo").val(data[2]);
        $("#id_movimiento").val(data[3]);
        $("#id_terminos").val(data[4]);
        $("#id_bultos").val(data[5]);
        $("#id_precio").val(data[6]);
        $("#id_profit").val(data[7]);
        $("#id_bonifcli").val(data[8]);
        $("#id_nrocontenedor").val(data[9]);
        $("#id_marcas").val(data[10]);
        $("#id_precio").val(data[11]);
        $("#id_envase").val(data[12]);
        $("#id_tara").val(data[13]);
        $("#id_peso").val(data[14]);
        $("#id_volumen").val(data[15]);
        $("#id_precinto").val(data[16]);
        $("#ingresar_envase").html('Modificar');
        $("#cancelar_envase").show();
    });
    $('#tabla_gastos tbody').on('dblclick', 'tr', function () {
        var data = table_gastos.row(this).data();
        console.log(data);
        $("#id_gasto_id").val(data[0]);
        if(data[3] > 0){
            $("#id_compra_venta").val('C');
            $("#id_importe").val(data[3]);
        }else{
            $("#id_compra_venta").val('V');
            $("#id_importe").val(data[4]);
        }
        $("#id_detalle").val(data[5]);
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
        $("#ingresar_gasto").html('Modificar');
        $("#cancelar_gasto").show();
    });
    $('#tabla_embarques tbody').on('dblclick', 'tr', function () {
        var data = table_embarques.row(this).data();
        $("#id_embarque_id").val(data[0]);
        $("#id_producto").val(data[9]);
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

    $('#embarques_btn').click(function () {
        row = table.rows('.table-secondary').data();
        get_datos_embarques();
        if (row.length === 1) {
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
                                row = table_embarques.rows('.selected').data();
                                let formDataExtra = $("#embarques_extra_form").serializeArray();
                                let data_extra = JSON.stringify(formDataExtra);
                                if (row.length === 1) {
                                    miurl = "/eliminar_embarque/";
                                    var toData = {
                                        'id': row[0][0],
                                        'data_extra' : data_extra,
                                        'csrfmiddlewaretoken': csrf_token,
                                    };
                                    $.ajax({
                                        type: "POST",
                                        url: miurl,
                                        data: toData,
                                        success: function (resultado) {
                                            aux = resultado['resultado'];
                                            if (aux == 'exito') {
                                                mostrarToast('¡Embarque eliminado correctamente!', 'success');
                                               $("#tabla_embarques").dataTable().fnDestroy();
                                                $("#ingresar_embarque").html('Agregar');
                                                $('#embarques_btn').addClass('triggered').trigger('click');
                                                $('#id_embarque_id').val("");
                                                table.ajax.reload(function(json) {
                                                    // Callback function to handle the response data
                                                    console.log('Data reloaded:', json);

                                                });
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
                            miurl = "/actualizo_datos_embarque/";
                            let formDataExtra = $("#embarques_extra_form").serializeArray();
                            let data_extra = JSON.stringify(formDataExtra);
                            var toData = {
                                'numero': row[0][1],
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
                                        alert(resultado['resultado']);
                                    }
                                }
                            });
                            $(this).dialog("close");
                        },
                    }],
                beforeClose: function (event, ui) {
                    // table.ajax.reload();
                    $("#tabla_embarques").dataTable().fnDestroy();
                }
            })
        } else {
            alert('Debe seleccionar al menos un registro');
        }
    });
    $('.nuevo_seguimiento ').click(function (event) {
        tipo_seguimiento = this.getAttribute('data-tp');
        var titulo = this.getAttribute('data-tt');
        var tipo = this.getAttribute('data-tipo');
        if (!event.target.classList.contains('triggered')) {
            var titulo = "Nuevo seguimiento de " + titulo;
            $('#impo_marit_form').trigger("reset");
            $('.form-control').css({"border-color": "", 'box-shadow': ''});
        } else {
            var titulo = "Modificar seguimiento de " + titulo + " N° " + row_number;
            $('.nuevo_seguimiento').removeClass('triggered');
        }
        $("#impo_marit_modal").dialog({
            autoOpen: true,
            open: function () {

            },
            modal: true,
            title: titulo,
            height: wHeight * 0.95,
            width: wWidth * 0.95,
            class: 'modal fade',
            buttons: [
                {
                    text: "Guardar",
                    class: "btn btn-primary",
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
                                            mostrarToast("!Seguimiento MODIFICADO con exito¡", 'success');
                                        }
                                        table.ajax.reload();
                                    } else {
                                        alert(resultado['resultado']);
                                    }
                                },
                                error: function (e) {
                                    alert(e);
                                }
                            });
                            $(this).dialog("close");
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
                // table.ajax.reload();
            }
        })
    });
    /* FIN MODALES */

    // ESCONDER MENSAJES
    $(".alert").delay(4000).slideUp(200, function () {
        $(this).alert('close');
    });

    // AUTOCOMPLETES
    $("#cliente_add").autocomplete({
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
    $("#embarcador_add").autocomplete({
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
    $("#consignatario_add").autocomplete({
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
    $("#notificar_add").autocomplete({
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
    $("#agente_add").autocomplete({
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
    $("#transportista_add").autocomplete({
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
    $("#armador_add").autocomplete({
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
    $("#agecompras_add").autocomplete({
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
    $("#ageventas_add").autocomplete({
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
    $("#origen_add").autocomplete({
        source: '/autocomplete_ciudades/',
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
    $("#deposito_add").autocomplete({
        source: '/autocomplete_depositos/',
        minLength: 0,
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
        source: '/autocomplete_ciudades/',
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
    $("#vendedor_add").autocomplete({
        source: '/autocomplete_vendedores/',
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
    $("#loading_add").autocomplete({
        source: '/autocomplete_ciudades/',
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
        source: '/autocomplete_ciudades/',
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
    $("#proyecto_add").autocomplete({
        source: '/autocomplete_proyectos/',
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
    $("#trafico_add").autocomplete({
        source: '/autocomplete_traficos/',
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
    $("#actividad_add").autocomplete({
        source: '/autocomplete_actividades/',
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
    // FIN AUTOCOMPLETES

});

function format(d) {
    // `d` is the original data object for the row
    return '<table class="table table-sm table-responsive   " cellpadding="5" cellspacing="0" border="0" style="padding-left:30px;">' +
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
        '<th class="derecha">Ag.Compras:</th>' +
        '<td colspan="5">' + d[16] + '</td>' +
        '<th class="derecha">Vapor:</th>' +
        '<td colspan="5">' + d[23] + '</td>' +
        '<th class="derecha">Track ID:</th>' +
        '<td colspan="5">' + d[36] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha">Ag.Ventas:</th>' +
        '<td colspan="5">' + d[17] + '</td>' +
        '<th class="derecha">Viaje:</th>' +
        '<td colspan="5">' + d[24] + '</td>' +
        '<th class="derecha">Proyecto:</th>' +
        '<td colspan="5">' + d[37] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha">Despachante:</th>' +
        '<td colspan="5">' + d[18] + '</td>' +
        '<th class="derecha">Master:</th>' +
        '<td colspan="5">' + d[25] + '</td>' +
        '<th class="derecha">Trafico:</th>' +
        '<td colspan="5">' + d[38] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha">Observaciones</th>' +
        '<td colspan="5">' + d[8] + '</td>' +
        '<th class="derecha">House:</th>' +
        '<td colspan="5">' + d[26] + '</td>' +
        '<th class="derecha">Actividad:</th>' +
        '<td colspan="5">' + d[39] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha"></th>' +
        '<td colspan="5"></td>' +
        '<th class="derecha">Operacion:</th>' +
        '<td colspan="5">' + d[27] + '</td>' +
        '<th class="derecha">Dias demora:</th>' +
        '<td colspan="5">' + d[40] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha"></th>' +
        '<td colspan="5"></td>' +
        '<th class="derecha">Orden cliente:</th>' +
        '<td colspan="5">' + d[28] + '</td>' +
        '<th class="derecha">Dias almacenaje:</th>' +
        '<td colspan="5">' + d[41] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha" colspan="4"></th>' +
        '<th class="derecha">WR:</th>' +
        '<td colspan="5">' + d[42] + '</td>' +
        '</tr>' +
        '<tr>' +
        '<th class="derecha" colspan="4"></th>' +
        '<th class="derecha">Valor:</th>' +
        '<td colspan="5">' + d[43] + '</td>' +
        '</tr>' +
        '</tbody>' +
        '</table>';
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
function get_datos_cronologia(id) {
    $("#id_originales").val("S");
    $.ajax({
        url: '/get_data_cronologia/' + id + '/',
        type: 'GET',
        async: false,
        success: function (data) {
            var datos = data;
            // Establece los valores en los campos del formulario
            if (datos['fecha'] !== null) {
                $("#id_fecha").val(datos['fecha'].substring(0, 10))
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
            return datos;
        },
        error: function (xhr, status, error) {
            alert(error);
        }
    });
}
function get_datos_seguimiento(id, modo = '') {
    $("#id_originales").val("S");
    $.ajax({
        url: '/get_data_seguimiento/' + id + '/',
        type: 'GET',
        async: false,
        success: function (data) {
            var datos = data;
            // Establece los valores en los campos del formulario
            if (datos['cliente'] !== null && datos['cliente'] !== 0) {
                $("#cliente_add").val(datos['cliente'])
                $("#cliente_add").attr('data-id', datos['cliente_codigo']);
                $("#cliente_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['deposito'] !== null && datos['deposito'] !== 0) {
                $("#deposito_add").val(datos['deposito'])
                $("#deposito_add").attr('data-id', datos['deposito_codigo']);
                $("#deposito_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['embarcador'] !== null && datos['embarcador'] !== 0) {
                $("#embarcador_add").val(datos['embarcador'])
                $("#embarcador_add").attr('data-id', datos['embarcador_codigo']);
                $("#embarcador_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['consignatario'] !== null && datos['consignatario'] !== 0) {
                $("#consignatario_add").val(datos['consignatario'])
                $("#consignatario_add").attr('data-id', datos['consignatario_codigo']);
                $("#consignatario_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['notificar'] !== null && datos['notificar'] !== 0) {
                $("#notificar_add").val(datos['notificar'])
                $("#notificar_add").attr('data-id', datos['notificar_codigo']);
                $("#notificar_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['agente'] !== null && datos['agente'] !== 0) {
                $("#agente_add").val(datos['agente'])
                $("#agente_add").attr('data-id', datos['agente_codigo']);
                $("#agente_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['transportista'] !== null && datos['transportista'] !== 0) {
                $("#transportista_add").val(datos['transportista'])
                $("#transportista_add").attr('data-id', datos['transportista_codigo']);
                $("#transportista_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['armador'] !== null && datos['armador'] !== 0) {
                $("#armador_add").val(datos['armador'])
                $("#armador_add").attr('data-id', datos['armador_codigo']);
                $("#armador_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['agecompras'] !== null && datos['agecompras'] !== 0) {
                $("#agecompras_add").val(datos['agecompras'])
                $("#agecompras_add").attr('data-id', datos['agecompras_codigo']);
                $("#agecompras_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['ageventas'] !== null && datos['ageventas'] !== 0) {
                $("#ageventas_add").val(datos['ageventas'])
                $("#ageventas_add").attr('data-id', datos['ageventas_codigo']);
                $("#ageventas_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['origen'] !== null && datos['origen'] !== 0) {
                $("#origen_add").val(datos['origen_text'])
                $("#origen_add").attr('data-id', datos['origen']);
                $("#origen_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['destino'] !== null && datos['destino'] !== 0) {
                $("#destino_add").val(datos['destino_text'])
                $("#destino_add").attr('data-id', datos['destino']);
                $("#destino_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['operacion'] !== '') {
                if (datos['operacion'] !== null) {
                    $("#id_operacion").val(datos['operacion'])
                }
                $("#id_operacion").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['moneda'] !== '') {
                if (datos['moneda'] !== null) {
                    $("#id_moneda").val(datos['moneda'])
                }
                $("#id_moneda").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['vendedor'] !== null && datos['vendedor'] !== 0) {
                $("#vendedor_add").val(datos['vendedor'])
                $("#vendedor_add").attr('data-id', datos['vendedor_codigo']);
                $("#vendedor_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['vapor'] !== null) {
                $("#vapor_add").val(datos['vapor'])
                $("#vapor_add").attr('data-id', datos['vapor_codigo']);
                $("#vapor_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['loading'] !== null && datos['loading'] !== 0) {
                $("#loading_add").val(datos['loading'])
                $("#loading_add").attr('data-id', datos['loading_codigo']);
                $("#loading_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['discharge'] !== null && datos['discharge'] !== 0) {
                $("#discharge_add").val(datos['discharge'])
                $("#discharge_add").attr('data-id', datos['discharge_codigo']);
                $("#discharge_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['proyecto'] !== null && datos['proyecto'] !== 0) {
                $("#proyecto_add").val(datos['proyecto'])
                $("#proyecto_add").attr('data-id', datos['proyecto_codigo']);
                $("#proyecto_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['trafico'] !== null && datos['trafico'] !== 0) {
                $("#trafico_add").val(datos['trafico'])
                $("#trafico_add").attr('data-id', datos['trafico_codigo']);
                $("#trafico_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['actividad'] !== null && datos['actividad'] !== 0) {
                $("#actividad_add").val(datos['actividad'])
                $("#actividad_add").attr('data-id', datos['actividad_codigo']);
                $("#actividad_add").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }

            if (datos['desposito'] !== '') {
                if (datos['desposito'] !== null) {
                    $("#id_desposito").val(datos['desposito'])
                }
                $("#id_desposito").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['status'] !== '') {
                if (datos['status'] !== null) {
                    $("#id_status").val(datos['status'])
                }
                $("#id_status").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['pago'] !== '') {
                if (datos['pago'] !== null) {
                    $("#id_pago").val(datos['pago'])
                }
                $("#id_pago").css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.07rem #3D9A37'});
            }
            if (datos['discharge'] !== null) {
                $("#discharge_add").val(datos['discharge'])
            }
            if (datos['awb'] !== null) {
                $("#id_awb").val(datos['awb'])
            }
            if (datos['hawb'] !== null) {
                $("#id_hawb").val(datos['hawb'])
            }
            if (datos['wreceipt'] !== null) {
                $("#id_wreceipt").val(datos['wreceipt'])
            }
            if (datos['valor'] !== null) {
                $("#id_valor").val(datos['valor'])
            }
            if (datos['notas'] !== null) {
                $("#notas_seguimiento").val(datos['notas'])
            }
            if (datos['posicion'] !== null) {
                $("#id_posicion").val(datos['posicion'])
            }
            if (datos['arbitraje'] !== null) {
                $("#id_arbitraje").val(datos['arbitraje'])
            }
            if (datos['viaje'] !== null) {
                $("#id_viaje").val(datos['viaje'])
            }
            if (datos['ubicacion'] !== null) {
                $("#id_ubicacion").val(datos['ubicacion'])
            }
            if (datos['booking'] !== null) {
                $("#id_booking").val(datos['booking'])
            }
            if (datos['trackid'] !== null) {
                $("#id_trackid").val(datos['trackid'])
            }
            if (datos['diasalmacenaje'] !== null) {
                $("#id_diasalmacenaje").val(datos['diasalmacenaje'])
            }
            if (datos['demora'] !== null) {
                $("#id_demora").val(datos['demora'])
            }
            if (datos['id'] !== null) {
                $("#id_id").val(datos['id'])
            }
            if (datos['modo'] !== null) {
                $("#id_modo").val(datos['modo'])
            }
            return datos;
        },
        error: function (xhr, status, error) {
            alert(error);
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
                    "numero": row_number,
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
                    "numero": row_number,
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
function get_datos_logs() {
    $("#tabla_logs").dataTable().fnDestroy();
    table_logs = $('#tabla_logs').DataTable({
        "order": [[2, "desc"], [1, "desc"]],
        "columnDefs": [
            {
                "targets": [ 0 ],
                "orderable": false,
                "data": null,
                "defaultContent": '',
                "visible": false
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
                    "numero": row_number,
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
                    "numero": row_number,
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
        ],"initComplete": function(settings, json) {
            console.log('Datos JSON:', json['data_extra']);
            $("#id_aplicable").val(json['data_extra']['aplicable']);
            $("#id_tarifaprofit").val(json['data_extra']['tarifaprofit']);
            $("#id_tarifaventa").val(json['data_extra']['tarifaventa']);
            $("#id_tarifacompra").val(json['data_extra']['tarifacompra']);
            $("#id_muestroflete").val(json['data_extra']['muestroflete']);
            $("#volumen").val(json['data_extra']['volumen']);
            $("input[type='radio'][value='" + json['data_extra']['tomopeso']+ "'][id^='id_tomopeso_']").prop("checked", true);
            $("input[type='radio'][value='" + json['data_extra']['tipobonifcli']+ "'][id^='id_tipobonifcli_']").prop("checked", true);
            if(json['data_extra']['tarifafija'] == 'S'){
                $("#id_tarifafija").prop("checked", true);
            }else{
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
                    "numero": row_number,
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
            },{
                "targets": [8],
                "className": 'derecha',
            },
            {
                "targets": [11],
                "className": 'derecha',
            },
        ],"rowCallback": function (row, data) {
                $(row).find('td:eq(3)').css('background-color', '#99cc99');
                $(row).find('td:eq(4)').css('background-color', '#CC9393');
                if (parseFloat(data[3]) > 0){
                    ingresos += parseFloat(data[3]);
                    diferencia += parseFloat(data[3]);
                }else{
                    egresos += parseFloat(data[4]);
                    diferencia -= parseFloat(data[3]);
                }
        },"initComplete": function( settings, json ) {
            $('#gastos_ingresos').val(ingresos.toFixed(2));
            $('#gastos_egresos').val(egresos.toFixed(2));
            $('#gastos_diferencia').val((ingresos-egresos).toFixed(2));
        }
    });
    console.log(ingresos.toFixed(2));
    console.log(egresos.toFixed(2));
    console.log(ingresos-egresos.toFixed(2));
}
function imprimirPDF() {
    var contenido = $('#pdf_add_input').summernote('code'); // Obtener el HTML del Summernote
    // Crear una nueva ventana emergente
    var ventanaImpresion = window.open('', '_blank');
    // Escribir el HTML del Summernote en la ventana emergente
    ventanaImpresion.document.write('<html><head><title></title></head><body>');
    ventanaImpresion.document.write(contenido);
    ventanaImpresion.document.write('</body></html>');
    ventanaImpresion.document.addEventListener('DOMContentLoaded', function () {
        setTimeout(function () {
        }, 2000);
    });
    ventanaImpresion.print();
    ventanaImpresion.close();
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
                    "numero": row_number,
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
function sendEmail(to,cc,cco,subject,message,title,seguimiento) {
    let miurl = "/envio_notificacion_seguimiento";
    var toData = {
        'to': to,
        'cc': cc,
        'cco': cco,
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
function get_data_email(row,title,row_number) {
    let miurl = "/get_data_email/";
    var toData = {
        'title': title,
        'row_number': row_number,
        'csrfmiddlewaretoken': csrf_token,
    };
    $.ajax({
        type: "POST",
        url: miurl,
        data: toData,
        async: false,
        success: function (resultado) {
            if (resultado['resultado'] === 'exito') {
                let textarea = document.getElementById("email_add_input");
//                textarea.innerHTML = resultado['mensaje'];
                textarea.value = resultado['mensaje'];
                $("#id_subject").val(resultado['asunto']);
            } else {
                alert(resultado['resultado']);
            }
        }
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
function recalculo_embarques(){
    monto = 0;
    aplicable = 0;
    tomopeso = $("input[name='tomopeso']:checked").val();
    table_embarques.rows().data().each(function (fila) {
        let peso = parseFloat(fila[4]);
        let medidas = fila[5];
        let tarifaventa = $("#id_tarifaventa").val();
        if(tomopeso == '1'){
            monto += redondear_a_05_o_0(peso) * tarifaventa
            aplicable += peso
        }else if(tomopeso == '2'){
            let params = medidas.split('*');
            let value = parseFloat(params[0]) * parseFloat(params[1]) * parseFloat(params[2]);
            let ap = redondear_a_05_o_0(value * 166.67);
            aplicable += ap;
            monto += ap * parseFloat(tarifaventa);
        }
    });
    $("#id_muestroflete").val(monto.toFixed(2));
    $("#id_aplicable").val(aplicable.toFixed(2));
}
function redondear_a_05_o_0(numero) {
    // Redondea el número a 1 decimal
    var numero_redondeado = parseFloat(numero.toFixed(1));

    // Calcula la parte decimal
    var parte_decimal = numero_redondeado - parseInt(numero_redondeado);

    // Redondea al valor más cercano a 0.5 o 0
    if (parte_decimal < 0.25) {
        return parseInt(numero_redondeado);
    } else if (parte_decimal < 0.75) {
        return parseFloat((parseInt(numero_redondeado) + 0.5).toFixed(1));
    } else {
        return parseInt(numero_redondeado) + 1;
    }
}