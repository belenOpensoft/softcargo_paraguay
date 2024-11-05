$(document).ready(function() {
$('#div_tabla').css('display', 'none');
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
            const id = 123;
            console.log(ui.item);
            let codigo;
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

function cargar_tabla_imputable(codigo){
    const table = $('#imputableTable').DataTable({
                ajax: {
                    url: '/obtener_imputables',
                    data: { codigo: '123' },  // Reemplaza '123' con el código adecuado
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
                lengthMenu: [5, 10, 25, 50],
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