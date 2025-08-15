let numeros = [];

$(document).ready(function () {
  let contador = 0;
//  $.ajax({
//    type: "GET",
//    url: "/importacion_terrestre/source_archivos/",
//    success: function(response) {
//        console.log(response);
//    },
//    error: function(error) {
//        console.log('Error:', error);
//    }
//});
       $(document).on("submit", "#searchFormDirecto", function(e) {
        e.preventDefault();
        let formData = $(this).serialize();
        filtrar_tabla_houses(formData, e);
        $("#searchModalDirecto").dialog("close");
    });

    $("#modalSeleccionEmailHouse10").dialog({
        autoOpen: false,
        modal: true,
        width: 400,
        height: 400,
        resizable: false,
        draggable: false,
        title: 'Seleccione el tipo de aviso House',
        open: function (event, ui) {
            $(this).parent().css('overflow', 'hidden');
            $('#buscadorEmailsHouse10').val('');
            $("#listaEmailsHouse10 tr").show();
        }
    });
$('#buscadorEmailsHouse10').on('keyup', function () {
    let valor = $(this).val().toLowerCase();
    $("#listaEmailsHouse10 tr").filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(valor) > -1);
    });
});
    //buscadores
    $('#tabla_house_directo_it tfoot th').each(function(index) {
        let title = $('#tabla_house_directo_it th').eq(index).text();

        if (index === 0) {
            // Si es la primera columna, colocar el botón de limpiar filtros
            $(this).html('<button class="btn btn-danger" title="Borrar filtros" id="clear"><span class="glyphicon glyphicon-erase"></span> Limpiar</button>');
        } else if (title !== '') {
            // Agregar inputs de búsqueda en las demás columnas
            $(this).html('<input type="text" class="form-control filter-input" autocomplete="off" id="buscoid_' + index + '" placeholder="Buscar ' + title + '" />');
        }
    });

    // Evento para limpiar todos los filtros
    $(document).on("click", "#clear", function() {
        $(".filter-input").val("").trigger("keyup"); // Limpia los inputs y activa la búsqueda
        $(".filter-input").removeClass("is-invalid"); // Se quita el rojo si se vacía
    });

    // Evento para resaltar los inputs cuando tienen contenido
    $(document).on("input", ".filter-input", function() {
        if ($(this).val().trim() !== "") {
            $(this).addClass("is-invalid"); // Se pone en rojo
        } else {
            $(this).removeClass("is-invalid"); // Se quita el rojo si se vacía
        }
    });
    // Tabla general
    table = $('#tabla_house_directo_it').DataTable({
        "stateSave": true,
        "dom": 'Btlipr',
        "scrollX": true,
        "bAutoWidth": false,
        "scrollY": wHeight * 0.60,
        "order": [[1, "desc"]],
        "processing": true,
        "serverSide": true,
        "pageLength": 100,
        "ajax": {
            "url": "/importacion_terrestre/source_embarque_consolidado/",
            'type': 'GET',
            "data": function (d) {
                // Obtener los valores de búsqueda de los inputs del footer
                $('#tabla_house_directo_it tfoot input').each(function() {
                    const index = $(this).parent().index();  // Obtener el índice de la columna
                    d['columns[' + index + '][search][value]'] = this.value;  // Asignar el valor de búsqueda
                });
                return $.extend({}, d, {
                    "buscar": buscar,
                    "que_buscar": que_buscar,
                    "numeros": JSON.stringify(numeros)

                });

            }
        },
        "columnDefs": [
            { "orderable": true, "targets": "_all" },
            {
                "targets": [0],
                "visible": true,  // La columna sigue existiendo en la tabla
                "data": "id",  // Asegura que se use el ID del dataset
                "render": function (data, type, row, meta) {
                    return '<span style="display:none;">' + row[0] + '</span>'; // Oculta el número visualmente
                }
            },
            {
                "targets": [1],
                "render": function (data, type, row, meta) {
                    return row[23]; // Toma el índice 5 para la columna 6
                }
            },
            {
                "targets": [2],
                    "render": function (data, type, row, meta) {
                    return row[24]; // Toma el índice 5 para la columna 6
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
                    return row[21]; // Toma el índice 22 para la columna 4
                }
            },
            {
                "targets": [5],
                "render": function (data, type, row, meta) {
                    return row[4]; // Toma el índice 4 para la columna 5
                }
            },
            {
                "targets": [6],
                "render": function (data, type, row, meta) {
                    return row[5]; // Toma el índice 5 para la columna 6
                }
            },
            {
                "targets": [7],
                "render": function (data, type, row, meta) {
                    return row[6]; // Toma el índice 6 para la columna 7
                }
            },
            {
                "targets": [8],
                "render": function (data, type, row, meta) {
                    return row[7]; // Toma el índice 7 para la columna 8
                }
            },
            {
                "targets": [9],
                "render": function (data, type, row, meta) {
                    return row[8]; // Toma el índice 8 para la columna 9
                }
            },
            {
                "targets": [10],
                "render": function (data, type, row, meta) {
                    return row[9]; // Toma el índice 9 para la columna 10
                }
            },
            {
                "targets": [11],
                "render": function (data, type, row, meta) {
                    return row[10]; // Toma el índice 10 para la columna 11
                }
            },
            {
                "targets": [12],
                "render": function (data, type, row, meta) {
                    return row[11]; // Toma el índice 11 para la columna 12
                }
            },
            {
                "targets": [13],
                "render": function (data, type, row, meta) {
                    return row[12]; // Toma el índice 12 para la columna 13
                }
            },
            {
                "targets": [14],
                "render": function (data, type, row, meta) {
                    return row[13]; // Toma el índice 13 para la columna 14
                }
            },

        ],

        "language": {
            url: "/static/datatables/es_ES.json"
        },
        "rowCallback": function (row, data) {

        $('td:eq(3)', row).html('');
            let texto = ''
            if (data[14] > 0) {
            //archivo
                texto += ' <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-filetype-docx" viewBox="0 0 16 16"' +
                            '><path fill-rule="evenodd" d="M14 4.5V11h-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5L14 4.5Zm-6.839 9.688v-.522a1.54 1.54 0 0 0-.117-.641.861.861 0 0 0-.322-.387.862.862 0 0 0-.469-.129.868.868 0 0 0-.471.13.868.868 0 0 0-.32.386 1.54 1.54 0 0 0-.117.641v.522c0 .256.04.47.117.641a.868.868 0 0 0 .32.387.883.883 0 0 0 .471.126.877.877 0 0 0 .469-.126.861.861 0 0 0 .322-.386 1.55 1.55 0 0 0 .117-.642Zm.803-.516v.513c0 .375-.068.7-.205.973a1.47 1.47 0 0 1-.589.627c-.254.144-.56.216-.917.216a1.86 1.86 0 0 1-.92-.216 1.463 1.463 0 0 1-.589-.627 2.151 2.151 0 0 1-.205-.973v-.513c0-.379.069-.704.205-.975.137-.274.333-.483.59-.627.257-.147.564-.22.92-.22.357 0 .662.073.916.22.256.146.452.356.59.63.136.271.204.595.204.972ZM1 15.925v-3.999h1.459c.406 0 .741.078 1.005.235.264.156.46.382.589.68.13.296.196.655.196 1.074 0 .422-.065.784-.196 1.084-.131.301-.33.53-.595.689-.264.158-.597.237-.999.237H1Zm1.354-3.354H1.79v2.707h.563c.185 0 .346-.028.483-.082a.8.8 0 0 0 .334-.252c.088-.114.153-.254.196-.422a2.3 2.3 0 0 0 .068-.592c0-.3-.04-.552-.118-.753a.89.89 0 0 0-.354-.454c-.158-.102-.361-.152-.61-.152Zm6.756 1.116c0-.248.034-.46.103-.633a.868.868 0 0 1 .301-.398.814.814 0 0 1 .475-.138c.15 0 .283.032.398.097a.7.7 0 0 1 .273.26.85.85 0 0 1 .12.381h.765v-.073a1.33 1.33 0 0 0-.466-.964 1.44 1.44 0 0 0-.49-.272 1.836 1.836 0 0 0-.606-.097c-.355 0-.66.074-.911.223-.25.148-.44.359-.571.633-.131.273-.197.6-.197.978v.498c0 .379.065.704.194.976.13.271.321.48.571.627.25.144.555.216.914.216.293 0 .555-.054.785-.164.23-.11.414-.26.551-.454a1.27 1.27 0 0 0 .226-.674v-.076h-.765a.8.8 0 0 1-.117.364.699.699 0 0 1-.273.248.874.874 0 0 1-.401.088.845.845 0 0 1-.478-.131.834.834 0 0 1-.298-.393 1.7 1.7 0 0 1-.103-.627v-.495Zm5.092-1.76h.894l-1.275 2.006 1.254 1.992h-.908l-.85-1.415h-.035l-.852 1.415h-.862l1.24-2.015-1.228-1.984h.932l.832 1.439h.035l.823-1.439Z"' +
                            '/></svg>';
            }
            if (data[15] > 0) {
            //embarque
            texto += '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-truck" viewBox="0 0 16 16">\n' +
                         '<path d="M0 3.5A1.5 1.5 0 0 1 1.5 2h9A1.5 1.5 0 0 1 12 3.5V5h1.02a1.5 1.5 0 0 1 1.17.563l1.481 1.85a1.5 1.5 0 0 1 .329.938V10.5a1.5 1.5 0 0 1-1.5 1.5H14a2 2 0 1 1-4 0H5a2 2 0 1 1-3.998-.085A1.5 1.5 0 0 1 0 10.5zm1.294 7.456A2 2 0 0 1 4.732 11h5.536a2 2 0 0 1 .732-.732V3.5a.5.5 0 0 0-.5-.5h-9a.5.5 0 0 0-.5.5v7a.5.5 0 0 0 .294.456M12 10a2 2 0 0 1 1.732 1h.768a.5.5 0 0 0 .5-.5V8.35a.5.5 0 0 0-.11-.312l-1.48-1.85A.5.5 0 0 0 13.02 6H12zm-9 1a1 1 0 1 0 0 2 1 1 0 0 0 0-2m9 0a1 1 0 1 0 0 2 1 1 0 0 0 0-2"/>\n' +
                         '</svg>';


            }
            if (data[17] > 0) {
            //gastos
                texto += '   <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-currency-dollar" viewBox="0 0 16 16"' +
                    '><path d="M4 10.781c.148 1.667 1.513 2.85 3.591 3.003V15h1.043v-1.216c2.27-.179 3.678-1.438 3.678-3.3 0-1.59-.947-2.51-2.956-3.028l-.722-.18' +
                    '7V3.467c1.122.11 1.879.714 2.07 1.616h1.47c-.166-1.6-1.54-2.748-3.54-2.875V1H7.591v1.233c-1.939.23-3.27 1.472-3.27 3.156 0 1.454.966 2.483 2.' +
                    '661 2.917l.61.162v4.031c-1.149-.17-1.94-.8-2.131-1.718H4zm3.391-3.836c-1.043-.263-1.6-.825-1.6-1.616 0-.944.704-1.641 1.8-1.828v3.495l-.2-.05z' +
                    'm1.591 1.872c1.287.323 1.852.859 1.852 1.769 0 1.097-.826 1.828-2.2 1.939V8.73l.348.086z"/>sss</svg>';
            }
            if (data[18] > 0) {
            //rutas
                texto += '   <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-geo-alt" viewBox="0 0 16 16">\n' +
                    '<path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"/>\n' +
                    '<path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>\n' +
                    '</svg>';
            }
            if (data[19] > 0) {
    //notas
            texto += '   <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-sticky" viewBox="0 0 16 16">\n' +
            '<path d="M2.5 1A1.5 1.5 0 0 0 1 2.5v11A1.5 1.5 0 0 0 2.5 15h6.086a1.5 1.5 0 0 0 1.06-.44l4.915-4.914A1.5 1.5 0 0 0 15 8.586V2.5A1.5 1.5 0 0 0 13.5 1zM2 2.5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 .5.5V8H9.5A1.5 1.5 0 0 0 8 9.5V14H2.5a.5.5 0 0 1-.5-.5zm7 11.293V9.5a.5.5 0 0 1 .5-.5h4.293z"/>\n' +
            '</svg>';

                }
            $('td:eq(3)', row).html(texto + " " + data[21]);

        },
        "initComplete": function() {
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
        }
    });
    $('#tabla_house_directo_it tbody').off('dblclick').on('dblclick', 'tr', function () {
                    var table = $('#tabla_house_directo_it').DataTable();
                    var row = table.row($(this));
                    var rowData = row.data();

                    if (rowData) {
                        var selectedRowId = rowData[3];
                        localStorage.setItem('numero_embarque', selectedRowId);

                        $.ajax({
                        url: '/importacion_terrestre/house-detail',
                        data: { id: selectedRowId},
                        method: 'GET',
                        success: function (data) {
                            $("#edit_house_modal").dialog({
                                autoOpen: true,
                                open: function (event, ui) {
                                localStorage.setItem('lugar','edit_directo');
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
                                       localStorage.removeItem('lugar');
                                           $(this).dialog("close");
                                       },
                                   },
                       {
                           text: "Modificar",
                           class: "btn btn-primary boton-modificar-directo",
                           style: "width:100px",
                           click: function () {
                            if (confirm('¿Confirma la acción de modificar el H B/L?')) {
                                $('#edit_house_form').trigger('submit'); // Dispara el evento submit del formulario
                            }

                           },
                       },
                                ],
                                beforeClose: function (event, ui) {
                                localStorage.removeItem('lugar');
                                try {
                                desbloquearDatos();
                            } catch (error) {
                                console.error("⚠️ Error en desbloquearDatos:", error);
                            }
                                }

                            });

                            fillFormWithDataHouse(data);
                            if(data.bloqueado){
                                alert(data.mensaje);
                                $('.boton-modificar-directo').prop('disabled',true);
                            } else{
                                $('.boton-modificar-directo').prop('disabled',false);
                            }
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
    $('#tabla_house_directo_it tbody').off('click').on('click', 'tr', function (event) {
                event.stopPropagation();
                if ($(this).hasClass('table-secondary')) {
                } else {
                    $('#tabla_house_directo_it tbody tr').removeClass('table-secondary');
                    $(this).addClass('table-secondary');
                }

                var table = $('#tabla_house_directo_it').DataTable();
                var row = table.row($(this));
                var rowData = row.data();

                if (rowData) {
                    var selectedRowId = rowData[0];
                    var selectedRowN = rowData[3];
                    localStorage.setItem('id_house_gasto', selectedRowId);
                    localStorage.setItem('num_house_gasto', selectedRowN);
        localStorage.setItem('tabla_origen', 'tabla_house_directo_it');

                    localStorage.setItem('clase_house', 'IT');

                }
            });
    //add house
    $('#nuevo_directo').click(function () {
        $("#add_house_modal").dialog({
                    autoOpen: true,
                    open: function (event, ui) {
                    localStorage.setItem('lugar_editar','edit_directo');
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
                           localStorage.removeItem('lugar');
                               $(this).dialog("close");
                           },
                       },

                    ],
                    beforeClose: function (event, ui) {
                    localStorage.removeItem('lugar_editar');
                    }
                });
if (!$('#id_awbhijo').val()) {
    $('#id_awbhijo').val(0);
}

                generar_posicion();
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
    //importar house
        $('#nuevo_directo_importado').click(function () {
        localStorage.setItem('lugar_importarhijo','directo');
            importar_hijo_tabla_directo();

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
                  localStorage.removeItem('lugar_importarhijo');
                }
            });
        });
    //mails
        $('.email2').click(function () {

    $("#modalSeleccionEmailHouse10").dialog('close');
                let id = localStorage.getItem('id_house_gasto');
                let numero = localStorage.getItem('num_house_gasto');

                let title = this.getAttribute('data-tt');
                var row = $('#tabla_house_directo_it').DataTable().rows('.table-secondary').data();
                $("#id_to").val('');
                $("#id_cc").val('');
                $("#id_cco").val('');
                cco = $("#id_subject").val('');
                $('#email_add_input').summernote('destroy');
                $("#arhivos_adjuntos").html('');
                archivos_adjuntos = {};
                let transportista=false;
                let master=false;
                let gastos = false;
                let directo = false;
                if(title=='Notificación de llegada de carga'){
                    if(confirm('¿Desea informar Máster?')){
                        master=true;
                    }
                    if(confirm('¿Desea informar Gastos?')){
                        gastos=true;
                    }
                }
                if(title=='Aviso de embarque'){
                    if(confirm('¿Desea informar Transportista?')){
                        transportista=true;
                    }
                    if(confirm('¿Desea informar Máster?')){
                        master=true;
                    }
                    if(confirm('¿Desea informar Gastos?')){
                        gastos=true;
                    }
                }
                        if(title=='Instruccion de embarque'){
            if(confirm('¿Desea informar Transportista?')){
                transportista=true;
            }
            if(confirm('¿Desea una instrucción Completa o Directa? Directa=Cancelar, Completa=Aceptar')){
                directo=true;
            }
        }
                        if(title=='Shipping instruction'){
            if(confirm('¿Desea informar Transportista?')){
                transportista=true;
            }
            if(confirm('¿Desea una instrucción Completa o Directa? Directa=Cancelar, Completa=Aceptar')){
                directo=true;
            }
        }
                if (row.length === 1) {
                    let selectedRowN= localStorage.getItem('num_house_gasto');

            $.ajax({
                url: '/importacion_terrestre/house-detail/',
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    get_data_email(row, title, numero, id, transportista, master, gastos, directo);
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
                                    $('#modalSeleccionEmail').dialog("close");

                                },
                            },],
                        beforeClose: function (event, ui) {
                            //  localStorage.removeItem('num_house_gasto');
                            $('#table_add_im tbody tr').removeClass('table-secondary');
                            $('#table_edit_im tbody tr').removeClass('table-secondary');
                            $('#tabla_house_directo_it tbody tr').removeClass('table-secondary');
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
})
function generar_posicion(){
    return $.ajax({
        type: "GET",
        url: "/importacion_terrestre/generar_posicion/",
        success: function(response) {
            $('#posicion_gh').val(response.posicion);
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
}
function eliminar_house_directo(){
    let selectedRowN= localStorage.getItem('num_house_gasto');

            $.ajax({
                url: '/importacion_terrestre/house-detail/',
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    if (confirm('¿Confirma eliminar seleccionado?')) {

                        let id = localStorage.getItem('num_house_gasto');
                        if (id) {
                            miurl = "/importacion_terrestre/eliminar_house/";
                            var toData = {
                                'id': id,
                                'csrfmiddlewaretoken': csrf_token,
                            };
                            $.ajax({
                                type: "POST",
                                url: miurl,
                                data: toData,
                                success: function (resultado) {
                                    aux = resultado['resultado'];
                                    if (aux === 'exito') {
                                        $('#tabla_house_directo_it').DataTable().ajax.reload(null, false);
                                        alert('Eliminado correctamente');
                                    } else {
                                        alert(aux);
                                    }
                                }
                            });
                        } else {
                            alert('Debe seleccionar un registro');
                        }
                    }

                }
            });
}
function importar_hijo_tabla_directo(){
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
            "url": "/importacion_terrestre/source_seguimientos_modo/IMPORT%20TERRESTRE/",
            'type': 'GET',
            "data": function (d) {
                console.log(d);
                return $.extend({}, d, {
                    "buscar": buscar,
                    "que_buscar": que_buscar,
                });
            }
        },
        "language": {
            url: "/static/datatables/es_ES.json"
        },
       "rowCallback": function (row, data) {
        let seleccionados = JSON.parse(localStorage.getItem('seleccionados')) || [];

        if (seleccionados.includes(data[0])) {
            $(row).addClass('highlighted');
            $(row).find('.checkbox_seleccion').prop('checked', true);
        } else {
            $(row).removeClass('highlighted');
            $(row).find('.checkbox_seleccion').prop('checked', false);
        }


        $(row).find('.checkbox_seleccion').off('change').on('change', function () {
            let id = $(this).val();
            let seleccionados = JSON.parse(localStorage.getItem('seleccionados')) || [];

            if (this.checked) {
                if (!seleccionados.includes(id)) {
                    seleccionados.push(id);
                }
                $(row).addClass('highlighted');
            } else {
                seleccionados = seleccionados.filter(item => item !== id);
                $(row).removeClass('highlighted');
            }

            localStorage.setItem('seleccionados', JSON.stringify(seleccionados));
        });
    }
    });
}
function guardar_importado_house_directo(data, seguimientos) {
    //agregar campo consolidado al data
    let dataConsolidado = data.map(function(item) {
    return { ...item, consolidado: 1 };
    });
    $.ajax({
        url: '/importacion_terrestre/add_house_importado/',
        type: 'POST',
        data: JSON.stringify(dataConsolidado),
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
                //traer embarques
                alert('House/s importado/s con éxito');
                $("#importar_hijo_modal").dialog('close');
                $('#tabla_seguimiento_IH').DataTable().destroy();
                $('#tabla_house_directo_it').DataTable().ajax.reload(null, false);
                localStorage.removeItem('seleccionados');
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

function get_datos_logs_h() {
let selectedRowN = localStorage.getItem('num_house_gasto');

            $.ajax({
                url: '/importacion_terrestre/house-detail/',
                data: {id: selectedRowN},
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    row = table.rows('.table-secondary').data();
                    console.log(row);
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
                            try {
                                desbloquearDatos();
                            } catch (error) {
                                console.error("⚠️ Error en desbloquearDatos:", error);
                            }
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
                                "url": "/importacion_terrestre/source_logs/",
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
function abrir_modal_mails_d(e){
    e.preventDefault();

    let row = table.rows('.table-secondary').data();
    if (row.length !== 1) {
        alert('Debe seleccionar un embarque primero.');
        return;
    }

    $("#modalSeleccionEmailHouse10").dialog('open');
}
function modal_buscar_directos(){
$("#searchModalDirecto").dialog({
        autoOpen: true,
        modal: true,
        width: 400,
        buttons: [
            {
                text: "Buscar",
                class: "btn btn-success",
                click: function(e) {
                    let formData = $("#searchFormDirecto").serialize();
                    filtrar_tabla_houses(formData,e);
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

function filtrar_tabla_houses(data, e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: '/importacion_terrestre/buscar_registros_directos/',
        data: $("#searchFormDirecto").serialize(),
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function(response) {
            // numeros = response.resultados;
            table.ajax.reload();
        },
        error: function(xhr, status, error) {
            console.error("Error al obtener AWB:", error);
        }
    });
}