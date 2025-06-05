var wWidth = $(window).width();
var wHeight = $(window).height();

document.addEventListener("DOMContentLoaded", function () {
   $("#impucompra_nota").dialog({
        autoOpen: false,
        resizable: false,
        draggable: true,
        width: "auto",
        height: "auto",
        maxWidth: $(window).width() * 0.90,
        minWidth: 600,
        maxHeight: $(window).height() * 0.90,
        modal: true,
        position: { my: "center", at: "center", of: window },
        open: function () {
            resetModal("#impucompra_nota");
            $(this).dialog("option", "width", "auto");
            $(this).dialog("option", "height", "auto");
            $(this).dialog("option", "position", { my: "center", at: "center", of: window });
        },
         buttons: [
        {
            class: "btn btn-dark btn-sm",
            text: "Cerrar",
            click: function() {
                $(this).dialog("close");
            }
        }
    ],
    });
    const omitirFechas = document.getElementById("id_omitir_fechas");
    const fechaDesde = document.getElementById("id_fecha_desde");
    const fechaHasta = document.getElementById("id_fecha_hasta");

    function toggleFechas() {
      const disabled = omitirFechas.checked;
      fechaDesde.disabled = disabled;
      fechaHasta.disabled = disabled;
    }

    // Ejecutar al cargar
    toggleFechas();

    // Escuchar cambios
    omitirFechas.addEventListener("change", toggleFechas);


    $('#id_cliente').autocomplete({
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
        $('#id_cliente').val(nombre);
        $('#id_cliente_codigo').val(codigo);
    }
    });
    $('#id_cliente').on('input', function () {
      const valor = $(this).val().trim();
      if (valor === '') {
        $('#id_cliente_codigo').val('');
      }
    });

  $('#consultaCobranzasForm').on('submit', function (e) {
    e.preventDefault();
        $('#spinnerCarga').show();

    $.ajax({
      url: $(this).attr('action') || window.location.href,
      method: 'GET',
      data: $(this).serialize(),
      success: function (response) {
        const tbody = $('#tabla_consultar_cobranzas tbody');
        tbody.empty();

        if (response.resultados.length === 0) {
          tbody.append('<tr><td colspan="5" class="text-center">No hay resultados.</td></tr>');
          return;
        }

        response.resultados.forEach(function (item) {
          const row = `
            <tr>
              <td>${item.documento}</td>
              <td>${item.fecha}</td>
              <td>${item.cliente}</td>
              <td>${item.importe.toFixed(2)}</td>
              <td class="oculto">${item.autogenerado}</td>
              <td class="oculto">${item.numero}</td>
              <td class="oculto">${item.nrocliente}</td>
            </tr>`;
          tbody.append(row);
        });
        $('#spinnerCarga').hide();

      },
      error: function () {
        alert('Hubo un error al consultar los datos.');
      }
    });
  });
  $('table tbody').on('click', 'tr', function () {
    $('table tbody tr').removeClass('table-secondary');
    $(this).toggleClass('table-secondary');
  });

$(document).on('dblclick', '#tabla_consultar_cobranzas tbody tr', function () {
    const autogenerado = $(this).find('td:nth-child(5)').text().trim();
    const numero = $(this).find('td:nth-child(6)').text().trim();
    const nrocliente = $(this).find('td:nth-child(7)').text().trim();
    $("#modalCobranzaDetalle").dialog({
      modal: true,
      width: 'auto',
      height: 'auto',
    buttons: [
      {
        text: "Anular",
        style: "width:90px;",
        class: "btn btn-danger",
        click: function () {
        let autogen=$('#autogen_detalle_cobranza').val();
            anularCobranza(autogen);
        }
      },
      {
        text: "Modificar",
        style: "width:90px;",
        class: "btn btn-primary",
        click: function () {
          guardarCambiosCobranza();
        }
      },
      {
        text: "Salir",
        class: "btn btn-secondary",
        style: "width:90px;",
        click: function () {
          $(this).dialog("close");
        }
      }
    ],
    });
    $('#autogen_detalle_cobranza').val(autogenerado);
    buscar_detalle(autogenerado);
    //buscar_ordenes(nrocliente,numero,autogenerado);
    // Mostrar el modal con jQuery UI

    //verificarEstadoImputaciones();
  });

  $("#tabla-impucompra tbody").on("click", "tr", function () {
    actualizarMonto();
});
$("#btn-imputar").on("click", function () {
    let montoDisponible = parseFloat($("#monto-imputar").val()) || 0;
    let saldoRestante = montoDisponible;
    let totalAImputar = 0;
    const imputacionesActuales = [];

    // Calcular cuánto se quiere imputar (de las filas seleccionadas)
    $("#tabla-impucompra tbody tr.table-secondary").each(function () {
        let saldoFactura = parseFloat($(this).find("td:nth-child(6)").text().replace(",", ".")) || 0;
        if (saldoFactura > 0 && saldoRestante > 0) {
            totalAImputar += Math.min(saldoRestante, saldoFactura);
            saldoRestante -= Math.min(saldoRestante, saldoFactura);
        }
    });

    // Verificación: ¿se quiere imputar más de lo disponible?
    if (totalAImputar > montoDisponible) {
        alert("El monto a imputar supera el monto disponible.");
        return; // Detener ejecución
    }

    // Si hay diferencia entre lo que se puede y lo que se quiere imputar → guardar en localStorage
    if (totalAImputar < montoDisponible) {
        const nuevoSaldo = (montoDisponible - totalAImputar).toFixed(2);
        localStorage.setItem("nuevo_saldo", nuevoSaldo);
    }

    // Reiniciamos saldo restante para imputación real
    saldoRestante = montoDisponible;

    // Ejecutar imputación visual y lógica
    $("#tabla-impucompra tbody tr.table-secondary").each(function () {
        const idFactura = $(this).find("td:nth-child(1)").text().trim();
        let saldoFactura = parseFloat($(this).find("td:nth-child(6)").text().replace(",", ".")) || 0;
        let montoImputado = 0;

        if (saldoRestante > 0 && saldoFactura > 0) {
            if (saldoRestante >= saldoFactura) {
                montoImputado = saldoFactura;
                saldoRestante -= saldoFactura;
                saldoFactura = 0;
            } else {
                montoImputado = saldoRestante;
                saldoFactura -= saldoRestante;
                saldoRestante = 0;
            }

            $(this).find("td:nth-child(7)").text(montoImputado.toFixed(2)).css("background-color", "#fcec3f");
            $(this).find("td:nth-child(6)").text(saldoFactura.toFixed(2));

            imputacionesActuales.push({
                autofac: idFactura,
                monto_imputado: montoImputado.toFixed(2)
            });

            $(this).removeClass("table-secondary");
        }
    });

    $("#monto-imputar").val(saldoRestante.toFixed(2));
    $("#btn-imputar").prop("disabled", saldoRestante === 0);

    actualizarImputado();

    const nro = $('#nro_cliente_detalle_cobranza').val();
    const autogen_compra = $('#autogen_detalle_cobranza').val();
    let nuevoSaldo = localStorage.getItem("nuevo_saldo");
    nuevoSaldo = nuevoSaldo ? parseFloat(nuevoSaldo) : null;
    $('#por_imputar_detalle_cobranza').val(nuevoSaldo);
    guardarImputacionesCobranza(autogen_compra, nro, imputacionesActuales, nuevoSaldo);
});

$("#eliminarImputaciones").on("click", function () {
    const autogen_compra = $('#autogen_detalle_cobranza').val();
    const filaSeleccionada = $("#tablaDocumentosImputados tr.table-secondary");

    if (filaSeleccionada.length > 0) {
        const autogeneradoFactura = filaSeleccionada.find("td:nth-child(1)").text().trim();
        console.log('autogencompra'+autogen_compra);
        console.log('autofac'+autogeneradoFactura);
        eliminarImputacionCobranza(autogen_compra,autogeneradoFactura);
    }else{
        alert('Seleccione una fila.');
        return;
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
    success: function(response) {
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
        $('#id_importe').val(data.total || 0);
        $('#nro_cliente_detalle_cobranza').val(data.nrocliente);
        $('#cliente_detalle_cobranza').val(data.cliente);

        $('#efectivo_recibido').val(data.efectivo || '');
        $('#transferencia_recibida').val(data.transferencia || '');
        $('#deposito_recibido').val(data.deposito || '');

        $('#tablaChequesRecibidos').empty();
        if (data.cheques && data.cheques.length > 0) {
          data.cheques.forEach(function(cheque) {
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
          data.imputados.forEach(function(doc) {
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
    error: function(xhr) {
      alert("No se pudo obtener el detalle de la cobranza.");
    }
  });
}

function abrir_impucompra(){
    let nro = $('#nro_cliente_detalle_cobranza').val();
    $("#impucompra_nota").dialog('open');
    const filas = document.querySelectorAll('#tablaImputaciones tr');
    let total= $('#por_imputar_detalle_cobranza').val();
    let sumaImputado = 0;

    filas.forEach(fila => {
        const celdaImputado = fila.cells[2];
        if (celdaImputado) {
            const valor = parseFloat(celdaImputado.textContent.replace(',', '.'));
            if (!isNaN(valor)) {
                sumaImputado += valor;
            }
        }
    });
    let monto = parseFloat(total)-sumaImputado;
    $('#monto-imputar').val(monto);
    //localStorage.removeItem('facturas_impucompra');
    cargar_facturas_imputacion(nro);
}

function cargar_facturas_imputacion(nrocliente) {
    $.ajax({
        url: "/admin_cont/cargar_pendientes_imputacion_cobranza/",
        type: "GET",
        data: { nrocliente: nrocliente },
        success: function (response) {
            let tbody = $("#tabla-impucompra tbody");
            tbody.empty();

            if(response.data.length==0){
              $('#tabla-impucompra tbody').html('<tr><td colspan="8" class="text-center text-muted">No hay facturas disponibles para este proveedor.</td></tr>');

            }

            response.data.forEach(item => {
                let fila = `
                    <tr data-id="${item.autogenerado}">
                        <td style="display: none;">${item.autogenerado}</td>
                        <td>${item.vto}</td>
                        <td>${item.emision}</td>
                        <td>${item.num_completo}</td>
                        <td>${item.total.toFixed(2)}</td>
                        <td>${item.saldo.toFixed(2)}</td>
                        <td>${item.imputado.toFixed(2)}</td>
                        <td>${item.tipo_cambio.toFixed(2)}</td>
                        <td>${item.detalle}</td>
                    </tr>
                `;
                tbody.append(fila);
            });
        },
        error: function (xhr) {
            alert("Error al cargar las facturas: " + xhr.responseJSON.error);
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
function actualizarMonto() {
        let total = 0;
        $("#tabla-impucompra tbody tr.table-secondary").each(function () {
            let monto = parseFloat($(this).find("td:nth-child(6)").text().replace(",", ".")) || 0;
            total += monto;
        });

        $("#se-imputaran").val(total.toFixed(2));
        console.log(total);
        $("#btn-imputar").prop("disabled", total === 0);
    }
function actualizarImputado() {
        let totalImputado = 0;

        // Recorre solo las filas que tienen un imputado mayor a 0
        $("#tabla-impucompra tbody tr").each(function () {
            let celdaImputado = $(this).find("td:nth-child(7)");
            let monto = parseFloat(celdaImputado.text().replace(",", ".")) || 0;

            if (monto > 0) {
                totalImputado += monto;
                celdaImputado.css("background-color", "#fcec3f"); // Mantener el color amarillo
            }
        });

        // Actualiza el input `#se-imputaran` con el total imputado
        $("#se-imputaran").val(totalImputado.toFixed(2));
    }
function guardarImputacionesCobranza(autogen, cliente, facturasImputadas,saldo) {
  fetch('/admin_cont/procesar_imputaciones_cobranza/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token
    },
    body: JSON.stringify({
      accion: 'guardar',
      autogen: autogen,
      cliente: cliente,
      facturas: facturasImputadas,
      saldo:saldo
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert("Imputaciones guardadas correctamente");
        buscar_detalle(autogen);
      $("#impucompra_nota").dialog('close');
    } else {
      alert("Error al guardar imputaciones:", data.error);
    }
  })
  .catch(error => {
    console.error("Error en la solicitud:", error);
  });
}
function eliminarImputacionCobranza(autogen, autofac) {
  fetch('/admin_cont/procesar_imputaciones_cobranza/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token
    },
    body: JSON.stringify({
      accion: 'eliminar',
      autogen: autogen,
      autofac: autofac
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert("Imputación eliminada correctamente");
      buscar_detalle(autogen);
    } else {
      alert("Error al eliminar imputación:", data.error);
    }
  })
  .catch(error => {
    console.error("Error en la solicitud:", error);
  });
}

// JS: guardar cambios en detalle de cobranza
function guardarCambiosCobranza() {
    const camposModificados = document.querySelectorAll(".bg-warning");
    const datos = {};

    const autogen = document.getElementById("autogen_detalle_cobranza").value;

    if (!autogen) {
        console.error("Faltan autogenerado.");
        return;
    }

    datos["autogen"] = autogen;

    camposModificados.forEach(campo => {
        const name = campo.name || campo.id;
        const value = campo.value;
        if (name) {
            datos[name.replace("id_", "")] = value;
        }
    });


    fetch("/admin_cont/actualizar_cobranza/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        },
        body: JSON.stringify(datos)
    })
    .then(res => res.json())
    .then(response => {
        if (response.success) {
            alert("Cambios guardados correctamente.");
            $("#modalCobranzaDetalle").dialog('close');
        } else {
            alert("Error al guardar: " + response.error);
        }
    })
    .catch(err => {
        console.error("Error al guardar cambios:", err);
    });
}
function anularCobranza(autogen) {
    if (!autogen) {
        alert("No se ha proporcionado el autogenerado.");
        return;
    }

    if (!confirm("¿Estás seguro de que deseas anular esta cobranza? Esta acción no se puede deshacer.")) {
        return;
    }

    fetch('/admin_cont/anular_cobranza/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrf_token
        },
        body: JSON.stringify({ autogen: autogen })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Cobranza anulada correctamente.");
            console.log("Eliminados:", data.eliminados);
        } else {
            alert("Error al anular: " + data.error);
        }
    })
    .catch(err => {
        console.error("Error en la solicitud:", err);
        alert("Error al conectar con el servidor.");
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
                // table.ajax.reload();
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
            } else {
                alert('Error: ' + resultado['detalle']);
            }
        }
    });
}
