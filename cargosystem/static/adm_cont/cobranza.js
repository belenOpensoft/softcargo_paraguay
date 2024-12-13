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
                console.log(data);
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
            $('#cliente_cobranza_hidden').val(id);
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
let existe_cliente;

function borrar_datos() {
    const selectedRow = document.querySelector('#exampleTable tbody tr.selected');

    if (selectedRow) {
        let accum = parseFloat($('#accumulated').val()) || 0;
        let importe = parseFloat($('#amount').html()) || 0;

        const total = parseFloat(selectedRow.cells[5].textContent) || 0;

        accum -= total;

        $('#accumulated').val(accum.toFixed(2));
        let diferencia = importe - accum;
        $('#difference').val(diferencia.toFixed(2));
        $('#cashAmount').val(diferencia.toFixed(2));
        $('#checkAmount').val(diferencia.toFixed(2));
        $('#checkAmount_trans').val(diferencia.toFixed(2));
        $('#checkAmount_deposito').val(diferencia.toFixed(2));
        $('#checkAmount_otro').val(diferencia.toFixed(2));
        selectedRow.remove();
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
                    existe_cliente=false;
                }
            }
        ]
    }).prev('.ui-dialog-titlebar').remove();
    $.ajax({
        url: "/admin_cont/cargar_arbitraje/",
        type: "GET",
        dataType: "json",
        success: function (data) {
            // Cargar los valores en los campos
            $('#id_arbitraje').val(data.arbitraje);
            $('#id_paridad').val(data.paridad);
        },
        error: function (xhr, status, error) {
            alert("Error al cargar los datos iniciales: " + error);
        }
    });
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
          let acumulado=$('#accumulated').val();
          let monto=$('#amount').val();
          //crear_impuventa_asiento_movimiento();
          verificar();
          localStorage.removeItem('medios_pago');
        },
      },
    ],beforeClose: function () {
        localStorage.removeItem('medios_pago');
    }

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
    existe_cliente=true;
    // Manejar selección de filas
    $('#imputacionTable tbody').on('click', 'tr', function () {
        $(this).toggleClass('selected');
    });


