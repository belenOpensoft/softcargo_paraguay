$(document).ready(function() {
    const valorInicial = $('#id_tipo').find('option:selected').text();
    $('#tipoSeleccionado').text(valorInicial);

    $('#id_tipo').change(function() {
        const valorSeleccionado = $(this).find('option:selected').text();
        $('#tipoSeleccionado').text(valorSeleccionado);
    });

    // Mostrar u ocultar tipo_factura
    function verificarTipoFactura() {
        const valorSeleccionado = $('#id_tipo').find('option:selected').val();
        if (valorSeleccionado === 'devolucion_contado') {
            $('#id_tipo_factura').hide();
        } else {
            $('#id_tipo_factura').show();
        }
    }

    verificarTipoFactura();

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

        // Función para mostrar u ocultar el campo proveedor2
        function toggleProveedor2() {
            if ($('#id_tercerizado').is(':checked')) {
                $('#proveedor2').show();
            } else {
                $('#proveedor2').hide();
            }
        }

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

    // Limpiar campos
    function limpiarCampos() {
        $('#item').val('');
        $('#id_descripcion_item input').val('');
        $('#id_precio input').val('');
    }

    function actualizarTotal() {
        let neto = 0;

        $('#itemTable tbody tr').each(function() {
            const precio = parseFloat($(this).data('precio')) || 0;
            neto += precio;
        });

        $('#id_neto input').val(neto.toFixed(2)).prop('readonly', true);

        let total = 0;
        $('#itemTable tbody tr').each(function() {
            const precio = parseFloat($(this).data('precio')) || 0;
            const iva = $(this).data('iva');

            const precioFinal = iva === 'Básico' ? precio * 1.22 : precio;
            total += precioFinal;
        });

        $('#id_total input').val(total.toFixed(2)).prop('readonly', true);

        const iva = total - neto;
        $('#id_iva input').val(iva.toFixed(2)).prop('readonly', true);
    }
});
var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;
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
                    resetModal("#dialog-form");
                    resetModal("#paymentModal");
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
    $('#proveedor').autocomplete({
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
        appendTo: "#proveedoresModal",
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
                        </tr>`;
                    $('#proveedorTable tbody').html(row);
                    $('#proveedorTable').show();
                },
                error: xhr => console.error('Error al obtener los detalles del cliente:', xhr)
            });
        }
    });
    $('#proveedor2').autocomplete({
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
        appendTo: "#proveedoresModal",
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
                        </tr>`;
                    $('#proveedor2Table tbody').html(row);
                    $('#proveedor2Table').show();
                },
                error: xhr => console.error('Error al obtener los detalles del cliente:', xhr)
            });
        }
    });
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