$(document).ready(function () {
    $('#id_fecha').on('change', function () {
            if ($(this).val()) {
                cargar_arbitraje();
            }
        });

    $('#id_cuenta_deposito').on('change', function () {
        const cuentaSeleccionada = $(this).val();

        switch (cuentaSeleccionada) {
            case '11120':
                $('#id_moneda_deposito').val('3');
                break;
            case '11121':
                $('#id_moneda_deposito').val('1');
                break;
            case '11122':
                $('#id_moneda_deposito').val('2');
                break;
            case '11123':
                $('#id_moneda_deposito').val('1');
                break;
            case '11124':
                $('#id_moneda_deposito').val('2');
                break;
            default:
                $('#id_moneda_deposito').val('2');
                break;
        }
    });
    $('#id_cuenta_transferencia').on('change', function () {
        const cuentaSeleccionada = $(this).val();

        switch (cuentaSeleccionada) {
            case '11120':
                $('#id_moneda_transferencia').val('3');
                break;
            case '11121':
                $('#id_moneda_transferencia').val('1');
                break;
            case '11122':
                $('#id_moneda_transferencia').val('2');
                break;
            case '11123':
                $('#id_moneda_transferencia').val('1');
                break;
            case '11124':
                $('#id_moneda_transferencia').val('2');
                break;
            default:
                $('#id_moneda_transferencia').val('2');
                break;
        }
    });
    $('#id_cuenta_cheque').on('change', function () {
        const cuentaSeleccionada = $(this).val();

        switch (cuentaSeleccionada) {
            case '11113':
                $('#id_moneda_cheque').val('1');
                break;
            case '11114':
                $('#id_moneda_cheque').val('2');
                break;
            default:
                $('#id_moneda_cheque').val('2');
                break;
        }
    });
    $('#id_cuenta_efectivo').on('change', function () {
        const cuentaSeleccionada = $(this).val();

        switch (cuentaSeleccionada) {
            case '11112':
                $('#id_moneda_efectivo').val('2');
                break;
            case '11111':
                $('#id_moneda_efectivo').val('1');
                break;
            default:
                $('#id_moneda_efectivo').val('2');
                break;
        }
    });
    $('#id_cuenta_otro').on('change', function () {
        const cuentaSeleccionada = $(this).val();

        switch (cuentaSeleccionada) {
            case '11112':
                $('#id_moneda_otro').val('2');
                break;
            case '11111':
                $('#id_moneda_otro').val('1');
                break;
            default:
                $('#id_moneda_otro').val('2');
                break;
        }
    });

    $('#id_cuenta_deposito').trigger('change');
    $('#id_cuenta_transferencia').trigger('change');
    $('#id_cuenta_cheque').trigger('change');
    $('#id_cuenta_efectivo').trigger('change');
    $('#id_cuenta_otro').trigger('change');

    $("input[name='paymentType']").on("change", function () {
        $(".payment-section").addClass("d-none");
        $(".payment-section").removeClass("d-grid");
        const selectedSection = `#${$(this).val()}Section`;
        $(selectedSection).removeClass("d-none");
        $(selectedSection).addClass('d-grid');
        if ($(this).val() == 'terceros') {
            abrir_cheques();
        }
    });
    $("#cashSection").removeClass("d-none");
    var buscar = '';
    var que_buscar = '';
    let contador = 0;

    table = $('#tabla_cobranzas').DataTable({
        "dom": 'Btlipr',
        "scrollX": true,
        "bAutoWidth": false,
        "scrollY": wHeight * 0.60,
        "order": [[2, "desc"]],
        "processing": true,
        "serverSide": true,
        "pageLength": 100,
        "ajax": {
            "url": "/admin_cont/source_cobranza/",
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
                "className": "",
                "searchable": false,
                "visible": true,
               render: function (data, type, row) {
                    return `<span class="badge bg-warning text-dark">${row[0] ?? ''}</span>`;
                }
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
            },
                        {
                "targets": [6,7,8],
                "className": "text-end",
            }
        ],
        "columns": [
            {"visible": true}, // Columna 0
            {"visible": false}, // Columna 1
            {"orderable": true}, // Columna 2 (Ordenable)
            {"orderable": true},
            {"orderable": true},
            {"orderable": true},
            {"orderable": true},
            {"orderable": true},
            {"orderable": true},
        ],
        "language": {
            url: "/static/datatables/es_ES.json"
        },
        initComplete: function () {
            var api = this.api();
            api.columns().every(function () {
                var that = this;
                $('.filter-input', this.footer()).on('keyup change', function () {
                    if (that.search() !== this.value) {
                        that.search(this.value).draw();
                    }
                });
            });
        },
        "rowCallback": function (row, data) {
        }
    });
    $('#tabla_cobranzas tfoot th').each(function (index) {
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
    $(document).on("click", "#clear", function () {
        awbRegex = '';
        $(".filter-input").val("").trigger("keyup"); // Limpia los inputs y activa la búsqueda
        $(".filter-input").removeClass("is-invalid"); // Se quita el rojo si se vacía
        table.ajax.reload();
    });
    // Evento para resaltar los inputs cuando tienen contenido
    $(document).on("input", ".filter-input", function () {
        if ($(this).val().trim() !== "") {
            $(this).addClass("is-invalid"); // Se pone en rojo
        } else {
            $(this).removeClass("is-invalid"); // Se quita el rojo si se vacía
        }
    });
    $('#cliente_cobranza').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "/admin_cont/buscar_cliente",
                dataType: 'json',
                data: {term: request.term},
                success: function (data) {
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
        select: function (event, ui) {
            const {id} = ui.item;
            $('#cliente_cobranza_hidden').val(id);
            tabla_facturas_pendientes(id, 2);
        }
    });

    document.querySelector('#exampleTableCobranza tbody').addEventListener('click', function (e) {
        const row = e.target.closest('tr');
        if (row) {
            document.querySelectorAll('#exampleTableCobranza tbody tr').forEach(r => r.classList.remove('table-secondary'));
            row.classList.add('table-secondary');
        }
    });


    $('#id_importe').on('focusout', function () {
        let importe = parseFloat($(this).val()) || 0;
        let acumulado = $('#acumulado').val();

        if (importe < 0) {
            alert('El importe no puede ser negativo.');
            $(this).val('');
            return;
        }

        let resultado = parseFloat($('#a_imputar').val()) || 0;
        if (acumulado != 0) {
            resultado = importe - acumulado;
        } else {
            resultado = importe;
        }

        $('#a_imputar').val(resultado.toFixed(2));
    });


    $("#tabla_cobranzas tbody").on("dblclick", "tr", function () {
        const row = $('#tabla_cobranzas').DataTable().row(this).data();
        const autogenerado = row[1];
        const nrocliente = row[9];
        const numero = row[10];


        $("#autogen_detalle_cobranza").val(autogenerado);
        buscar_detalle(autogenerado);

        $("#modalCobranzaDetalle").dialog({
            modal: true,
            width: '80%',
            height: 'auto',
            position: {my: "center top", at: "center top+20", of: window},
            autoOpen: true,
        });
    });

    $("#tabla_cobranzas tbody").on("click", "tr", function () {
        $("#tabla_cobranzas tbody tr").removeClass("table-secondary");
        $(this).addClass("table-secondary");
    });

});
/* INITIAL CONTROL PAGE */
var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;
let existe_cliente;

