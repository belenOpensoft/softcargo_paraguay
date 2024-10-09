$(document).ready(function () {
  let contador = 0;
//  $.ajax({
//    type: "GET",
//    url: "/importacion_maritima/source_archivos/",
//    success: function(response) {
//        console.log(response);
//    },
//    error: function(error) {
//        console.log('Error:', error);
//    }
//});
    //buscadores
    $('#tabla_house_directo tfoot th').each(function () {
        let title = $(this).text();
        if (title !== '') {
            $(this).html('<input type="text" class="form-control" autocomplete="off" id="buscoid_' + contador + '" placeholder="Buscar ' + title + '" />');
            contador++;
        } else {
            $(this).html('<button class="btn" title="Borrar filtros" id="clear"><span class="glyphicon glyphicon-erase"></span></button>');
        }
    });
    // Tabla general
    table = $('#tabla_house_directo').DataTable({
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
            "url": "/importacion_maritima/source_embarque_consolidado/",
            'type': 'GET',
            "data": function (d) {
                // Obtener los valores de búsqueda de los inputs del footer
                $('#tabla_house_directo tfoot input').each(function() {
                    const index = $(this).parent().index();  // Obtener el índice de la columna
                    d['columns[' + index + '][search][value]'] = this.value;  // Asignar el valor de búsqueda
                });

                return $.extend({}, d, {
                    "buscar": buscar,
                    "que_buscar": que_buscar
                });
            }
        },
        "columnDefs": [
            { "orderable": true, "targets": "_all" }
        ],
        "language": {
            url: "/static/datatables/es_ES.json"
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
    $('#tabla_house_directo tbody').off('dblclick').on('dblclick', 'tr', function () {
                    var table = $('#tabla_house_directo').DataTable();
                    var row = table.row($(this));
                    var rowData = row.data();

                    if (rowData) {
                        var selectedRowId = rowData[3];
                        localStorage.setItem('numero_embarque', selectedRowId);

                        $.ajax({
                        url: '/importacion_maritima/house-detail',
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

                                ],
                                beforeClose: function (event, ui) {
                                localStorage.removeItem('lugar');
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
    $('#tabla_house_directo tbody').off('click').on('click', 'tr', function (event) {
                event.stopPropagation();
                if ($(this).hasClass('table-secondary')) {
                } else {
                    $('#tabla_house_directo tbody tr').removeClass('table-secondary');
                    $(this).addClass('table-secondary');
                }

                var table = $('#tabla_house_directo').DataTable();
                var row = table.row($(this));
                var rowData = row.data();

                if (rowData) {
                    var selectedRowId = rowData[0];
                    var selectedRowN = rowData[3];
                    localStorage.setItem('id_house_gasto', selectedRowId);
                    localStorage.setItem('num_house_gasto', selectedRowN);
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
                $("td:contains('Master')").css('visibility', 'hidden');
                $('#id_awbhijo').css('display','none');
                $('#id_awbhijo').val(0);
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
                let id = localStorage.getItem('id_house_gasto');
                let numero = localStorage.getItem('num_house_gasto');

                let title = this.getAttribute('data-tt');
                var row = $('#tabla_house_directo').DataTable().rows('.table-secondary').data();
                $("#id_to").val('');
                $("#id_cc").val('');
                $("#id_cco").val('');
                cco = $("#id_subject").val('');
                $('#email_add_input').summernote('destroy');
                $("#arhivos_adjuntos").html('');
                archivos_adjuntos = {};
                if (row.length === 1) {
                    get_data_email(row,title,numero,id);
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
                        title:   title  + " para el house N°: " + numero,
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
                                    sendEmail(to,cc,cco,subject,message,title,numero);
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
                        localStorage.removeItem('num_house_gasto');
                        $('#table_add_im tbody tr').removeClass('table-secondary');
                        $('#table_edit_im tbody tr').removeClass('table-secondary');
                        $('#tabla_house_directo tbody tr').removeClass('table-secondary');
                        }
                    })
                } else {
                    alert('Debe seleccionar al menos un registro');
                }
            });
})
function generar_posicion(){
    return $.ajax({
        type: "GET",
        url: "/importacion_maritima/generar_posicion/",
        success: function(response) {
            $('#posicion_gh').val(response.posicion);
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
}
function eliminar_house_directo(){
if (confirm('¿Confirma eliminar seleccionado?')) {

      let id= localStorage.getItem('id_house_gasto');
        if (id) {
            miurl = "/importacion_maritima/eliminar_house/";
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
                           $('#tabla_house_directo').DataTable().ajax.reload(null, false);
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
function importar_hijo_tabla_directo(){
table_seg = $('#tabla_seguimiento_IH').DataTable({
//        "stateSave": true,
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
            "url": "/importacion_maritima/source_seguimientos_modo/IMPORT%20MARITIMO/",
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
        url: '/importacion_maritima/add_house_importado/',
        type: 'POST',
        data: JSON.stringify(dataConsolidado),
        contentType: 'application/json',
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (response) {
            if (response.success) {
                traer_gastos_importado(seguimientos, response.numeros_guardados);
                traer_envases_importado(seguimientos,response.numeros_guardados);
                traer_rutas_importado(seguimientos, response.numeros_guardados);
                traer_embarques_importado(seguimientos, response.numeros_guardados);
                traer_archivos_importado(seguimientos, response.numeros_guardados);
                //traer embarques
                alert('House/s importado/s con éxito');
                $("#importar_hijo_modal").dialog('close');
                $('#tabla_seguimiento_IH').DataTable().destroy();
                $('#tabla_house_directo').DataTable().ajax.reload(null, false);
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