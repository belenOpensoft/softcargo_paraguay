$(document).ready(function() {

let total=0;
let neto = 0;
let iva=0;

var buscar = '';
var que_buscar = '';

    const valorInicial = $('#id_tipo').find('option:selected').text();
    $('#tipoSeleccionado').text(valorInicial);

    $('#id_tipo').change(function() {
        const valorSeleccionado = $(this).find('option:selected').text();
        $('#tipoSeleccionado').text(valorSeleccionado);
    });

    $('#cliente').autocomplete({
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
        appendTo: "#facturaM",
        select: function(event, ui) {
            const { id } = ui.item;
            $.ajax({
                url: "/admin_cont/buscar_clientes",
                data: { id },
                dataType: 'json',
                success: cliente => {
                    const row = `
                        <tr id="cliente-${id}">
                            <td class="d-none">${cliente.codigo}</td>
                            <td>${cliente.empresa}</td>
                            <td>${cliente.ruc}</td>
                            <td>${cliente.direccion}</td>
                            <td>${cliente.localidad}</td>
                            <td>${cliente.telefono}</td>
                        </tr>`;
                    $('#clienteTable tbody').html(row);
                    $('#clienteTable').show();
                },
                error: xhr => console.error('Error al obtener los detalles del cliente:', xhr)
            });
        }
    });

    // Autocomplete para el input "item"
    $('#item').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/admin_cont/buscar_item_v",
                dataType: 'json',
                data: {
                    term: request.term
                },
                success: data => response(data.map(item => ({
                    label: item.text,
                    value: item.text,
                    id: item.id
                }))),
                error: xhr => console.error('Error al buscar items:', xhr)
            });
        },
        minLength: 2,
        appendTo: "#facturaM",
        select: function(event, ui) {
            $.ajax({
                url: "/admin_cont/buscar_items_v",
                data: { id: ui.item.id },
                dataType: 'json',
                success: servicio => {
                    $('#id_precio input').data({
                        iva: servicio.iva,
                        cuenta: servicio.cuenta,
                        codigo: servicio.item
                    });
                    $('#id_descripcion_item input').val(servicio.nombre);
                },
                error: xhr => console.error('Error al obtener los detalles del item:', xhr)
            });
        }
    });

    let itemCounter = 0;

    // Agregar Item a la tabla
    $('#agregarItem').on('click', function() {
        const item = $('#item').val();
        const descripcion = $('#id_descripcion_item input').val();
        const precio = parseFloat($('#id_precio input').val());

        if (item && descripcion && !isNaN(precio)) {
            const iva = $('#id_precio input').data('iva');
            const cuenta = $('#id_precio input').data('cuenta');
            const codigo = $('#id_precio input').data('codigo');

            itemCounter++;
            const rowId = `item-${itemCounter}`;

            const row = `
                <tr id="${rowId}" data-precio="${precio}" data-iva="${iva}" data-cuenta="${cuenta}">
                    <td>${codigo}</td>
                    <td>${descripcion}</td>
                    <td>${precio.toFixed(2)}</td>
                    <td>${iva}</td>
                    <td>${cuenta}</td>
                </tr>`;

            $('#itemTable tbody').append(row);
            $('#itemTable').show();
            $('#eliminarSeleccionados').show();
            limpiarCampos();
            actualizarTotal();
            $('#totales').show();
        } else {
            alert('Por favor, completa todos los campos antes de agregar el item.');
        }
    });

   // Seleccionar/Deseleccionar fila
    $('#itemTable tbody').on('click', 'tr', function() {
        $(this).toggleClass('table-active table-primary');
    });

    $('#eliminarSeleccionados').on('click', function() {
        if (confirm('¿Está seguro de que desea eliminar la selección?')) {
            $('#itemTable tbody tr.table-active').remove();
            actualizarTotal();

            if ($('#itemTable tbody tr').length === 0) {
                $('#itemTable').hide();
                $('#eliminarSeleccionados').hide();
                $('#totales').hide();
            }
        }
    });

    $('#facturaForm').submit(function(event) {
        event.preventDefault();
        if (confirm('¿Está seguro de que desea facturar?')) {
            let tipoFac = $('#id_tipo').val();
            let serie = $('#id_serie').val();
            let prefijo = $('#id_prefijo').val();
            let numero = $('#id_numero').val();
            let cliente = $('#cliente').val();
            let fecha = $('#id_fecha').val();
            let paridad = $('#id_paridad').val();
            let arbitraje = $('#id_arbitraje').val();
            let imputar = $('#id_imputar').val();
            let moneda = $('#id_moneda select').val();
            let clienteData = {
                codigo: $('#clienteTable tbody tr td').eq(0).text(),
                empresa: $('#clienteTable tbody tr td').eq(1).text(),
                rut: $('#clienteTable tbody tr td').eq(2).text(),
                direccion: $('#clienteTable tbody tr td').eq(3).text(),
                localidad: $('#clienteTable tbody tr td').eq(4).text(),
                telefono: $('#clienteTable tbody tr td').eq(5).text()
            };

            let items = [];
            $('#itemTable tbody tr').each(function() {
                const itemData = {
                    id: $(this).find('td').eq(0).text(),
                    descripcion: $(this).find('td').eq(1).text(),
                    precio: $(this).find('td').eq(2).text(),
                    iva: $(this).find('td').eq(3).text(),
                    cuenta: $(this).find('td').eq(4).text(),
                };
                items.push(itemData);
            });

            let preventa = JSON.parse(localStorage.getItem('preventa')) || [];
            let data=[];
            if (preventa!=null){
                //es preventa
                data={
                    csrfmiddlewaretoken: csrf_token,
                    fecha: fecha,
                    tipoFac: tipoFac,
                    serie: serie,
                    prefijo: prefijo,
                    numero: numero,
                    cliente: cliente,
                    arbitraje: arbitraje,
                    paridad: paridad,
                    imputar: imputar,
                    moneda: moneda,
                    clienteData: JSON.stringify(clienteData),
                    items: JSON.stringify(items),
                    total:total,
                    iva:iva,
                    neto:neto,
                    preventa:JSON.stringify(preventa),
                }
            }else{
                data={
                    csrfmiddlewaretoken: csrf_token,
                    fecha: fecha,
                    tipoFac: tipoFac,
                    serie: serie,
                    prefijo: prefijo,
                    numero: numero,
                    cliente: cliente,
                    arbitraje: arbitraje,
                    paridad: paridad,
                    imputar: imputar,
                    moneda: moneda,
                    clienteData: JSON.stringify(clienteData),
                    items: JSON.stringify(items),
                    total:total,
                    iva:iva,
                    neto:neto,
                    preventa:0,
                }
            }

            $.ajax({
                url: "/admin_cont/procesar_factura/",
                dataType: 'json',
                type: 'POST',
                data: data,
                headers: { 'X-CSRFToken': csrf_token },
                success: function(data) {
                    $('#facturaM').dialog('close');
                    $('#facturaForm').trigger('reset');
                    total=0;
                    iva=0;
                    neto=0;
                    //window.location.reload();
                },
                error: function(xhr) {
                    console.error('Error al facturar:', xhr);
                    alert('Error al procesar la factura');
                }
            });
        }
    });

    //buscadores tabla facturas
    let contador = 0;

    $('#tabla_facturas tfoot th').each(function () {
        let title = $(this).text();
        if (title !== '') {
            $(this).html('<input type="text" class="form-control"  autocomplete="off" id="buscoid_' + contador + '" type="text" placeholder="Buscar ' + title + '"  autocomplete="off" />');
            contador++;
        } else {
            $(this).html('<button class="btn" title="Borrar filtros" id="clear" ><span class="glyphicon glyphicon-erase"></span></button> ');
        }
    });
    //tabla general master


    table = $('#tabla_facturas').DataTable({
    "dom": 'Btlipr',
    "scrollX": true,
    "bAutoWidth": false,
    "scrollY": wHeight * 0.60,
    "columnDefs": [
        {
            "targets": [0, 1],  // Ocultamos ambas columnas en una sola configuración
            "visible": false,
            "searchable": false  // Opcional: evita que se incluyan en las búsquedas
        },
        {
            "targets": 2,  // Asignamos la columna de fecha
            "type": "date-iso", // Indica que esta columna es de tipo fecha
            "orderable": true // Habilita el ordenamiento
        }
    ],
    "columns": [
        { "visible": false }, // Columna 0
        { "visible": false }, // Columna 1
        { "orderable": true }, // Columna 2 (Ordenable)
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
    ],
    "order": [[2, "desc"]],
    "processing": true,
    "serverSide": true,
    "pageLength": 10,
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

function abrir_modalfactura(){
$('#facturaForm').trigger('reset');
$('#itemTable tbody').empty();
$('#itemTable').hide();
$('#clienteTable tbody').empty();
$('#clienteTable').hide();
$('#totales').hide();

$("#facturaM").dialog({
        autoOpen: true,
        modal: true,
        width: wWidth*0.60,
        height: wHeight*0.80,
        position: { my: "top", at: "top+20", of: window },
        buttons: [{
            text: "Salir",
            class: "btn btn-dark",
            style: "width:100px",
            click: function () {
                $(this).dialog("close");
                localStorage.removeItem('preventa');
                localStorage.removeItem('gastos');

            },
        }],
    }).prev('.ui-dialog-titlebar').remove();
}

$('#preventa').on('click', function() {
    $("#preventa_modal").dialog({
        autoOpen: true,
        modal: true,
        width: wWidth*0.90,
        height: wHeight*0.90,
        buttons: [{
        class: "btn btn-dark",
                    style: "width:100px",
                    text:"Cerrar",
                    click: function() {
                $(this).dialog("close");
                $('#preventa_table').DataTable().destroy();

            }
        }]
    });
    $('#preventa_table').DataTable({
        serverSide: true,
        ajax: {
            url: "/admin_cont/source_infofactura",
            type: "GET"
        },
        columns: [
            { data: 'numero' },
            { data: 'cliente' },
            { data: 'posicion' },
            { data: 'master' },
            { data: 'house' },
            { data: 'vapor_vuelo' },
            { data: 'contenedor' },
            { data: 'clase' },
            { data: 'referencia' },
            { data: 'fecha' }
        ],
        responsive: true,
        processing: true,
        language: {
            url: "//cdn.datatables.net/plug-ins/1.10.24/i18n/Spanish.json"
        }
    });
});

$('#preventa_table tbody').on('dblclick', 'tr', function() {
    $('#pararesetear').trigger('reset');
    $('#pararesetear2').trigger('reset');
    let referencia = $(this).find('td').eq(8).text();
    let clase = $(this).find('td').eq(7).text();
    let preventa = $(this).find('td').eq(0).text();

    $.ajax({
        url: "/admin_cont/cargar_preventa_infofactura/",
        method: 'POST',
        data: {
            'referencia': referencia,
            'clase': clase,
            'preventa': preventa
        },
        headers: { 'X-CSRFToken': csrf_token },
        success: function(response) {
        console.log(response);
            let preventa = response.data_preventa;
            let gastos = response.data;

            localStorage.setItem('gastos_preventa',JSON.stringify(gastos));
            localStorage.setItem('preventa',JSON.stringify(preventa));

            // Asignar valores de preventa a los campos de la interfaz
            $('#moneda').val(preventa.moneda);
            $('#total_con_iva').val(preventa.total_con_iva);
            $('#total_sin_iva').val(preventa.total_sin_iva);
            $('#cliente_i').val(preventa.cliente_i);
            $('#peso').val(preventa.peso);
            $('#direccion').val(preventa.direccion);
            $('#localidad').val(preventa.localidad);
            $('#aplic').val(preventa.aplic);
            $('#bultos').val(preventa.bultos);
            $('#volumen').val(preventa.volumen);
            $('#commodity').val(preventa.commodity);
            $('#inconterms').val(preventa.inconterms);
            $('#flete').val(preventa.flete);
            $('#deposito').val(preventa.deposito);
            $('#wr').val(preventa.wr);
            $('#referencia').val(preventa.referencia);
            $('#llegada_salida').val(preventa.llegada_salida);
            $('#origen').val(preventa.origen);
            $('#destino').val(preventa.destino);
            $('#transportista').val(preventa.transportista);
            $('#consignatario').val(preventa.consignatario);
            $('#embarcador').val(preventa.embarcador);
            $('#agente').val(preventa.agente);
            $('#vuelo_vapor').val(preventa.vuelo_vapor);
            $('#seguimiento').val(preventa.seguimiento);
            $('#mawb_mbl_mcrt').val(preventa.mawb_mbl_mcrt);
            $('#hawb_hbl_hcrt').val(preventa.hawb_hbl_hcrt);
            $('#posicion').val(preventa.posicion);
            $('#status').val(preventa.status);
            $('#orden').val(preventa.orden);
            $('#modo').val(preventa.modo);

            // Configurar y cargar los datos en la tabla DataTables
            if ($.fn.DataTable.isDataTable("#tabla_gastos_preventa_factura")) {
                $('#tabla_gastos_preventa_factura').DataTable().clear().destroy();
            }

            $('#tabla_gastos_preventa_factura').DataTable({
                data: gastos,
                columns: [
                    { data: 'descripcion', title: 'Descripcion' },
                    { data: 'total', title: 'Total' },
                    { data: 'iva', title: 'IVA' },
                    { data: 'original', title: 'Original' },
                    { data: 'moneda', title: 'Moneda' }
                ],
                paging: true,
                searching: true,
                ordering: true,
                responsive: true,
                language: {
                    url: "//cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json"
                },
                "columnDefs": [
                        {
                            targets: 0,  // Primera columna: Descripcion
                            className: "dt-body-left",  // Aplica una clase CSS para alinear a la izquierda
                            render: function (data, type, row) {
                                return data; // Puedes aplicar un formato o transformación aquí si es necesario
                            }
                        },
                        {
                            targets: 1,  // Segunda columna: Total
                            className: "dt-body-right",  // Aplica una clase CSS para alinear a la derecha
                            render: function (data, type, row) {
                                // Ejemplo de formatear como moneda
                                return '$' + parseFloat(data).toFixed(2);  // Si 'data' es el total, puedes formatearlo como moneda
                            }
                        },
                        {
                            targets: 2,  // Tercera columna: IVA
                            className: "dt-body-center",  // Aplica una clase CSS para centrar el texto
                            render: function (data, type, row) {
                                return data;  // Se puede transformar el texto si es necesario
                            }
                        },
                        {
                            targets: 3,  // Cuarta columna: Original
                            className: "dt-body-center",  // Aplica una clase CSS para centrar el texto
                            render: function (data, type, row) {
                                return data;  // Transformación si es necesario
                            }
                        },
                        {
                            targets: 4,  // Quinta columna: Moneda
                            className: "dt-body-center",  // Aplica una clase CSS para centrar el texto
                            render: function (data, type, row) {
                                return data;  // Transformación si es necesario
                            }
                        }
                    ],
            });

        },
        error: function() {
            alert('Error al realizar la consulta.');
        }
    });
});
$('#preventa_table tbody').on('click', 'tr', function() {
    let preventa = $(this).find('td').eq(0).text();
    let clase = $(this).find('td').eq(7).text();

    if ($(this).hasClass('table-secondary')) {
        $(this).removeClass('table-secondary');
        localStorage.removeItem('preventa_id',preventa);
        localStorage.removeItem('preventa_clase',clase);
    } else {
        $('#preventa_table tbody tr.table-secondary').removeClass('table-secondary');
        $(this).addClass('table-secondary');
        localStorage.setItem('preventa_id',preventa);
        localStorage.setItem('preventa_clase',clase);
    }
});

function facturar_preventa() {
    $("#preventa_modal").dialog('close');
    let gastos = JSON.parse(localStorage.getItem('gastos_preventa')) || [];
    let preventa = JSON.parse(localStorage.getItem('preventa')) || [];

    // Cargar cliente
    $("#cliente").val(preventa.cliente_i);
    $("#cliente").autocomplete("search", preventa.cliente_i);

    $.Deferred(function(deferred) {
        setTimeout(function() {
            const li = $('#cliente').autocomplete('widget').find("li:contains('" + preventa.cliente_i + "')");
            if (li.length > 0) {
                li.trigger('click');
                deferred.resolve();
            } else {
                console.error('No se encontró el cliente en los resultados');
                deferred.reject();
            }
        }, 300);
    }).done(function() {
        // Cargar cada item después de seleccionar el cliente
        gastos.forEach(gasto => {
            const desc = gasto.descripcion.split(' - ')[1];
            const codigo= gasto.descripcion.split('-')[0];
            agregarItem(desc,codigo,gasto.total)

        });
    }).fail(function() {
        console.error('Falló la carga del cliente');
    });
}

function agregarItem(desc,codigo,precio) {
    const item = desc;
    const descripcion = desc;

    if (item && descripcion && !isNaN(precio)) {
        $.ajax({
            url: "/admin_cont/buscar_items_v",
            data: { id: codigo },
            dataType: 'json',
            success: servicio => {
                const iva = servicio.iva;
                const cuenta = servicio.cuenta;
                const codigo = servicio.item;

                const row = `
                    <tr data-precio="${precio}" data-iva="${iva}" data-cuenta="${cuenta}">
                        <td>${codigo}</td>
                        <td>${descripcion}</td>
                        <td>${precio.toFixed(2)}</td>
                        <td>${iva}</td>
                        <td>${cuenta}</td>
                    </tr>`;

                $('#itemTable tbody').append(row);
                $('#itemTable').show();
                $('#eliminarSeleccionados').show();
                //limpiarCampos();
                actualizarTotal();
                $('#totales').show();
            },
            error: xhr => console.error('Error al obtener los detalles del item:', xhr)
        });

    } else {
        alert('Por favor, completa todos los campos antes de agregar el item.');
    }
}

function limpiarCampos() {
    $('#item').val('');
    $('#id_descripcion_item input').val('');
    $('#id_precio input').val('');
}

function actualizarTotal() {
let precio = 0;
let neto_fun = 0;
total = 0;  // Asegúrate de inicializar total aquí
iva = 0;

// Recorre cada fila y calcula el neto
$('#itemTable tbody tr').each(function() {
    precio = parseFloat($(this).data('precio')) || 0;
    neto_fun += precio;
});

neto = neto_fun;

// Actualiza el valor del neto en el campo correspondiente
$('#id_neto input').val(neto.toFixed(2)).prop('readonly', true);

// Recorre cada fila y calcula el total con IVA
$('#itemTable tbody tr').each(function() {
    precio = parseFloat($(this).data('precio')) || 0;
    iva = $(this).data('iva');

    const precioFinal = iva === 'Basico' ? precio * 1.22 : precio;
    total += precioFinal;
});

// Actualiza el valor del total en el campo correspondiente
$('#id_total input').val(total.toFixed(2)).prop('readonly', true);

// Calcula y actualiza el IVA
iva = total - neto;
$('#id_iva input').val(iva.toFixed(2)).prop('readonly', true);
}

function cancelar_preventa(){
//agregar a formularios los demas bloques para poder resetearlos
$('#pararesetear').trigger('reset');
$('#pararesetear2').trigger('reset');
if ($.fn.DataTable.isDataTable("#tabla_gastos_preventa_factura")) {
    $('#tabla_gastos_preventa_factura').DataTable().clear().destroy();
}
}

function borrar_preventa(){
id=localStorage.getItem('preventa_id');

    $.ajax({
        url: '/admin_cont/eliminar_preventa/',
        method: 'POST',
        headers: { 'X-CSRFToken': csrf_token },
        data: JSON.stringify({ id: id }),
        contentType: 'application/json',
        success: function(response) {
            if (response.resultado === "éxito") {
                alert("Preventa eliminada correctamente");
                $('#preventa_table').DataTable().ajax.reload(null, false);
            } else {
                alert(response.mensaje);
            }
        },
        error: function(xhr) {
            alert("Error al eliminar la preventa: " + xhr.responseText);
        }
    });
}


//imprimir caratula house
function imprimir_preventa(){
id=localStorage.getItem('preventa_id');
        $("#pdf_add_input").html('');
        $('#pdf_add_input').summernote('destroy');
        get_datos_pdf();
        if (id!=null) {
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
                title: "Preventa N°: " + id,
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
                    // table.ajax.reload();
                }
            })
        } else {
            alert('Debe seleccionar al menos un registro');
        }
}
function imprimirPDF() {
    var contenido = $('#pdf_add_input').summernote('code');
    var ventanaImpresion = window.open('', '_blank');

    ventanaImpresion.document.write('<html><head><title>Impresión</title>');
    ventanaImpresion.document.write('<style>');
    ventanaImpresion.document.write(`
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            line-height: 1.5;
            font-size:12px;
        }
        @media print {
            @page {
                size: portrait; /* Establece la orientación en vertical (portrait) */
                margin: 20mm;   /* Márgenes alrededor del contenido */
            }
            body {
                width: 100%;
                margin: 0;
                padding: 0;
            }
            .container {
                display: block;
                width: 100%;
                text-align: left;
            }
        }
        .container {
            margin: 20px; /* Margen interior para el contenido */
        }
        h1, h2 {
            text-align: center;
        }
        p {
            text-align: left;
        }
        hr {
            border: 1px solid #000;
        }
    `);
    ventanaImpresion.document.write('</style></head><body>');
    ventanaImpresion.document.write('<div class="container">');
    ventanaImpresion.document.write(contenido);
    ventanaImpresion.document.write('</div></body></html>');
    ventanaImpresion.document.close();

    ventanaImpresion.onload = function () {
        ventanaImpresion.focus(); // Asegurarse de que la ventana esté en foco
        ventanaImpresion.print(); // Iniciar la impresión
        ventanaImpresion.close(); // Cerrar la ventana después de la impresión
    };
}
function get_datos_pdf() {
id=localStorage.getItem('preventa_id');
clase=localStorage.getItem('preventa_clase');
let modo='';
if(clase=='IM' || clase=='EM' ){
modo='MARITIMO';
}else if(clase=='IA' || clase=='EA'){
modo='AEREO';
}else if(clase=='IT'||clase=='ET'){
modo='TERRESTRE';
}else{
modo='SINMODO';
}

    miurl = "/admin_cont/get_datos_pdf_preventa/";
    var toData = {
    'clase':clase,
        'modo':modo,
        'id': id,
        'csrfmiddlewaretoken': csrf_token,
    };
    $.ajax({
        type: "POST",
        url: miurl,
        data: toData,
        async: false,
        success: function (resultado) {
            if (resultado['resultado'] === 'exito') {
                $("#pdf_add_input").html(resultado['texto']);
            } else {
                alert(resultado['resultado']);
            }
        }
    });
}

