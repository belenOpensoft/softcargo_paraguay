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

document.querySelector('#exampleTable tbody').addEventListener('click', function (e) {
    const row = e.target.closest('tr');
    if (row) {
        document.querySelectorAll('#exampleTable tbody tr').forEach(r => r.classList.remove('selected'));
        row.classList.add('selected');
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

function borrar_datos() {
    const selectedRow = document.querySelector('#exampleTable tbody tr.selected');

    if (selectedRow) {
        selectedRow.remove(); // Eliminar la fila seleccionada
    } else {
        alert('Por favor, selecciona una fila para borrar.');
    }
}

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
//        if ($.fn.DataTable.isDataTable('#imputacionTable')) {
//            $('#imputacionTable').DataTable().ajax.reload(null, false);
//        }
        },
      },
      {
        text: "Grabar",
        class: "btn btn-primary",
        click: function () {
          let acumulado=$('#accumulated').val();
          let monto=$('#amount').val();
//          if(acumulado>monto){
//          alert('El acumulado supera al importe. Revise.');
//          }else{
          crear_impuventa_asiento_movimiento();
          //alert("Datos guardados");
//          }
        },
      },
    ],
  });

  cargar_datos_formadepago();

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

    // Vector para almacenar las filas afectadas
    let filasAfectadas = [];

    if (seleccionadas.count() < 1) {
        alert('Debe seleccionar al menos una fila.');
        return;
    }

    if (importe <= 0) {
        alert('Digite un importe.');
        return;
    }

    let imputar = $('#a_imputar').val();
    if (imputar == 0) {
        alert('No hay más dinero disponible. Aumente el importe.');
        return;
    }

    // Calcular acumulado
    seleccionadas.nodes().each(function (node) {
        let saldo = parseFloat(table.cell(node, 5).data()) || 0;
        acumulado += saldo;
    });

    // Validar si el importe alcanza
    if (seleccionadas.count() > 1 && importe < acumulado) {
        alert('No alcanza el importe para cubrir la selección. Seleccione de a una para hacer pagos parciales.');
        seleccionadas.nodes().to$().removeClass('selected');
        return;
    }

    if (seleccionadas.count() === 1 && imputado < acumulado) {
        seleccionadas.nodes().each(function (node) {
            let saldo = parseFloat(table.cell(node, 5).data()) || 0;
            let imputadoActual = parseFloat(table.cell(node, 6).data()) || 0;

            let resto = saldo - imputado; // Calcular el saldo restante
            table.cell(node, 5).data(resto.toFixed(2)); // Actualizar la columna 5
            table.cell(node, 6).data(imputadoActual + imputado); // Actualizar la columna 6

            $(table.cell(node, 5).node()).css('background-color', '#fcec3f'); // Amarillo para columna 5
            $(table.cell(node, 6).node()).css('background-color', '#fcec3f'); // Amarillo para columna 6

            // Agregar datos actualizados al vector
            filasAfectadas.push({
                modo: table.cell(node, 0).data(), // Columna Modo
                numero: table.cell(node, 3).data(), // Columna Número
                nuevoSaldo: resto.toFixed(2), // Nuevo saldo
                imputado: (imputadoActual + imputado).toFixed(2) // Nuevo imputado
            });
        });

        seleccionadas.nodes().to$().removeClass('selected');
        $('#a_imputar').val(0);
        let ac = parseFloat($('#acumulado').val());
        ac = ac + imputado;
        $('#acumulado').val(ac.toFixed(2));

        console.log(filasAfectadas); // Vector con datos actualizados
        return;
    }

    // Procesar todas las filas seleccionadas
    seleccionadas.nodes().each(function (node) {
        let saldo = parseFloat(table.cell(node, 5).data()) || 0;
        let imputadoActual = parseFloat(table.cell(node, 6).data()) || 0;

        table.cell(node, 6).data(imputadoActual + saldo); // Actualizar la columna 6
        table.cell(node, 5).data(0); // Actualizar la columna 5

        $(table.cell(node, 5).node()).css('background-color', '#fcec3f'); // Amarillo para columna 5
        $(table.cell(node, 6).node()).css('background-color', '#fcec3f'); // Amarillo para columna 6

        // Agregar datos actualizados al vector
        filasAfectadas.push({
            modo: table.cell(node, 0).data(), // Columna Modo
            numero: table.cell(node, 3).data(), // Columna Número
            nuevoSaldo: '0.00', // Nuevo saldo
            imputado: (imputadoActual + saldo).toFixed(2) // Nuevo imputado
        });
    });

    // Actualizar importe restante
    const total = importe - acumulado;
    let ac = parseFloat($('#acumulado').val());
    ac = ac + acumulado;
    $('#acumulado').val(ac.toFixed(2));
    $('#a_imputar').val(total.toFixed(2));

    seleccionadas.nodes().to$().removeClass('selected');

    console.log(filasAfectadas);
    localStorage.setItem('filasAfectadas',JSON.stringify(filasAfectadas));
});



}

