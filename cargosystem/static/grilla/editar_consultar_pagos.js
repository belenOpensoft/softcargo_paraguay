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
$('#abrir_arbi').on('click', function (event) {
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
