$(document).ready(function() {
    $('#cliente').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "{% url 'buscar_cliente' %}",
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
        minLength: 2, // Mínimo de caracteres para activar la búsqueda
        select: function(event, ui) {
            const { id } = ui.item;

            $.ajax({
                url: "{% url 'buscar_clientes' %}",
                data: { id },
                dataType: 'json',
                success: cliente => {
                    const row = `
                        <tr id="cliente-${id}">
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
            const tipo = $('#id_tipo select').val();
            $.ajax({
                url: "{% url 'buscar_item' %}",
                dataType: 'json',
                data: {
                    term: request.term,
                    tipo_gasto: tipo
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
                url: "{% url 'buscar_items' %}",
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

    // Eliminar filas seleccionadas
    $('#eliminarSeleccionados').on('click', function() {
        if (confirm('¿Está seguro de que desea eliminar la selección?')) {
            $('#itemTable tbody tr.table-active').remove();
            actualizarTotal();

            // Ocultar el div de totales si no hay items
            if ($('#itemTable tbody tr').length === 0) {
                $('#itemTable').hide();
                $('#eliminarSeleccionados').hide();
                $('#totales').hide();
            }
        }
    });

    // Limpiar campos del formulario
    function limpiarCampos() {
        $('#item').val('');
        $('#id_descripcion_item input').val('');
        $('#id_precio input').val('');
    }

    // Actualizar total
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

        const facturaData = {
            tipo: $('#id_tipo select').val(),
            serie: $('#id_serie select').val(),
            prefijo: $('#id_prefijo select').val(),
            numero: $('#id_numero input').val(),
            fecha: $('#id_fecha input').val(),
            moneda: $('#id_moneda select').val(),
            arbitraje: $('#id_arbitraje input').val(),
            paridad: $('#id_paridad input').val(),
            imputar: $('#id_imputar select').val(),
            cliente: $('#cliente').val()
        };

        let items = [];
        $('#itemTable tbody tr').each(function() {
            const item = {
                codigo: $(this).find('td').eq(0).text(),
                descripcion: $(this).find('td').eq(1).text(),
                precio: $(this).find('td').eq(2).text(),
                iva: $(this).find('td').eq(3).text(),
                cuenta: $(this).find('td').eq(4).text()
            };
            items.push(item);
        });

        const data = {
            factura: facturaData,
            items: items,
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
        };

        $.ajax({
            url: "{% url 'procesar_factura' %}",
            method: 'POST',
            data: data,
            dataType: 'json',
            success: function(response) {
                alert('Factura enviada correctamente');
            },
            error: function(xhr) {
                console.error('Error al enviar la factura:', xhr);
            }
        });
    });
});