function borrar_datos() {
    const selectedRow = document.querySelector('#exampleTableCobranza tbody tr.selected');

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
        width: 'auto',
        height: 'auto',
        maxWidth: $(window).width() * 0.90,
        maxHeight: $(window).height() * 0.90,
        minWidth: 500,
        minHeight: 200,
        beforeClose: function () {
            existe_cliente = false;
            resetModal("#dialog-form");
            resetModal("#paymentModal");
            localStorage.removeItem('medios_pago');
            localStorage.removeItem('filasAfectadas');
            localStorage.removeItem('historial');
            window.location.reload();

        },
        buttons: [
            {
                class: "btn btn-dark btn-sm",
                style: "width:90px; height:30px; font-size:14px;",
                text: "Salir",
                click: function () {
                    $(this).dialog("close");
                    existe_cliente = false;
                    localStorage.removeItem('medios_pago');
                    resetModal("#dialog-form");
                    resetModal("#paymentModal");
                }
            }
        ]
    }).prev('.ui-dialog-titlebar').remove();
    cargar_arbitraje();
    traer_proximo_numero();
}

function resetModal(modalId) {
    const modal = $(modalId);

    // Resetea todos los formularios dentro del modal a sus valores iniciales
    modal.find("form").each(function () {
        this.reset(); // Reinicia el formulario completo
    });

    // Si tienes tablas que no son parte del formulario, límpialas manualmente
    modal.find("table").each(function () {
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

function tabla_para_imputar() {
    $('#imputacionTable').DataTable({
        info: false,        // Oculta "Mostrando X a Y de Z registros"
        lengthChange: false,
        "dom": 'Btlipr',
        "scrollX": true,
        "responsive": false,
        "bAutoWidth": false,
        "scrollY": $(window).height() * 0.60,
        "columnDefs": [
            {
                "targets": [0],
                "className": 'text-left',
                "data": 'vencimiento',
                "title": 'Vencimiento'
            },
            {
                "targets": [1],
                "className": 'text-left',
                "data": 'emision',
                "title": 'Emisión'
            },
            {
                "targets": [2],
                "className": 'text-left',
                "data": 'documento',
                "title": 'Documento'
            },
            {
                "targets": [3],
                "className": 'text-left',
                "data": 'total',
                "title": 'Total'
            },
            {
                "targets": [4],
                "className": 'text-left',
                "data": 'saldo',
                "title": 'Saldo'
            },
            {
                "targets": [5],
                "className": 'text-left',
                "data": 'imputado',
                "title": 'Imputado'
            },
            {
                "targets": [6],
                "className": 'text-center',
                "data": 't_cambio',
                "title": 'T. Cambio'
            },
            {
                "targets": [7],
                "className": 'text-left',
                "data": 'embarque',
                "title": 'Embarque'
            },
            {
                "targets": [8],
                "className": 'text-left',
                "data": 'detalle',
                "title": 'Detalle'
            },
            {
                "targets": [9],
                "className": 'text-left',
                "data": 'posicion',
                "title": 'Posición'
            },
            {
                "targets": [10],
                "className": 'text-left',
                "data": 'moneda',
                "title": 'Moneda'
            },
            {
                "targets": [11],
                "className": 'text-left',
                "data": 'paridad',
                "title": 'Paridad'
            },
            {
                "targets": [12],
                "className": 'text-left',
                "data": 'tipo_doc',
                "title": 'Tipo documento'
            }
        ],
        "order": [[0, "desc"]],
        "processing": true,
        "serverSide": true,
        "pageLength": 100,
        "ajax": {
            "url": "/admin_cont/source_cobranza/",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "cliente": $('#socio_com_filtro').val()
                });
            }
        },
        "language": {
            "url": "/static/datatables/es_ES.json"
        }
    });
}

function abrir_forma_pago() {
    $("#paymentModal").dialog({
        autoOpen: true,
        modal: true,
        width: 'auto',
        height: 'auto',
        maxWidth: $(window).width() * 0.90,
        maxHeight: $(window).height() * 0.90,
        minWidth: 500,
        minHeight: 200,
        buttons: [
            {
                text: "Salir",
                class: "btn btn-dark btn-sm",
                style: "width:90px; height:30px; font-size:14px;",
                click: function () {
                    $(this).dialog("close");

                },
            },
            {
                text: "Grabar",
                class: "btn btn-primary btn-sm",
                style: "width:90px; height:30px; font-size:14px;",
                click: function () {
                    let acumulado = $('#accumulated').val();
                    let monto = $('#amount').val();
                    //crear_impuventa_asiento_movimiento();
                    verificar();
                    //localStorage.removeItem('medios_pago');
                },
            },
        ], beforeClose: function () {
            resetModal('paymentModal');
        },
        open: function () {
            // Obtener fecha de hoy en formato YYYY-MM-DD
            const hoy = new Date().toISOString().split('T')[0];

            // Asignar la fecha de hoy a todos los inputs tipo date
            $('#paymentModal input[type="date"]').each(function () {
                if (!$(this).val()) {
                    $(this).val(hoy);
                }
            });
        }

    });

    cargar_datos_formadepago();


    // Mostrar por defecto la sección de efectivo
    $("#cashSection").show();
}

