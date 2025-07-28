var table  = false;
var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;

$(document).ready(function() {

    $("#cliente-modal").dialog({
        autoOpen: false,
        width: 800,
        modal: true
    });
    $("#cliente-modal").tabs();

    $("#id_vendedor").autocomplete({
        source: '/autocomplete_vendedores/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
            $('#vendedor_input').val(ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#id_vendedor').val(ui.item['label']);
                 $('#id_vendedor').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#id_vendedor').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#id_vendedor').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    var contador = 1;


        $('#tabla_cliente tfoot th').each(function(index) {
            let title = $('#tabla_cliente thead th').eq(index).text();

            if (index === 0) {
                // Si es la primera columna, colocar el botón de limpiar filtros
                $(this).html('<button class="btn btn-danger" title="Borrar filtros" id="clear"><span class="glyphicon glyphicon-erase"></span> Limpiar</button>');
            } else if (title !== '') {
                // Agregar inputs de búsqueda en las demás columnas
                $(this).html('<input type="text" class="form-control filter-input" autocomplete="off" id="buscoid_' + index + '" placeholder="Buscar ' + title + '" />');
            }
        });
    // Inicializar DataTable
    table = $('#tabla_cliente').DataTable({
        "stateSave": true,
        "dom": 'Btlipr',
        "scrollX": true,
        "buttons": [
            {
                text: 'Agregar',
                action: function (e, dt, button, config) {
                    //window.location.replace("/agregar_socio_comercial");
                    $('#clienteform')[0].reset();
                    $("#cliente-modal").tabs("refresh");
                    $('#cliente-modal').dialog("open");
                    $('#id_socio').val('');
                }
            },
            {
            text: 'Modificar',
            action: function (e, dt, button, config) {
                if (row = table.row('.table-secondary').data()) {
                    var id_socio = row[0];  // ID del socio comercial seleccionado
                    console.log(id_socio);

                    // Hacer la petición AJAX para obtener los datos
                    $.ajax({
                        type: "GET",
                        url: "/modificar_socio_comercial/" + id_socio,  // Llama a la vista con el ID
                        success: function(response) {
                            if (response.status === "success") {
                                var formData = response.form_data;

                                // Llenar los campos del formulario con los datos recibidos
                                $("#id_socio").val(id_socio); // Asignar ID al campo oculto
                                $("#id_tipo").val(formData.tipo);
                                $("#id_empresa").val(formData.empresa);
                                $("#id_razonsocial").val(formData.razonsocial);
                                $("#id_direccion").val(formData.direccion);
                                $("#id_localidad").val(formData.localidad);
                                $("#id_cpostal").val(formData.cpostal);
                                $("#id_ruc").val(formData.ruc);
                                $("#id_telefono").val(formData.telefono);
                                $("#id_fecalta").val(formData.fecalta);
                                $("#id_contactos").val(formData.contactos);
                                $("#id_observaciones").val(formData.observaciones);
                                $("#ciudad-select").val(formData.ciudad);
                                $("#pais-select").val(formData.pais);
                                $("#id_activo").prop("checked", formData.activo);
                                $("#vendedor_input").val(formData.vendedor_input);
                                $("#id_vendedor").val(formData.vendedor);
                                $("#id_plazo").val(formData.plazo);
                                $("#id_limite").val(formData.limite);
                                $("#id_ctavta").val(formData.ctavta);
                                $("#id_ctacomp").val(formData.ctacomp);
                                $("#id_emailad").val(formData.emailad);
                                $("#id_emailem").val(formData.emailem);
                                $("#id_emailea").val(formData.emailea);
                                $("#id_emailet").val(formData.emailet);
                                $("#id_emailim").val(formData.emailim);
                                $("#id_emailia").val(formData.emailia);
                                $("#id_emailit").val(formData.emailit);
                                $("#id_prefijoguia").val(formData.prefijoguia);

                                // Actualizar las pestañas del modal
                                $("#cliente-modal").tabs("refresh");

                                // Abrir el modal
                                $('#cliente-modal').dialog("open");
                            } else {
                                alert(response.message);
                            }
                        },
                        error: function() {
                            alert("Ocurrió un error al obtener los datos del socio comercial.");
                        }
                    });
                } else {
                    alert('Debe seleccionar un registro');
                }
            }
        },

            {
                text: 'Eliminar',
                action: function (e, dt, button, config) {
                    if (row = table.row('.table-secondary').data()) {
                        if (confirm('Esta seguro de eliminar: ' + row[2])) {
                            var miurl = "/eliminar_socio_comercial";
                            var toData = { 'id': row[0] };
                            $.ajax({
                                type: "GET",
                                url: miurl,
                                data: toData,
                                success: function (resultado) {
                                    var aux = resultado['resultado'];
                                    if (aux == 'exito') {
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
            }
        ],
        "columnDefs": [
            {
                "targets": [0],
                "orderable": false,
                "data": null,
                "defaultContent": '',
                "visible": false
            },
            {
                "targets": [1]
            },
            {
                "targets": [2]
            },
            {
                "targets": [3]
            },
            {
                "targets": [4]
            },
            {
                "targets": [5]
            },
            {
                "targets": [6]
            },
            {
                "targets": [7]
            },
            {
                "targets": [8]
            },
            {
                "targets": [9], // Columna "Tipo"

            }
        ],
        "order": [[1, "asc"]],
        "processing": true,
        "serverSide": true,
        "ajax": "/source_socios_comerciales",
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

            // Apply the select filter
            $('#select_tipo').on('change', function() {
                var value = $(this).val();
                table.column(9).search(value).draw(); // Filtra por columna de tipo
            });
        },
        "drawCallback": function(settings) {
            // Callback al dibujar la tabla
        }
    });


    $(table.table().container()).on('keyup', 'tfoot input', function() {
        table.column($(this).data('index')).search(this.value).draw();
    });

    var state = table.state.loaded();
    if (state) {
        table.columns().eq(0).each(function(colIdx) {
            var colSearch = state.columns[colIdx].search;
            if (colSearch.search) {
                var aux = colSearch.search;
                document.getElementById('buscoid_' + colIdx).value = aux;
            }
        });
        table.draw();
    }

    $('#tabla_cliente tbody').on('click', 'tr', function() {
        if ($(this).hasClass('table-secondary')) {
            $(this).removeClass('table-secondary');
        } else {
            var row = table.row($(this).closest('tr')).data();
            table.$('tr.table-secondary').removeClass('table-secondary');
            $(this).addClass('table-secondary');
        }
    });

    $(".alert").delay(4000).slideUp(200, function() { $(this).alert('close'); });

     $('#tipo_filter').on('change', function() {
        var selectedTipo = $(this).val();
        table.column(9).search(selectedTipo).draw();
    });

    $("#id_emailad").on("blur", function() {
        var emailVal = $(this).val();
        if (emailVal.trim() !== "") {
            $("#id_emailem").val(emailVal);
            $("#id_emailea").val(emailVal);
            $("#id_emailet").val(emailVal);
            $("#id_emailim").val(emailVal);
            $("#id_emailia").val(emailVal);
            $("#id_emailit").val(emailVal);
        }
    });
});


function enviar_form(e){
    e.preventDefault();
    let id_socio=$('#id_socio').val();
    let url;
    if (id_socio){
    url="/modificar_socio_comercial/" + id_socio;
    }else{
    url="/agregar_socio_comercial";
    }


$.ajax({
    type: "POST",
    url: url,  // Agregar ID si es edición
    data: $('#clienteform').serialize(),
    success: function(response) {
        if (response.status === 'success') {
            alert(response.message);
            $('#cliente-modal').dialog("close");
            table.ajax.reload(); // Recargar la tabla
        } else {
            if (response.errors) {
                let errorMessages = "";
                $(".error-message").remove(); // Limpiar errores anteriores

                $.each(response.errors, function(field, errorList) {
                    let inputField = $(`[name="${field}"]`);
                    // Mostrar errores en los campos correspondientes
                    inputField.after(`<span class="error-message" style="color: red;">${errorList.join(", ")}</span>`);

                    errorMessages += `${field}: ${errorList.join(", ")}\n`;
                });

                alert("Errores en el formulario:\n" + errorMessages);
            } else {
                alert(response.message);
            }
        }
    },
    error: function() {
        alert("Ocurrió un error inesperado.");
    }
});

}


