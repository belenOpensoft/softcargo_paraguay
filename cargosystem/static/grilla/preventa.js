//facturar
function facturar(){
    let selectedRowN = localStorage.getItem('num_house_gasto');
    let tablaOrigen = localStorage.getItem('tabla_origen')

    if(selectedRowN==null){
    alert('Seleccione una fila.');
    return;
    }
    const wHeight = $(window).height();
    const wWidth = $(window).width();
    $('#destinatario').val('');
    $('#destinatario_input').val('');
    $('#destinatario').css({"border-color": "", 'box-shadow': ''});
    $('#destinatario_input').css({"border-color": "", 'box-shadow': ''});
    if ($.fn.DataTable.isDataTable('#' + tablaOrigen)) {
        var table = $('#' + tablaOrigen).DataTable();
        var rowData = table.row('.table-secondary').data();
        if (rowData) {
            var $destinatario = $('#destinatario');
            var $destinatarioInput = $('#destinatario_input');

            var nombre = rowData[4];
            var codigo = '';

            if (tablaOrigen.endsWith('_em') || tablaOrigen.endsWith('_ea')) {
                codigo = rowData[20];
            } else if (tablaOrigen.endsWith('_et')) {
                codigo = rowData[22];
            } else if (tablaOrigen.endsWith('_im')) {
                codigo = rowData[23];
            } else if (tablaOrigen.endsWith('_it')) {
                codigo = rowData[21];
            } else if (tablaOrigen.endsWith('_ia')) {
                codigo = rowData[23];
            }

            $destinatario.val(nombre);
            $destinatario.attr('data-id', codigo);
            $destinatarioInput.val(codigo);

            $destinatario.css({
                "border-color": "#3D9A37",
                'box-shadow': '0 0 0 0.1rem #3D9A37'
            });
        }
    } else {
        console.log("La tabla no está inicializada.");
    }

    $("#facturar_modal").dialog({
        autoOpen: true,
        open: function (event, ui) {
            if(tablaOrigen.includes('tabla_general')){
                cargar_gastos_factura_general(function() {
            sumar_ingresos_tabla();
            asignar_costo_todos(event);

        });
            }
        cargar_gastos_factura(function() {
            sumar_ingresos_tabla();
            asignar_costo_todos(event);
        });
        },
        position: {
        my: "center top+20",
        at: "center top",
        of: window
        },
        modal: true,
        title: "Facturar el House N°: " + selectedRowN,
        height: 'auto',
        width: 'auto',
        class: 'modal fade',
        buttons: [

            {
                text: "Cancelar",
                class: "btn btn-dark",
                style: "width:100px",
                click: function () {
                    $(this).dialog("close");
                }
            },
                        {
                text: "Enviar Datos",
                class: "btn btn-primary",
                click: function () {
                    enviarDatosTabla();
                }
            },
        ],
        beforeClose: function (event, ui) {
        // localStorage.removeItem('num_house_gasto');
         $('#facturar_table').DataTable().destroy();
         $("#facturar_form").trigger("reset");

        }
    })
}
function asignar_costo_old() {
    const filaSeleccionada = $('#facturar_table tbody tr.table-secondary');

    if (filaSeleccionada.length > 0) {
        const data = $('#facturar_table').DataTable().row(filaSeleccionada).data();
        let cliente = $('#destinatario').val();
        let cliente_id = $('#destinatario_input').val();

        if(cliente){
            $('#facturar_table').DataTable().cell(filaSeleccionada, 3).data(cliente);
            $(filaSeleccionada).find('td').eq(3).text(cliente);

        } else {
           // alert('Debe seleccionar un destinatario.');
        }

    } else {
        alert("No hay ninguna fila seleccionada.");
    }
}
function asignar_costo_todos_old() {
    let cliente = $('#destinatario').val();
    let cliente_id = $('#destinatario_input').val();

    if (!cliente) {
        //alert('Debe seleccionar un destinatario.');
        return;
    }

    let tabla = $('#facturar_table').DataTable();
    tabla.rows().every(function() {
        this.cell(this, 3).data(cliente);
        $(this.node()).find('td').eq(3).text(cliente);
    });


}
function asignar_no() {
    const filaSeleccionada = $('#facturar_table tbody tr.table-secondary');

    if (filaSeleccionada.length > 0) {
        const data = $('#facturar_table').DataTable().row(filaSeleccionada).data();
        const mensaje = 'NO SE FACTURA EL CONCEPTO'; // Texto a asignar


        // Asigna el valor a la columna y al DOM
        $('#facturar_table').DataTable().cell(filaSeleccionada, 4).data(mensaje);
        $(filaSeleccionada).find('td').eq(4).text(mensaje);

    } else {
        alert("No hay ninguna fila seleccionada.");
    }
}
function asignar_no_todos() {
    const mensaje = 'NO SE FACTURA EL CONCEPTO'; // Texto a asignar

    let tabla = $('#facturar_table').DataTable();
    tabla.rows().every(function() {
        // Asigna el valor a la columna y al DOM
        this.cell(this, 4).data(mensaje);
        $(this.node()).find('td').eq(4).text(mensaje);
    });

    // tabla.draw(); // Descomentar si necesitas que la tabla se redibuje
}
function enviarDatosTabla_old() {

    let hayFilaSinClase = false;

    $('#facturar_table tbody tr').each(function () {
        if (!$(this).hasClass('fila-rojo') && !$(this).hasClass('fila-amarillo')) {
            hayFilaSinClase = true;
            return false;
        }
    });

    if (!hayFilaSinClase){
        alert('Todos los gastos estan pasados a facturacion.');
        return;
    }

    let preventa;
    let num=localStorage.getItem('num_house_gasto');
    let clase=localStorage.getItem('clase_house');
    let tablaOrigen = localStorage.getItem('tabla_origen')
    let num_destina=$('#destinatario_input').val();
    let dest=$('#destinatario').val();
    $.ajax({
        url: '/admin_cont/house_detail_factura/',
        data: { numero: num, clase:clase},
        method: 'GET',
        success: function (house) {
            let tipoElegido;
                preventa=({
                    seguimiento:house.seguimiento,
                    referencia:num,
                    transportista:getNameByIdClientes(house.transportista_e),
                    vuelo:house.viaje_e,
                    master:house.awb_e,
                    house:house.hawb_e,
                    fecha:house.fecharetiro_e,
                    kilos:house.bruto,
                    bultos:house.bultos,
                    volumen:house.cbm,
                    origen:house.origen_e,
                    destino:house.destino_e,
                    consigna:dest,
                    cliente:num_destina,
                    embarca:getNameByIdClientes(house.embarcador_e),
                    agente:getNameByIdClientes(house.agente_e),
                    posicion:house.posicion_e,
                    terminos:house.terminos,
                    pagoflete:house.pago,
                    commodity:house.producto_id,
                });
                if(['EM','EA','ET'].includes(clase)){
                    const confirmacion = confirm("¿Desea facturar gastos como 'Collect'?\n\nPresione ACEPTAR para 'Collect'\nPresione CANCELAR para 'Prepaid'");
                    tipoElegido = confirmacion ? "Collect" : "Prepaid";
                }else{
                    tipoElegido='Collect';
                }

                    guardar_preventa(preventa, tipoElegido);

                // preguntar a ana si se pasan todos los disponibles o
            // si se seleccionan por fila

                   $('#facturar_modal').dialog('close');
                   $('#'+tablaOrigen).DataTable().ajax.reload(null, false);

        },
        error: function (xhr, status, error) {
            console.error("Error fetching data:", error);
        }
    });
}
function enviarDatosTabla() {
  const tabla = $('#facturar_table').DataTable();

  // 1) ¿Queda alguna fila "válida" (sin rojo/amarillo) en TODAS las páginas?
  const filasNoPasadas = $(tabla.rows({ page: 'all' }).nodes())
    .filter(function () {
      const $tr = $(this);
      return !$tr.hasClass('fila-rojo') && !$tr.hasClass('fila-amarillo') && !$tr.hasClass('fila-verde');
      // Si querés excluir también las verdes, agrega: && !$tr.hasClass('fila-verde')
    });

  if (filasNoPasadas.length === 0) {
    alert('Todos los gastos estan pasados a facturacion.');
    return;
  }

  // 2) Tomar SOLO los checkboxes tildados (en todas las páginas)
  //    y además que su fila sea "válida" (sin rojo/amarillo)
  const idsSeleccionados = tabla
    .$('input.fila-check:checked', { page: 'all' })
    .map(function () {
      const $tr = $(this).closest('tr');
      const esValida = !$tr.hasClass('fila-rojo') && !$tr.hasClass('fila-amarillo') && !$tr.hasClass('fila-verde');
      // Si querés excluir también .fila-verde: && !$tr.hasClass('fila-verde')
      return esValida ? this.value : null;
    })
    .get()
    .filter(Boolean);

  if (idsSeleccionados.length === 0) {
    alert('Seleccioná al menos un gasto válido para facturar.');
    return;
  }

  // 3) (tu lógica actual)
  let num = localStorage.getItem('num_house_gasto');
  let clase = localStorage.getItem('clase_house');
  let tablaOrigen = localStorage.getItem('tabla_origen');
  let num_destina = $('#destinatario_input').val();
  let dest = $('#destinatario').val();

  $.ajax({
    url: '/admin_cont/house_detail_factura/',
    data: { numero: num, clase: clase },
    method: 'GET',
    success: function (house) {
      let tipoElegido;
      const preventa = {
        seguimiento: house.seguimiento,
        referencia: num,
        transportista: getNameByIdClientes(house.transportista_e),
        vuelo: house.viaje_e,
        master: house.awb_e,
        house: house.hawb_e,
        fecha: house.fecharetiro_e,
        kilos: house.bruto,
        bultos: house.bultos,
        volumen: house.cbm,
        origen: house.origen_e,
        destino: house.destino_e,
        consigna: dest,
        cliente: num_destina,
        embarca: getNameByIdClientes(house.embarcador_e),
        agente: getNameByIdClientes(house.agente_e),
        posicion: house.posicion_e,
        terminos: house.terminos,
        pagoflete: house.pago,
        commodity: house.producto_id,
        // 👉 mandamos los IDs seleccionados y válidos
        items_ids: idsSeleccionados
      };

      if (['EM', 'EA', 'ET'].includes(clase)) {
        const confirmacion = confirm(
          "¿Desea facturar gastos como 'Collect'?\n\nPresione ACEPTAR para 'Collect'\nPresione CANCELAR para 'Prepaid'"
        );
        tipoElegido = confirmacion ? 'Collect' : 'Prepaid';
      } else {
        tipoElegido = 'Collect';
      }

      guardar_preventa(preventa, tipoElegido);
      $('#facturar_modal').dialog('close');
      $('#' + tablaOrigen).DataTable().ajax.reload(null, false);
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
function guardar_preventa(preventa,tipo){
    $.ajax({
        type: "POST",
        url: "/admin_cont/preventa/",
        data: JSON.stringify({'preventa':preventa,'tipo':tipo}),
        contentType: "application/json",
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function(response) {
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
function sumar_ingresos_tabla() {
    let totalIngresos = 0;
    const tabla = $('#facturar_table').DataTable();

    // Verifica si DataTable está inicializado y tiene filas
    if (!$.fn.DataTable.isDataTable('#facturar_table') || tabla.rows().count() === 0) {
        console.log("DataTable no está inicializado o no tiene filas.");
        return;
    }

    // Obtiene los datos de las filas de la tabla
    const dataRows = tabla.rows().data();

    // Itera sobre cada fila y suma el valor de la columna 3 (índice 2)
    dataRows.each(function(data) {

        const valor = parseFloat(data[4]) // Elimina caracteres no numéricos si es necesario
        totalIngresos += valor;

    });

    // Asigna el resultado total al input con ID #total_ingresos
    $('#total_ingresos').val(totalIngresos.toFixed(2)); // Redondea a 2 decimales si es necesario
}

//orden factura
$('#orden_factura').click(function () {

        $("#pdf_add_input").html('');
        $('#pdf_add_input').summernote('destroy');
        let clase = getPathSegment();
        get_datos_pdf_ordenfac(clase);

            $("#pdf_modal").dialog({
                autoOpen: true,
                open: function (event, ui) {
                    $('#pdf_add_input').summernote('destroy');

                    $('#pdf_add_input').summernote({
                        placeholder: '',
                        title: 'Orden Factura',
                        tabsize: 10,
                        fontNames: ['Arial', 'Arial Black', 'Comic Sans MS', 'Courier New', 'Merriweather'],
                        height: wHeight * 0.90,
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
                },
                modal: true,
                title: "Orden factura embarque N°: " + localStorage.getItem('num_house_gasto'),
                height: wHeight * 0.90,
                width: wWidth * 0.90,
                class: 'modal fade',
                buttons: [
                    {
                        // text:"Imprimir",
                        html: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-printer" viewBox="0 0 16 16">\n' +
                            '  <path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/>\n' +
                            '  <path d="M5 1a2 2 0 0 0-2 2v2H2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v1a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1h1a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3a2 2 0 0 0-2-2H5zM4 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2H4V3zm1 5a2 2 0 0 0-2 2v1H2a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v-1a2 2 0 0 0-2-2H5zm7 2v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1z"/>\n' +
                            '</svg> Imprimir',
                        class: "btn btn-warning ",
                        style: "width:100px",
                        icons: {primary: "bi bi-star"},
                        click: function () {
                            imprimirPDFordenfac();
                        },
                    }, {
                        text: "Salir",
                        class: "btn btn-dark",
                        style: "width:100px",
                        click: function () {
                            $(this).dialog("close");
                        },
                    },
                ],
                beforeClose: function (event, ui) {
                    // table.ajax.reload();
                }
            })

    });

function get_datos_pdf_ordenfac(clase) {
    miurl = "/admin_cont/get_datos_ordenfactura/";
    var toData = {
        'numero': localStorage.getItem('num_house_gasto'),
        'clase':clase,
        'csrfmiddlewaretoken': csrf_token,
    };
    $.ajax({
        type: "POST",
        url: miurl,
        data: toData,
        async: false,
        success: function (resultado) {
            if (resultado['resultado'] === 'exito') {
                //     LLENAR DATOS
                $("#pdf_add_input").html(resultado['texto']);
            } else {
                alert(resultado['resultado']);
            }
        }
    });
}
function imprimirPDFordenfac() {
    var contenido = $('#pdf_add_input').summernote('code'); // Obtener el HTML del Summernote
    var ventanaImpresion = window.open('', '_blank'); // Crear una nueva ventana emergente

    // Escribir el HTML del Summernote en la ventana emergente
    ventanaImpresion.document.write('<html><head><title>Impresión</title>');
    ventanaImpresion.document.write('<style>');
    ventanaImpresion.document.write(`
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            line-height: 1.5;
            font-size:12px;
        }
        @media print {
            @page {
                size: portrait; /* Establece la orientación en vertical (portrait) */
                margin: 20mm;   /* Márgenes alrededor del contenido */
            }
            body {
                width: 100%;
                margin: 0;
                padding: 0;
            }
            .container {
                display: block;
                width: 100%;
                text-align: left;
            }
        }
        .container {
            margin: 20px; /* Margen interior para el contenido */
        }
        h1, h2 {
            text-align: center;
        }
        p {
            text-align: left;
        }
        hr {
            border: 1px solid #000;
        }
    `);
    ventanaImpresion.document.write('</style></head><body>');
    ventanaImpresion.document.write('<div class="container">'); // Aplicar un contenedor con estilo
    ventanaImpresion.document.write(contenido); // Insertar el contenido de Summernote
    ventanaImpresion.document.write('</div></body></html>');
    ventanaImpresion.document.close(); // Cerrar el flujo de escritura del documento

    // Esperar a que la nueva ventana se cargue completamente antes de imprimir
    ventanaImpresion.onload = function () {
        ventanaImpresion.focus(); // Asegurarse de que la ventana esté en foco
        ventanaImpresion.print(); // Iniciar la impresión
        ventanaImpresion.close(); // Cerrar la ventana después de la impresión
    };
}
function getPathSegment() {
    var currentUrl = window.location.href;  // Obtiene la URL completa
    var urlParts = currentUrl.split('/');  // Divide la URL por cada barra '/'

    var pathSegment = urlParts[3];  // Esto te dará 'importacion_aerea'
    return pathSegment;  // Devuelve el segmento deseado
}

//excel factura
$('#excel_factura').click(function () {
    let clase = getPathSegment();
    let miurl = "/admin_cont/datos_xls/"; // La URL de la vista que genera el archivo
    var toData = {
        'numero': localStorage.getItem('num_house_gasto'),
        'clase': clase,
        'csrfmiddlewaretoken': csrf_token,
        'total': $('#total_ingresos').val()
    };

    // Construir la URL con los parámetros para enviar al backend
    var params = new URLSearchParams(toData).toString();
    window.location.href = miurl + '?' + params; // Redirigir al navegador para descargar el archivo
});

// 👉 Ajustá este índice si tu columna "Facturar a.." cambia de posición
const COL_FACTURAR_A = 4; // (0-based) usando tu config actual

// Helper: ¿la fila está bloqueada por color?
function filaBloqueada($tr) {
  const clasesBloqueo = [
    'fila-rojo','fila-amarillo','fila-verde',
  ];
  return clasesBloqueo.some(cls => $tr.hasClass(cls));
}

// Asignar al seleccionado
function asignar_costo() {
    const tabla = $('#facturar_table').DataTable();
    const $filaSeleccionada = $('#facturar_table tbody tr.table-secondary');

    if (!$filaSeleccionada.length) {
        alert("No hay ninguna fila seleccionada.");
        return;
    }
    if (filaBloqueada($filaSeleccionada)) {
        // opcional: avisar
        // alert('La fila seleccionada no permite asignación.');
        return;
    }

    const cliente = $('#destinatario').val();
    const cliente_id = $('#destinatario_input').val();

    if (!cliente) {
        // opcional: avisar
        // alert('Debe seleccionar un destinatario.');
        return;
    }

    // Actualizar DataTables + DOM
    tabla.cell($filaSeleccionada, COL_FACTURAR_A).data(cliente).invalidate('dom');
    $filaSeleccionada.find('td').eq(COL_FACTURAR_A).text(cliente);
}

// Asignar a todos (solo filas no bloqueadas)
function asignar_costo_todos() {
    const tabla = $('#facturar_table').DataTable();
    const cliente = $('#destinatario').val();
    const cliente_id = $('#destinatario_input').val();

    if (!cliente) {
        // opcional: avisar
        // alert('Debe seleccionar un destinatario.');
        return;
    }
    tabla.rows().every(function () {
        const $tr = $(this.node());
        if (filaBloqueada($tr)) return; // saltar filas bloqueadas

        // si querés además saltar filas sin checkbox:
        if (!$tr.find('.fila-check').length) return;

        this.cell($tr, COL_FACTURAR_A).data(cliente).invalidate('dom');
        $tr.find('td').eq(COL_FACTURAR_A).text(cliente);
    });
}