function cargar_datos_formadepago(){
let imputar=$('#a_imputar').val();
let importe=$('#id_importe').val();
let acumulado=$('#acumulado').val();


const table = $('#imputacionTable').DataTable();

let documentos = '';

table.rows().nodes().each(function (node) {
    let imputado = parseFloat(table.cell(node, 6).data()) || 0;

    if (imputado !== 0) {
        let nroDocumento = table.cell(node, 3).data();
        documentos += nroDocumento + ';';
    }
});

documentos = documentos.slice(0, -1);

$('#observations').val(documentos);
acumulado = parseFloat(acumulado || 0).toFixed(2); // Convertir a número y aplicar toFixed
importe = parseFloat(importe || 0).toFixed(2);     // Convertir a número y aplicar toFixed

if(imputar<=0){
$('#amount').html(acumulado);

}else{
$('#amount').html(importe);
}
$('#cashAmount').val(acumulado);
$('#checkAmount').val(acumulado);
$('#checkAmount_trans').val(acumulado);
$('#checkAmount_deposito').val(acumulado);
$('#checkAmount_otro').val(acumulado);
}

function ingresar_datos(){
let monto=$('#cashAmount').val();
let importe=$('#amount').html();
let arbitraje=$('#id_arbitraje').val();

const tbody = $('#exampleTable tbody');
//tbody.empty();

let modo, emision,banco,numero,moneda,total,tc,vencimiento,cuenta;

if ($('#efectivo').is(':checked')){
const selectElement = document.getElementById('id_cuenta_efectivo');
const moneda_select = document.getElementById('id_moneda_efectivo');
const labelSeleccionado = selectElement.options[selectElement.selectedIndex].text;
const valueSeleccionado = selectElement.value;
const monedaV = moneda_select.value;
modo='EFECTIVO';
emision=obtenerFechaHoy();
banco=valueSeleccionado;
numero=0;
moneda=monedaV;
total=monto;
tc=arbitraje;
cuenta=valueSeleccionado;
vencimiento=obtenerFechaHoy();

}else if ($('#cheque').is(':checked')){
const selectElement = document.getElementById('id_cuenta_cheque');
const moneda_select = document.getElementById('id_moneda_cheque');
const monedaV = moneda_select.value;
const labelSeleccionado = selectElement.options[selectElement.selectedIndex].text;
const valueSeleccionado = selectElement.value;
modo='CHEQUE';
emision=$('#checkEmission').val();
banco=labelSeleccionado;
numero=$('#checkNumber').val();
tc=arbitraje;
cuenta=valueSeleccionado;
moneda=monedaV;
vencimiento=$('#checkDueDate').val();
total=$('#checkAmount').val();

}else if ($('#trans').is(':checked')){
const selectElement = document.getElementById('id_cuenta_transferencia');
const moneda_select = document.getElementById('id_moneda_transferencia');
const monedaV = moneda_select.value;
const labelSeleccionado = selectElement.options[selectElement.selectedIndex].text;
modo='TRANSFER';
emision=$('#checkEmission_trans').val();
banco=labelSeleccionado;
numero=$('#checkNumber_trans').val();
tc=arbitraje;
cuenta=$('#cuenta_trans').val();
moneda=monedaV;
vencimiento=$('#checkDueDate_trans').val();
total=$('#checkAmount_trans').val();
}else if ($('#deposito').is(':checked')){
const selectElement = document.getElementById('id_cuenta_deposito');
const moneda_select = document.getElementById('id_moneda_deposito');
const monedaV = moneda_select.value;
const labelSeleccionado = selectElement.options[selectElement.selectedIndex].text;
modo='DEPOSITO';
emision=$('#checkEmission_deposito').val();
banco=labelSeleccionado;
numero=$('#checkNumber_deposito').val();
tc=arbitraje;
cuenta=$('#cuenta_deposito').val();
moneda=monedaV;
vencimiento=$('#checkDueDate_deposito').val();
total=$('#checkAmount_deposito').val();
}else if ($('#otro').is(':checked')){
const selectElement = document.getElementById('id_cuenta_otro');
const moneda_select = document.getElementById('id_moneda_otro');
const monedaV = moneda_select.value;
const labelSeleccionado = selectElement.options[selectElement.selectedIndex].text;
modo='OTRO';
emision=$('#checkEmission_otro').val();
banco=labelSeleccionado;
numero=$('#checkNumber_otro').val();
tc=arbitraje;
cuenta=$('#cuenta_otro').val();
moneda=monedaV;
vencimiento=$('#checkDueDate_otro').val();
total=$('#checkAmount_otro').val();
}
    const nuevaFilaObj = {
        modo: modo,
        emision: emision,
        banco: banco,
        numero: numero,
        moneda: moneda,
        total: total,
        tc: tc,
        vencimiento: vencimiento,
        cuenta: cuenta
    };

    let medios_pago=[];

    medios_pago.push(nuevaFilaObj);

    localStorage.setItem('medios_pago', JSON.stringify(medios_pago));

const nuevaFila = `
            <tr>
                <td>${modo}</td>
                <td>${emision}</td>
                <td>${banco}</td>
                <td>${numero}</td>
                <td>${moneda}</td>
                <td>${total}</td>
                <td>${tc}</td>
                <td>${vencimiento}</td>
                <td>${cuenta}</td>
            </tr>
        `;
        tbody.append(nuevaFila);

let accum = parseFloat($('#accumulated').val()) || 0;
let totalParsed = parseFloat(total || 0);
accum += totalParsed;
$('#accumulated').val(accum.toFixed(2));
let diferencia = parseFloat(importe || 0) - accum;
$('#difference').val(diferencia.toFixed(2));


}