//llamar cuando se seleccione un cliente


function tabla_facturas_pendientes(cliente, moneda) {
    if ($.fn.DataTable.isDataTable('#imputacionTable')) {
        $('#imputacionTable tbody').off(); // Elimina todos los eventos previos en el tbody
        $('#imputacionTable').DataTable().destroy(); // Destruye la tabla completamente
        $('#imputacionTable tbody').empty(); // Limpia el DOM del tbody
    }


    const table = $('#imputacionTable').DataTable({
        info: false,        // Oculta "Mostrando X a Y de Z registros"
        lengthChange: false,
        serverSide: true,
        ajax: {
            url: "/admin_cont/source_facturas_pendientes",
            type: "GET",
            data: function (d) {
                d.cliente = cliente;
                d.moneda = $('#id_moneda').val();
            }
        },
        rowId: function (data) {
            const id = `${data.documento}-${data.tipo_doc}`;
            return id;
        },
        columns: [
            {data: 'id', visible: false}, // Oculto
            {data: 'vencimiento', },
            {data: 'emision', },
              {
                  data: 'documento',
                  createdCell: function (td, cellData, rowData) {
                    // limpiamos estilos previos por si la celda se reutiliza
                    td.classList.remove('bg-success','bg-primary','text-white','doc-verde','doc-azul');

                    // Opción A: usando clases de Bootstrap (bg-success / bg-primary)
                    if (rowData.source === 'VERDE') {
                      td.classList.add('bg-success','text-white');
                    } else if (rowData.source === 'AZUL') {
                      td.classList.add('bg-primary','text-white');
                    }

                    // ---- Opción B (si NO usás Bootstrap), comentá A y descomentá esto:
                    // if (rowData.source === 'VERDE') {
                    //   td.classList.add('doc-verde');
                    // } else if (rowData.source === 'AZUL') {
                    //   td.classList.add('doc-azul');
                    // }
                  }
                },
            {data: 'total'},
            {data: 'saldo'},
            {data: 'imputado'},
            {data: 'tipo_cambio'},
            {data: 'embarque', visible:false },   // OCULTO
            {data: 'detalle'},
            {data: 'posicion', },   // OCULTO
            {data: 'moneda'},
            {data: 'paridad' , visible: false},
            {data: 'tipo_doc', },   // OCULTO
            {data: 'source', visible: false }      // OCULTO
        ],
        responsive: true,
        processing: true,
        lengthChange: false,
        language: {
            url: "//cdn.datatables.net/plug-ins/1.10.24/i18n/Spanish.json"
        },
        initComplete: function () {
        },
        drawCallback: function () {
            updateBalance();

            // Reasignar evento de clic a las filas
            $('#imputacionTable tbody').off('click', 'tr').on('click', 'tr', function () {
                $(this).toggleClass('table-secondary');
                const selectedRows = table.rows('.table-secondary').count();
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
                    $('#deshacer').prop('disabled', false); // Habilitar el botón
                } else {
                    $('#deshacer').prop('disabled', true);  // Deshabilitar el botón
                }

                let totalImporte = 0;
                table.rows('.table-secondary').nodes().each(function (node) {
                    let saldo = parseFloat(table.cell(node, 5).data()) || 0;
                    totalImporte += saldo;
                });
                $('#id_importe').val(totalImporte.toFixed(2));
                $('#a_imputar').val(totalImporte.toFixed(2));
            });
        }



    });
    existe_cliente = true;


    $('#imputarSeleccion').on('click', function () {
        if (!existe_cliente) {
            alert('Seleccione un cliente para continuar');
            return;
        }

        const seleccionadas = table.rows('.table-secondary'); // Obtener las filas seleccionadas
        const data = seleccionadas.data().toArray(); // Convertir a array para depuración
        let importe = parseFloat($('#id_importe').val()) || 0; // Obtener el importe disponible
        let imputado = parseFloat($('#a_imputar').val()) || 0; // Obtener el importe disponible
        let acumulado = 0;
        let saldoAFavor = 0; // Saldos negativos a favor
        let balance = 0;


        // Validación inicial para acreedores
        const esInvalida = data.some(row => row.source === 'acreedor' && row.tipo_doc !== 'FACTURA');
        if (esInvalida) {
            alert('No se puede imputar registros de acreedor que no sean del tipo "FACTURA".');
            return;
        }


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
            let saldo = parseFloat(table.cell(node, 5).data()) || 0;
            let imputadoActual = parseFloat(table.cell(node, 6).data()) || 0;

            // Guardar estado original en el historial
            historial.push({
                modo: table.cell(node, 0).data(),
                numero: table.cell(node, 3).data(),
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
                let saldo = parseFloat(table.cell(node, 5).data()) || 0;

                // Si el saldo es negativo (a favor)
                if (saldo < 0 && saldoAFavor > 0) {
                    const compensacion = Math.min(Math.abs(saldo), saldoAFavor); // Compensar hasta donde sea posible
                    saldo += compensacion; // Reducir el saldo negativo
                    saldoAFavor -= compensacion; // Reducir el saldo a favor
                    table.cell(node, 5).data(saldo.toFixed(2)); // Actualizar saldo en la tabla
                    $(table.cell(node, 5).node()).css('background-color', '#fcec3f'); // Colorear celda
                }

                // Si el saldo es positivo (en contra)
                if (saldo > 0 && acumulado > 0) {
                    const compensacion = Math.min(saldo, acumulado); // Compensar hasta donde sea posible
                    saldo -= compensacion; // Reducir el saldo positivo
                    acumulado -= compensacion; // Reducir el saldo acumulado
                    table.cell(node, 5).data(saldo.toFixed(2)); // Actualizar saldo en la tabla
                    $(table.cell(node, 5).node()).css('background-color', '#fcec3f'); // Colorear celda
                }
            });

            // Actualizar el importe restante con lo que quede sin compensar
            if (diferencia > 0) {
                acumulado = diferencia; // Queda saldo positivo
                saldoAFavor = 0; // Todo el saldo negativo se compensa
            } else if (diferencia < 0) {
                saldoAFavor = Math.abs(diferencia); // Queda saldo negativo
                acumulado = 0; // Todo el saldo positivo se compensa
            } else {
                acumulado = 0;
                saldoAFavor = 0; // Saldos completamente compensados
            }
        }


        // Incrementar el importe disponible con el saldo a favor compensado
        importe += saldoAFavor;

        // Validar si el importe alcanza
        if (seleccionadas.count() > 0 && importe < acumulado) {
            let restante = importe; // Inicializar importe restante

            seleccionadas.nodes().each(function (node) {
                if (restante <= 0) return; // Detener si no queda importe por asignar

                let saldo = parseFloat(table.cell(node, 5).data()) || 0;
                let imputadoActual = parseFloat(table.cell(node, 6).data()) || 0;

                if (saldo >= 0) {
                    let asignacion = Math.min(saldo, restante); // Determinar cuánto se puede imputar
                    saldo -= asignacion; // Reducir el saldo por el importe asignado
                    restante -= asignacion; // Reducir el importe restante

                    table.cell(node, 5).data(saldo.toFixed(2)); // Actualizar la columna de saldo
                    table.cell(node, 6).data((imputadoActual + asignacion).toFixed(2)); // Actualizar la columna de imputado

                    $(table.cell(node, 5).node()).css('background-color', '#fcec3f'); // Amarillo para columna 5
                    $(table.cell(node, 6).node()).css('background-color', '#fcec3f'); // Amarillo para columna 6

                    // Actualizar balance
                    balance += asignacion;

                    // Agregar datos actualizados al vector
                    filasAfectadas.push({
                        modo: table.cell(node, 0).data(),
                        numero: table.cell(node, 3).data(),
                        nuevoSaldo: saldo.toFixed(2),
                        imputado: (imputadoActual + asignacion).toFixed(2),
                        source: table.cell(node, 9).data()
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
            seleccionadas.nodes().to$().removeClass('table-secondary');
            updateBalance();
            return;
        }

        // Procesar todas las filas seleccionadas normalmente si el importe alcanza
        seleccionadas.nodes().each(function (node) {
            let saldo = parseFloat(table.cell(node, 5).data()) || 0;
            let imputadoActual = parseFloat(table.cell(node, 6).data()) || 0;

            if (saldo >= 0) {

                if (saldo > imputado) {
                    let restante = imputado;
                    let asignacion = Math.min(saldo, restante); // Determinar cuánto se puede imputar
                    saldo -= asignacion; // Reducir el saldo por el importe asignado
                    restante -= asignacion; // Reducir el importe restante

                    table.cell(node, 5).data(saldo.toFixed(2)); // Actualizar la columna de saldo
                    table.cell(node, 6).data((imputadoActual + asignacion).toFixed(2)); // Actualizar la columna de imputado

                    $(table.cell(node, 5).node()).css('background-color', '#fcec3f'); // Amarillo para columna 5
                    $(table.cell(node, 6).node()).css('background-color', '#fcec3f'); // Amarillo para columna 6

                    // Actualizar balance
                    balance += asignacion;

                    // Agregar datos actualizados al vector
                    filasAfectadas.push({
                        modo: table.cell(node, 0).data(),
                        numero: table.cell(node, 3).data(),
                        nuevoSaldo: saldo.toFixed(2),
                        imputado: (imputadoActual + asignacion).toFixed(2),
                        source: table.cell(node, 9).data()
                    });
                } else {
                    table.cell(node, 6).data(imputadoActual + saldo); // Actualizar la columna 6
                    table.cell(node, 5).data(0); // Actualizar la columna 5

                    $(table.cell(node, 5).node()).css('background-color', '#fcec3f'); // Amarillo para columna 5
                    $(table.cell(node, 6).node()).css('background-color', '#fcec3f'); // Amarillo para columna 6

                    // Actualizar balance
                    balance += saldo;

                    // Agregar datos actualizados al vector
                    filasAfectadas.push({
                        modo: table.cell(node, 0).data(),
                        numero: table.cell(node, 3).data(),
                        nuevoSaldo: '0.00',
                        imputado: (imputadoActual + saldo).toFixed(2),
                        source: table.cell(node, 9).data()
                    });
                }
            }
        });

        // Actualizar importe restante
//    const total = imputado - acumulado;
        const total = imputado - balance;
        let ac = parseFloat($('#acumulado').val());
        ac = ac + acumulado;

        //$('#acumulado').val(ac.toFixed(2));
        calcular_acumulado();
        $('#a_imputar').val(total.toFixed(2));

        seleccionadas.nodes().to$().removeClass('table-secondary');

        localStorage.setItem('filasAfectadas', JSON.stringify(filasAfectadas));
        localStorage.setItem('historial', JSON.stringify(historial));
        updateBalance();
        $('#deshacer').prop('disabled', false);
    });

    $('#deshacer').on('click', function () {
        const seleccionadas = table.rows('.table-secondary');
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
            const imputadoActual = parseFloat(table.cell(node, 6).data()) || 0; // Valor actual en imputado
            imputarTotal += imputadoActual; // Sumar a imputarTotal
        });

        // Restaurar los valores originales desde el historial
        seleccionadas.nodes().each(function (node) {
            let modo = table.cell(node, 0).data();
            let numero = table.cell(node, 3).data();

            let filaOriginal = historial.find(f => f.modo === modo && f.numero === numero);

            if (filaOriginal) {
                table.cell(node, 5).data(filaOriginal.saldoOriginal); // Restaurar saldo
                table.cell(node, 6).data(filaOriginal.imputadoOriginal); // Restaurar imputado

                // Quitar colores de las celdas restauradas
                $(table.cell(node, 5).node()).css('background-color', '');
                $(table.cell(node, 6).node()).css('background-color', '');

                // Actualizar balance y acumulado
                balance += parseFloat(filaOriginal.saldoOriginal) || 0;
                acumulado += parseFloat(filaOriginal.imputadoOriginal) || 0;
            } else {
                console.warn('No se encontró historial para la fila:', {modo, numero});
            }
        });

        // Actualizar los campos con los valores calculados
        $("#balance").val(balance.toFixed(2));
        $("#acumulado").val(acumulado.toFixed(2));
        $("#a_imputar").val(imputarTotal.toFixed(2)); // Actualizar el valor de a_imputar

        // Quitar la clase 'selected' de las filas seleccionadas
        seleccionadas.nodes().to$().removeClass('table-secondary');

        // Llamar a updateBalance para recalcular cualquier dato adicional
        updateBalance();
        calcular_acumulado();
        // Notificar al usuario que los cambios han sido revertidos
        verificarImputado(table); // Deshabilitar el botón
        $('#id_importe').prop('readonly', false);
        alert('Cambios deshechos en las filas seleccionadas.');
    });

}

function updateBalance() {
    let balanceTotal = 0;

    // Verifica si DataTable está inicializado
    if ($.fn.DataTable.isDataTable('#imputacionTable')) {
        const table = $('#imputacionTable').DataTable();

        // Itera sobre todas las filas visibles de la tabla
        table.rows().every(function () {
            let data = this.data(); // Obtén los datos de la fila
            let saldo = parseFloat(data.saldo) || 0; // Asegúrate de convertir el saldo a número
            balanceTotal += saldo; // Suma el saldo al balance total
        });

        // Actualiza el campo del balance con el total calculado
        $('#balance').val(balanceTotal.toFixed(2));
    } else {
        console.warn('La tabla #imputacionTable no está inicializada.');
    }
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
        $('#deshacer').prop('disabled', false); // Habilitar el botón
    } else {
        $('#deshacer').prop('disabled', true);  // Deshabilitar el botón
    }
}

