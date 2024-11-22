$(document).ready(function() {
    $('#cliente').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/admin_cont/buscar_cliente", // Endpoint para buscar clientes
                dataType: 'json',
                data: { term: request.term }, // Término buscado
                success: function(data) {
                    response(data.map(cliente => ({
                        label: cliente.text, // Lo que se muestra en el menú de autocompletado
                        value: cliente.text, // Lo que se llena en el campo
                        id: cliente.id // ID único del cliente
                    })));
                },
                error: function(xhr) {
                    console.error('Error al buscar clientes:', xhr);
                }
            });
        },
        minLength: 2, // Longitud mínima para buscar
        appendTo: "#dialog-form", // Asegura que el menú de autocompletar esté dentro del modal
        select: function(event, ui) {
            const { id } = ui.item; // Obtener el ID seleccionado

            // Hacer una solicitud para obtener detalles del cliente seleccionado
            $.ajax({
                url: "/admin_cont/buscar_clientes",
                data: { id }, // Enviar el ID seleccionado
                dataType: 'json',
                success: function(cliente) {
                    // Crear una fila en la tabla con los detalles del cliente
                    const row = `
                        <tr id="cliente-${id}">
                            <td class="d-none">${cliente.codigo}</td>
                            <td>${cliente.empresa}</td>
                            <td>${cliente.ruc}</td>
                        </tr>`;
                    // Agregar la fila a la tabla y mostrarla
                    $('#clienteTable tbody').html(row);
                    $('#clienteTable').show();
                },
                error: function(xhr) {
                    console.error('Error al obtener los detalles del cliente:', xhr);
                }
            });
        }
    });

    var buscar = '';
    var que_buscar = '';
    //buscadores tabla facturas
    let contador = 0;
    $('#tabla_cobranzas tfoot th').each(function () {
        let title = $(this).text();
        if (title !== '') {
            $(this).html('<input type="text" class="form-control"  autocomplete="off" id="buscoid_' + contador + '" type="text" placeholder="Buscar ' + title + '"  autocomplete="off" />');
            contador++;
        } else {
            $(this).html('<button class="btn" title="Borrar filtros" id="clear" ><span class="glyphicon glyphicon-erase"></span></button> ');
        }
    });
    //tabla general master
    table = $('#tabla_cobranzas').DataTable({
    "stateSave": true,
    "dom": 'Btlipr',
    "scrollX": true,
    "bAutoWidth": false,
    "scrollY": wHeight * 0.60,
    "columnDefs": [
        {
            "targets": [0],
            "className": '',
            "orderable": false,
            "data": null,
            "defaultContent": '',
            render: function (data, type, row) { }
        },
        {
            "targets": [1],
            "className": 'derecha archivos',
        },
        // Más definiciones de columnas...
    ],
    "order": [[1, "desc"]],
    "processing": true,
    "serverSide": true,
    "pageLength": 100,
    "ajax": {
        "url": "/admin_cont/source_facturacion/",
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
                    that.search(this.value).draw();
                }
            });
        });
    },
    "rowCallback": function (row, data) {}
});
});
/* INITIAL CONTROL PAGE */
var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;


function abrir_cobranza() {
    $("#dialog-form").dialog({
        autoOpen: true,
        modal: true,
        width: wWidth * 0.90,
        height: wHeight * 0.90,
        buttons: [
            {
                class: "btn btn-dark",
                style: "width:100px",
                text: "Guardar",
                click: function() {
                    // Lógica para guardar
                    $("#cobranzaForm").submit();
                }
            },
            {
                class: "btn btn-dark",
                style: "width:100px",
                text: "Salir",
                click: function() {
                    $(this).dialog("close");
                }
            }
        ]
    }).prev('.ui-dialog-titlebar').remove();
}

function tabla_para_imputar(){
    $('#imputacionTable').DataTable({
        "stateSave": true,
        "dom": 'Btlipr',
        "scrollX": true,
        "bAutoWidth": false,
        "scrollY": $(window).height() * 0.60,
        "columnDefs": [
            {
                "targets": [0],
                "className": 'text-left',
                "data": 'vencimiento',
                "title": 'Vencimiento'
            },
            {
                "targets": [1],
                "className": 'text-left',
                "data": 'emision',
                "title": 'Emisión'
            },
            {
                "targets": [2],
                "className": 'text-left',
                "data": 'documento',
                "title": 'Documento'
            },
            {
                "targets": [3],
                "className": 'text-left',
                "data": 'total',
                "title": 'Total'
            },
            {
                "targets": [4],
                "className": 'text-left',
                "data": 'saldo',
                "title": 'Saldo'
            },
            {
                "targets": [5],
                "className": 'text-left',
                "data": 'imputado',
                "title": 'Imputado'
            },
            {
                "targets": [6],
                "className": 'text-center',
                "data": 't_cambio',
                "title": 'T. Cambio'
            },
            {
                "targets": [7],
                "className": 'text-left',
                "data": 'embarque',
                "title": 'Embarque'
            },
            {
                "targets": [8],
                "className": 'text-left',
                "data": 'detalle',
                "title": 'Detalle'
            },
            {
                "targets": [9],
                "className": 'text-left',
                "data": 'posicion',
                "title": 'Posición'
            },
            {
                "targets": [10],
                "className": 'text-left',
                "data": 'moneda',
                "title": 'Moneda'
            },
            {
                "targets": [11],
                "className": 'text-left',
                "data": 'paridad',
                "title": 'Paridad'
            },
            {
                "targets": [12],
                "className": 'text-left',
                "data": 'tipo_doc',
                "title": 'Tipo documento'
            }
        ],
        "order": [[0, "desc"]],
        "processing": true,
        "serverSide": true,
        "pageLength": 100,
        "ajax": {
            "url": "/admin_cont/source_cobranza/",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "cliente": $('#socio_com_filtro').val()
                });
            }
        },
        "language": {
            "url": "/static/datatables/es_ES.json"
        }
    });
}
