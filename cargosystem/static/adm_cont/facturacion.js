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
                url: "/buscar_cliente",
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
        select: function(event, ui) {
            const { id } = ui.item;
            $.ajax({
                url: "/buscar_clientes",
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
                url: "/buscar_item_v",
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
        select: function(event, ui) {
            $.ajax({
                url: "/buscar_items_v",
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

            $.ajax({
                url: "/procesar_factura/",
                dataType: 'json',
                type: 'POST',
                data: {
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
                    neto:neto
                },
                success: function(data) {
                    console.log('Factura procesada:', data);
                    alert('Factura procesada con éxito');
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
        "url": "/source_facturacion/",
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
            },
        }],
    }).prev('.ui-dialog-titlebar').remove();
}

$('#preventa').on('click', function() {
    $("#preventa_modal").dialog({
        autoOpen: true,
        modal: true,
        width: wWidth*0.60,
        height: wHeight*0.90,
        buttons: {
            "Cerrar": function() {
                $(this).dialog("close");
                $('#preventa_table').DataTable().destroy();

            }
        }
    });
    $('#preventa_table').DataTable({
        serverSide: true,
        ajax: {
            url: "/source_infofactura",
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
    let referencia = $(this).find('td').eq(8).text();
    let clase = $(this).find('td').eq(7).text();
    let preventa = $(this).find('td').eq(0).text();

    $.ajax({
        url: "/cargar_preventa_infofactura/",
        method: 'POST',
        data: {
            'referencia': referencia,
            'clase': clase,
            'preventa': preventa
        },
        headers: { 'X-CSRFToken': csrf_token },
        success: function(response) {
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

function facturar_preventa() {
    $("#preventa_modal").dialog('close');
    let gastos = JSON.parse(localStorage.getItem('gastos_preventa')) || [];
    let preventa = JSON.parse(localStorage.getItem('preventa')) || [];
    console.log(gastos);

    $("#cliente").val(preventa.cliente_i);
    $("#cliente").autocomplete("search", preventa.cliente_i);

    setTimeout(function () {
        const li = $('#cliente').autocomplete('widget').find("li:contains('" + preventa.cliente_i + "')");

        if (li.length > 0) {
            li.trigger('click');  // Disparar el click si se encuentra el cliente
        } else {
            console.error('No se encontró el cliente en los resultados');
        }
    }, 300);  // Ajustar el tiempo de espera según sea necesario

    // Iterar sobre los gastos para agregar cada uno
    gastos.forEach(gasto => {
        const desc = gasto.descripcion.split(' - ')[1];
        $('#id_precio_fac').val(gasto.total);
        $('#item').val(desc);
        $('#item').autocomplete("search", desc);
        console.log(desc);
        setTimeout(function () {
            const ce = $('#item').autocomplete('widget').find("li:contains('" + desc + "')");

            if (ce.length > 0) {
                ce.trigger('click');  // Seleccionar el item

            setTimeout(function () {
                $("#agregarItem").trigger('click');
             }, 300);

            } else {
                console.error('No se encontró el item en los resultados');
            }
        }, 300);  // Asegurarse de que se carguen los resultados antes de seleccionar el item
    });
}

