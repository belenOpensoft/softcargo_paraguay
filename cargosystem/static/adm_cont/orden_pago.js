$(document).ready(function() {
$('#div_tabla').css('display', 'none');
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
            const id = 123;
            console.log(ui.item);
            let codigo;
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
                    codigo = $('#proveedorTable tbody tr#proveedor-' + id + ' .d-none').text();
                    alert("Código del proveedor:" + codigo);
                    cargar_tabla_imputable(codigo);
                    $('.totalesImputables').css('display', 'block');
                    $('#div_tabla').css('display', 'block');
                },
                error: xhr => console.error('Error al obtener los detalles del proveedor:', xhr)

            });


        }
    });
});
var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;
let total=0;
function cargar_tabla_imputable(codigo){
    const table = $('#imputableTable').DataTable({
                ajax: {
                    url: '/admin_cont/obtener_imputables',
                    data: { codigo: codigo },  // Reemplaza '123' con el código adecuado
                    dataSrc: 'data'  // Indica dónde están los datos en la respuesta JSON
                },
                columns: [
                    { data: 'id' },
                    { data: 'vto' },
                    { data: 'fecha_emision' },
                    { data: 'documento' },
                    { data: 'monto_total' },
                    { data: 'saldo' },
                    { data: 'detalle' },
                    { data: 'embarque' },
                    { data: 'co' },
                    { data: 'posicion' },
                    { data: 'tc' },
                    { data: 'moneda' },
                    { data: 'paridad' },
                    { data: 'monto_original' }
                ],
                searching: false,
                pageLength: 5,
                lengthMenu: false,
                language: {
                    "sProcessing": "Procesando...",
                    "sLengthMenu": "Mostrar _MENU_ entradas",
                    "sZeroRecords": "No se encontraron resultados",
                    "sEmptyTable": "No hay datos disponibles en la tabla",
                    "sInfo": "Mostrando de _START_ a _END_ de _TOTAL_ entradas",
                    "sInfoEmpty": "Mostrando 0 a 0 de 0 entradas",
                    "sInfoFiltered": "(filtrado de _MAX_ entradas totales)",
                    "sInfoPostFix": "",
                    "sSearch": "Buscar:",
                    "sUrl": "",
                    "sInfoThousands": ",",
                    "sLoadingRecords": "Cargando...",
                    "oPaginate": {
                        "sFirst": "Primero",
                        "sLast": "Último",
                        "sNext": "Siguiente",
                        "sPrevious": "Anterior"
                    },
                    "oAria": {
                        "sSortAscending": ": Activar para ordenar la columna de forma ascendente",
                        "sSortDescending": ": Activar para ordenar la columna de forma descendente"
                    }
                },
            });
}
function abrir_modal() {
    $("#pagosModal").dialog({
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
                    resetModal("#pagosModal");
                    //resetModal("#paymentModal");
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