//multiples preventas

//$('#infofacturaTable').DataTable().ajax.reload();
function multiples_preventas(){
$("#prev_multiple_modal").dialog({
        autoOpen: true,
        modal: true,
        width: wWidth*0.60,
        height: wHeight*0.80,
        position: { my: "top", at: "top+20", of: window },
        buttons: [{
            text: "Salir",
            class: "btn btn-dark",
            style: "width:100px",
            click: function () {
                $(this).dialog("close");
                $('#pendientes_tabla').DataTable().destroy();
                $('#preventa_unificada_tabla').DataTable().destroy();
                $('#conceptos_unificar_tabla').DataTable().destroy();
                $('#socio_com_filtro').val();

            },
        }],
    }).prev('.ui-dialog-titlebar').remove();
}
$('#socio_com_filtro').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/admin_cont/buscar_cliente",
                dataType: 'json',
                data: { term: request.term },
                success: function(data) {
                    response(data.map(cliente => ({
                        label: cliente.text,
                        value: cliente.text,
                        id: cliente.text
                    })));
                },
                error: xhr => console.error('Error al buscar clientes:', xhr)
            });
        },
        minLength: 2,
        select: function(event, ui) {
            tabla_pendientes();

        }
    });
function tabla_pendientes() {
    $('#pendientes_tabla').DataTable({
        "stateSave": false,
        "dom": 'Btlipr',
        "scrollX": true,
        "bAutoWidth": false,
        "scrollY": true,
        "lengthMenu": [5, 10, 25],
        "columnDefs": [
            {
                "targets": [0],
                "className": 'text-left',
                "data": 'numero',
                "title": 'Número'
            },
            {
                "targets": [1],
                "className": 'text-left',
                "data": 'sale_llega',
                "title": 'Sale/Llega'
            },
            {
                "targets": [2],
                "className": 'text-left',
                "data": 'referencia',
                "title": 'Ref.'
            },
            {
                "targets": [3],
                "className": 'text-left',
                "data": 'consignatario',
                "title": 'Consignatario'
            },
            {
                "targets": [4],
                "className": 'text-left',
                "data": 'master',
                "title": 'Máster'
            },
            {
                "targets": [5],
                "className": 'text-left',
                "data": 'house',
                "title": 'House'
            },
            {
                "targets": [6],
                "className": 'text-center',
                "orderable": false,
                "data": null,
                "defaultContent": '',
                "render": function (data, type, row) {
                    return `<input type="checkbox" value="${row.numero}">`;
                },
                "title": 'Seleccionar'
            },
            {
                "targets": [7],
                "className": 'text-left',
                "data": 'vapor_vuelo',
                "title": 'Vuelo/Vapor'
            },
            {
                "targets": [8],
                "className": 'text-left',
                "data": 'clase',
                "title": 'Clase'
            }
        ],
        "order": [[0, "desc"]], // Ordena inicialmente por la columna 'Número'
        "processing": true,
        "serverSide": true,
        "pageLength": 5,
        "ajax": {
            "url": "/admin_cont/source_infofactura_cliente/",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "cliente": $('#socio_com_filtro').val() // Se pasa el valor del cliente
                });
            }
        },
        "language": {
            "url": "/static/datatables/es_ES.json" // Ruta de traducción al español
        }
    });
}
function unificar(x){
// 1 es unificados, 0 es originales
$('#guardar_preventa_unificada').attr('data-id', x);

let seleccionados = [];

    $('#pendientes_tabla input[type="checkbox"]:checked').each(function () {
        let fila = $(this).closest('tr');
        let numero = $(this).val();
        let referencia = fila.find('td').eq(2).text().trim();
        let clase = fila.find('td').eq(8).text().trim();
        seleccionados.push({ numero: numero, referencia: referencia, clase: clase });
    });

    if (seleccionados.length === 0) {
        alert('Por favor, seleccione al menos una fila.');
        return;
    }

    $.ajax({
        url: "/admin_cont/cargar_preventa_infofactura_multiple/",
        method: 'POST',
        data: {
            'seleccionados': JSON.stringify(seleccionados)
        },
        headers: { 'X-CSRFToken': csrf_token },
        success: function(response) {
            let todo = response.data;

            let resultado=unificarPreventas(todo);
            let gastos=resultado.gastosUnificados;
            let preventa=resultado.preventaUnificada.data_preventa;
            let gastos_originales=resultado.preventaUnificada.gastos_originales;
            let gastos_mostrar;

            if ($.fn.DataTable.isDataTable("#conceptos_unificar_tabla")) {
                $('#conceptos_unificar_tabla').DataTable().clear().destroy();
            }
            if ($.fn.DataTable.isDataTable("#gastos_no_unificados")) {
                $('#gastos_no_unificados').DataTable().clear().destroy();
            }

            if ($.fn.DataTable.isDataTable("#preventa_unificada_tabla")) {
                $('#preventa_unificada_tabla').DataTable().clear().destroy();
            }

            if(x==1){
                gastos_mostrar=gastos;
            }else{
                gastos_mostrar=gastos_originales;
            }


            var tabla = $('#preventa_unificada_tabla tbody');
                tabla.empty();
                    var fila = $('<tr>');
                    fila.append('<td class="editable">' + preventa.llegada_salida + '</td>');
                    fila.append('<td class="">' + preventa.referencia + '</td>');
                    fila.append('<td class="">' + preventa.consignatario + '</td>');
                    fila.append('<td class="">' + preventa.master + '</td>');
                    fila.append('<td class="editable">' + preventa.house + '</td>');
                    fila.append('<td class="">' + preventa.posicion + '</td>');
                    fila.append('<td class="">' + preventa.seguimiento + '</td>');
                    fila.append('<td class="">' + preventa.cliente_i + '</td>');
                    fila.append('<td class="editable">' + preventa.vuelo_vapor + '</td>');
                    fila.append('<td class="">' + resultado.preventaUnificada.clase + '</td>');
                    tabla.append(fila);

            $('.editable').on('dblclick', function () {
        var celda = $(this);
        var valorActual = celda.text();
        var input = $('<input type="text" class="form-control">').val(valorActual);

        // Reemplazar el contenido de la celda con el input
        celda.html(input);

        // Enfocar el input y seleccionar el texto
        input.focus().select();

        // Manejar el evento blur (cuando el usuario sale del campo)
        input.on('blur', function () {
            var nuevoValor = $(this).val(); // Obtener el nuevo valor
            celda.html(nuevoValor); // Reemplazar el input con el nuevo valor
        });

        // Manejar el evento Enter para confirmar la edición
        input.on('keypress', function (e) {
            if (e.which === 13) { // Enter key
                $(this).blur(); // Simular blur para confirmar el cambio
            }
        });
    });

            $('#conceptos_unificar_tabla').DataTable({
                data: gastos_mostrar,
                columns: [
                    { data: 'descripcion', title: 'Descripcion' },
                    { data: 'total', title: 'Total' },
                    { data: 'iva', title: 'IVA' },
                    { data: 'original', title: 'Original' },
                    { data: 'moneda', title: 'Moneda' },

                ],
                paging: true,
                searching: true,
                ordering: true,
                responsive: true,
                language: {
                    url: "//cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json"
                },
                "columnDefs": [
                        {
                            targets: 0,
                            className: "dt-body-left",
                            render: function (data, type, row) {
                                return data;
                            }
                        },
                        {
                            targets: 1,
                            className: "dt-body-right",
                            render: function (data, type, row) {
                                return '$' + parseFloat(data).toFixed(2);
                            }
                        },
                        {
                            targets: 2,
                            className: "dt-body-center",
                            render: function (data, type, row) {
                                return data;
                            }
                        },
                        {
                            targets: 3,
                            className: "dt-body-center",
                            render: function (data, type, row) {
                                return '$' + parseFloat(data).toFixed(2);
                            }
                        },
                        {
                            targets: 4,
                            className: "dt-body-center",
                            render: function (data, type, row) {
                                return data;
                            }
                        }
                    ],
                "lengthMenu": [5, 10, 25],
                "pageLength": 5,
            });
            $('#gastos_no_unificados').DataTable({
                data: gastos_originales,
                columns: [
                    { data: 'descripcion', title: 'Descripcion' },
                    { data: 'total', title: 'Total' },
                    { data: 'iva', title: 'IVA' },
                    { data: 'original', title: 'Original' },
                    { data: 'moneda', title: 'Moneda' },

                ],
                paging: true,
                searching: true,
                ordering: true,
                responsive: true,
                language: {
                    url: "//cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json"
                },
                "columnDefs": [
                        {
                            targets: 0,
                            className: "dt-body-left",
                            render: function (data, type, row) {
                                return data;
                            }
                        },
                        {
                            targets: 1,
                            className: "dt-body-right",
                            render: function (data, type, row) {
                                return '$' + parseFloat(data).toFixed(2);
                            }
                        },
                        {
                            targets: 2,
                            className: "dt-body-center",
                            render: function (data, type, row) {
                                return data;
                            }
                        },
                        {
                            targets: 3,
                            className: "dt-body-center",
                            render: function (data, type, row) {
                                return '$' + parseFloat(data).toFixed(2);
                            }
                        },
                        {
                            targets: 4,
                            className: "dt-body-center",
                            render: function (data, type, row) {
                                return data;
                            }
                        }
                    ],
                "lengthMenu": [5, 10, 25],
                "pageLength": 5,
            });

        },
        error: function() {
            alert('Error al realizar la consulta.');
        }
    });

}
function unificarPreventas(preventas) {
    let ids=[];
    const gastosOriginales = preventas.flatMap(preventa => preventa.gastos);

    const gastosUnificados = gastosOriginales.reduce((acumulador, actual) => {
        const existente = acumulador.find(
            gasto => gasto.descripcion === actual.descripcion && gasto.moneda === actual.moneda
        );

        if (existente) {
            existente.total += parseFloat(actual.total) || 0;
            existente.original += parseFloat(actual.original) || 0;
        } else {
            acumulador.push({
                ...actual,
                total: parseFloat(actual.total) || 0,
                original: parseFloat(actual.original) || 0
            });
        }

        return acumulador;
    }, []);

    const preventaUnificada = JSON.parse(JSON.stringify(preventas[0]));

    preventaUnificada.data_preventa.total_con_iva = 0;
    preventaUnificada.data_preventa.total_sin_iva = 0;
    preventaUnificada.data_preventa.bultos = 0;
    preventaUnificada.data_preventa.peso = 0;

    preventas.forEach(preventa => {
        preventaUnificada.data_preventa.total_con_iva += parseFloat(preventa.data_preventa.total_con_iva) || 0;
        preventaUnificada.data_preventa.total_sin_iva += parseFloat(preventa.data_preventa.total_sin_iva) || 0;
        preventaUnificada.data_preventa.bultos += parseInt(preventa.data_preventa.bultos, 10) || 0;
        preventaUnificada.data_preventa.peso += parseFloat(preventa.data_preventa.peso) || 0;
        ids.push(preventa.numero);
    });

    preventaUnificada.data_preventa.total_con_iva = preventaUnificada.data_preventa.total_con_iva.toFixed(4);
    preventaUnificada.data_preventa.total_sin_iva = preventaUnificada.data_preventa.total_sin_iva.toFixed(4);

    preventaUnificada.gastos = gastosUnificados;
    preventaUnificada.gastos_originales = gastosOriginales;
    preventaUnificada.ids=ids;
    preventaUnificada.data_preventa.referencia = generarNumero();
    //preventaUnificada.referencia = preventaUnificada.data_preventa.referencia;

    const datosParaGuardar = {
        preventaUnificada,
        gastosUnificados
    };
    const datosJSON = JSON.stringify(datosParaGuardar);
    localStorage.setItem('preventaUnificada', datosJSON);

    return {
        preventaUnificada,
        gastosUnificados
    };
}

