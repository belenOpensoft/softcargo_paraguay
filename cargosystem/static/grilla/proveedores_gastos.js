$(document).ready(function() {
    var buscar = '';
    var que_buscar = '';
    let contador = 0;

    verificarTipoFactura();


    // Evento para el primer campo (id_fecha_registro)
    $("#id_fecha_registro").change(function () {
        actualizarFechas(this, "#id_fecha_documento");  // Copia la fecha al segundo campo
        actualizarFechas(this, "#id_vencimiento");  // Copia la fecha al tercer campo
    });

    // Evento para el segundo campo (id_fecha_documento)
    $("#id_fecha_documento").change(function () {
        actualizarFechas(this, "#id_vencimiento");  // Copia la fecha al tercer campo
    });
    $('#tabla_proveedoresygastos tfoot th').each(function(index) {
        let title = $('#tabla_proveedoresygastos thead th').eq(index).text();

        if (index === 0) {
            // Si es la primera columna, colocar el botón de limpiar filtros
            $(this).html('<button class="btn btn-danger" title="Borrar filtros" id="clear"><span class="glyphicon glyphicon-erase"></span> Limpiar</button>');
        } else if (title !== '') {
            // Agregar inputs de búsqueda en las demás columnas
            $(this).html('<input type="text" class="form-control filter-input" autocomplete="off" id="buscoid_' + index + '" placeholder="Buscar ' + title + '" />');
        }
    });
    // Evento para limpiar todos los filtros
    $(document).on("click", "#clear", function() {
        awbRegex='';
        $(".filter-input").val("").trigger("keyup"); // Limpia los inputs y activa la búsqueda
        $(".filter-input").removeClass("is-invalid"); // Se quita el rojo si se vacía
        table.ajax.reload();
    });
    // Evento para resaltar los inputs cuando tienen contenido
    $(document).on("input", ".filter-input", function() {
        if ($(this).val().trim() !== "") {
            $(this).addClass("is-invalid"); // Se pone en rojo
        } else {
            $(this).removeClass("is-invalid"); // Se quita el rojo si se vacía
        }
    });
    table = $('#tabla_proveedoresygastos').DataTable({
    "dom": 'Btlipr',
    "scrollX": true,
    "bAutoWidth": false,
    "scrollY": wHeight * 0.60,
    "columnDefs": [
        {
            "targets": [0],  // Ocultamos ambas columnas en una sola configuración
            "visible": true,
            "searchable": false ,
            "className": "invisible-column",
             "render": function(data, type, row) {
            return "";  // Devuelve una celda vacía
        }
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
        let api = this.api();
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

    // Al hacer clic en "Agregar Item" se agrega una nueva fila o se actualiza la fila en edición
    $('#agregarItem').on('click', function() {
        const item = $('#item').val();
        const descripcion = $('#id_descripcion_item input').val();
        const precio = parseFloat($('#id_precio input').val());

        if (item && descripcion && !isNaN(precio)) {
            const iva = $('#id_precio input').data('iva') || "";   // puede estar vacío en un nuevo item
            const cuenta = $('#id_precio input').data('cuenta') || "";
            const codigo = $('#id_precio input').data('codigo') || "";

            // Si hay una fila en edición, se actualiza en lugar de agregar
            if ($("#itemTable tr.editing").length > 0) {
                var $editingRow = $("#itemTable tr.editing");
                // Actualiza los atributos data del <tr>
                $editingRow.data("precio", precio);
                $editingRow.data("iva", iva);
                $editingRow.data("cuenta", cuenta);

                // Actualiza el contenido de cada celda
                $editingRow.find("td").eq(0).text(codigo);
                $editingRow.find("td").eq(1).text(item);
                $editingRow.find("td").eq(2).text(descripcion);
                $editingRow.find("td").eq(3).text(precio.toFixed(2));
                $editingRow.find("td").eq(4).text(iva);
                $editingRow.find("td").eq(5).text(cuenta);

                $editingRow.removeClass("editing");
            }else {
                // Agregar nueva fila
                itemCounter++;
                const rowId = `item-${itemCounter}`;
                const row = `
                    <tr id="${rowId}" data-precio="${precio}" data-iva="${iva}" data-cuenta="${cuenta}">
                        <td style="display:none;">${codigo}</td>
                        <td>${item}</td>
                        <td>${descripcion}</td>
                        <td>${precio.toFixed(2)}</td>
                        <td>${iva}</td>
                        <td>${cuenta}</td>
                    </tr>`;
                $('#itemTable tbody').append(row);
                $('#itemTable').show();

            }
            $('#eliminarSeleccionados').show();
            $('#clonarItem').css('display','block');
            $('#itemTable').css('visibility', 'visible');
            actualizarTotal();
            $('#totales').show();
            limpiarCampos();
        } else {
            alert('Por favor, completa todos los campos antes de agregar el item.');
        }
    });
    $("#itemTable").on("dblclick", "tr", function() {
        var $row = $(this);
        // Asume que la fila tiene las 6 celdas en el orden correcto
        var codigo = $row.find("td").eq(0).text().trim();    // Código (oculto)
        var item = $row.find("td").eq(1).text().trim();        // Item
        var descripcion = $row.find("td").eq(2).text().trim(); // Descripción
        var precio = $row.find("td").eq(3).text().trim();      // Precio
        var iva = $row.find("td").eq(4).text().trim();         // IVA
        var cuenta = $row.find("td").eq(5).text().trim();      // Cuenta

        // Cargar los datos en los campos de entrada
        $("#item").val(item);
        $("#id_descripcion_item input").val(descripcion);
        $("#id_precio input").val(precio);

        // Guardar datos adicionales en el input de precio (por si se necesitan al actualizar)
        $("#id_precio input").data("iva", iva);
        $("#id_precio input").data("cuenta", cuenta);
        $("#id_precio input").data("codigo", codigo);

        // Marcar la fila como "editing" para que se actualice en lugar de agregar una nueva
        $("#itemTable tr").removeClass("editing");
        $row.addClass("editing");
    });
    // Botón para clonar la fila seleccionada
    $("#clonarItem").on("click", function() {
        var $selected = $("#itemTable tr.table-active");
        if ($selected.length > 0) {
            itemCounter++;
            var $clone = $selected.clone();
            $clone.attr("id", "item-" + itemCounter);
            $clone.removeClass("selected editing");
            $clone.removeClass("table-active");
            $clone.removeClass("table-primary");
            $("#itemTable tbody").append($clone);
            actualizarTotal();
        } else {
            alert("Selecciona una fila para clonar.");
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
                    $('#proveedoresModal').dialog('close');
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
        console.log($(this));
    });

    $('#id_neto input').val(neto.toFixed(2)).prop('readonly', true);

    $('#itemTable tbody tr').each(function() {
        const precio = parseFloat($(this).data('precio')) || 0;
        const iva = $(this).data('iva');

        // Calcular el precio final con IVA
        const precioFinal = iva === 'Basico' ? precio * 1.22 : precio;
        total += precioFinal;

    });

    $('#id_total input').val(total.toFixed(2)).prop('readonly', true);

    const iva_t = total - neto;
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
function actualizarFechas(origen, destino) {
    let fechaSeleccionada = $(origen).val();
    if (fechaSeleccionada) {
        $(destino).val(fechaSeleccionada);
    }
}