$('#proveedores').autocomplete({
    source: function(request, response) {
        $.ajax({
            url: "/buscar_proveedor/",
            dataType: 'json',
            type: 'GET',
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
});

function abrir_modalFiltro() {
    $('#filtroM').find('form').trigger('reset');

    $("#filtroM").dialog({
        autoOpen: true,
        modal: true,
        width: $(window).width() * 0.60,
        height: $(window).height() * 0.80,
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

