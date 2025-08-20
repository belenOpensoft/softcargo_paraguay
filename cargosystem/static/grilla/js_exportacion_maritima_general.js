let table_general_em;
let numeros_general=[];
$(document).ready(function () {
    $(document).on("click", "#clear", function() {
        awbRegex = '';
        $(".filter-input").val("").trigger("keyup");
        $(".filter-input").removeClass("is-invalid");
        table_general_em.ajax.reload();
    });

    // Evento para resaltar los inputs cuando tienen contenido
    $(document).on("input", ".filter-input", function() {
        if ($(this).val().trim() !== "") {
            $(this).addClass("is-invalid");
        } else {
            $(this).removeClass("is-invalid");
        }
    });

    // tabla general master
    table_general_em = $('#tabla_general_em').DataTable({
        "stateSave": true,
        "dom": 'Btlipr',
        "scrollX": true,
        "bAutoWidth": false,
        "scrollY": wHeight * 0.60,
        "columnDefs": [
            {
                "targets": [0],
                "orderable": false,
                "defaultContent": '',
                render: function (data, type, row) {
                    return `<span class="badge bg-primary text-light">${row[19] ?? ''}</span>`;
                }
            },

            {
                "targets": [11, 10, 12],
                "visible": false
            }
        ],
        "order": [[0, "desc"]],
        "processing": true,
        "serverSide": true,
        "pageLength": 100,
        "ajax": {
            "url": "/exportacion_maritima/source_embarques_general",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "numeros": JSON.stringify(numeros_general)

                });
            }
        },
        "language": {
            url: "/static/datatables/es_ES.json"
        },
        initComplete: function () {
            let api = this.api();

            let state = table_general_em.state.loaded();
            if (state) {
                api.columns().every(function(index) {
                    let colState = state.columns[index];
                    if (colState && colState.search.search) {
                        let input = $('#buscoid_' + index);
                        input.val(colState.search.search);
                        if (colState.search.search.trim() !== "") {
                            input.addClass("is-invalid");
                        }
                    }
                });
            }

            $(document).on("input", ".filter-input", function() {
                if ($(this).val().trim() !== "") {
                    $(this).addClass("is-invalid");
                } else {
                    $(this).removeClass("is-invalid");
                }
            });

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
        $('td:eq(1)', row).html('');
            let texto = ''
            if (data[13] > 0) {
            //archivo
                texto += ' <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-filetype-docx" viewBox="0 0 16 16"' +
                            '><path fill-rule="evenodd" d="M14 4.5V11h-1V4.5h-2A1.5 1.5 0 0 1 9.5 3V1H4a1 1 0 0 0-1 1v9H2V2a2 2 0 0 1 2-2h5.5L14 4.5Zm-6.839 9.688v-.522a1.54 1.54 0 0 0-.117-.641.861.861 0 0 0-.322-.387.862.862 0 0 0-.469-.129.868.868 0 0 0-.471.13.868.868 0 0 0-.32.386 1.54 1.54 0 0 0-.117.641v.522c0 .256.04.47.117.641a.868.868 0 0 0 .32.387.883.883 0 0 0 .471.126.877.877 0 0 0 .469-.126.861.861 0 0 0 .322-.386 1.55 1.55 0 0 0 .117-.642Zm.803-.516v.513c0 .375-.068.7-.205.973a1.47 1.47 0 0 1-.589.627c-.254.144-.56.216-.917.216a1.86 1.86 0 0 1-.92-.216 1.463 1.463 0 0 1-.589-.627 2.151 2.151 0 0 1-.205-.973v-.513c0-.379.069-.704.205-.975.137-.274.333-.483.59-.627.257-.147.564-.22.92-.22.357 0 .662.073.916.22.256.146.452.356.59.63.136.271.204.595.204.972ZM1 15.925v-3.999h1.459c.406 0 .741.078 1.005.235.264.156.46.382.589.68.13.296.196.655.196 1.074 0 .422-.065.784-.196 1.084-.131.301-.33.53-.595.689-.264.158-.597.237-.999.237H1Zm1.354-3.354H1.79v2.707h.563c.185 0 .346-.028.483-.082a.8.8 0 0 0 .334-.252c.088-.114.153-.254.196-.422a2.3 2.3 0 0 0 .068-.592c0-.3-.04-.552-.118-.753a.89.89 0 0 0-.354-.454c-.158-.102-.361-.152-.61-.152Zm6.756 1.116c0-.248.034-.46.103-.633a.868.868 0 0 1 .301-.398.814.814 0 0 1 .475-.138c.15 0 .283.032.398.097a.7.7 0 0 1 .273.26.85.85 0 0 1 .12.381h.765v-.073a1.33 1.33 0 0 0-.466-.964 1.44 1.44 0 0 0-.49-.272 1.836 1.836 0 0 0-.606-.097c-.355 0-.66.074-.911.223-.25.148-.44.359-.571.633-.131.273-.197.6-.197.978v.498c0 .379.065.704.194.976.13.271.321.48.571.627.25.144.555.216.914.216.293 0 .555-.054.785-.164.23-.11.414-.26.551-.454a1.27 1.27 0 0 0 .226-.674v-.076h-.765a.8.8 0 0 1-.117.364.699.699 0 0 1-.273.248.874.874 0 0 1-.401.088.845.845 0 0 1-.478-.131.834.834 0 0 1-.298-.393 1.7 1.7 0 0 1-.103-.627v-.495Zm5.092-1.76h.894l-1.275 2.006 1.254 1.992h-.908l-.85-1.415h-.035l-.852 1.415h-.862l1.24-2.015-1.228-1.984h.932l.832 1.439h.035l.823-1.439Z"' +
                            '/></svg>';
            }
            if (data[14] > 0) {
            //embarque
            texto += '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-truck" viewBox="0 0 16 16">\n' +
                         '<path d="M0 3.5A1.5 1.5 0 0 1 1.5 2h9A1.5 1.5 0 0 1 12 3.5V5h1.02a1.5 1.5 0 0 1 1.17.563l1.481 1.85a1.5 1.5 0 0 1 .329.938V10.5a1.5 1.5 0 0 1-1.5 1.5H14a2 2 0 1 1-4 0H5a2 2 0 1 1-3.998-.085A1.5 1.5 0 0 1 0 10.5zm1.294 7.456A2 2 0 0 1 4.732 11h5.536a2 2 0 0 1 .732-.732V3.5a.5.5 0 0 0-.5-.5h-9a.5.5 0 0 0-.5.5v7a.5.5 0 0 0 .294.456M12 10a2 2 0 0 1 1.732 1h.768a.5.5 0 0 0 .5-.5V8.35a.5.5 0 0 0-.11-.312l-1.48-1.85A.5.5 0 0 0 13.02 6H12zm-9 1a1 1 0 1 0 0 2 1 1 0 0 0 0-2m9 0a1 1 0 1 0 0 2 1 1 0 0 0 0-2"/>\n' +
                         '</svg>';


            }
            if (data[15] > 0) {
            //envase
                texto += ' <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-box-seam" viewBox="0 0 16 16"' +
                            '><path d="M8.186 1.113a.5.5 0 0 0-.372 0L1.846 3.5l2.404.961L10.404 2l-2.218-.887zm3.564 1.426L5.596 5 8 5.961 14.154 3.5l-2.404-.' +
                            '961zm3.25 1.7-6.5 2.6v7.922l6.5-2.6V4.24zM7.5 14.762V6.838L1 4.239v7.923l6.5 2.6zM7.443.184a1.5 1.5 0 0 1 1.114 0l7.129 2.852A.5.5 0 0 1 16' +
                            ' 3.5v8.662a1 1 0 0 1-.629.928l-7.185 2.874a.5.5 0 0 1-.372 0L.63 13.09a1 1 0 0 1-.63-.928V3.5a.5.5 0 0 1 .314-.464L7.443.184z"/> </svg>';
            }
            if (data[16] > 0) {
            //gastos
                texto += '   <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-currency-dollar" viewBox="0 0 16 16"' +
                    '><path d="M4 10.781c.148 1.667 1.513 2.85 3.591 3.003V15h1.043v-1.216c2.27-.179 3.678-1.438 3.678-3.3 0-1.59-.947-2.51-2.956-3.028l-.722-.18' +
                    '7V3.467c1.122.11 1.879.714 2.07 1.616h1.47c-.166-1.6-1.54-2.748-3.54-2.875V1H7.591v1.233c-1.939.23-3.27 1.472-3.27 3.156 0 1.454.966 2.483 2.' +
                    '661 2.917l.61.162v4.031c-1.149-.17-1.94-.8-2.131-1.718H4zm3.391-3.836c-1.043-.263-1.6-.825-1.6-1.616 0-.944.704-1.641 1.8-1.828v3.495l-.2-.05z' +
                    'm1.591 1.872c1.287.323 1.852.859 1.852 1.769 0 1.097-.826 1.828-2.2 1.939V8.73l.348.086z"/>sss</svg>';
            }
            if (data[17] > 0) {
            //rutas
                texto += '   <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-geo-alt" viewBox="0 0 16 16">\n' +
                    '<path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"/>\n' +
                    '<path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>\n' +
                    '</svg>';
            }
            if (data[18] > 0) {
    //notas
            texto += '   <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-sticky" viewBox="0 0 16 16">\n' +
            '<path d="M2.5 1A1.5 1.5 0 0 0 1 2.5v11A1.5 1.5 0 0 0 2.5 15h6.086a1.5 1.5 0 0 0 1.06-.44l4.915-4.914A1.5 1.5 0 0 0 15 8.586V2.5A1.5 1.5 0 0 0 13.5 1zM2 2.5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 .5.5V8H9.5A1.5 1.5 0 0 0 8 9.5V14H2.5a.5.5 0 0 1-.5-.5zm7 11.293V9.5a.5.5 0 0 1 .5-.5h4.293z"/>\n' +
            '</svg>';

                }
            $('td:eq(1)', row).html(texto + " " + data[1]);

        },
    });

    table_general_em.columns().iterator('column', function (ctx, idx) {
        table_general_em.column(idx).nodes().to$().addClass('columna-acciones');
    });

    table_general_em.on('draw', function () {
        // Evento tras redibujado
    });

    $(table_general_em.table().container()).on('keyup', 'tfoot input', function () {
        $(this).addClass('is-invalid');
        table_general_em
            .column($(this).data('index'))
            .search(this.value)
            .draw();
    });

    $('#tabla_general_em tfoot th').each(function(index) {
        let title = $('#tabla_general_em thead th').eq(index).text();

        if (index === 0) {
            $(this).html('<button class="btn btn-danger" title="Borrar filtros" id="clear"><span class="glyphicon glyphicon-erase"></span> Limpiar</button>');
        } else if (title !== '') {
            $(this).html('<input type="text" class="form-control filter-input" autocomplete="off" id="buscoid_' + index + '" placeholder="Buscar ' + title + '" />');
        }
    });

    $('#tabla_general_em tbody').on('click', 'tr', function (event) {
        event.stopPropagation();

        if (!$(this).hasClass('table-secondary')) {
            $('#tabla_general_em tbody tr').removeClass('table-secondary');
            $(this).addClass('table-secondary');
        }
    });

    $('#tabla_general_em tbody').on('dblclick', 'tr', function() {
        var tr = $(this).closest('tr');
        var row = table_general_em.row(tr);
        var rowData = row.data();

        if (rowData) {
            var numero_embarque = rowData[10];
            var numero_reserva = rowData[11];
            var id_embarque = rowData[0];
            var id_master = rowData[12];
            var master = rowData[4];
            localStorage.setItem('tabla_origen', 'tabla_general_em');

            if (id_master && numero_reserva) {
                localStorage.setItem('id_master_editar', id_master);
                localStorage.setItem('master_editar', master);
                localStorage.setItem('numero_master_seleccionado', numero_reserva);
                localStorage.setItem('lugar_importarhijo', 'editmaster')

                editar_madre();
            } else {
                localStorage.setItem('num_house_gasto', numero_embarque);
                localStorage.setItem('id_house_gasto', id_embarque);
                localStorage.setItem('numero_embarque', id_embarque);

                editar_directo(numero_embarque);
            }
        }
    });

    $('#edit_house_form_general').submit(function(e){
        e.preventDefault();
        if(document.getElementById('arbitraje_house_e_general').value<0||document.getElementById('dias_demora_e_general').value<0){
    alert('No se admiten valores negativos en los campos numéricos.')
    }else{
        var numero = localStorage.getItem('num_house_gasto');
        var formData = $(this).serialize();
        $('#edit_house_form_general').attr('action', '/exportacion_maritima/edit_house/' + numero + '/');

        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: formData,
            dataType: 'json',
            success: function (response) {
                if (response.success) {
                    alert('Datos actualizados con éxito');
                    if(localStorage.getItem('fecha_editada_house')){
                        if(confirm('Desea modificar la fecha en los demás houses (si existen)?')){
                        modificar_fecha_retiro(1);
                        }else{
                        localStorage.removeItem('fecha_editada_house');
                        }
                    }
                    table_general_em.ajax.reload(null, false);

                  $('#edit_house_modal_general').dialog('close');
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

    $('#fecha_retiro_e_general').on('change', function() {

   let vector = JSON.parse(localStorage.getItem('fecha_editada_house')) || [];
    var nuevaFecha = $(this).val();
    let master = $('#id_awbhijo_e_general').val();

    let itemEncontrado = vector.find(item => item.master === master);

    if (!itemEncontrado) {
        vector.push({ master: master, fecha: nuevaFecha });
    } else {
        itemEncontrado.fecha = nuevaFecha;
    }
    localStorage.setItem('fecha_editada_house', JSON.stringify(vector));

});

    $("#armador_addh_e_general").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#armador_ih_e_general').val(ui.item['id']);
                 $('#armador_ih_e_general').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#armador_ih_e_general').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#armador_ih_e_general').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#vendedor_addh_e_general").autocomplete({
        source: '/autocomplete_vendedores/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#vendedor_ih_e_general').val(ui.item['id']);
                 $('#vendedor_ih_e_general').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#vendedor_ih_e_general').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#vendedor_ih_e_general').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#transportista_addh_e_general").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#transportista_ih_e_general').val(ui.item['id']);
                 $('#transportista_ih_e_general').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#transportista_ih_e_general').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#transportista_ih_e_general').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#consignatario_addh_e_general").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#consignatario_ih_e_general').val(ui.item['id']);
                 $('#consignatario_ih_e_general').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#consignatario_ih_e_general').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#consignatario_ih_e_general').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#agente_addh_e_general").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#agente_ih_e_general').val(ui.item['id']);
                 $('#agente_ih_e_general').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#agente_ih_e_general').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#agente_ih_e_general').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#cliente_addh_e_general").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#cliente_ih_e_general').val(ui.item['id']);
                 $('#cliente_ih_e_general').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#cliente_ih_e_general').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#embarcador_addh_e_general").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#embarcador_ih_e_general').val(ui.item['id']);
                 $('#embarcador_ih_e_general').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#embarcador_ih_e_general').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#embarcador_ih_e_general').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#agecompras_addh_e_general").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#agcompras_ih_e_general').val(ui.item['id']);
                 $('#agcompras_ih_e_general').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#agcompras_ih_e_general').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#agcompras_ih_e_general').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#ageventas_addh_e_general").autocomplete({
        source: '/autocomplete_clientes/',
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);
        },
        change: function (event, ui) {
            if (ui.item) {
                $(this).css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37'});
                 $('#agventas_ih_e_general').val(ui.item['id']);
                 $('#agventas_ih_e_general').css({"border-color": "#3D9A37", 'box-shadow': '0 0 0 0.1rem #3D9A37', 'font-size':'10px'});
            } else {
                $(this).val('');
                $('#agventas_ih_e_general').val('');
                $(this).css({"border-color": "", 'box-shadow': ''});
                $('#agventas_ih_e_general').css({"border-color": "", 'box-shadow': ''});
            }
        }
    });
    $("#loading_addh_e_general").autocomplete({
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
    $("#discharge_addh_e_general").autocomplete({
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
    $("#origen_addh_e_general").autocomplete({
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
    $("#destino_addh_e_general").autocomplete({
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


    //emails general
    $('.email3').click(function () {
            $("#modalSeleccionEmailHouse_general").dialog('close');
                let id = localStorage.getItem('id_house_gasto');
                let numero = localStorage.getItem('num_house_gasto');

                let title = this.getAttribute('data-tt');
                var row = null;
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
                }
                if(title=='Instruccion de embarque'){
                    if(confirm('¿Desea informar Transportista?')){
                        transportista=true;
                    }
                    if(confirm('¿Desea una instrucción Completa o Directa? Directa=Cancelar, Completa=Aceptar')){
                        directo=true;
                    }
                }
                let selectedRowN= localStorage.getItem('num_house_gasto');
                if (selectedRowN) {


            $.ajax({
                url: '/exportacion_maritima/house-detail/',
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
                            //localStorage.removeItem('num_house_gasto');
                            $('#table_add_im tbody tr').removeClass('table-secondary');
                            $('#table_edit_im tbody tr').removeClass('table-secondary');
                            $('#tabla_house_directo tbody tr').removeClass('table-secondary');
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
    $("#modalSeleccionEmailHouse_general").dialog({
        autoOpen: false,
        modal: true,
        width: 400,
        height: 400,
        resizable: false,
        draggable: false,
        title: 'Seleccione el tipo de aviso House',
        open: function (event, ui) {
            $(this).parent().css('overflow', 'hidden');
            $('#buscadorEmailsHouse_general').val('');
            $("#listaEmailsHouse_general tr").show();
        }
    });
    $('#buscadorEmailsHouse_general').on('keyup', function () {
    let valor = $(this).val().toLowerCase();
    $("#listaEmailsHouse_general tr").filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(valor) > -1);
    });

});
    $(document).on("submit", "#searchFormGeneral", function(e) {
        e.preventDefault();
        let formData = $(this).serialize();
        filtrar_tabla_general(formData, e);
        $("#searchModalGeneral").dialog("close");
    });

});

function editar_madre(){
    let selectedRowId = localStorage.getItem('id_master_editar');

    if (selectedRowId !== null) {
        $.ajax({
            url: '/exportacion_maritima/master-detail',
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
                                $('#table_edit_im').DataTable().destroy();
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
                    if ($.fn.dataTable.isDataTable('#tabla_importmarit')) {
                        $('#tabla_importmarit').DataTable().ajax.reload(null, false);
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
}

function editar_directo(selectedRowId) {
    $.ajax({
        url: '/exportacion_maritima/house-detail',
        data: {id: selectedRowId},
        method: 'GET',
        success: function (data) {
            $("#edit_house_modal_general").dialog({
                autoOpen: true,
                open: function (event, ui) {
                },
                modal: true,
                title: "Editar house",
                width: 'auto',  // Ajusta el ancho al contenido
                height: 'auto', // Ajusta la altura al contenido
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
                                $('#edit_house_form_general').trigger('submit');
                                console.log('asjhdjkasd');
                            }

                        },
                    },

                ],
                beforeClose: function (event, ui) {
                    localStorage.removeItem('fecha_editada_house');
                }

            });

            fillFormWithDataHouseGeneral(data);
        },
        error: function (xhr, status, error) {
            console.error("Error fetching data:", error);
        }
    });
}

function fillFormWithDataHouseGeneral(data) {
    // Campos visibles (nombres)
    $('#transportista_addh_e_general').val(!data.transportista_e || data.transportista_e === 0 ? '' : getNameById(data.transportista_e));
    $('#agente_addh_e_general').val(!data.agente_e || data.agente_e === 0 ? '' : getNameById(data.agente_e));
    $('#consignatario_addh_e_general').val(!data.consignatario_e || data.consignatario_e === 0 ? '' : getNameById(data.consignatario_e));
    $('#armador_addh_e_general').val(!data.armador_e || data.armador_e === 0 ? '' : getNameById(data.armador_e));
    $('#cliente_addh_e_general').val(!data.cliente_e || data.cliente_e === 0 ? '' : getNameById(data.cliente_e));
    $('#vendedor_addh_e_general').val(!data.vendedor_e || data.vendedor_e === 0 ? '' : getNameByIdVendedor(data.vendedor_e));
    $('#embarcador_addh_e_general').val(!data.embarcador_e || data.embarcador_e === 0 ? '' : getNameById(data.embarcador_e));
    $('#agecompras_addh_e_general').val(!data.agcompras_e || data.agcompras_e === 0 ? '' : getNameById(data.agcompras_e));
    $('#ageventas_addh_e_general').val(!data.agventas_e || data.agventas_e === 0 ? '' : getNameById(data.agventas_e));

    // Inputs ocultos (ids)
    $('#armador_ih_e_general').val(data.armador_e);
    $('#transportista_ih_e_general').val(data.transportista_e);
    $('#agente_ih_e_general').val(data.agente_e);
    $('#consignatario_ih_e_general').val(data.consignatario_e);
    $('#cliente_ih_e_general').val(data.cliente_e);
    $('#vendedor_ih_e_general').val(data.vendedor_e);
    $('#embarcador_ih_e_general').val(data.embarcador_e);
    $('#agcompras_ih_e_general').val(data.agcompras_e);
    $('#agventas_ih_e_general').val(data.agventas_e);

    // Otros datos
    $('#origen_addh_e_general').val(data.origen_e);
    $('#destino_addh_e_general').val(data.destino_e);
    $('#loading_addh_e_general').val(data.loading_e);
    $('#discharge_addh_e_general').val(data.discharge_e);
    $('#viaje_house_e_general').val(data.viaje_e);
    $('#vapor_addh_e_general').val(data.vapor_e);
    $('#dias_demora_e_general').val(data.demora_e);
    $('#moneda_e_general').val(data.moneda_e);
    $('#arbitraje_house_e_general').val(data.arbitraje_e);
    $('#pago_house_e_general').val(data.pagoflete_e);
    $('#id_pago_general').val(data.pagoflete_e);

    $('#status_h_e_general').val(data.status_e);
    $('#wreceipt_he_general').val(data.wreceipt_e);
    $('#id_awbhijo_e_general').val(data.awb_e);
    $('#house_addh_e_general').val(data.hawb_e);
    $('#posicion_gh_e_general').val(data.posicion_e);
    $('#operacion_editar_general').val(data.operacion_e);

    $('#eta_e_general').val(data.eta_e ? formatDateToYYYYMMDD(data.eta_e) : '');
    $('#etd_e_general').val(data.etd_e ? formatDateToYYYYMMDD(data.etd_e) : '');
}

// funcionalidades para el menu de directos en tabla general
function eliminar_house_general(){
    let selectedRowN= localStorage.getItem('num_house_gasto');

            $.ajax({
                url: '/importacion_martima/house-detail/',
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
                            miurl = "/exportacion_maritima/eliminar_house/";
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
                                        $('#tabla_general_em').DataTable().ajax.reload(null, false);
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
function gastos_btn_h_click_general(){
        let selectedRowN,url;

         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';


            $.ajax({
                url: '/exportacion_maritima/'+url,
                data: { id: selectedRowN },
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    $("#id_gasto_id_house").val('');
                    let selectedRowId = localStorage.getItem('id_house_gasto');
                    let selectedRowN = localStorage.getItem('num_house_gasto');
                    // let consignatario_code;
                    // if ($.fn.dataTable.isDataTable('#table_edit_im')) {
                    //     consignatario_code = $('#table_edit_im').DataTable().row('.table-secondary').data()[21];
                    // } else {
                    //     consignatario_code = $('#tabla_house_directo').DataTable().row('.table-secondary').data()[21];
                    // }
                    if (selectedRowN != null) {
                        get_datos_gastos_house();
                        $('#gastos_form_house').trigger("reset");
                        // $("#id_socio_h").val(consignatario_code);
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
                                                miurl = "/exportacion_maritima/eliminar_gasto_house/";
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
                                                            if ($.fn.DataTable.isDataTable('#table_add_im')) {
                                                                $('#table_add_im').DataTable().ajax.reload(null, false);
                                                            }

                                                            if ($.fn.DataTable.isDataTable('#table_edit_im')) {
                                                                $('#table_edit_im').DataTable().ajax.reload(null, false);
                                                            }
                                                            if ($.fn.DataTable.isDataTable('#tabla_house_directo')) {
                                                                $('#tabla_house_directo').DataTable().ajax.reload(null, false);
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
                                $("#tabla_gastos").dataTable().fnDestroy();
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
function rutas_btn_h_click_general(){
        let selectedRowN,url;

         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';

            $.ajax({
                url: '/exportacion_maritima/'+url,
                data: { id: selectedRowN },
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
                                                miurl = "/exportacion_maritima/eliminar_ruta_house/";
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
                                                            if ($.fn.DataTable.isDataTable('#table_add_im')) {
                                                                $('#table_add_im').DataTable().ajax.reload(null, false);
                                                            }

                                                            if ($.fn.DataTable.isDataTable('#table_edit_im')) {
                                                                $('#table_edit_im').DataTable().ajax.reload(null, false);
                                                            }
                                                            if ($.fn.DataTable.isDataTable('#tabla_house_directo')) {
                                                                $('#tabla_house_directo').DataTable().ajax.reload(null, false);
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
                                $("#table_rutas_house").dataTable().fnDestroy();
//                 $('#table_add_im tbody tr').removeClass('table-secondary');
//                $('#table_edit_im tbody tr').removeClass('table-secondary');
//                $('#tabla_house_directo_im tbody tr').removeClass('table-secondary');
                            }
                        })

                    } else {
                        alert('Debe seleccionar al menos un registro');
                    }
                }
            });
}
function envases_btn_h_click_general(){
        let selectedRowN,url;

         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';

            $.ajax({
                url: '/exportacion_maritima/'+url,
                data: { id: selectedRowN },
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    $("#id_envase_id").val('');
                    let selectedRowId = localStorage.getItem('id_house_gasto');
                    let selectedRowN = localStorage.getItem('num_house_gasto');

                    if (selectedRowN != null) {
                        get_datos_envases_house();
                        $('#envases_form_house').trigger("reset");
                        $("#envases_modal_house").dialog({
                            autoOpen: true,
                            open: function () {
                                document.getElementById('numero_envase').value = selectedRowN;
                            },
                            modal: true,
                            title: "Envases para el House N°: " + selectedRowN,
                            height: wHeight * 0.90,
                            width: wWidth * 0.70,
                            class: 'modal fade',
                            buttons: [
                                {
                                    text: "Eliminar",
                                    class: "btn btn-danger",
                                    style: "width:100px",
                                    click: function () {
                                        if (confirm('¿Confirma eliminar el seleccionado?')) {
                                            var row = $('#tabla_envases_house').DataTable().rows('.table-secondary').data();
                                            if (row.length === 1) {
                                                miurl = "/exportacion_maritima/eliminar_envases_house/";
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
                                                            $("#tabla_envases_house").dataTable().fnDestroy();
                                                            get_datos_envases_house();
                                                            alert('Eliminado correctamente');
                                                            if ($.fn.DataTable.isDataTable('#table_add_im')) {
                                                                $('#table_add_im').DataTable().ajax.reload(null, false);
                                                            }

                                                            if ($.fn.DataTable.isDataTable('#table_edit_im')) {
                                                                $('#table_edit_im').DataTable().ajax.reload(null, false);
                                                            }
                                                            if ($.fn.DataTable.isDataTable('#tabla_house_directo')) {
                                                                $('#tabla_house_directo').DataTable().ajax.reload(null, false);
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
                                $("#tabla_envases_house").dataTable().fnDestroy();
//                 $('#table_add_im tbody tr').removeClass('table-secondary');
//                $('#table_edit_im tbody tr').removeClass('table-secondary');
//                $('#'#tabla_house_directo' tbody tr').removeClass('table-secondary');
                            }
                        })
                        get_sugerencias_envases(selectedRowN);
                    } else {
                        alert('Debe seleccionar al menos un registro');
                    }
                }
            });
}
function embarques_btn_h_click_general(){
        let selectedRowN,url;

         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';
            $.ajax({
                url: '/exportacion_maritima/'+url,
                data: { id: selectedRowN },
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
                            width: wWidth * 0.70,
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
                                                miurl = "/exportacion_maritima/eliminar_embarques_house/";
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
                                                            if ($.fn.DataTable.isDataTable('#table_add_im')) {
                                                                $('#table_add_im').DataTable().ajax.reload(null, false);
                                                            }

                                                            if ($.fn.DataTable.isDataTable('#table_edit_im')) {
                                                                $('#table_edit_im').DataTable().ajax.reload(null, false);
                                                            }
                                                            if ($.fn.DataTable.isDataTable('#tabla_house_directo')) {
                                                                $('#tabla_house_directo').DataTable().ajax.reload(null, false);
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
//                 $('#table_add_im tbody tr').removeClass('table-secondary');
//                $('#table_edit_im tbody tr').removeClass('table-secondary');
//                $('#'#tabla_house_directo_im' tbody tr').removeClass('table-secondary');
                            }
                        })

                    } else {
                        alert('Debe seleccionar al menos un registro');
                    }
                }
            });
}
function archivos_btn_h_click_general(){
        let selectedRowN,url;

         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';
            $.ajax({
                url: '/exportacion_maritima/'+url,
                data: { id: selectedRowN },
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    $("#tabla_archivos").dataTable().fnDestroy();
                    // row = table.rows('.table-secondary').data();
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
                                        var url = '/exportacion_maritima/descargar_archivo/' + localStorage.getItem('id_archivo');  // Ruta de la vista que devuelve el archivo
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
                                            miurl = "/exportacion_maritima/eliminar_archivo/";
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
                                                        if ($.fn.DataTable.isDataTable('#table_add_im')) {
                                                            $('#table_add_im').DataTable().ajax.reload(null, false);
                                                        }

                                                        if ($.fn.DataTable.isDataTable('#table_edit_im')) {
                                                            $('#table_edit_im').DataTable().ajax.reload(null, false);
                                                        }
                                                        if ($.fn.DataTable.isDataTable('#tabla_house_directo')) {
                                                            $('#tabla_house_directo').DataTable().ajax.reload(null, false);
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

                        }
                    })
                }
            });
}
function pdf_btn_h_click_general(){
        let selectedRowN,url;

         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';

            $.ajax({
                url: '/exportacion_maritima/'+url,
                data: { id: selectedRowN },
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
function notas_house_general() {
        let selectedRowNM,url;

         selectedRowNM= localStorage.getItem('num_house_gasto');
         url='house-detail/';

            $.ajax({
                url: '/exportacion_maritima/'+url,
                data: { id: selectedRowNM },
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
//                 $('#table_add_im tbody tr').removeClass('table-secondary');
//                $('#table_edit_im tbody tr').removeClass('table-secondary');
//                $('#tabla_house_directotbody tr').removeClass('table-secondary');
                        }
                    })
                }
            });
}
function cargar_gastos_factura_general(callback){
        let selectedRowN,url;

         selectedRowN= localStorage.getItem('num_house_gasto');
         url='house-detail/';

            $.ajax({
                url: '/exportacion_maritima/'+url,
                data: { id: selectedRowN },
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    let numero = localStorage.getItem('num_house_gasto');

                    $("#facturar_table").dataTable().fnDestroy();
                    let tabla_factura = $('#facturar_table').DataTable({
                        info: false,
                        lengthChange: false,
                        "order": [[1, "desc"], [1, "desc"]],
                        "processing": true,
                        "serverSide": true,
                        "pageLength": 10,
                        "language": {
                            url: "/static/datatables/es_ES.json"
                        },
                        "ajax": {
                            "url": "/exportacion_maritima/source_gastos_house_preventa/",
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
                                        return "0.00";
                                    }
                                }
                            },
                            {
                                "data": null,
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
                            // Remover clases anteriores si hay
                            $(row).removeClass('fila-rojo fila-amarillo fila-verde');

                            const color = data[17];
                            if (color === 'ROJO') {
                                $(row).addClass('fila-rojo');
                            } else if (color === 'AMARILLO') {
                                $(row).addClass('fila-amarillo');
                            } else if(color === 'VERDE'){
                                $(row).addClass('fila-verde');
                            }

                            // Evento para resaltar fila seleccionada
                            $(row).off('click').on('click', function () {
                                $('#facturar_table tbody tr').removeClass('table-secondary');
                                $(this).addClass('table-secondary');

                                const valorColumna7 = $(row).find('td').eq(7).text().trim();
                                $('#concepto_detalle').prop('checked', valorColumna7 !== 'S/I');
                            });
                        }

                    });

                    setTimeout(function () {
                        callback();
                    }, 2000);
                }
            });
}
function abrir_modal_mails_d_general(e){
    e.preventDefault();

    let selectedRowN= localStorage.getItem('num_house_gasto');
    if (!selectedRowN) {
        alert('Debe seleccionar un embarque primero.');
        return;
    }


    $("#modalSeleccionEmailHouse_general").dialog('open');

}
function get_datos_logs_general() {
        let selectedRowN,url,selectedRowid;

         selectedRowN= localStorage.getItem('num_house_gasto');
         selectedRowid= localStorage.getItem('id_house_gasto');
         url='house-detail/';

            $.ajax({
                url: '/exportacion_maritima/'+url,
                data: { id: selectedRowN },
                type: 'GET',
                success: function (data) {
                    if (data.bloqueado) {
                        alert(data.mensaje);
                        return;
                    }
                    if (selectedRowN) {
                        $("#logs_modal").dialog({
                            autoOpen: true,
                            open: function () {

                            },
                            modal: true,
                            title: "Log de interacciones para en el embarque N°: " + selectedRowN,
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
                                "url": "/exportacion_maritima/source_logs/",
                                'type': 'GET',
                                "data": function (d) {
                                    return $.extend({}, d, {
                                        "id": selectedRowid, 'numero': selectedRowN
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
function modal_buscar_general(){
$("#searchModalGeneral").dialog({
        autoOpen: true,
        modal: true,
        width: 400,
        buttons: [
            {
                text: "Buscar",
                class: "btn btn-success",
                click: function(e) {
                    let formData = $("#searchFormGeneral").serialize();
                    filtrar_tabla_general(formData,e);
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
function filtrar_tabla_general(data, e) {
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: '/exportacion_maritima/buscar_registros_general/',
        data: $("#searchFormGeneral").serialize(),
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function(response) {
            // numeros_general = response.resultados;
            // console.log(numeros_general);
            table_general_em.ajax.reload();
        },
        error: function(xhr, status, error) {
            console.error("Error al obtener AWB:", error);
        }
    });
}