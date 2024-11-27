$(document).ready(function() {


    $("input[name='paymentType']").on("change", function () {
    $(".payment-section").addClass("d-none");
    const selectedSection = `#${$(this).val()}Section`;
    $(selectedSection).removeClass("d-none");
  });
  $("#cashSection").removeClass("d-none");

    var buscar = '';
    var que_buscar = '';
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

    $('#cliente_cobranza').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/admin_cont/buscar_cliente",
                dataType: 'json',
                data: { term: request.term },
                success: function(data) {
                    response(data.map(cliente => ({
                        label: cliente.text,
                        value: cliente.text,
                        id: cliente.id
                    })));
                },
                error: xhr => console.error('Error al buscar clientes:', xhr)
            });
        },
        minLength: 2,
        appendTo: "#dialog-form",
        select: function(event, ui) {
            const { id } = ui.item;
        tabla_facturas_pendientes(id);
        }
    });


$('#id_importe').on('focusout', function () {
    let importe = parseFloat($(this).val()) || 0;
    let acumulado=$('#acumulado').val();

    if (importe < 0) {
        alert('El importe no puede ser negativo.');
        $(this).val('');
        return;
    }

    let resultado = parseFloat($('#a_imputar').val()) || 0;
    if(acumulado!=0){
    resultado = importe - acumulado;
    }else{
    resultado=importe;
    }

    $('#a_imputar').val(resultado);
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
        width: wWidth * 0.60,
        height: wHeight * 0.90,
        buttons: [
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

function abrir_forma_pago() {
  $("#paymentModal").dialog({
    autoOpen: true,
    modal: true,
    width: $(window).width() * 0.6,
    height: $(window).height() * 0.9,
    buttons: [
      {
        text: "Salir",
        class: "btn btn-secondary",
        click: function () {
          $(this).dialog("close");
        },
      },
      {
        text: "Grabar",
        class: "btn btn-primary",
        click: function () {
          alert("Datos guardados");
        },
      },
    ],
  });

  // Manejo de los botones de radio para mostrar las secciones correspondientes
  $("input[name='paymentType']").on("change", function () {
    $(".payment-section").hide(); // Oculta todas las secciones
    const selectedSection = `#${$(this).val()}Section`;
    $(selectedSection).show(); // Muestra la sección seleccionada
  });

  // Mostrar por defecto la sección de efectivo
  $("#cashSection").show();
}

//llamar cuando se seleccione un cliente
function tabla_facturas_pendientes(cliente) {
    if ($.fn.DataTable.isDataTable('#imputacionTable')) {
        $('#imputacionTable').DataTable().clear().destroy();
    }

    const table = $('#imputacionTable').DataTable({
        serverSide: true,
        ajax: {
            url: "/admin_cont/source_facturas_pendientes",
            type: "GET",
            data: function (d) {
                d.cliente = cliente;
            }
        },
        columns: [
            { data: 'id', visible: false }, // Oculto
            { data: 'vencimiento' },
            { data: 'emision' },
            { data: 'documento' },
            { data: 'total' },
            { data: 'saldo' },
            { data: 'imputado' },
            { data: 'tipo_cambio' },
            { data: 'embarque' },
            { data: 'detalle' },
            { data: 'posicion' },
            { data: 'moneda' },
            { data: 'paridad' },
            { data: 'tipo_doc' }
        ],
        responsive: true,
        processing: true,
        lengthChange: false,
        language: {
            url: "//cdn.datatables.net/plug-ins/1.10.24/i18n/Spanish.json"
        }
    });

    // Manejar selección de filas
    $('#imputacionTable tbody').on('click', 'tr', function () {
        $(this).toggleClass('selected');
    });


    $('#imputarSeleccion').on('click', function () {
    const seleccionadas = table.rows('.selected'); // Obtener las filas seleccionadas
    const data = seleccionadas.data().toArray(); // Convertir a array para depuración
    let importe = parseFloat($('#id_importe').val()) || 0; // Obtener el importe disponible
    let imputado = parseFloat($('#a_imputar').val()) || 0; // Obtener el importe disponible
    let acumulado = 0;

    if(seleccionadas.count()<1){
    alert('Debe seleccionar al menos una fila.');
    return;
    }

    if(importe<=0){
    alert('Digite un importe.');
    return;
    }

    let imputar=$('#a_imputar').val();
    if(imputar==0){
    alert('No hay más dinero disponible. Aumente el importe.');
    return;
    }


    seleccionadas.nodes().each(function (node) {
        let saldo = parseFloat(table.cell(node, 5).data()) || 0;
        acumulado += saldo;
    });

    if (seleccionadas.count() > 1 && importe < acumulado) {
        alert('No alcanza el importe para cubrir la selección. Seleccione de a una para hacer pagos parciales.');
        seleccionadas.nodes().to$().removeClass('selected');
        return;
    }

    if (seleccionadas.count() === 1 && imputado< acumulado) {
        seleccionadas.nodes().each(function (node) {
            let saldo = parseFloat(table.cell(node, 5).data()) || 0;
            let imputadoActual = parseFloat(table.cell(node, 6).data()) || 0;

            let resto = saldo - imputado; // Calcular el saldo restante
            table.cell(node, 5).data(resto.toFixed(2)); // Actualizar la columna 5 con el saldo restante
            table.cell(node, 6).data(imputadoActual + imputado); // Actualizar la columna 6 con el importe imputado

            $(table.cell(node, 5).node()).css('background-color', '#fcec3f'); // Amarillo para columna 5
            $(table.cell(node, 6).node()).css('background-color', '#fcec3f'); // Amarillo para columna 6

        });
        seleccionadas.nodes().to$().removeClass('selected');

        $('#a_imputar').val(0);
        let ac=parseFloat($('#acumulado').val());
        ac=ac+imputado;
        $('#acumulado').val(ac);
        return;
    }

    seleccionadas.nodes().each(function (node) {
        let saldo = parseFloat(table.cell(node, 5).data()) || 0;
        let imputadoActual = parseFloat(table.cell(node, 6).data()) || 0;

        table.cell(node, 6).data(imputadoActual + saldo); // Columna 6
        table.cell(node, 5).data(0); // Columna 5

        $(table.cell(node, 5).node()).css('background-color', '#fcec3f'); // Amarillo para columna 5
        $(table.cell(node, 6).node()).css('background-color', '#fcec3f'); // Amarillo para columna 6
        seleccionadas.nodes().to$().removeClass('selected');
    });

    const total = importe - acumulado;
    let ac=parseFloat($('#acumulado').val());
    ac=ac+acumulado;
    $('#acumulado').val(ac);
    $('#a_imputar').val(total);

});


}


function obtenerFilasSeleccionadas() {
    const table = $('#imputacionTable').DataTable();
    const seleccionadas = table.rows('.selected').data().toArray();
    return seleccionadas;
}