const obtenerFechaHoy = () =>
    new Date().toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' });

function crear_impuventa_asiento_movimiento(){
//traer cliente tambien
let impuventa = JSON.parse(localStorage.getItem('filasAfectadas')) || [];
let medios_pago = JSON.parse(localStorage.getItem('medios_pago')) || [];

let vector=[];
let imputaciones=[];
let asiento=[];
let movimiento=[];
let cobranza=[];

impuventa.forEach((item) => {
        imputaciones.push({
            nroboleta: item.numero,
        });
        movimiento.push({
            imputado:item.modo,
            saldo:item.nuevoSaldo,
            boletas:$('#observations').val()
        });
    });

medios_pago.forEach((item) => {
        asiento.push({
            modo:item.modo,
            cuenta:item.cuenta,
            banco:item.banco,
            nro_mediopago:item.numero,
            total_pago:item.total,
            vencimiento:item.vencimiento
        });
    });

    cobranza.push({
        nrocliente:$('#cliente_cobranza').val(),
        serie:$('#id_serie').val(),
        prefijo:$('#id_prefijo').val(),
        numero:$('#id_numero').val(),
        total:$('#id_importe').val(),
        nromoneda:$('#id_moneda').val(),
        arbitraje:$('#id_arbitraje').val(),
        paridad:$('#id_paridad').val()
    });



vector.cobranza=cobranza;
vector.imputaciones=imputaciones;
vector.asiento=asiento;
vector.movimiento=movimiento;

console.log(vector);

}