$('#imputarSeleccion').on('click', function () {
    if(!existe_cliente){
    alert('Seleccione un cliente para continuar');
    return;
    }
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
$('#cashAmount').val(importe);
$('#checkAmount').val(importe);
$('#checkAmount_trans').val(importe);
$('#checkAmount_deposito').val(importe);
$('#checkAmount_otro').val(importe);
}

function ingresar_datos(){
let monto=$('#cashAmount').val();
let importe=$('#amount').html();
let arbitraje=$('#id_arbitraje').val();

const tbody = $('#exampleTable tbody');
//tbody.empty();

let modo, emision,banco,numero,moneda,total,tc,vencimiento,cuenta;
modo=emision=banco=numero=moneda=total=tc=vencimiento=cuenta=0;

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
let bancoText = $('#id_banco_cheque option:selected').text();
banco=bancoText;
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

    let medios_pago=JSON.parse(localStorage.getItem('medios_pago')) || [];

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
$('#cashAmount').val(diferencia.toFixed(2));
$('#checkAmount').val(diferencia.toFixed(2));
$('#checkAmount_trans').val(diferencia.toFixed(2));
$('#checkAmount_deposito').val(diferencia.toFixed(2));
$('#checkAmount_otro').val(diferencia.toFixed(2));


}

const obtenerFechaHoy = () => {
    const fechaHoy = new Date();
    const año = fechaHoy.getFullYear();
    const mes = String(fechaHoy.getMonth() + 1).padStart(2, '0'); // Meses van de 0 a 11
    const día = String(fechaHoy.getDate()).padStart(2, '0');
    return `${año}-${mes}-${día}`;
};

function crear_impuventa_asiento_movimiento(){

if(!$('#id_cuenta_observaciones').val() && $('#difference').val()!=0){
alert('Debe asignar la diferencia a una cuenta');
return;
}
//traer cliente tambien
let impuventa = JSON.parse(localStorage.getItem('filasAfectadas')) || [];
let medios_pago = JSON.parse(localStorage.getItem('medios_pago')) || [];

let vector={};
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
        nrocliente:$('#cliente_cobranza_hidden').val(),
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
if($('#difference').val()!=0){
let nuevaFila = {
    modo: "DIFERENCIA",
    cuenta: $('#id_cuenta_observaciones').val(),
    banco:$('#id_cuenta_observaciones option:selected').text() ,
    nro_mediopago: 0,
    total_pago: $('#difference').val(),
    vencimiento: null
};

vector.asiento.push(nuevaFila);
}

console.log(vector);


$.ajax({
        url: '/admin_cont/guardar_impuventa/', // Cambia esto a la URL correcta
        method: 'POST',
        headers: { 'X-CSRFToken': csrf_token }, // Asegúrate de tener el CSRF token
        data: JSON.stringify({ 'vector':vector }),
        contentType: 'application/json',
        success: function(response) {
            if (response.status === 'exito') {
                alert("Datos guardados correctamente");
                // Opcional: recargar una tabla o actualizar la UI
            } else {
                alert("ghfghfgh: " + response.status);
            }
        },
        error: function(xhr) {
            alert("Error al guardar los datos: " + xhr.responseText);
        },
    });

}

function crear_anticipo(){
if(!$('#id_cuenta_observaciones').val() && $('#difference').val()!=0){
alert('Debe asignar la diferencia a una cuenta');
return;
}
//traer cliente tambien
let impuventa = JSON.parse(localStorage.getItem('filasAfectadas')) || [];
let medios_pago = JSON.parse(localStorage.getItem('medios_pago')) || [];

let vector={};
let asiento=[];
let cobranza=[];


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
        nrocliente:$('#cliente_cobranza_hidden').val(),
        serie:$('#id_serie').val(),
        prefijo:$('#id_prefijo').val(),
        numero:$('#id_numero').val(),
        total:$('#id_importe').val(),
        nromoneda:$('#id_moneda').val(),
        arbitraje:$('#id_arbitraje').val(),
        paridad:$('#id_paridad').val()
    });



vector.cobranza=cobranza;
vector.asiento=asiento;
if($('#difference').val()!=0){
let nuevaFila = {
    modo: "DIFERENCIA",
    cuenta: $('#id_cuenta_observaciones').val(),
    banco:$('#id_cuenta_observaciones option:selected').text() ,
    nro_mediopago: 0,
    total_pago: $('#difference').val(),
    vencimiento: null
};

vector.asiento.push(nuevaFila);
}

console.log('anticipo '+vector);


$.ajax({
        url: '/admin_cont/guardar_anticipo/', // Cambia esto a la URL correcta
        method: 'POST',
        headers: { 'X-CSRFToken': csrf_token }, // Asegúrate de tener el CSRF token
        data: JSON.stringify({ 'vector':vector }),
        contentType: 'application/json',
        success: function(response) {
            if (response.status === 'exito') {
                alert("Datos guardados correctamente");
                // Opcional: recargar una tabla o actualizar la UI
            } else {
                alert("ghfghfgh: " + response.status);
            }
        },
        error: function(xhr) {
            alert("Error al guardar los datos: " + xhr.responseText);
        },
    });

}

function verificar(){
let key=false;
let rows = document.querySelectorAll('#imputacionTable tbody tr');
rows.forEach(row => {
    let imputado = row.cells[5]?.textContent.trim();
    let imputadoValue = parseFloat(imputado) || 0;

    if (imputadoValue !== 0) {
        console.log('Fila con Imputado diferente de cero:', imputadoValue);
        key = true;
    }
});

    if(key){
     crear_impuventa_asiento_movimiento();
    }else{
        if (confirm('No hay una boleta seleccionada, ¿Desea continuar como anticipo?')) {
            crear_anticipo();
        }
    }

}