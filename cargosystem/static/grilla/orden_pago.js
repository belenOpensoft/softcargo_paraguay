$(document).ready(function() {

    $('#retencion_irpf').change(function() {
            if ($(this).is(':checked')) {
                // Habilitar los campos relacionados con Retención IRPF
                $('#monto_irpf').prop('disabled', false);
                $('#retenciones_irpf_select').prop('disabled', false);
            } else {
                // Deshabilitar los campos relacionados con Retención IRPF
                $('#monto_irpf').prop('disabled', true);
                $('#retenciones_irpf_select').prop('disabled', true);
            }
        });
    $('#retencion_iva').change(function() {
            if ($(this).is(':checked')) {
                // Habilitar los campos relacionados con Retención IVA
                $('#monto_iva').prop('disabled', false);
                $('#retenciones_iva_select').prop('disabled', false);
            } else {
                // Deshabilitar los campos relacionados con Retención IVA
                $('#monto_iva').prop('disabled', true);
                $('#retenciones_iva_select').prop('disabled', true);
            }
        });

    $("input[name='paymentType']").on("change", function () {
    $(".payment-section").addClass("d-none");
    $(".payment-section").removeClass("d-grid");
    const selectedSection = `#${$(this).val()}Section`;
    $(selectedSection).removeClass("d-none");
    $(selectedSection).addClass('d-grid');
    if($(this).val()=='terceros'){
        abrir_cheques();
    }
  });
    $("#cashSection").removeClass("d-none");

    var buscar = '';
    var que_buscar = '';
    let contador = 0;

    $('#tabla_cobranzas tfoot th').each(function(index) {
        let title = $('#tabla_cobranzas thead th').eq(index).text();

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
    table = $('#tabla_cobranzas').DataTable({
    "stateSave": true,
    "dom": 'Btlipr',
    "scrollX": true,
    "bAutoWidth": false,
    "scrollY": wHeight * 0.60,
    "order": [[1, "desc"]],
    "processing": true,
    "serverSide": true,
    "pageLength": 100,
    "ajax": {
        "url": "/admin_cont/source_ordenes/",
        'type': 'GET',
        "data": function (d) {
            return $.extend({}, d, {
                "buscar": buscar,
                "que_buscar": que_buscar,
            });
        }
    },
    "columnDefs": [
        {
            "targets": 0,  // Columna 0 (se mantiene pero oculta su contenido)
            "className": "invisible-column",
            "searchable": false,
            "visible":true,
        },
        {
            "targets": 1,  // Oculta completamente la columna 1
            "visible": false,
            "searchable": false
        },
        {
            "targets": 2,  // Asignamos la columna de fecha
            "type": "date-iso", // Indica que esta columna es de tipo fecha
            "orderable": true // Habilita el ordenamiento
        }
    ],
    "columns": [
        { "visible": true }, // Columna 0
        { "visible": false }, // Columna 1
        { "orderable": true }, // Columna 2 (Ordenable)
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
    ],

    "language": {
        url: "/static/datatables/es_ES.json"
    },
    initComplete: function () {
        var api = this.api();
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

    $('#cliente_cobranza').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/admin_cont/buscar_cliente",
                dataType: 'json',
                data: { term: request.term },
                success: function(data) {
                console.log(data);
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
        appendTo: "#dialog-form",
        select: function(event, ui) {
            const { id } = ui.item;
            $('#cliente_cobranza_hidden').val(id);
        tabla_facturas_pendientes(id,2);
        }
    });



document.querySelector('#exampleTable tbody').addEventListener('click', function (e) {
    const row = e.target.closest('tr');
    if (row) {
        document.querySelectorAll('#exampleTable tbody tr').forEach(r => r.classList.remove('selected'));
        row.classList.add('selected');
    }
});


$('#id_importe').on('focusout', function () {
    let importe = parseFloat($(this).val()) || 0;
    let acumulado=$('#acumulado').val();

    if (importe < 0) {
        alert('El importe no puede ser negativo.');
        $(this).val('');
        return;
    }

    let resultado = parseFloat($('#a_imputar').val()) || 0;
    if(acumulado!=0){
    resultado = importe - acumulado;
    }else{
    resultado=importe;
    }

    $('#a_imputar').val(resultado.toFixed(2));
});

});
/* INITIAL CONTROL PAGE */
var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;
let existe_cliente;

function borrar_datos() {
    const selectedRow = document.querySelector('#exampleTable tbody tr.selected');

    if (selectedRow) {
        let accum = parseFloat($('#accumulated').val()) || 0;
        let importe = parseFloat($('#amount').html()) || 0;

        const total = parseFloat(selectedRow.cells[5].textContent) || 0;

        accum -= total;

        $('#accumulated').val(accum.toFixed(2));
        let diferencia = importe - accum;
        $('#difference').val(diferencia.toFixed(2));
        $('#cashAmount').val(diferencia.toFixed(2));
        $('#checkAmount').val(diferencia.toFixed(2));
        $('#checkAmountTerceros').val(diferencia.toFixed(2));
        $('#checkAmount_trans').val(diferencia.toFixed(2));
        $('#checkAmount_deposito').val(diferencia.toFixed(2));
        $('#checkAmount_otro').val(diferencia.toFixed(2));
        selectedRow.remove();
    } else {
        alert('Por favor, selecciona una fila para borrar.');
    }
}


function abrir_cobranza() {
    $("#dialog-form").dialog({
        autoOpen: true,
        modal: true,
        width:'auto',
        height:'auto',
        maxWidth: $(window).width() * 0.90,
        maxHeight: $(window).height() * 0.90,
        minWidth: 500,
        minHeight: 200,
        buttons: [
            {
                class: "btn btn-dark btn-sm",
                style: "width:90px; height:30px; font-size:14px;",
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
}
function resetModal(modalId) {
    const modal = $(modalId);

    // Resetea todos los formularios dentro del modal a sus valores iniciales
    modal.find("form").each(function() {
        this.reset(); // Reinicia el formulario completo
    });

    // Si tienes tablas que no son parte del formulario, límpialas manualmente
    modal.find("table").each(function() {
        if ($.fn.DataTable.isDataTable(this)) {
            console.log('Limpiando DataTable:', this.id); // Log para verificar cuál tabla se está procesando
            $(this).DataTable().clear().destroy(); // Limpia los datos de la tabla y redibuja
        } else {
            console.log('No es una DataTable:', this.id); // Log para identificar tablas no gestionadas
            $(this).find("tbody").empty(); // Limpia manualmente el tbody si no es DataTable
        }
    });


    // Opcional: Restablece los valores iniciales específicos de algunos inputs
    $("#a_imputar").val("0.0");
    $("#acumulado").val("0.0");
    $("#balance").val("0.0");
    $('#id_importe').prop('readonly', false);

}

function abrir_forma_pago() {
  $("#paymentModal").dialog({
    autoOpen: true,
    modal: true,
    width:'auto',
    height:'auto',
    maxWidth: $(window).width() * 0.90,
    maxHeight: $(window).height() * 0.90,
    minWidth: 500,
    minHeight: 200,
    buttons: [
      {
        text: "Salir",
        class: "btn btn-dark btn-sm",
        style: "width:90px;height:30px;font-size:14px;",
        click: function () {
          $(this).dialog("close");

        },
      },
      {
        text: "Grabar",
        class: "btn btn-primary btn-sm",
        style: "width:90px;height:30px;font-size:14px;",
        click: function () {
          let acumulado=$('#accumulated').val();
          let monto=$('#amount').val();
          //crear_impuventa_asiento_movimiento();
          verificar();
          localStorage.removeItem('medios_pago');
        },
      },
    ],beforeClose: function () {
        localStorage.removeItem('medios_pago');
    }

  });

  cargar_datos_formadepago();


  // Mostrar por defecto la sección de efectivo
  $("#cashSection").show();
}

//llamar cuando se seleccione un cliente


function tabla_facturas_pendientes(cliente,moneda) {
    if ($.fn.DataTable.isDataTable('#imputacionTablePagos')) {
        $('#imputacionTablePagos tbody').off(); // Elimina todos los eventos previos en el tbody
        $('#imputacionTablePagos').DataTable().destroy(); // Destruye la tabla completamente
        $('#imputacionTablePagos tbody').empty(); // Limpia el DOM del tbody
    }

    const table = $('#imputacionTablePagos').DataTable({
        serverSide: true,
        ajax: {
            url: "/admin_cont/obtener_imputables",
            type: "GET",
            data: function (d) {
                d.codigo = $('#cliente_cobranza_hidden').val();
            }
        },
        columns: [
            { data: 'autogenerado', visible: false }, // Oculto
            { data: 'fecha' },
            { data: 'documento' },
            { data: 'total' },
            { data: 'monto' },
            { data: 'iva' },
            { data: 'tipo' },
            { data: 'moneda' },
            { data: 'saldo' },
            { data: 'imputado' },

        ],
        responsive: true,
        processing: true,
        lengthChange: false,
        info: false,
        language: {
            url: "//cdn.datatables.net/plug-ins/1.10.24/i18n/Spanish.json"
        },
    initComplete: function () {
    },
    drawCallback: function () {
        updateBalance();

        // Reasignar evento de clic a las filas
        $('#imputacionTablePagos tbody').off('click', 'tr').on('click', 'tr', function () {
             $(this).toggleClass('selected');
            const selectedRows = table.rows('.selected').count();
            if (selectedRows > 0) {
                $('#imputarSeleccion').prop('disabled', false);  // Habilitar el botón
            } else {
                $('#imputarSeleccion').prop('disabled', true);   // Deshabilitar el botón
            }

            let filaImputada = false;

            table.rows().every(function () {
                const data = this.data(); // Obtener los datos de la fila
                const imputado = parseFloat(data.imputado); // Obtener el valor de la celda 'imputado'

                if (imputado !== 0) {
                    filaImputada = true;
                }
            });

            if (filaImputada) {
                $('#abrirpago').prop('disabled', false); // Habilitar el botón
                $('#deshacer').prop('disabled', false); // Habilitar el botón
            } else {
                $('#abrirpago').prop('disabled', true);  // Deshabilitar el botón
                $('#deshacer').prop('disabled', true);  // Deshabilitar el botón
            }
        });
    }

    });
    existe_cliente=true;

$('#imputarSeleccion').on('click', function () {

    if (!existe_cliente) {
        alert('Seleccione un cliente para continuar');
        return;
    }

    const seleccionadas = table.rows('.selected'); // Obtener las filas seleccionadas
    const data = seleccionadas.data().toArray(); // Convertir a array para depuración
    let importe = parseFloat($('#id_importe').val()) || 0; // Obtener el importe disponible
    let imputado = parseFloat($('#a_imputar').val()) || 0; // Obtener el importe disponible
    let acumulado = 0;
    let saldoAFavor = 0; // Saldos negativos a favor
    let balance = 0;

//    // Validación inicial para acreedores
//    const esInvalida = data.some(row => row.source === 'acreedor' && row.tipo_doc !== 'FACTURA');
//    if (esInvalida) {
//        alert('No se puede imputar registros de acreedor que no sean del tipo "FACTURA".');
//        return;
//    }


    // Validar si se seleccionaron filas

    if (seleccionadas.count() < 1) {
        alert('Debe seleccionar al menos una fila.');
        return;
    }

    if (importe <= 0) {
        alert('Digite un importe.');
        return;
    }

    let imputar = $('#a_imputar').val();
    if (imputar == 0) {
        alert('No hay más dinero disponible. Aumente el importe.');
        return;
    }

    $('#id_importe').prop('readonly', true);


    // Vectores para almacenar las filas afectadas y su estado original
    let filasAfectadas = [];
    let historial = [];

    // Calcular acumulado (saldos positivos) y saldoAFavor (saldos negativos)
    seleccionadas.nodes().each(function (node) {
        let saldo = parseFloat(table.cell(node, 8).data()) || 0;
        let imputadoActual = parseFloat(table.cell(node, 9).data()) || 0;

        // Guardar estado original en el historial
        historial.push({
            modo: table.cell(node, 0).data(),
            numero: table.cell(node, 2).data(),
            saldoOriginal: saldo.toFixed(2),
            imputadoOriginal: imputadoActual.toFixed(2)
        });

        if (saldo < 0) {
            saldoAFavor += Math.abs(saldo); // Sumar saldos negativos
        } else {
            acumulado += saldo; // Sumar saldos positivos
        }
    });

    // Compensar saldos positivos y negativos antes de imputar
    if (saldoAFavor > 0 && acumulado > 0) {
        const diferencia = acumulado - saldoAFavor;

        seleccionadas.nodes().each(function (node) {
            let saldo = parseFloat(table.cell(node, 8).data()) || 0;

            // Si el saldo es negativo (a favor)
            if (saldo < 0 && saldoAFavor > 0) {
                const compensacion = Math.min(Math.abs(saldo), saldoAFavor); // Compensar hasta donde sea posible
                saldo += compensacion; // Reducir el saldo negativo
                saldoAFavor -= compensacion; // Reducir el saldo a favor
                table.cell(node, 8).data(saldo.toFixed(2)); // Actualizar saldo en la tabla
                $(table.cell(node, 8).node()).css('background-color', '#fcec3f'); // Colorear celda
            }

            // Si el saldo es positivo (en contra)
            if (saldo > 0 && acumulado > 0) {
                const compensacion = Math.min(saldo, acumulado); // Compensar hasta donde sea posible
                saldo -= compensacion; // Reducir el saldo positivo
                acumulado -= compensacion; // Reducir el saldo acumulado
                table.cell(node, 8).data(saldo.toFixed(2)); // Actualizar saldo en la tabla
                $(table.cell(node, 8).node()).css('background-color', '#fcec3f'); // Colorear celda
            }
        });

        // Actualizar el importe restante con lo que quede sin compensar
        if (diferencia > 0) {
            acumulado = diferencia;
            saldoAFavor = 0;
        } else if (diferencia < 0) {
            saldoAFavor = Math.abs(diferencia);
            acumulado = 0;
        } else {
            acumulado = 0;
            saldoAFavor = 0;
        }
    }


    // Incrementar el importe disponible con el saldo a favor compensado
    importe += saldoAFavor;

    // Validar si el importe alcanza
    if (seleccionadas.count() > 0 && importe < acumulado) {
        let restante = importe; // Inicializar importe restante

        seleccionadas.nodes().each(function (node) {
            if (restante <= 0) return; // Detener si no queda importe por asignar

            let saldo = parseFloat(table.cell(node, 8).data()) || 0;
            let imputadoActual = parseFloat(table.cell(node, 9).data()) || 0;

            if (saldo >= 0) {
                let asignacion = Math.min(saldo, restante); // Determinar cuánto se puede imputar
                saldo -= asignacion; // Reducir el saldo por el importe asignado
                restante -= asignacion; // Reducir el importe restante

                table.cell(node, 8).data(saldo.toFixed(2)); // Actualizar la columna de saldo
                table.cell(node, 9).data((imputadoActual + asignacion).toFixed(2)); // Actualizar la columna de imputado

                $(table.cell(node, 8).node()).css('background-color', '#fcec3f'); // Amarillo para columna 5
                $(table.cell(node, 9).node()).css('background-color', '#fcec3f'); // Amarillo para columna 6

                // Actualizar balance
                balance += asignacion;

                // Agregar datos actualizados al vector
                filasAfectadas.push({
                    modo: table.cell(node, 0).data(),
                    numero: table.cell(node, 2).data(),
                    nuevoSaldo: saldo.toFixed(2),
                    imputado: (imputadoActual + asignacion).toFixed(2),
                    source: table.cell(node, 6).data()
                });
            }
        });

        $('#a_imputar').val(restante.toFixed(2)); // Actualizar el importe restante
        let ac = parseFloat($('#acumulado').val());
        ac += (parseFloat($('#id_importe').val()) || 0) - restante; // Incrementar acumulado correctamente
        $('#acumulado').val(ac.toFixed(2));

        //$("#balance").val(balance.toFixed(2)); // Actualizar el balance dinámicamente

        localStorage.setItem('filasAfectadas', JSON.stringify(filasAfectadas));
        localStorage.setItem('historial', JSON.stringify(historial));
        seleccionadas.nodes().to$().removeClass('selected');
        updateBalance();
        return;
    }

    // Procesar todas las filas seleccionadas normalmente si el importe alcanza
    seleccionadas.nodes().each(function (node) {
        let saldo = parseFloat(table.cell(node, 8).data()) || 0;
        let imputadoActual = parseFloat(table.cell(node, 9).data()) || 0;

        if (saldo >= 0) {
            if(saldo>imputado){
                let restante = imputado;
                let asignacion = Math.min(saldo, restante); // Determinar cuánto se puede imputar
                saldo -= asignacion; // Reducir el saldo por el importe asignado
                restante -= asignacion; // Reducir el importe restante

                table.cell(node, 8).data(saldo.toFixed(2)); // Actualizar la columna de saldo
                table.cell(node, 9).data((imputadoActual + asignacion).toFixed(2)); // Actualizar la columna de imputado

                $(table.cell(node, 8).node()).css('background-color', '#fcec3f'); // Amarillo para columna 5
                $(table.cell(node, 9).node()).css('background-color', '#fcec3f'); // Amarillo para columna 6

                // Actualizar balance
                balance += asignacion;

                // Agregar datos actualizados al vector
                filasAfectadas.push({
                    modo: table.cell(node, 0).data(),
                    numero: table.cell(node, 2).data(),
                    nuevoSaldo: saldo.toFixed(2),
                    imputado: (imputadoActual + asignacion).toFixed(2),
                    source: table.cell(node, 6).data()
                });
            }else{
            table.cell(node, 9).data(imputadoActual + saldo); // Actualizar la columna 6
            table.cell(node, 8).data(0); // Actualizar la columna 5

            $(table.cell(node, 8).node()).css('background-color', '#fcec3f'); // Amarillo para columna 5
            $(table.cell(node, 9).node()).css('background-color', '#fcec3f'); // Amarillo para columna 6

            // Actualizar balance
            balance += saldo;

            // Agregar datos actualizados al vector
            filasAfectadas.push({
                modo: table.cell(node, 0).data(),
                numero: table.cell(node, 2).data(),
                nuevoSaldo: '0.00',
                imputado: (imputadoActual + saldo).toFixed(2),
                source: table.cell(node, 6).data()
            });
            }
        }
    });

    // Actualizar importe restante
    const total = imputado - balance;
    let ac = parseFloat($('#acumulado').val());
    ac = ac + acumulado;
    calcular_acumulado();
    //$('#acumulado').val(ac.toFixed(2));
    $('#a_imputar').val(total.toFixed(2));

    seleccionadas.nodes().to$().removeClass('selected');

    localStorage.setItem('filasAfectadas', JSON.stringify(filasAfectadas));
    localStorage.setItem('historial', JSON.stringify(historial));
    updateBalance();
    $('#abrirpago').prop('disabled', false);
    $('#deshacer').prop('disabled', false);
});


$('#deshacer').on('click', function () {
    const seleccionadas = table.rows('.selected');
    if (seleccionadas.count() === 0) {
        alert('No hay filas seleccionadas para deshacer cambios.');
        return;
    }

    let historial = JSON.parse(localStorage.getItem('historial')) || [];
    if (historial.length === 0) {
        alert('No hay historial disponible para deshacer cambios.');
        return;
    }

    let balance = 0;
    let acumulado = 0;
    let imputarTotal = 0;

 // Sumar los valores actuales de la columna "imputado" antes de deshacer
    seleccionadas.nodes().each(function (node) {
        const imputadoActual = parseFloat(table.cell(node, 9).data()) || 0; // Valor actual en imputado
        imputarTotal += imputadoActual; // Sumar a imputarTotal
    });

    // Restaurar los valores originales desde el historial
    seleccionadas.nodes().each(function (node) {
        let modo = table.cell(node, 0).data();
        let numero = table.cell(node, 2).data();

        let filaOriginal = historial.find(f => f.modo === modo && f.numero === numero);

        if (filaOriginal) {
            table.cell(node, 8).data(filaOriginal.saldoOriginal); // Restaurar saldo
            table.cell(node, 9).data(filaOriginal.imputadoOriginal); // Restaurar imputado

            // Quitar colores de las celdas restauradas
            $(table.cell(node, 8).node()).css('background-color', '');
            $(table.cell(node, 9).node()).css('background-color', '');

            // Actualizar balance y acumulado
            balance += parseFloat(filaOriginal.saldoOriginal) || 0;
            acumulado += parseFloat(filaOriginal.imputadoOriginal) || 0;
        } else {
            console.warn('No se encontró historial para la fila:', { modo, numero });
        }
    });

    // Actualizar los campos con los valores calculados
    $("#balance").val(balance.toFixed(2));
    $("#acumulado").val(acumulado.toFixed(2));
    $("#a_imputar").val(imputarTotal.toFixed(2)); // Actualizar el valor de a_imputar

    // Quitar la clase 'selected' de las filas seleccionadas
    seleccionadas.nodes().to$().removeClass('selected');

    // Llamar a updateBalance para recalcular cualquier dato adicional
    updateBalance();
    calcular_acumulado();
    // Notificar al usuario que los cambios han sido revertidos
    verificarImputado(table);  // Deshabilitar el botón
    alert('Cambios deshechos en las filas seleccionadas.');
});


}
function verificarImputado(table) {
        let filaImputada = false;

        // Recorre todas las filas de la tabla
        table.rows().every(function () {
            const data = this.data(); // Obtener los datos de la fila
            const imputado = parseFloat(data.imputado); // Obtener el valor de la celda 'imputado'

            // Si el valor de 'imputado' es diferente de cero, habilitar el botón
            if (imputado !== 0) {
                filaImputada = true;
            }
        });

        // Habilitar o deshabilitar el botón basado en si alguna fila fue imputada
        if (filaImputada) {
            $('#abrirpago').prop('disabled', false); // Habilitar el botón
            $('#deshacer').prop('disabled', false); // Habilitar el botón
        } else {
            $('#abrirpago').prop('disabled', true);  // Deshabilitar el botón
            $('#deshacer').prop('disabled', true);  // Deshabilitar el botón
        }
    }
function updateBalance() {
    let balanceTotal = 0;

    // Verifica si DataTable está inicializado
    if ($.fn.DataTable.isDataTable('#imputacionTablePagos')) {
        const table = $('#imputacionTablePagos').DataTable();

        // Itera sobre todas las filas visibles de la tabla
        table.rows().every(function () {
            let data = this.data(); // Obtén los datos de la fila
            let saldo = parseFloat(data.saldo) || 0; // Asegúrate de convertir el saldo a número
            balanceTotal += saldo; // Suma el saldo al balance total
        });

        // Actualiza el campo del balance con el total calculado
        $('#balance').val(balanceTotal.toFixed(2));
    } else {
        console.warn('La tabla #imputacionTablePagos no está inicializada.');
    }
}
function calcular_acumulado() {
    let acumulado = 0;

    // Verifica si DataTable está inicializado
    if ($.fn.DataTable.isDataTable('#imputacionTablePagos')) {
        const table = $('#imputacionTablePagos').DataTable();

        // Itera sobre todas las filas visibles de la tabla
        table.rows().every(function () {
            let data = this.data(); // Obtén los datos de la fila
            let imputado = parseFloat(data.imputado) || 0; // Asegúrate de convertir el saldo a número
            acumulado += imputado; // Suma el saldo al balance total
        });

        // Actualiza el campo del balance con el total calculado
        $('#acumulado').val(acumulado.toFixed(2));
    } else {
        console.warn('La tabla #imputacionTablePagos no está inicializada.');
    }
}
function cargar_datos_formadepago(){
let imputar=$('#a_imputar').val();
let importe=$('#id_importe').val();
let acumulado=$('#acumulado').val();


const table = $('#imputacionTablePagos').DataTable();

let documentos = '';
table.rows().nodes().each(function (node) {
    let imputado = parseFloat(table.cell(node, 9).data()) || 0;

    if (imputado != 0) {
        let nroDocumento = table.cell(node, 2).data();
        documentos += nroDocumento + ';';
    }
});


$('#observations').val(documentos);
acumulado = parseFloat(acumulado || 0).toFixed(2); // Convertir a número y aplicar toFixed
importe = parseFloat(importe || 0).toFixed(2);     // Convertir a número y aplicar toFixed

if(imputar<=0){
$('#amount').html(acumulado);

}else{
$('#amount').html(importe);
}
$('#cashAmount').val(importe);
$('#checkAmount').val(importe);
$('#checkAmount_trans').val(importe);
$('#checkAmount_deposito').val(importe);
$('#checkAmount_otro').val(importe);
}

function ingresar_datos(){
let monto=$('#cashAmount').val();
let importe=$('#amount').html();
let arbitraje=$('#id_arbitraje').val();

const tbody = $('#exampleTable tbody');
//tbody.empty();

let modo, emision,banco,numero,moneda,total,tc,vencimiento,cuenta;
modo=emision=banco=numero=moneda=total=tc=vencimiento=cuenta=0;

if ($('#efectivo').is(':checked')){
const selectElement = document.getElementById('id_cuenta_efectivo');
const moneda_select = document.getElementById('id_moneda_efectivo');
const labelSeleccionado = selectElement.options[selectElement.selectedIndex].text;
const valueSeleccionado = selectElement.value;
const monedaV = moneda_select.value;
modo='EFECTIVO';
emision=obtenerFechaHoy();
banco=valueSeleccionado;
numero=0;
moneda=monedaV;
total=monto;
tc=arbitraje;
cuenta=valueSeleccionado;
vencimiento=obtenerFechaHoy();

}else if ($('#cheque').is(':checked')){
const selectElement = document.getElementById('id_cuenta_cheque');
const moneda_select = document.getElementById('id_moneda_cheque');
const monedaV = moneda_select.value;
const labelSeleccionado = selectElement.options[selectElement.selectedIndex].text;
const valueSeleccionado = selectElement.value;
modo='CHEQUE';
emision=$('#checkEmission').val();
let bancoText = $('#id_banco_cheque option:selected').text();
banco=bancoText;
numero=$('#checkNumber').val();
tc=arbitraje;
cuenta=valueSeleccionado;
moneda=monedaV;
vencimiento=$('#checkDueDate').val();
total=$('#checkAmount').val();

}else if ($('#trans').is(':checked')){
const selectElement = document.getElementById('id_cuenta_transferencia');
const moneda_select = document.getElementById('id_moneda_transferencia');
const monedaV = moneda_select.value;
const labelSeleccionado = selectElement.options[selectElement.selectedIndex].text;
modo='TRANSFER';
emision=$('#checkEmission_trans').val();
banco=labelSeleccionado;
numero=$('#checkNumber_trans').val();
tc=arbitraje;
cuenta=$('#cuenta_trans').val();
moneda=monedaV;
vencimiento=$('#checkDueDate_trans').val();
total=$('#checkAmount_trans').val();
}else if ($('#deposito').is(':checked')){
const selectElement = document.getElementById('id_cuenta_deposito');
const moneda_select = document.getElementById('id_moneda_deposito');
const monedaV = moneda_select.value;
const labelSeleccionado = selectElement.options[selectElement.selectedIndex].text;
modo='DEPOSITO';
emision=$('#checkEmission_deposito').val();
banco=labelSeleccionado;
numero=$('#checkNumber_deposito').val();
tc=arbitraje;
cuenta=$('#cuenta_deposito').val();
moneda=monedaV;
vencimiento=$('#checkDueDate_deposito').val();
total=$('#checkAmount_deposito').val();
}else if ($('#otro').is(':checked')){
const selectElement = document.getElementById('id_cuenta_otro');
const moneda_select = document.getElementById('id_moneda_otro');
const monedaV = moneda_select.value;
const labelSeleccionado = selectElement.options[selectElement.selectedIndex].text;
modo='OTRO';
emision=$('#checkEmission_otro').val();
banco=labelSeleccionado;
numero=$('#checkNumber_otro').val();
tc=arbitraje;
cuenta=$('#cuenta_otro').val();
moneda=monedaV;
vencimiento=$('#checkDueDate_otro').val();
total=$('#checkAmount_otro').val();
}else if ($('#cheque_terceros').is(':checked')){
cheques_terceros_tabla();
return;
}
    const nuevaFilaObj = {
        modo: modo,
        emision: emision,
        banco: banco,
        numero: numero,
        moneda: moneda,
        total: total,
        tc: tc,
        vencimiento: vencimiento,
        cuenta: cuenta
    };

    let medios_pago=JSON.parse(localStorage.getItem('medios_pago')) || [];

    medios_pago.push(nuevaFilaObj);

    localStorage.setItem('medios_pago', JSON.stringify(medios_pago));

const nuevaFila = `
            <tr>
                <td>${modo}</td>
                <td>${emision}</td>
                <td>${banco}</td>
                <td>${numero}</td>
                <td>${moneda}</td>
                <td>${total}</td>
                <td>${tc}</td>
                <td>${vencimiento}</td>
                <td>${cuenta}</td>
            </tr>
        `;
        tbody.append(nuevaFila);

let accum = parseFloat($('#accumulated').val()) || 0;
let totalParsed = parseFloat(total || 0);
accum += totalParsed;
$('#accumulated').val(accum.toFixed(2));
let diferencia = parseFloat(importe || 0) - accum;
$('#difference').val(diferencia.toFixed(2));
$('#cashAmount').val(diferencia.toFixed(2));
$('#checkAmount').val(diferencia.toFixed(2));
$('#checkAmount_trans').val(diferencia.toFixed(2));
$('#checkAmount_deposito').val(diferencia.toFixed(2));
$('#checkAmount_otro').val(diferencia.toFixed(2));


}

const obtenerFechaHoy = () => {
    const fechaHoy = new Date();
    const año = fechaHoy.getFullYear();
    const mes = String(fechaHoy.getMonth() + 1).padStart(2, '0'); // Meses van de 0 a 11
    const día = String(fechaHoy.getDate()).padStart(2, '0');
    return `${año}-${mes}-${día}`;
};

function cheques_terceros_tabla(){
let importe=$('#checkAmountTerceros').val();
let importe_o=$('#amount').html();
let monto=$('#cashAmount').val();

const tbody = $('#exampleTable tbody');
let modo,emision,banco,numero,tc,cuenta,moneda,vencimiento,total;
let seleccionadas = JSON.parse(localStorage.getItem('chequesData'));
const moneda_select = document.getElementById('id_moneda_cheque_terceros');
const monedaV = moneda_select.value;
modo='CHEQUE TERCEROS';
let arbitraje=$('#id_arbitraje').val();
tc=arbitraje;
moneda=monedaV;
let nuevaFilaObj;
let nuevaFila;
for (let i = 0; i < seleccionadas.length; i++) {
    let cheque = seleccionadas[i];
    emision=cheque.emision;
    banco=cheque.banco;
    numero=cheque.numero;
    vencimiento=cheque.vto;
    total=cheque.total;
    cuenta=cheque.id;

    nuevaFilaObj = {
        modo: modo,
        emision: emision,
        banco: banco,
        numero: numero,
        moneda: moneda,
        total: total,
        tc: tc,
        vencimiento: vencimiento,
        cuenta: cuenta
    };
    nuevaFila = `
            <tr>
                <td>${modo}</td>
                <td>${emision}</td>
                <td>${banco}</td>
                <td>${numero}</td>
                <td>${moneda}</td>
                <td>${total}</td>
                <td>${tc}</td>
                <td>${vencimiento}</td>
                <td>${cuenta}</td>
            </tr>
        `;

        tbody.append(nuevaFila);
}

    let medios_pago=JSON.parse(localStorage.getItem('medios_pago')) || [];
    medios_pago.push(nuevaFilaObj);
    localStorage.setItem('medios_pago', JSON.stringify(medios_pago));

    let accum = parseFloat($('#accumulated').val()) || 0;
    let totalParsed = parseFloat(importe || 0);
    accum += totalParsed;
    $('#accumulated').val(accum.toFixed(2));
    let diferencia = parseFloat(importe_o || 0) - accum;
    $('#difference').val(diferencia.toFixed(2));
    $('#cashAmount').val(diferencia.toFixed(2));
    $('#checkAmount').val(diferencia.toFixed(2));
    $('#checkAmount_trans').val(diferencia.toFixed(2));
    $('#checkAmount_deposito').val(diferencia.toFixed(2));
    $('#checkAmount_otro').val(diferencia.toFixed(2));


}

function crear_impuventa_asiento_movimiento(){

if(!$('#id_cuenta_observaciones').val() && $('#difference').val()!=0){
alert('Debe asignar la diferencia a una cuenta');
return;
}
//traer cliente tambien
let impuventa = JSON.parse(localStorage.getItem('filasAfectadas')) || [];
let medios_pago = JSON.parse(localStorage.getItem('medios_pago')) || [];

let vector={};
let imputaciones=[];
let asiento=[];
let movimiento=[];
let cobranza=[];
let definitivo;
if ($('#definitivo').is(':checked')) {
        definitivo=true;
    } else if ($('#intencion').is(':checked')) {
        definitivo=false;
    }
impuventa.forEach((item) => {
        imputaciones.push({
            nroboleta: item.numero,
            imputado:item.imputado,
            saldo_imputado:item.nuevoSaldo,
            source:item.source
        });
        movimiento.push({
            imputado:item.modo,
            saldo:item.nuevoSaldo,
            boletas:$('#observations').val()
        });
    });

medios_pago.forEach((item) => {
        asiento.push({
            modo:item.modo,
            cuenta:item.cuenta,
            banco:item.banco,
            nro_mediopago:item.numero,
            total_pago:item.total,
            vencimiento:item.vencimiento
        });
    });

cobranza.push({
        nrocliente:$('#cliente_cobranza_hidden').val(),
        numero:$('#id_numero').val(),
        total:$('#id_importe').val(),
        definitivo:definitivo,
        nromoneda:$('#id_moneda').val(),
        arbitraje:$('#id_arbitraje').val(),
        paridad:$('#id_paridad').val()
    });



vector.cobranza=cobranza;
vector.imputaciones=imputaciones;
vector.asiento=asiento;
vector.movimiento=movimiento;
if($('#difference').val()!=0){
let nuevaFila = {
    modo: "DIFERENCIA",
    cuenta: $('#id_cuenta_observaciones').val(),
    banco:$('#id_cuenta_observaciones option:selected').text() ,
    nro_mediopago: 0,
    total_pago: $('#difference').val(),
    vencimiento: null
};

vector.asiento.push(nuevaFila);
}


$.ajax({
        url: '/admin_cont/guardar_impuorden/', // Cambia esto a la URL correcta
        method: 'POST',
        headers: { 'X-CSRFToken': csrf_token }, // Asegúrate de tener el CSRF token
        data: JSON.stringify({ 'vector':vector }),
        contentType: 'application/json',
        success: function(response) {
        console.log(response);
            if (response.status === 'exito') {
                $('#dialog-form').dialog('close');
                $('#dialog-form').dialog('close');
                $('#paymentModal').dialog('close');

            } else {
                alert(response.status);
            }
        },
        error: function(xhr) {
            alert("Error al guardar los datos: " + xhr.responseText);
        },
    });

}

function crear_anticipo(){
if(!$('#id_cuenta_observaciones').val() && $('#difference').val()!=0){
alert('Debe asignar la diferencia a una cuenta');
return;
}
//traer cliente tambien
let impuventa = JSON.parse(localStorage.getItem('filasAfectadas')) || [];
let medios_pago = JSON.parse(localStorage.getItem('medios_pago')) || [];

let vector={};
let asiento=[];
let cobranza=[];


medios_pago.forEach((item) => {
        asiento.push({
            modo:item.modo,
            cuenta:item.cuenta,
            banco:item.banco,
            nro_mediopago:item.numero,
            total_pago:item.total,
            vencimiento:item.vencimiento
        });
    });

cobranza.push({
        nrocliente:$('#cliente_cobranza_hidden').val(),
        serie:null,
        prefijo:null,
        numero:$('#id_numero').val(),
        total:$('#id_importe').val(),
        nromoneda:$('#id_moneda').val(),
        arbitraje:$('#id_arbitraje').val(),
        paridad:$('#id_paridad').val()
    });



vector.cobranza=cobranza;
vector.asiento=asiento;
if($('#difference').val()!=0){
let nuevaFila = {
    modo: "DIFERENCIA",
    cuenta: $('#id_cuenta_observaciones').val(),
    banco:$('#id_cuenta_observaciones option:selected').text() ,
    nro_mediopago: 0,
    total_pago: $('#difference').val(),
    vencimiento: null
};

vector.asiento.push(nuevaFila);
}
//no sale esto en la consola
console.log('anticipo '+vector);


$.ajax({
        url: '/admin_cont/guardar_anticipo_orden/', // Cambia esto a la URL correcta
        method: 'POST',
        headers: { 'X-CSRFToken': csrf_token }, // Asegúrate de tener el CSRF token
        data: JSON.stringify({ 'vector':vector }),
        contentType: 'application/json',
        success: function(response) {
            if (response.status === 'exito') {
                console.log("Datos guardados correctamente");
                // Opcional: recargar una tabla o actualizar la UI
            } else {
                alert("ghfghfgh: " + response.status);
            }
        },
        error: function(xhr) {
            alert("Error al guardar los datos: " + xhr.responseText);
        },
    });

}

function verificar(){
let key=true;
//let key=false;
//let rows = document.querySelectorAll('#imputacionTablePagos tbody tr');
//rows.forEach(row => {
//    let imputado = row.cells[9]?.textContent.trim();
//    let imputadoValue = parseFloat(imputado) || 0;
//
//    if (imputadoValue !== 0) {
//        console.log('Fila con Imputado diferente de cero:', imputadoValue);
//        key = true;
//    }
//});
let importe = $('#id_importe').val();
let imputar = $('#a_imputar').val();


    if(key){
        if(imputar!=0){
        if (confirm('No se ha asignado todo el IMPORTE, ¿Desea continuar como anticipo?')) {
            crear_anticipo_consaldo();
        }
        }
     crear_impuventa_asiento_movimiento();
    }else{
        if (confirm('No hay una boleta seleccionada, ¿Desea continuar como anticipo?')) {
            crear_anticipo();
        }
    }

}
function crear_anticipo_consaldo(){
if(!$('#id_cuenta_observaciones').val() && $('#difference').val()!=0){
alert('Debe asignar la diferencia a una cuenta');
return;
}
//traer cliente tambien
let impuventa = JSON.parse(localStorage.getItem('filasAfectadas')) || [];
let medios_pago = JSON.parse(localStorage.getItem('medios_pago')) || [];

let vector={};
let asiento=[];
let cobranza=[];


medios_pago.forEach((item) => {
        asiento.push({
            modo:item.modo,
            cuenta:item.cuenta,
            banco:item.banco,
            nro_mediopago:item.numero,
            total_pago:item.total,
            vencimiento:item.vencimiento
        });
    });

cobranza.push({
        nrocliente:$('#cliente_cobranza_hidden').val(),
        serie:null,
        prefijo:null,
        numero:$('#id_numero').val(),
        total:$('#id_importe').val(),
        nromoneda:$('#id_moneda').val(),
        arbitraje:$('#id_arbitraje').val(),
        paridad:$('#id_paridad').val(),
        saldo:$('#a_imputar').val()
    });



vector.cobranza=cobranza;
vector.asiento=asiento;
if($('#difference').val()!=0){
let nuevaFila = {
    modo: "DIFERENCIA",
    cuenta: $('#id_cuenta_observaciones').val(),
    banco:$('#id_cuenta_observaciones option:selected').text() ,
    nro_mediopago: 0,
    total_pago: $('#difference').val(),
    vencimiento: null
};

vector.asiento.push(nuevaFila);
}

console.log('cobranza '+cobranza);


$.ajax({
        url: '/admin_cont/guardar_anticipo_orden/', // Cambia esto a la URL correcta
        method: 'POST',
        headers: { 'X-CSRFToken': csrf_token }, // Asegúrate de tener el CSRF token
        data: JSON.stringify({ 'vector':vector }),
        contentType: 'application/json',
        success: function(response) {
            if (response.status === 'exito') {
                alert("Datos guardados correctamente");
                // Opcional: recargar una tabla o actualizar la UI
            } else {
                alert("ghfghfgh: " + response.status);
            }
        },
        error: function(xhr) {
            alert("Error al guardar los datos: " + xhr.responseText);
        },
    });

}


$('#id_moneda').on('change', function () {
        const cliente = $('#cliente_cobranza_hidden').val();
        const moneda = $(this).val();

        tabla_facturas_pendientes(cliente, moneda);
    });

function abrir_cheques(){
$('#id_buscar_terciarizado').val(0);
$('#cliente_terciarizado_buscar').val('');

    if ($.fn.DataTable.isDataTable('#tabla_cheques_disponibles')) {
        $('#tabla_cheques_disponibles').DataTable().destroy(); // Destruye la tabla completamente
        $('.checkbox-bajar:checked').each(function() {
            $(this).prop('checked', false);  // Desmarcar la fila
        });
    }

    $("#cheques_disponibles").dialog({
        autoOpen: true,
        modal: true,
        width: wWidth * 0.60,
        height: wHeight * 0.90,
        buttons: [
            {
                class: "btn btn-dark",
                style: "width:90px;height:30px;font-size:14px;",
                text: "Salir",
                click: function() {
                    $(this).dialog("close");
                }
            }
        ]
    }).prev('.ui-dialog-titlebar').remove();
    const table = $('#tabla_cheques_disponibles').DataTable({
        serverSide: true,
        ajax: {
            url: "/admin_cont/obtener_cheques_disponibles",  // Cambia esta URL por la que corresponde en tu API
            type: "GET",
            data: function(d) {
                // Aquí puedes agregar más parámetros si es necesario
               // d.codigo = $('#cliente_cobranza_hidden').val();  // Si necesitas enviar algún valor extra
                d.cliente = $('#id_buscar_terciarizado').val();
            }
        },
        columns: [
            { data: 'id', visible: false }, // Ocultar la columna ID
            { data: 'moneda', visible: false }, // Ocultar la columna ID
            { data: 'vto' },
            { data: 'emision' },
            { data: 'banco' },
            { data: 'numero' },
            { data: 'cliente' },
            { data: 'total' },
            {
                data: 'id',  // Usar el ID para el checkbox
                render: function(data, type, row) {
                    // Crear un checkbox con el value igual a la ID de la fila
                    return `<input type="checkbox" class="checkbox-bajar" value="${data}">`;
                }
            }
        ],
        responsive: true,
        processing: true,
        lengthChange: false,
        language: {
            url: "//cdn.datatables.net/plug-ins/1.10.24/i18n/Spanish.json"
        },
        initComplete: function() {
            // Aquí puedes hacer otras inicializaciones si es necesario
        },
        drawCallback: function() {

        $('.checkbox-bajar').change(function() {
            localStorage.removeItem('cheques');
            localStorage.removeItem('chequesData');
            const selectedRows = [];
            let monedaCoincide = true; // Variable para verificar si todos los valores de moneda son iguales
            let monedaValor = null; // Almacenar el valor de "moneda" de la primera fila seleccionada
            let monto = 0;
            let ids = [];

            $('.checkbox-bajar:checked').each(function() {
                const row = table.row($(this).closest('tr'));
                const rowData = row.data();
                ids.push(rowData.id);
                selectedRows.push(rowData);

                // Parsear el monto a float para realizar la suma correctamente
                const total = parseFloat(rowData.total) || 0;  // Si rowData.total es NaN, usa 0
                monto += total;

                const moneda = rowData.moneda;

                // Verificar si las monedas coinciden
                if (monedaValor === null) {
                    monedaValor = moneda;
                } else if (moneda !== monedaValor) {
                    monedaCoincide = false;
                }
            });

            // Si las monedas no coinciden, mostramos un alert y desmarcamos las filas seleccionadas
            if (!monedaCoincide) {
                alert('Las monedas de los cheques no coinciden.');
                $('.checkbox-bajar:checked').each(function() {
                    $(this).prop('checked', false);  // Desmarcar la fila
                });
                return;
            }
            let restante=$('#checkAmount').val();

            if(monto>restante){
                alert('El monto del cheque no debe superar el monto a pagar.');
                $('.checkbox-bajar:checked').each(function() {
                    $(this).prop('checked', false);  // Desmarcar la fila
                });
                return;
            }


            // Si las monedas coinciden, actualizar los campos de monto y moneda
            $('#checkAmountTerceros').val(monto);
            $('#id_moneda_cheque_terceros').val(monedaValor);

            // Guardar los ids de las filas seleccionadas en el localStorage
            localStorage.setItem('cheques', JSON.stringify(ids));
            localStorage.setItem('chequesData', JSON.stringify(selectedRows));
        });

        }
    });
    $('#cliente_terciarizado_buscar').autocomplete({
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
        appendTo: "#cheques_disponibles",
        select: function(event, ui) {
            const { id } = ui.item;
            $('#id_buscar_terciarizado').val(id); // Guardar el ID del cliente seleccionado
           table.ajax.reload(); // Recargar la tabla con el nuevo filtro de cliente
        }
    });

    // Filtro personalizado por cliente (aplicado en el evento de cambio de selección)
    $('#cliente_terciarizado_buscar').on('change', function() {
//        const clienteId = $('#id_buscar_terciarizado').val();
//        table.column(5).search(clienteId).draw(); // Filtrar en la columna de cliente
        table.ajax.reload();
        $('#id_buscar_terciarizado').val(0);
    });
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