document.addEventListener('DOMContentLoaded', function () {
    $('#id_socio_comercial').autocomplete({
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
    select: function(event, ui) {
        const codigo = ui.item.codigo;
        const nombre = ui.item.value;
        $('#id_socio_comercial').val(nombre);
        $('#id_cliente_hidden').val(codigo);
    }
    });
});