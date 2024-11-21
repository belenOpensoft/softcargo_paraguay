//facturar
function facturar(){
    let selectedRowN = localStorage.getItem('num_house_gasto');
    const wHeight = $(window).height();
    const wWidth = $(window).width();
                $('#destinatario').val('');
                $('#destinatario_input').val('');
                $('#destinatario').css({"border-color": "", 'box-shadow': ''});
                $('#destinatario_input').css({"border-color": "", 'box-shadow': ''});
            $("#facturar_modal").dialog({
                autoOpen: true,
                open: function (event, ui) {
                cargar_gastos_factura();
                },
                modal: true,
                title: "Facturar el House N°: " + selectedRowN,
                height: wHeight * 0.90,
                width: wWidth * 0.70,
                class: 'modal fade',
                       buttons: [
                    {
                        text: "Cancelar",
                        class: "btn btn-dark",
                        style: "width:100px",
                        click: function () {
                            $(this).dialog("close");
                        }
                    }
                ],
                beforeClose: function (event, ui) {
                // localStorage.removeItem('num_house_gasto');
                 $('#facturar_table').DataTable().destroy();
                 $("#facturar_form").trigger("reset");
//                 $('#table_add_im tbody tr').removeClass('table-secondary');
//                $('#table_edit_im tbody tr').removeClass('table-secondary');
//                $('#tabla_house_directo tbody tr').removeClass('table-secondary');
                }
            })

}
function asignar_costo(event) {
event.preventDefault();
    const filaSeleccionada = $('#facturar_table tbody tr.table-secondary');

    if (filaSeleccionada.length > 0) {
        const data = $('#facturar_table').DataTable().row(filaSeleccionada).data();
        let cliente = $('#destinatario').val();
        let cliente_id = $('#destinatario_input').val();

        if(cliente){
            $('#facturar_table').DataTable().cell(filaSeleccionada, 3).data(cliente);
            $(filaSeleccionada).find('td').eq(3).text(cliente);
            $('#destinatario').val('');
            $('#destinatario_input').val('');
            $('#destinatario').css({"border-color": "", 'box-shadow': ''});
            $('#destinatario_input').css({"border-color": "", 'box-shadow': ''});

        } else {
            alert('Debe seleccionar un destinatario.');
        }

    } else {
        alert("No hay ninguna fila seleccionada.");
    }
}
function asignar_costo_todos(event) {
event.preventDefault();
    let cliente = $('#destinatario').val();
    let cliente_id = $('#destinatario_input').val();

    if (!cliente) {
        alert('Debe seleccionar un destinatario.');
        return;
    }

    let tabla = $('#facturar_table').DataTable();
    tabla.rows().every(function() {
        this.cell(this, 3).data(cliente);
        $(this.node()).find('td').eq(3).text(cliente);
    });


}
function asignar_no(event) {
    event.preventDefault();
    const filaSeleccionada = $('#facturar_table tbody tr.table-secondary');

    if (filaSeleccionada.length > 0) {
        const data = $('#facturar_table').DataTable().row(filaSeleccionada).data();
        const mensaje = 'NO SE FACTURA EL CONCEPTO'; // Texto a asignar

        console.log(data[0]);
        console.log(mensaje);

        // Asigna el valor a la columna y al DOM
        $('#facturar_table').DataTable().cell(filaSeleccionada, 3).data(mensaje);
        $(filaSeleccionada).find('td').eq(3).text(mensaje);

    } else {
        alert("No hay ninguna fila seleccionada.");
    }
}
function asignar_no_todos(event) {
event.preventDefault();
    const mensaje = 'NO SE FACTURA EL CONCEPTO'; // Texto a asignar

    let tabla = $('#facturar_table').DataTable();
    tabla.rows().every(function() {
        // Asigna el valor a la columna y al DOM
        this.cell(this, 3).data(mensaje);
        $(this.node()).find('td').eq(3).text(mensaje);
    });

    // tabla.draw(); // Descomentar si necesitas que la tabla se redibuje
}
function sumar_ingresos() {
    let totalIngresos = 0;
    const tabla = $('#facturar_table').DataTable();

    // Verifica si DataTable está inicializado
    if (!$.fn.DataTable.isDataTable('#facturar_table')) {
        console.log("DataTable no está inicializado.");
        return;
    }

    // Itera sobre cada fila de la tabla y suma el valor en la columna 3
    tabla.rows().every(function() {
        const data = this.data();
        console.log("Datos de la fila:", data); // Verifica el contenido de cada fila
        const valor = parseFloat(data[3]) || 0;
        totalIngresos += valor;
        console.log("Total acumulado:", totalIngresos);
    });

    // Asigna el resultado total al input con ID #total_ingresos
    $('#total_ingresos').val(totalIngresos.toFixed(2)); // Redondea a 2 decimales si es necesario
}
function enviarDatosTabla() {
let preventa;
    let num=localStorage.getItem('num_house_gasto');
    let clase=localStorage.getItem('clase_house');
    $.ajax({
                url: '/admin_cont/house_detail_factura',
                data: { numero: num, clase:clase},
                method: 'GET',
                success: function (house) {
                    console.log(house.awb_e);
                    if(house.awb_e==0){
                        $.ajax({
                        url: '/admin_cont/source_embarque_factura/',
                        data: { numero: num, clase:clase},
                        method: 'GET',
                        success: function (embarque) {
                                preventa=({
                                    seguimiento:house.seguimiento,
                                    referencia:num,
                                    transportista:getNameByIdClientes(house.transportista_e),
                                    vuelo:house.viaje_e,
                                    master:house.awb_e,
                                    house:house.hawb_e,
                                    fecha:house.fecharetiro_e,
                                    kilos:0,
                                    bultos:0,
                                    volumen:0,
                                    origen:house.origen_e,
                                    destino:house.destino_e,
                                    consigna:getNameByIdClientes(house.consignatario_e),
                                    embarca:getNameByIdClientes(house.embarcador_e),
                                    agente:getNameByIdClientes(house.agente_e),
                                    posicion:house.posicion_e,
                                    terminos:house.terminos,
                                    pagoflete:house.pago,
                                    commodity:embarque[0].producto_id,
                                });

                                //guardar la preventa
                                    guardar_preventa(preventa);
                                    const tabla = $('#facturar_table').DataTable();
                                    let datosTabla = [];

                                    tabla.rows().every(function() {
                                        const data = this.data();

                                        datosTabla.push({
                                            id_gasto: data[0],
                                            notas: $(this.node()).find('td').eq(7).text(),
                                            descripcion: $(this.node()).find('td').eq(3).text()
                                        });
                                    });
                                   update_gastos(datosTabla);
                                   $('#facturar_modal').dialog('close');
                                    if ($.fn.DataTable.isDataTable('#table_add_im')) {
                                        $('#table_add_im').DataTable().ajax.reload(null, false);
                                    }

                                    if ($.fn.DataTable.isDataTable('#table_edit_im')) {
                                        $('#table_edit_im').DataTable().ajax.reload(null, false);
                                    }
                                    if ($.fn.DataTable.isDataTable('#tabla_house_directo')) {
                                        $('#tabla_house_directo').DataTable().ajax.reload(null, false);
                                    }

                        },
                        error: function (xhr, status, error) {
                            console.error("Error fetching data:", error);
                        }
                    });
                    }else{
                    $.ajax({
                        url: '/admin_cont/source_master_factura/',
                        data: { master: house.awb_e, clase:clase},
                        method: 'GET',
                        success: function (master) {
                        console.log(master);
                            $.ajax({
                        url: '/admin_cont/source_embarque_factura/',
                        data: { numero: num, clase:clase},
                        method: 'GET',
                        success: function (embarque) {
                                preventa=({
                                    seguimiento:house.seguimiento,
                                    referencia:num,
                                    transportista_id:house.transportista_e,
                                    vuelo:house.viaje_e,
                                    master:house.awb_e,
                                    house:house.hawb_e,
                                    fecha:house.fecharetiro_e,
                                    kilos:master.kilos,
                                    bultos:master.bultos,
                                    volumen:master.volumen,
                                    origen:house.origen_e,
                                    destino:house.destino_e,
                                    consigna:getNameByIdClientes(house.consignatario_e),
                                    embarca:getNameByIdClientes(house.embarcador_e),
                                    agente:getNameByIdClientes(house.agente_e),
                                    posicion:house.posicion_e,
                                    terminos:house.terminos,
                                    pagoflete:house.pago,
                                    wr:house.wr,
                                    commodity:getNameByIdProductos(embarque[0].producto_id),
                                });
                                console.log(preventa);
                                    //guardar la preventa
                                    guardar_preventa(preventa);
                                    const tabla = $('#facturar_table').DataTable();
                                    let datosTabla = [];
                                    tabla.rows().every(function() {
                                        const data = this.data();

                                        datosTabla.push({
                                            id_gasto: data[0],
                                            notas: $(this.node()).find('td').eq(7).text(),
                                            descripcion: $(this.node()).find('td').eq(3).text()
                                        });
                                    });
                                   update_gastos(datosTabla);
                                   $('#facturar_modal').dialog('close');
                                    if ($.fn.DataTable.isDataTable('#table_add_im')) {
                                        $('#table_add_im').DataTable().ajax.reload(null, false);
                                    }

                                    if ($.fn.DataTable.isDataTable('#table_edit_im')) {
                                        $('#table_edit_im').DataTable().ajax.reload(null, false);
                                    }
                                    if ($.fn.DataTable.isDataTable('#tabla_house_directo')) {
                                        $('#tabla_house_directo').DataTable().ajax.reload(null, false);
                                    }

                        },
                        error: function (xhr, status, error) {
                            console.error("Error fetching data:", error);
                        }
                    });
                        },
                        error: function (xhr, status, error) {
                            console.error("Error fetching data:", error);
                        }
                    });
                    }

                },
                error: function (xhr, status, error) {
                    console.error("Error fetching data:", error);
                }
            });


}
$('#concepto_detalle').change(function() {
    const filaSeleccionada = $('#facturar_table tbody tr.table-secondary');

    if (filaSeleccionada.length > 0) {
        const dataTable = $('#facturar_table').DataTable();

        if ($(this).is(':checked')) {
            // Obtener los valores de las columnas 0 y 6 de la fila seleccionada
            const valorColumna0 = dataTable.cell(filaSeleccionada, 0).data();
            const valorColumna6 = dataTable.cell(filaSeleccionada, 6).data();

            // Concatenar los valores y actualizar la columna 7
            const valorConcatenado = `${valorColumna0} ${valorColumna6}`;
            dataTable.cell(filaSeleccionada, 7).data(valorConcatenado);
            $(filaSeleccionada).find('td').eq(7).text(valorConcatenado);
        } else {
            // Establecer el valor 'S/I' cuando el checkbox se desmarca
            dataTable.cell(filaSeleccionada, 7).data('S/I');
            $(filaSeleccionada).find('td').eq(7).text('S/I');
        }
    }
});
function update_gastos(x){

    $.ajax({
        url: '/admin_cont/update_gasto_house/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(x),
        headers: {
            "X-CSRFToken": csrf_token
        },
        success: function (respuesta) {
        },
        error: function (xhr, status, error) {
            console.error('Error en la solicitud AJAX:', error);
        }
    });
}
function guardar_preventa(preventa){
console.log(preventa);
    $.ajax({
        type: "POST",
        url: "/admin_cont/preventa/",
        data: JSON.stringify(preventa),
        contentType: "application/json",
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function(response) {
        console.log(response);
            if (response.resultado === 'exito') {
                alert("Los datos se han enviado correctamente.");
            } else {
                alert("Error al enviar los datos.");
            }
        },
        error: function() {
            alert("Error en la solicitud.");
        }
    });
}
function getNameByIdClientes(id) {
var name = "";
$.ajax({
    url: '/importacion_maritima/get_name_by_id',
    data: { id: id},
    async: false,
    success: function (response) {
        name = response.name;
    }
});
return name;
}
function getNameByIdProductos(id){
var name = "";
$.ajax({
    url: '/admin_cont/get_name_by_id_productos',
    data: { id: id},
    async: false,
    success: function (response) {
        name = response.name;
    }
});
return name;
}
function checkIfReferenceExists() {
    let numero = localStorage.getItem('num_house_gasto');
    $.ajax({
        url: '/admin_cont/check_if_reference_exists/',
        type: 'GET',
        data: { numero: numero },
        success: function(response) {
            if (response.exists) {
                alert('Ya ingresó una preventa para este registro.');
            } else {
                facturar();
            }
        },
        error: function(xhr, status, error) {
            console.error('Error en la solicitud:', error);
            return false;
        }
    });
}