function guardar_preventa_unificada(){
let x = $('#guardar_preventa_unificada').attr('data-id');
let preventaUnificada = JSON.parse(localStorage.getItem('preventaUnificada')) || [];
let preventa=preventaUnificada.preventaUnificada.data_preventa;
preventa.numero=preventaUnificada.preventaUnificada.numero;
let clase = preventaUnificada.preventaUnificada.clase;
let referencia = preventaUnificada.preventaUnificada.data_preventa.referencia;

let gastos=preventaUnificada.gastosUnificados;
let gastos_originales=preventaUnificada.preventaUnificada.gastos_originales;
let gastos_mostrar;
let ids=preventaUnificada.preventaUnificada.ids;

if(x==1){
    gastos_mostrar=gastos;
}else{
    gastos_mostrar=gastos_originales;
}

console.log(preventa);
    $.ajax({
        type: "POST",
        url: "/admin_cont/preventa/",
        data: JSON.stringify(preventa),
        contentType: "application/json",
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function(response) {
        console.log(response);
            if (response.resultado === 'exito') {
                guardar_gastos_uni(gastos_mostrar, clase,referencia);
                borrar_preventas_multiples(ids);
                alert("Los datos se han enviado correctamente.");
            } else {
                alert("Error al enviar los datos.");
            }
        },
        error: function() {
            alert("Error en la solicitud.");
        }
    });
}

