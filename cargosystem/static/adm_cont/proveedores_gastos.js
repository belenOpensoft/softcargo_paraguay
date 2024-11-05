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
                url: "/buscar_proveedor",
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
                url: "/buscar_proveedores",
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
                url: "/buscar_proveedor",
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
                url: "/buscar_proveedores",
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
                url: "/buscar_item_c",
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
                url: "/buscar_items_c",
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