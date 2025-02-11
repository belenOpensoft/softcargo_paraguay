$(document).ready(function() {
    var buscar = '';
    var que_buscar = '';
    let contador = 0;

    verificarTipoFactura();

    $('#tabla_proveedoresygastos tfoot th').each(function () {
        let title = $(this).text();
        if (title !== '') {
            $(this).html('<input type="text" class="form-control"  autocomplete="off" id="buscoid_' + contador + '" type="text" placeholder="Buscar ' + title + '"  autocomplete="off" />');
            contador++;
        } else {
            $(this).html('<button class="btn" title="Borrar filtros" id="clear" ><span class="glyphicon glyphicon-erase"></span></button> ');
        }
    });
    //tabla general master
    table = $('#tabla_proveedoresygastos').DataTable({
    "dom": 'Btlipr',
    "scrollX": true,
    "bAutoWidth": false,
    "scrollY": wHeight * 0.60,
    "columnDefs": [
        {
            "targets": [0],  // Ocultamos ambas columnas en una sola configuración
            "visible": false,
            "searchable": false  // Opcional: evita que se incluyan en las búsquedas
        },
    ],
    "order": [[2, "desc"]],
    "processing": true,
    "serverSide": true,
    "pageLength": 100,
    "ajax": {
        "url": "/admin_cont/source_proveedoresygastos/",
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
    const valorInicial = $('#id_tipo').find('option:selected').text();

    $('#tipoSeleccionado').text(valorInicial);

    $('#id_tipo').change(function() {
        const valorSeleccionado = $(this).find('option:selected').text();
        $('#tipoSeleccionado').text(valorSeleccionado);
    });

    $('#id_tipo').change(function() {
        const valorSeleccionado = $(this).find('option:selected').text();
        $('#tipoSeleccionado').text(valorSeleccionado);
        verificarTipoFactura();
    });

    // Verificar el estado inicial de tercerizado
        toggleProveedor2();

    // Detectar cambios en el campo tercerizado
    $('#id_tercerizado').change(function() {
        toggleProveedor2();
    });

    // Autocomplete proveedor
    $('#proveedor').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/admin_cont/buscar_proveedor",
                dataType: 'json',
                data: { term: request.term },
                success: function(data) {
                    response(data.map(proveedor => ({
                        label: proveedor.text,
                        value: proveedor.text,
                        codigo: proveedor.codigo
                    })));
                },
                error: xhr => console.error('Error al buscar proveedores:', xhr)
            });
        },
        minLength: 2,
        appendTo: "#proveedoresModal",
        select: function(event, ui) {
            let codigo = ui.item['codigo'];
            $.ajax({
                url: "/admin_cont/buscar_proveedores",
                data: { 'codigo': codigo, },
                dataType: 'json',
                success: proveedor => {
                    const row = `
                        <tr id="proveedor-${codigo}">
                            <td class="d-none">${proveedor.codigo}</td>
                            <td>${proveedor.empresa}</td>
                            <td>${proveedor.ruc}</td>
                        </tr>`;
                    $('#proveedorTable tbody').html(row);
                    $('#proveedorTable').show();
                },
                error: xhr => console.error('Error al obtener los detalles del proveedor:', xhr)
            });
        }
    });

    // Autocomplete proveedor2
    $('#proveedor2').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/admin_cont/buscar_proveedor",
                dataType: 'json',
                data: { term: request.term },
                success: function(data) {
                    response(data.map(proveedor => ({
                        label: proveedor.text,
                        value: proveedor.text,
                        id: proveedor.id
                    })));
                },
                error: xhr => console.error('Error al buscar proveedores:', xhr)
            });
        },
        minLength: 2,
        select: function(event, ui) {
            const { id } = ui.item;

            $.ajax({
                url: "/admin_cont/buscar_proveedores",
                data: { id },
                dataType: 'json',
                success: proveedor => {
                    const row = `
                        <tr id="proveedor-${id}">
                            <td class="d-none">${proveedor.codigo}</td>
                            <td>${proveedor.empresa}</td>
                        </tr>`;
                    $('#proveedor2Table tbody').html(row);
                    $('#proveedor2Table').show();
                },
                error: xhr => console.error('Error al obtener los detalles del proveedor:', xhr)
            });
        }
    });

    let itemCounter = 0;

    // Autocomplete para el input "item"
    $('#item').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/admin_cont/buscar_item_c",
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
            const tipoCobroActual = $('#id_tipo_cobro select').val();
            const cobroActual = $('#id_cobro select').val();
            const precio = parseFloat($('#id_precio input').val());


            $.ajax({
                url: "/admin_cont/buscar_items_c",
                data: { id: ui.item.id },
                dataType: 'json',
                success: servicio => {
                    $('#id_precio input').val(servicio.precio).data({
                        iva: servicio.iva,
                        cuenta: servicio.cuenta,
                        codigo: servicio.item,
                        embarque: servicio.embarque,
                        gasto: servicio.gasto
                    });
                    $('#id_descripcion_item input').val(servicio.nombre);
                    $('#id_tipo_cobro select').val(tipoCobroActual);
                    $('#id_cobro select').val(cobroActual);
                    $('#id_precio input').val(precio);
                },
                error: xhr => console.error('Error al obtener los detalles del item:', xhr)
            });
        }
    });

    // Agregar Item a la tabla
    $('#agregarItem').on('click', function() {
        const item = $('#item').val();
        const descripcion = $('#id_descripcion_item input').val();
        const precio = parseFloat($('#id_precio input').val());
        const tipo = $('#id_tipo_cobro select').val();
        const pago = $('#id_cobro select').val();

        if (item && descripcion && !isNaN(precio)) {
            const iva = $('#id_precio input').data('iva');
            const cuenta = $('#id_precio input').data('cuenta');
            const codigo = $('#id_precio input').data('codigo');
            const embarque = $('#id_precio input').data('embarque') || '';
            const comp = $('#id_precio input').data('comp') || '';
            const gasto = $('#id_precio input').data('gasto') || '';

            itemCounter++;
            const rowId = `item-${itemCounter}`;

            const row = `
                <tr id="${rowId}" data-precio="${precio}" data-iva="${iva}" data-cuenta="${cuenta}">
                    <td style="display:none;">${rowId}</td>
                    <td>${codigo}</td>
                    <td>${descripcion}</td>
                    <td>${precio.toFixed(2)}</td>
                    <td>${iva}</td>
                    <td>${cuenta}</td>
                    <td>${embarque}</td>
                    <td>${''}</td>
                    <td>${''}</td>
                    <td>${comp}</td>
                    <td>${''}</td>
                    <td>${''}</td>
                    <td>${gasto}</td>
                    <td>${tipo}</td>
                    <td>${pago}</td>
                    <td>${''}</td>
                    <td>${''}</td>
                    <td>${''}</td>
                </tr>`;

            // Añadir la fila a la tabla
            $('#itemTable tbody').append(row);
            $('#itemTable').css('visibility','visible');
            $('#eliminarSeleccionados').show();
            limpiarCampos();
            actualizarTotal();

            $('#totales').show();
        } else {
            alert('Por favor, completa todos los campos antes de agregar el item.');
        }
    });


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
            let fecha = $('#id_fecha_registro').val();
            let paridad = $('#id_paridad').val();
            let arbitraje = $('#id_arbitraje').val();
            let imputar = $('#id_imputar').val();
            let moneda = $('#id_moneda').val();
            let clienteData = {
                codigo: $('#proveedorTable tbody tr td').eq(0).text(),
                empresa: $('#proveedorTable tbody tr td').eq(1).text(),
                rut: $('#proveedorTable tbody tr td').eq(2).text(),
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
            let data=[];
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
                    total:$('#id_total input').val(),
                    iva:$('#id_iva input').val(),
                    neto:$('#id_neto input').val(),
                }
            $.ajax({
                url: "/admin_cont/procesar_factura_proveedor/",
                dataType: 'json',
                type: 'POST',
                data: data,
                headers: { 'X-CSRFToken': csrf_token },
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
});
var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;
let total=0;