function calcular_acumulado() {
    let acumulado = 0;

    // Verifica si DataTable está inicializado
    if ($.fn.DataTable.isDataTable('#imputacionTable')) {
        const table = $('#imputacionTable').DataTable();

        // Itera sobre todas las filas visibles de la tabla
        table.rows().every(function () {
            let data = this.data(); // Obtén los datos de la fila
            let imputado = parseFloat(data.imputado) || 0; // Asegúrate de convertir el saldo a número
            acumulado += imputado; // Suma el saldo al balance total
        });

        // Actualiza el campo del balance con el total calculado
        $('#acumulado').val(acumulado.toFixed(2));
    } else {
        console.warn('La tabla #imputacionTable no está inicializada.');
    }
}

function cargar_datos_formadepago() {
    let imputar = $('#a_imputar').val();
    let importe = $('#id_importe').val();
    let acumulado = $('#acumulado').val();


    const table = $('#imputacionTable').DataTable();

    let documentos = '';

    table.rows().nodes().each(function (node) {
        let imputado = parseFloat(table.cell(node, 6).data()) || 0;

    if (imputado !== 0) {
      let nroDocumento = table.cell(node, 3).data();
      const [, parte] = String(nroDocumento).split('-', 2);
      documentos += (parte ?? '').trim() + ';';
    }

    });

    documentos = documentos.slice(0, -1);

    $('#observations').val(documentos);
    acumulado = parseFloat(acumulado || 0).toFixed(2); // Convertir a número y aplicar toFixed
    importe = parseFloat(importe || 0).toFixed(2);     // Convertir a número y aplicar toFixed

    if (imputar <= 0) {
        $('#amount').html(acumulado);

    } else {
        $('#amount').html(importe);
    }
    $('#cashAmount').val(importe);
    $('#checkAmount').val(importe);
    $('#checkAmount_trans').val(importe);
    $('#checkAmount_deposito').val(importe);
    $('#checkAmount_otro').val(importe);
}