function guardar_gastos_uni(gastos, clase,referencia){
    $.ajax({
        method: "POST",
        url: "/admin_cont/guardar_gasto_unificado/",
        data: JSON.stringify({
            gastos: gastos,  // Asegúrate de que los datos sean un objeto JavaScript
            clase: clase,
            referencia:referencia
        }),
        contentType: "application/json",
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function(response) {
            console.log(response);
        },
        error: function() {
            alert("Error en la solicitud.");
        }
    });
}

function borrar_preventas_multiples(preventas){

    preventas.forEach(function(p) {
    console.log(p);
    $.ajax({
        url: '/admin_cont/eliminar_preventa/',
        method: 'POST',
        headers: { 'X-CSRFToken': csrf_token },
        data: JSON.stringify({ id: p }),
        contentType: 'application/json',
        success: function(response) {
            console.log(response);
        },
        error: function(xhr) {
            alert("Error al eliminar la preventa: " + xhr.responseText);
        }
    });
    });
}

function generarNumero() {
    const now = new Date();

    const segundos = now.getSeconds();

    const milisegundos = now.getMilliseconds();

    const numero = `${segundos % 100}${milisegundos % 100}`.padStart(4, '0');

    return -parseInt(numero);
}


$('#abrir_arbi').on('click', function (event) {
    $("#arbitraje_modal").dialog({
        autoOpen: true,
        modal: true,
        title: "Cargar un arbitraje para el día de hoy",
        height: 300,
        width: 500,
        position: { my: "top", at: "top+20", of: window },
        buttons: [
            {
                text: "Guardar",
                class: "btn btn-primary",
                style: "width:100px",
                click: function () {
                    let arbDolar = $('#valor_arbitraje').val();
                    let parDolar = $('#valor_paridad').val();
                    let tipoMoneda = $('#moneda_select').val();
                    let pizDolar = $('#valor_pizarra').val();
                    let fecha = $('#fecha_arbi').val();

                    $.ajax({
                        url: "/admin_cont/guardar_arbitraje/",
                        dataType: 'json',
                        type: 'POST',
                        headers: { 'X-CSRFToken': csrf_token },
                        data: {
                            arbDolar: arbDolar,
                            parDolar: parDolar,
                            tipoMoneda: tipoMoneda,
                            pizDolar: pizDolar,
                            fecha:fecha
                        },
                        success: function(data) {
                            if(data['status'].length == 0){
                                alert("Valores guardados correctamente");
                                $("#arbitraje_modal").dialog("close");
                            }else{
                                alert(data['status']);
                            }
                        },
                        error: function(xhr, status, error) {
                            alert("Error al guardar los datos: " + error);
                        }
                    });
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
    });
        const hoy = new Date().toISOString().split('T')[0];
    // Establecer el valor predeterminado del campo de fecha
    document.getElementById('fecha_arbi').value = hoy;
        $.ajax({
        url: "/admin_cont/cargar_arbitraje/",
        type: "GET",
        dataType: "json",
        success: function (data) {
            // Cargar los valores en los campos
            $('#valor_arbitraje').val(data.arbitraje);
            $('#valor_pizarra').val(data.pizarra);
            $('#valor_paridad').val(data.paridad);
            $('#moneda_select').val(data.moneda);
        },
        error: function (xhr, status, error) {
            alert("Error al cargar los datos iniciales: " + error);
        }
    });
});