// Mostrar u ocultar tipo_factura
function verificarTipoFactura() {
    const valorSeleccionado = $('#id_tipo').find('option:selected').val();
    if (valorSeleccionado === 'devolucion_contado') {
        $('#id_tipo_factura').hide();
    } else {
        $('#id_tipo_factura').show();
    }
}
function abrir_modal() {
    $("#proveedoresModal").dialog({
        autoOpen: true,
        modal: true,
        width: wWidth * 0.90,
        height: wHeight * 0.95,
        buttons: [
            {
                class: "btn btn-dark",
                style: "width:100px",
                text: "Salir",
                click: function() {
                    $(this).dialog("close");
                    existe_cliente=false;
                    resetModal("#proveedoresModal");
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
//    $('#proveedor2').autocomplete({
//        source: function(request, response) {
//            $.ajax({
//                url: "/admin_cont/buscar_cliente",
//                dataType: 'json',
//                data: { term: request.term },
//                success: function(data) {
//                    response(data.map(cliente => ({
//                        label: cliente.text,
//                        value: cliente.text,
//                        id: cliente.id
//                    })));
//                },
//                error: xhr => console.error('Error al buscar clientes:', xhr)
//            });
//        },
//        minLength: 2,
//        appendTo: "##proveedoresModal",
//        select: function(event, ui) {
//            const { id } = ui.item;
//            $.ajax({
//                url: "/admin_cont/buscar_clientes",
//                data: { id },
//                dataType: 'json',
//                success: cliente => {
//                    const row = `
//                        <tr id="cliente-${id}">
//                            <td class="d-none">${cliente.codigo}</td>
//                            <td>${cliente.empresa}</td>
//                        </tr>`;
//                    $('#proveedor2Table tbody').html(row);
//                    $('#proveedor2Table').show();
//                },
//                error: xhr => console.error('Error al obtener los detalles del cliente:', xhr)
//            });
//        }
//    });
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
    appendTo: "#proveedoresModal", // Asegúrate de usar el contenedor modal adecuado
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

$('#agregarItem').off('click').on('click', function() {
    // Obtén los valores antes de cualquier operación
    const item = $('#item').val();
    const descripcion = $('#id_descripcion_item input').val();
    const precio = parseFloat($('#id_precio input').val());
    const iva = $('#id_precio input').data('iva');
    const cuenta = $('#id_precio input').data('cuenta');
    const codigo = $('#id_precio input').data('codigo');

    // Valida los campos antes de proceder
    if (item && descripcion && !isNaN(precio)) {
        itemCounter++;
        const rowId = `item-${itemCounter}`;

        // Agrega una nueva fila a la tabla
        const row = `
            <tr id="${rowId}" data-precio="${precio}" data-iva="${iva}" data-cuenta="${cuenta}">
                <td>${codigo}</td>
                <td>${descripcion}</td>
                <td>${precio.toFixed(2)}</td>
                <td>${iva}</td>
                <td>${cuenta}</td>
            </tr>`;

        $('#itemTable tbody').append(row);
        $('#itemTable').css('visibility', 'visible'); // Asegúrate de que la tabla sea visible
        $('#eliminarSeleccionados').show();

        // Limpia solo los campos relevantes
        $('#item').val('');
        $('#id_descripcion_item input').val('');
        $('#id_precio input').val('');
        $('#id_precio input').data('iva', '');
        $('#id_precio input').data('cuenta', '');
        $('#id_precio input').data('codigo', '');

        actualizarTotal(); // Actualiza los totales después de agregar el ítem
        $('#totales').show();
    } else {
        alert('Por favor, completa todos los campos antes de agregar el item.');
    }
});

}
function resetModal(modalId) {
    const modal = $(modalId);

    // Reinicia el formulario
    modal.find("form").each(function () {
        this.reset();
    });

    // Limpia tablas
    modal.find("table").each(function () {
        if ($.fn.DataTable.isDataTable(this)) {
            $(this).DataTable().clear().draw();
        } else {
            $(this).find("tbody").empty();
        }
    });
}
function limpiarCampos() {
    $('#item').val('');
    $('#id_descripcion_item input').val('');
    $('#id_precio input').val('');
}
// Función para mostrar u ocultar el campo proveedor2
function toggleProveedor2() {
        if ($('#id_tercerizado').is(':checked')) {
            $('#proveedor2').show();
        } else {
            $('#proveedor2').hide();
        }
}
function actualizarTotal() {
    let neto = 0;
    let total = 0; // Inicializar total aquí

    $('#itemTable tbody tr').each(function() {
        const precio = parseFloat($(this).data('precio')) || 0;
        neto += precio;
    });

    $('#id_neto input').val(neto.toFixed(2)).prop('readonly', true);

    $('#itemTable tbody tr').each(function() {
        const precio = parseFloat($(this).data('precio')) || 0;
        const iva = $(this).data('iva');

        // Calcular el precio final con IVA
        const precioFinal = iva === 'Basico' ? precio * 1.22 : precio;
        total += precioFinal;

        console.log(iva);
        console.log('precio ' + precio);
    });

    $('#id_total input').val(total.toFixed(2)).prop('readonly', true);

    const iva_t = total - neto;
    console.log('total ' + total);
    $('#id_iva input').val(iva_t.toFixed(2)).prop('readonly', true);
}
$('#abrir_arbi_prov').on('click', function (event) {
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