function ingresar_datos() {
    let monto = $('#cashAmount').val();
    let importe = $('#amount').html();
    let arbitraje = $('#id_arbitraje').val();

    const tbody = $('#exampleTableCobranza tbody');
//tbody.empty();

    let modo, emision, banco, numero, moneda, total, tc, vencimiento, cuenta;
    modo = emision = banco = numero = moneda = total = tc = vencimiento = cuenta = 0;

    if ($('#efectivo').is(':checked')) {
        const selectElement = document.getElementById('id_cuenta_efectivo');
        const moneda_select = document.getElementById('id_moneda_efectivo');
        const labelSeleccionado = selectElement.options[selectElement.selectedIndex].text;
        const valueSeleccionado = selectElement.value;
        const monedaV = moneda_select.value;
        modo = 'EFECTIVO';
        emision = obtenerFechaHoy();
        banco = valueSeleccionado;
        numero = 0;
        moneda = monedaV;
        total = monto;
        tc = arbitraje;
        cuenta = valueSeleccionado;
        vencimiento = obtenerFechaHoy();

    } else if ($('#cheque').is(':checked')) {
        const selectElement = document.getElementById('id_cuenta_cheque');
        const moneda_select = document.getElementById('id_moneda_cheque');
        const monedaV = moneda_select.value;
        const labelSeleccionado = selectElement.options[selectElement.selectedIndex].text;
        const valueSeleccionado = selectElement.value;
        modo = 'CHEQUE';
        emision = $('#checkEmission').val();
        let bancoText = $('#id_banco_cheque option:selected').text();
        banco = bancoText;
        numero = $('#checkNumber').val();
        tc = arbitraje;
        cuenta = valueSeleccionado;
        moneda = monedaV;
        vencimiento = $('#checkDueDate').val();
        total = $('#checkAmount').val();

    } else if ($('#trans').is(':checked')) {
        const selectElement = document.getElementById('id_cuenta_transferencia');
        const moneda_select = document.getElementById('id_moneda_transferencia');
        const monedaV = moneda_select.value;
        const labelSeleccionado = selectElement.options[selectElement.selectedIndex].text;
        modo = 'TRANSFER';
        emision = $('#checkEmission_trans').val();
        banco = labelSeleccionado;
        numero = 0;
        tc = arbitraje;
        cuenta = null;
        moneda = monedaV;
        vencimiento = $('#checkDueDate_trans').val();
        total = $('#checkAmount_trans').val();
    } else if ($('#deposito').is(':checked')) {
        const selectElement = document.getElementById('id_cuenta_deposito');
        const moneda_select = document.getElementById('id_moneda_deposito');
        const monedaV = moneda_select.value;
        const labelSeleccionado = selectElement.options[selectElement.selectedIndex].text;
        modo = 'DEPOSITO';
        emision = $('#checkEmission_deposito').val();
        banco = labelSeleccionado;
        numero = 0;
        tc = arbitraje;
        cuenta = null;
        moneda = monedaV;
        vencimiento = $('#checkDueDate_deposito').val();
        total = $('#checkAmount_deposito').val();
    } else if ($('#otro').is(':checked')) {
        const selectElement = document.getElementById('id_cuenta_otro');
        const moneda_select = document.getElementById('id_moneda_otro');
        const monedaV = moneda_select.value;
        const labelSeleccionado = selectElement.options[selectElement.selectedIndex].text;
        modo = 'OTRO';
        emision = $('#checkEmission_otro').val();
        banco = labelSeleccionado;
        numero = $('#checkNumber_otro').val();
        tc = arbitraje;
        cuenta = $('#cuenta_otro').val();
        moneda = monedaV;
        vencimiento = $('#checkDueDate_otro').val();
        total = $('#checkAmount_otro').val();
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

    let medios_pago = JSON.parse(localStorage.getItem('medios_pago')) || [];

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

function crear_impuventa_asiento_movimiento() {

    if (!$('#id_cuenta_observaciones').val() && $('#difference').val() != 0) {
        alert('Debe asignar la diferencia a una cuenta');
        return;
    }
//traer cliente tambien
    let impuventa = JSON.parse(localStorage.getItem('filasAfectadas')) || [];
    let medios_pago = JSON.parse(localStorage.getItem('medios_pago')) || [];

    let vector = {};
    let imputaciones = [];
    let asiento = [];
    let movimiento = [];
    let cobranza = [];

    impuventa.forEach((item) => {
        imputaciones.push({
            nroboleta: item.modo, //cambio hecho aca de numero
            imputado: item.imputado,
            saldo_imputado: item.nuevoSaldo
        });
        movimiento.push({
            imputado: item.modo,
            saldo: item.nuevoSaldo,
            boletas: $('#observations').val()
        });
    });

    medios_pago.forEach((item) => {
        asiento.push({
            modo: item.modo,
            cuenta: item.cuenta,
            banco: item.banco,
            nro_mediopago: item.numero,
            total_pago: item.total,
            vencimiento: item.vencimiento
        });
    });

    cobranza.push({
        nrocliente: $('#cliente_cobranza_hidden').val(),
        serie: $('#id_serie').val(),
        prefijo: $('#id_prefijo').val(),
        numero: $('#id_numero').val(),
        total: $('#id_importe').val(),
        nromoneda: $('#id_moneda').val(),
        arbitraje: $('#id_arbitraje').val(),
        paridad: $('#id_paridad').val()
    });


    vector.cobranza = cobranza;
    vector.imputaciones = imputaciones;
    vector.asiento = asiento;
    vector.movimiento = movimiento;
    if ($('#difference').val() != 0) {
        let nuevaFila = {
            modo: "DIFERENCIA",
            cuenta: $('#id_cuenta_observaciones').val(),
            banco: $('#id_cuenta_observaciones option:selected').text(),
            nro_mediopago: 0,
            total_pago: $('#difference').val(),
            vencimiento: null
        };

        vector.asiento.push(nuevaFila);
    }


    $.ajax({
        url: '/admin_cont/guardar_impuventa/', // Cambia esto a la URL correcta
        method: 'POST',
        headers: {'X-CSRFToken': csrf_token}, // Asegúrate de tener el CSRF token
        data: JSON.stringify({'vector': vector}),
        contentType: 'application/json',
        success: function (response) {
            if (response.status === 'exito') {

                table.ajax.reload();
                if(confirm('¿Desea enviar un email con el comprobante?')){
                    let autogenerado = response.autogenerado;
                    if(autogenerado!=null){
                        get_data_email(autogenerado);
                    }else{
                        alert('Algo salió mal.');
                        $('#dialog-form').dialog('close');
                        $('#paymentModal').dialog('close');
                    }
                }else{
                    $('#dialog-form').dialog('close');
                    $('#paymentModal').dialog('close');
                }

            } else {
                alert(response.status);
            }
        },
        error: function (xhr) {
            alert("Error al guardar los datos: " + xhr.responseText);
        },
    });

}

function crear_anticipo() {
    if (!$('#id_cuenta_observaciones').val() && $('#difference').val() != 0) {
        alert('Debe asignar la diferencia a una cuenta');
        return;
    }
//traer cliente tambien
    let impuventa = JSON.parse(localStorage.getItem('filasAfectadas')) || [];
    let medios_pago = JSON.parse(localStorage.getItem('medios_pago')) || [];

    let vector = {};
    let asiento = [];
    let cobranza = [];


    medios_pago.forEach((item) => {
        asiento.push({
            modo: item.modo,
            cuenta: item.cuenta,
            banco: item.banco,
            nro_mediopago: item.numero,
            total_pago: item.total,
            vencimiento: item.vencimiento
        });
    });

    cobranza.push({
        nrocliente: $('#cliente_cobranza_hidden').val(),
        serie: $('#id_serie').val(),
        prefijo: $('#id_prefijo').val(),
        numero: $('#id_numero').val(),
        total: $('#id_importe').val(),
        nromoneda: $('#id_moneda').val(),
        arbitraje: $('#id_arbitraje').val(),
        paridad: $('#id_paridad').val()
    });


    vector.cobranza = cobranza;
    vector.asiento = asiento;
    if ($('#difference').val() != 0) {
        let nuevaFila = {
            modo: "DIFERENCIA",
            cuenta: $('#id_cuenta_observaciones').val(),
            banco: $('#id_cuenta_observaciones option:selected').text(),
            nro_mediopago: 0,
            total_pago: $('#difference').val(),
            vencimiento: null
        };

        vector.asiento.push(nuevaFila);
    }

    console.log('anticipo ' + vector);


    $.ajax({
        url: '/admin_cont/guardar_anticipo/', // Cambia esto a la URL correcta
        method: 'POST',
        headers: {'X-CSRFToken': csrf_token}, // Asegúrate de tener el CSRF token
        data: JSON.stringify({'vector': vector}),
        contentType: 'application/json',
        success: function (response) {
            if (response.status === 'exito') {
                alert("Datos guardados correctamente");
                // Opcional: recargar una tabla o actualizar la UI
            } else {
                alert("ghfghfgh: " + response.status);
            }
        },
        error: function (xhr) {
            alert("Error al guardar los datos: " + xhr.responseText);
        },
    });

}

function verificar() {
    let key = false;
    let rows = document.querySelectorAll('#imputacionTable tbody tr');
    rows.forEach(row => {
        let imputado = row.cells[5]?.textContent.trim();
        let imputadoValue = parseFloat(imputado) || 0;

        if (imputadoValue !== 0) {
            console.log('Fila con Imputado diferente de cero:', imputadoValue);
            key = true;
        }
    });
    let importe = $('#id_importe').val();
    let imputar = $('#a_imputar').val();


    if (key) {
        if (imputar != 0) {
            if (confirm('No se ha asignado todo el IMPORTE, ¿Desea continuar como anticipo?')) {
                crear_anticipo_consaldo();
            }
        }
        crear_impuventa_asiento_movimiento();
    } else {
        if (confirm('No hay una boleta seleccionada, ¿Desea continuar como anticipo?')) {
            crear_anticipo();
        }
    }

}

function crear_anticipo_consaldo() {
    if (!$('#id_cuenta_observaciones').val() && $('#difference').val() != 0) {
        alert('Debe asignar la diferencia a una cuenta');
        return;
    }
//traer cliente tambien
    let impuventa = JSON.parse(localStorage.getItem('filasAfectadas')) || [];
    let medios_pago = JSON.parse(localStorage.getItem('medios_pago')) || [];

    let vector = {};
    let asiento = [];
    let cobranza = [];


    medios_pago.forEach((item) => {
        asiento.push({
            modo: item.modo,
            cuenta: item.cuenta,
            banco: item.banco,
            nro_mediopago: item.numero,
            total_pago: item.total,
            vencimiento: item.vencimiento
        });
    });

    cobranza.push({
        nrocliente: $('#cliente_cobranza_hidden').val(),
        serie: $('#id_serie').val(),
        prefijo: $('#id_prefijo').val(),
        numero: $('#id_numero').val(),
        total: $('#id_importe').val(),
        nromoneda: $('#id_moneda').val(),
        arbitraje: $('#id_arbitraje').val(),
        paridad: $('#id_paridad').val(),
        saldo: $('#a_imputar').val()
    });


    vector.cobranza = cobranza;
    vector.asiento = asiento;
    if ($('#difference').val() != 0) {
        let nuevaFila = {
            modo: "DIFERENCIA",
            cuenta: $('#id_cuenta_observaciones').val(),
            banco: $('#id_cuenta_observaciones option:selected').text(),
            nro_mediopago: 0,
            total_pago: $('#difference').val(),
            vencimiento: null
        };

        vector.asiento.push(nuevaFila);
    }

    console.log('cobranza ' + cobranza);


    $.ajax({
        url: '/admin_cont/guardar_anticipo/', // Cambia esto a la URL correcta
        method: 'POST',
        headers: {'X-CSRFToken': csrf_token}, // Asegúrate de tener el CSRF token
        data: JSON.stringify({'vector': vector}),
        contentType: 'application/json',
        success: function (response) {
            if (response.status === 'exito') {
                alert("Datos guardados correctamente");
                // Opcional: recargar una tabla o actualizar la UI
            } else {
                alert("ghfghfgh: " + response.status);
            }
        },
        error: function (xhr) {
            alert("Error al guardar los datos: " + xhr.responseText);
        },
    });

}

function traer_proximo_numero() {
    $.ajax({
        url: "/admin_cont/proximo_mboleta/",
        method: "GET",
        success: function (data) {
            if (data.proximo_mboleta) {
                $('#id_numero').val(data.proximo_mboleta);  // Cambiá el ID si es otro
            }
        },
        error: function (xhr) {
            console.error("No se pudo obtener el número de boleta:", xhr.responseText);
        }
    });
}

$('#id_moneda').on('change', function () {
    const cliente = $('#cliente_cobranza_hidden').val();
    const moneda = $(this).val();

    tabla_facturas_pendientes(cliente, moneda);
});
$('#abrir_arbi').on('click', function (event) {
    $("#arbitraje_modal").dialog({
        autoOpen: true,
        modal: true,
        title: "Cargar un arbitraje para el día de hoy",
        height: 'auto',
        width: 'auto',
        position: {my: "top", at: "top+20", of: window},
        buttons: [
            {
                text: "Guardar",
                class: "btn btn-primary btn-sm",
                style: "",
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
                        headers: {'X-CSRFToken': csrf_token},
                        data: {
                            arbDolar: arbDolar,
                            parDolar: parDolar,
                            tipoMoneda: tipoMoneda,
                            pizDolar: pizDolar,
                            fecha: fecha
                        },
                        success: function (data) {
                            if (data['status'].length == 0) {
                                alert("Valores guardados correctamente");
                                $("#arbitraje_modal").dialog("close");
                            } else {
                                alert(data['status']);
                            }
                        },
                        error: function (xhr, status, error) {
                            alert("Error al guardar los datos: " + error);
                        }
                    });
                },
            },
            {
                text: "Salir",
                class: "btn btn-dark btn-sm",
                style: "",
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
        data: { fecha: hoy },

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

function buscar_detalle(autogenerado) {
    $.ajax({
        url: '/admin_cont/detalle_cobranza/',
        method: 'GET',
        data: {
            autogenerado: autogenerado
        },
        success: function (response) {
            if (response.success) {
                const data = response.data;

                $('#autogen_detalle_cobranza').val(autogenerado);
                $('#numero_detalle_cobranza').val(data.numero);
                $('#moneda_detalle_cobranza').val(data.moneda);
                $('#fecha_detalle_cobranza').val(data.fecha);
                $('#arbitraje_detalle_cobranza').val(parseFloat(data.arbitraje || 0).toFixed(2));
                $('#por_imputar_detalle_cobranza').val(parseFloat(data.imputable || 0).toFixed(2));
                $('#paridad_detalle_cobranza').val(parseFloat(data.paridad || 0).toFixed(2));
                $('#detalle_detalle_cobranza').val(data.detalle);
                $('#diferencia_cobranza').val(data.diferencia || '');
                $('#id_importe_detalle').val(data.total || 0);
                $('#nro_cliente_detalle_cobranza').val(data.nrocliente);
                $('#cliente_detalle_cobranza').val(data.cliente);

                $('#efectivo_recibido').val(data.efectivo || '');
                $('#transferencia_recibida').val(data.transferencia || '');
                $('#deposito_recibido').val(data.deposito || '');

                $('#tablaChequesRecibidos').empty();
                if (data.cheques && data.cheques.length > 0) {
                    data.cheques.forEach(function (cheque) {
                        const fila = `
              <tr>
                <td>${cheque.fecha || ''}</td>
                <td>${cheque.banco || ''}</td>
                <td>${cheque.numero || ''}</td>
                <td class="text-right">${cheque.monto != null ? parseFloat(cheque.monto).toFixed(2) : ''}</td>
                <td>${cheque.vencimiento || ''}</td>
              </tr>
            `;
                        $('#tablaChequesRecibidos').append(fila);
                    });
                } else {
                    $('#tablaChequesRecibidos').html('<tr><td colspan="5" class="text-center text-muted">Sin cheques registrados.</td></tr>');
                }

                $('#tablaDocumentosImputados').empty();
                if (data.imputados && data.imputados.length > 0) {
                    data.imputados.forEach(function (doc) {
                        const fila = `
              <tr>
                <td class="oculto">${doc.autogenerado || ''}</td>
                <td>${doc.documento || ''}</td>
                <td class="text-right">${doc.imputado != null ? parseFloat(doc.imputado).toFixed(2) : ''}</td>
                <td>${doc.referencia || ''}</td>
                <td>${doc.posicion || ''}</td>
              </tr>
            `;
                        $('#tablaDocumentosImputados').append(fila);
                    });
                } else {
                    $('#tablaDocumentosImputados').html('<tr><td colspan="4" class="text-center text-muted">Sin documentos imputados.</td></tr>');
                }

                $("#modalCobranzaDetalle").dialog("open");

            }
        },
        error: function (xhr) {
            alert("No se pudo obtener el detalle de la cobranza.");
        }
    });
}

function sendEmail(to, cc, cco, subject, message, title) {
     let from = $('#id_from').val();
    if (!confirm('¿Realmente desea ENVIAR el correo?')) {
        return;
    }
    let miurl = "/envio_notificacion/AD/";
    var toData = {
        'to': to,
        'cc': cc,
        'cco': cco,
        'subject': subject,
        'from': from,
        'message': message,
        'tipo': title,
        'seguimiento': 0,
        'archivos_adjuntos': JSON.stringify([]),
        'csrfmiddlewaretoken': csrf_token,
    };
    $.ajax({
        type: "POST",
        url: miurl,
        data: toData,
        async: false,
        success: function (resultado) {
            if (resultado['resultado'] === 'exito') {
                mostrarToast('¡Mensaje enviado con exito!', 'success');
                return true;
            } else {
                alert(resultado['resultado']);
            }
        }
    });


}

function get_data_email(autogenerado) {
    let title = 'title';
    let mail_to = 'mail to';
    $("#id_to").val('');
    $("#id_cc").val('');
    $("#id_cco").val('');
    cco = $("#id_subject").val('');
    $('#email_add_input').summernote('destroy');

    $("#emails_modal").dialog({
            autoOpen: true,
            open: function (event, ui) {
                $('#email_add_input').summernote('destroy');
                $('#email_add_input').summernote({
                    placeholder: 'Ingrese su texto aqui',
                    tabsize: 10,
                    height: wHeight * 0.60,
                    width: wWidth * 0.88,
                    toolbar: [
                        ['style', ['style']],
                        ['font', ['bold', 'underline', 'clear']],
                        ['color', ['color']],
                        ['para', ['ul', 'ol', 'paragraph']],
                        ['table', ['table']],
                        ['insert', ['link', 'picture', 'video']],
                        ['view', ['fullscreen', 'codeview']]
                    ]
                });
                $('#email_add_input').focus();
            },
            modal: true,
            title: " Correo con comprobante de cobranza",
            height: wHeight * 0.90,
            width: wWidth * 0.90,
            class: 'modal fade',
            buttons: [
                {
                    text: "Enviar",
                    class: "btn btn-primary",
                    style: "width:100px",
                    click: function () {
                        to = $("#id_to").val();
                        cc = $("#id_cc").val();
                        cco = $("#id_cco").val();
                        subject = $("#id_subject").val();
                        message = $("#email_add_input").summernote('code');
                        sendEmail(to, cc, cco, subject, message, title);
                        $(this).dialog("close");
                    },
                }, {
                    text: "Salir",
                    class: "btn btn-dark",
                    style: "width:100px",
                    click: function () {
                        $(this).dialog("close");
                        $('#modalSeleccionEmail').dialog("close");
                    },
                },],
            beforeClose: function (event, ui) {
                            localStorage.removeItem('medios_pago');
            localStorage.removeItem('filasAfectadas');
            localStorage.removeItem('historial');
                    window.location.reload();
            }
        })

    $.ajax({
        type: "POST",
        url: "/admin_cont/get_email_recibo_cobranza/",
        data: {
            autogenerado: autogenerado,
            csrfmiddlewaretoken: csrf_token
        },
        success: function (resultado) {
            if (resultado['resultado'] === 'exito') {
                $("#id_subject").val(resultado['asunto']);
                $("#id_to").val(resultado['email_cliente']);
                $("#email_add_input").summernote('code', resultado['mensaje']);
                let selectEmails = document.getElementById("id_from");
                if (selectEmails && resultado['emails_disponibles']) {
                    selectEmails.innerHTML = "";

                    resultado['emails_disponibles'].forEach(function(email) {
                        let option = document.createElement("option");
                        option.value = email;
                        option.text = email;
                        selectEmails.appendChild(option);
                    });
                }
            } else {
                alert('Error: ' + resultado['detalle']);
            }
        }
    });
}

function cargar_arbitraje() {
    const fecha = $('#id_fecha').val();

    $.ajax({
        url: "/admin_cont/cargar_arbitraje/",
        type: "GET",
        data: { fecha: fecha },
        dataType: "json",
        success: function (data) {
            $('#id_arbitraje').val(data.arbitraje);
            $('#id_paridad').val(data.paridad);
        },
        error: function (xhr, status, error) {
            alert("Error al cargar los datos iniciales: " + error);
        }
    });
}
