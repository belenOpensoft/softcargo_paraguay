 document.addEventListener("DOMContentLoaded", function () {
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

  $('#id_proveedor').autocomplete({
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
    appendTo: "#proveedoresModal",
    select: function(event, ui) {
        const codigo = ui.item.codigo;
        const nombre = ui.item.value;
        $('#id_proveedor').val(nombre);
        $('#id_proveedor_codigo').val(codigo);
    }
});
  $('#id_proveedor').on('input', function () {
      const valor = $(this).val().trim();
      if (valor === '') {
        $('#id_proveedor_codigo').val('');
      }
    });
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
  $('#consultaComprasForm').on('submit', function (e) {
    e.preventDefault();
        $('#spinnerCarga').show();

    $.ajax({
      url: $(this).attr('action') || window.location.href,
      method: 'GET',
      data: $(this).serialize(),
      success: function (response) {
        const tbody = $('#tabla_consultar_compras tbody');
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
              <td>${item.proveedor}</td>
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
  $(document).on('dblclick', '#tabla_consultar_compras tbody tr', function () {
    const autogenerado = $(this).find('td:nth-child(5)').text().trim();
    const numero = $(this).find('td:nth-child(6)').text().trim();
    const nrocliente = $(this).find('td:nth-child(7)').text().trim();
    $('#autogen_detalle_compra').val(autogenerado);
    buscar_gastos(autogenerado);
    buscar_ordenes(nrocliente,numero,autogenerado);
    cargarImputacionesCompra(autogenerado);
    // Mostrar el modal con jQuery UI
    $("#modalFacturaDetalle").dialog({
      modal: true,
      width: 'auto',
      height: 600,
    buttons: [
      {
        text: "Anular",
        style: "width:90px;",
        class: "btn btn-danger",
        click: function () {
        let autogen=$('#autogen_detalle_compra').val();
        anularFactura(autogen);
        }
      },
      {
        text: "Modificar",
        style: "width:90px;",
        class: "btn btn-primary",
        click: function () {
          guardarCambiosFormulario();
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
    //verificarEstadoImputaciones();
  });
  $("#tabla-impucompra tbody").on("click", "tr", function () {
    actualizarMonto();
});
  $("#btn-imputar").on("click", function () {
    let montoDisponible = parseFloat($("#monto-imputar").val()) || 0;
    let saldoRestante = montoDisponible;

    const imputacionesActuales = [];

    $("#tabla-impucompra tbody tr.table-secondary").each(function () {
        const idFactura = $(this).find("td:nth-child(1)").text().trim(); // Autogenerado
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

            // Mostrar el monto imputado en la tabla
            const celdaImputado = $(this).find("td:nth-child(7)");
            celdaImputado.text(montoImputado.toFixed(2));
            celdaImputado.css("background-color", "#fcec3f"); // amarillo

            // Actualizar el saldo visualmente
            $(this).find("td:nth-child(6)").text(saldoFactura.toFixed(2));

            // Guardar en array para debug/log
            imputacionesActuales.push({
                autofac: idFactura,
                monto_imputado: montoImputado.toFixed(2)
            });

            // Desmarcar la fila imputada
            $(this).removeClass("table-secondary");
        }
    });

    // Actualizar input y botón
    $("#monto-imputar").val(saldoRestante.toFixed(2));
    $("#btn-imputar").prop("disabled", saldoRestante === 0);

    // Lógica adicional si la necesitás
    actualizarImputado(); // si tenés esta función, mantenela

    let nro = $('#nro_prov').val();
    let autogen_compra=$('#autogen_detalle_compra').val();
    guardarImputacionesCompra(autogen_compra,nro,imputacionesActuales);
});
  $("#eliminarImputaciones").on("click", function () {
    const autogen_compra = $('#autogen_detalle_compra').val();
    const filaSeleccionada = $("#tablaImputaciones tr.table-secondary");

    if (filaSeleccionada.length > 0) {
        const autogeneradoFactura = filaSeleccionada.find("td:nth-child(1)").text().trim();
        console.log('autogencompra'+autogen_compra);
        console.log('autofac'+autogeneradoFactura);
        eliminarImputacionCompra(autogen_compra,autogeneradoFactura);
    }else{
        alert('Seleccione una fila.');
        return;
        }

});
    $("#tabla_items_compra tbody").on("dblclick", "td:nth-child(6)", function () {
    filaSeleccionada = $(this).closest("tr");
    let embarqueValor = $(this).text().trim();
    if (embarqueValor!=='NO IMPUTABLE'){
       cargarDatosEmbarque(embarqueValor);
    }
});
  //seccion para modal de embarque
  // Detectar doble clic en la celda de la columna "Embarque"
  $("#tabla_items_compra tbody").on("dblclick", "td:nth-child(5)", function () {
    filaSeleccionada = $(this).closest("tr");
    let embarqueValor = $(this).text().trim();
    if (embarqueValor!=='NO IMPUTABLE'){
        let precioValor = filaSeleccionada.find("td:nth-child(3)").text().trim();
        localStorage.setItem("precio_item_imputar", precioValor);
        $("#modal-embarque").dialog("open");
    }
});
  $("#modal-embarque").dialog({
        autoOpen: false,
        width: "auto",
        height: "auto",
        maxWidth: $(window).width() * 0.90,
        minWidth: 600,
        maxHeight: $(window).height() * 0.90,
        modal: true,
        position: { my: "center top", at: "center top+20", of: window },
        create: function () {
            var $buttons = $(this).parent().find(".ui-dialog-buttonpane button");
            $buttons.eq(0).addClass("btn btn-warning");
            $buttons.eq(1).addClass("btn btn-success");
            $buttons.eq(2).addClass("btn btn-dark");
        },
        buttons: {
            "Armar": function () {
                // Lógica para guardar los cambios
                let precio = parseFloat($("#seleccionado-precio").val()) || 0;
                let cliente = $("#seleccionado-cliente").val();
                let lugar = $("#seleccionado-lugar").val();
                let embarque = $("#seleccionado-embarque").text();
                let total = parseFloat(localStorage.getItem('precio_item_imputar')) || 0;

                if (precio>total){
                alert('El monto ingresado: ' +precio+', es mayor al original: '+total);
                return;
                }

                let nuevaFila = `
                    <tr>
                        <td>${posicion}</td>
                        <td>${precio}</td>
                        <td><button class="btn btn-danger btn-sm eliminar-fila">Eliminar</button></td>
                        <td style="display:none;">${cliente}</td>
                        <td style="display:none;">${lugar}</td>
                        <td style="display:none;">${embarque}</td>
                    </tr>
                `;
                $("#guardado-tabla tbody").append(nuevaFila);

                // Agregar evento para eliminar fila al botón generado dinámicamente
                $(".eliminar-fila").off("click").on("click", function () {
                    $(this).closest("tr").remove();
                });

                // Limpiar los valores seleccionados después de agregar la fila
                $("#seleccionado-posicion").text("");
                $("#seleccionado-embarque").text("");
                $("#seleccionado-precio").val("");
                $("#seleccionado-tipo").val("");
                //$(this).dialog("close");
            },
            "Guardar y Cerrar": function () {
                let total= localStorage.getItem('precio_item_imputar');
                let total_tabla = 0;
                let filas = document.querySelectorAll("#guardado-tabla tbody tr");
                if(filas.length==0){
                alert('No se ha armado nada.');
                return;
                }
                filas.forEach(fila => {
                    let montoCelda = fila.querySelector("td:nth-child(2)");

                    if (montoCelda) {
                        let monto = parseFloat(montoCelda.textContent.trim().replace(',', '.')) || 0;
                        total_tabla += monto;
                    }
                });
                if(total!=total_tabla){
                alert('Los montos armados: '+ total_tabla+', difieren del ingresado: '+total);
                return;
                }

                //guardar_impucompra();
                rellenar_tabla();
                $(this).dialog("close");
            },
            "Cancelar": function () {
                $(this).dialog("close");
            }
        },
        beforeClose: function(event, ui) {
        limpiarModalEmbarque();
    }
    }).prev('.ui-dialog-titlebar').remove();

    let table = document.querySelector("#tabla-embarque-container tbody");
    let selectedRow = null;

    table.addEventListener("click", function (event) {
        let row = event.target.closest("tr");
        if (!row) return;

        if (selectedRow) {
            selectedRow.classList.remove("table-secondary");
        }

        row.classList.add("table-secondary");
        selectedRow = row;
    });
    //rellenar seleccionados
    table.addEventListener("dblclick", function (event) {
        let row = event.target.closest("tr");
        if (!row) return;

        let embarque = row.cells[0].textContent.trim();
        let tipo = row.cells[1].textContent.trim();
        posicion = row.cells[3].textContent.trim();
        cliente = row.cells[9].textContent.trim();

        let selectedRadio = $('input[name="imputar"]:checked').attr('id');
        let impucompra_tipo;
        if(selectedRadio=='imputar-masters'){
            impucompra_tipo='M';
        }else{
            impucompra_tipo='H';
        }

        document.querySelector("#seleccionado-embarque").textContent = embarque;
        document.querySelector("#seleccionado-tipo").textContent = tipo === "CONSOLIDADO" ? "C" : "D";
        document.querySelector("#seleccionado-posicion").textContent = posicion;
        $("#seleccionado-cliente").val(cliente);
        $("#seleccionado-precio").val(localStorage.getItem('precio_item_imputar'));
        $("#seleccionado-lugar").val(impucompra_tipo);

    });
    //buscadores
    document.querySelectorAll(".buscador").forEach(button => {
        button.addEventListener("click", function () {
            let selectedRadio = $('input[name="imputar"]:checked').attr('id');
            let impucompra_tipo;
            if(selectedRadio=='imputar-masters'){
                impucompra_tipo='master';
            }else{
                impucompra_tipo='house';
            }
            let departamento = document.getElementById("departamento").value;
            if(departamento==''){
                alert('Seleccione una Operativa');
                return;
            }
            let fechaDesde = document.getElementById("fecha-desde")?.value || "";
            let fechaHasta = document.getElementById("fecha-hasta")?.value || "";
            let posicion = document.getElementById("posicion-input")?.value || "";
            let tipoEmbarque = document.querySelector('input[name="tipo-embarque"]:checked')?.value || "todos";
            let conocimiento = document.getElementById("contenedor-input")?.value || "";
            let transportista = document.getElementById("transportista-input")?.value || "";
            let agente = document.getElementById("agente-input")?.value || "";
            let status = document.getElementById("status-input")?.value || "";
            let contenedor = document.getElementById("contenedor-input")?.value || "";
            let vapor = document.getElementById("vapor-input")?.value || "";
            let seguimiento = document.getElementById("seguimiento-input")?.value || "";
            let master = document.getElementById("master-input")?.value || "";
            let house = document.getElementById("house-input")?.value || "";
            let embarque = document.getElementById("embarque-input-buscar")?.value || "";

            let params = new URLSearchParams({
                departamento: departamento,
                fecha_desde: fechaDesde,
                fecha_hasta: fechaHasta,
                posicion: posicion,
                tipo_embarque: tipoEmbarque,
                conocimiento: conocimiento,
                transportista: transportista,
                agente: agente,
                status: status,
                contenedor: contenedor,
                vapor: vapor,
                seguimiento: seguimiento,
                master: master,
                house: house,
                embarque:embarque,
                cual:impucompra_tipo
            });

            fetch(`/admin_cont/buscar_embarques/?${params}`)
                .then(response => response.json())
                .then(data => {
                    let tbody = document.querySelector("#tabla-embarque-container tbody");
                    tbody.innerHTML = "";  // Limpiar la tabla antes de cargar nuevos datos

                    data.resultados.forEach(item => {
                        let row = `<tr>
                            <td>${item.embarque}</td>
                            <td>${item.tipo}</td>
                            <td>${item.fecha}</td>
                            <td>${item.posicion}</td>
                            <td>${item.conocimiento}</td>
                            <td>${item.transportista}</td>
                            <td>${item.agente}</td>
                            <td>${item.tarifa}</td>
                            <td>${item.status}</td>
                            <td>${item.cliente}</td>
                        </tr>`;
                        tbody.innerHTML += row;
                    });
                })
                .catch(error => console.error("Error al buscar embarques:", error));
     });
     });

    $("#modal-embarque").tabs();

    let radioMasters = document.getElementById("imputar-masters");
    let radioHouses = document.getElementById("imputar-houses");

    radioMasters.addEventListener("change", actualizarPestañas);
    radioHouses.addEventListener("change", actualizarPestañas);

    actualizarPestañas();

    $(document).on('dblclick', '#tablaRecibos tr', function () {
    var autogenerado = $(this).find('td.oculto').first().text().trim();
    $('#formComprasDetallePago input[name="autogenerado"]').val(autogenerado);
    $('#modalComprasDetallePago').dialog({
      modal: true,
      width: 'auto',
      height: 'auto',
      resizable: false,
      position: { my: "center", at: "center", of: window },
      buttons: [
        {
          text: "Salir",
          class: "btn btn-dark",
          click: function () {
            $(this).dialog("close");
          }
        }
      ]
    });
    cargarDatosComprasDetallePago(autogenerado);
  });



  });

function rellenar_tabla() {
if (!filaSeleccionada || filaSeleccionada.length === 0) {
    alert("No se ha seleccionado ninguna fila para actualizar.");
    return;
}

let guardadoFilas = document.querySelectorAll("#guardado-tabla tbody tr");

if (guardadoFilas.length === 0) {
    alert("No hay registros en la tabla guardado-tabla.");
    return;
}

if (guardadoFilas.length === 1) {
    let fila = guardadoFilas[0];
    let posicion = fila.querySelector("td:nth-child(1)")?.textContent.trim() || "";
    let precio = fila.querySelector("td:nth-child(2)")?.textContent.trim() || "";
    let embarque = fila.querySelector("td:nth-child(6)")?.textContent.trim() || "";
    let lugar = fila.querySelector("td:nth-child(5)")?.textContent.trim() || "";
    let cliente = fila.querySelector("td:nth-child(4)")?.textContent.trim() || "";
    let embarqueFinal = embarque + lugar;

    filaSeleccionada.find("td").eq(5).text(posicion);
    filaSeleccionada.find("td").eq(4).text(embarqueFinal);

} else {
    let filaBase = filaSeleccionada.clone();

    filaSeleccionada.remove();

    guardadoFilas.forEach(fila => {
        let posicion = fila.querySelector("td:nth-child(1)")?.textContent.trim() || "";
        let precio = fila.querySelector("td:nth-child(2)")?.textContent.trim() || "";
        let embarque = fila.querySelector("td:nth-child(6)")?.textContent.trim() || "";
        let lugar = fila.querySelector("td:nth-child(5)")?.textContent.trim() || "";
        let cliente = fila.querySelector("td:nth-child(4)")?.textContent.trim() || "";
        let embarqueFinal = embarque + lugar;

        let nuevaFila = filaBase.clone();
        nuevaFila.find("td").eq(5).text(posicion);
        nuevaFila.find("td").eq(4).text(embarqueFinal);
        nuevaFila.find("td").eq(2).text(precio);

        $("#tabla_items_compra tbody").append(nuevaFila);
    });
}

// Cerramos el modal
$("#modal-embarque").dialog("close");

}
function actualizarPestañas() {
    let radioMasters = document.getElementById("imputar-masters");
    let radioHouses = document.getElementById("imputar-houses");
    let tabMaster = document.querySelector('a[href="#master"]').parentElement;
    let tabHouse = document.querySelector('a[href="#house"]').parentElement;

    // Mostrar todas las pestañas antes de aplicar restricciones
    tabMaster.style.display = "block";
    tabHouse.style.display = "block";

    if (radioMasters.checked) {
        tabMaster.style.display = "none"; // Ocultar Master
        tabHouse.style.display = "none"; // Ocultar Master
    } else if (radioHouses.checked) {
        tabHouse.style.display = "none"; // Ocultar House
    }
}
function buscar_ordenes(cliente,numero,autogenerado){

        if (!cliente || !numero || !autogenerado) {
            alert('Faltan datos');
            return;
        }

        $.ajax({
            url: '/admin_cont/buscar_ordenes_por_boleta/',  // Cambia esto por tu URL real
            type: 'GET',
            data: {
                cliente: cliente,
                numero: numero,
                autogenerado: autogenerado
            },
            success: function(response) {
                let tbody = $('#tabla_pago_factura tbody');
                tbody.empty();

                if (response.resultados.length === 0) {
                    tbody.append('<tr><td colspan="4">No se encontraron resultados</td></tr>');
                } else {
                    $.each(response.resultados, function(i, orden) {
                        let row = `
                            <tr>
                                <td class="oculto">${orden.autogenerado}</td>
                                <td>${orden.nro_documento}</td>
                                <td>${orden.fecha}</td>
                                <td>${orden.monto}</td>
                                <td>${orden.tipo}</td>
                            </tr>
                        `;
                        tbody.append(row);
                    });
                }
            },
            error: function(xhr) {
                console.error(xhr.responseText);
                alert('Error al buscar órdenes');
            }
        });
}
function buscar_gastos(autogenerado){
    $.ajax({
      url: '/admin_cont/detalle_compra/',
      method: 'GET',
      data: {
        autogenerado: autogenerado
      },
      success: function(response) {
        if (response.success) {
          const data = response.data;
          $('#id_prefijo').val(data.prefijo);
          $('#id_serie').val(data.serie);
          $('#numero_detalle_compra').val(data.numero);
          $('#id_tipo').val(data.tipo);
          $('#id_moneda_detalle_compra').val(data.moneda);
          $('#id_fecha_detalle_compra').val(data.fecha);
          $('#id_fecha_ingreso').val(data.fecha_ingreso);
          $('#id_fecha_vencimiento').val(data.fecha_vencimiento);
          $('#id_proveedor_detalle').val(data.proveedor);
          $('#nro_prov').val(data.nroproveedor);
          $('#id_detalle_detalle_compra').val(data.detalle);

        $('#id_paridad_detalle_compra').val(parseFloat(data.paridad || 0).toFixed(2));
        $('#id_arbitraje_detalle_compra').val(parseFloat(data.arbitraje || 0).toFixed(2));
        $('#id_total').val(parseFloat(data.total || 0).toFixed(2));
        $('#id_imputable').val(parseFloat(data.imputable || 0).toFixed(2));


            if (data.items && data.items.length > 0) {
              $('#tablaItems').empty();

              data.items.forEach(function(item) {
                const fila = `
                  <tr>
                    <td>${item.concepto || ''}</td>
                    <td>${item.nombre || ''}</td>
                    <td class="text-right">${item.precio != null ? parseFloat(item.precio).toFixed(2) : ''}</td>
                    <td class="text-right">${item.iva != null ? parseFloat(item.iva).toFixed(2) : ''}</td>
                    <td>${item.embarque || ''}</td>
                    <td>${item.posicion || ''}</td>
                  </tr>
                `;
                $('#tablaItems').append(fila);
              });
            } else {
              // Si no hay items, opcionalmente podés mostrar una fila vacía o un mensaje
              $('#tablaItems').html('<tr><td colspan="6" class="text-center text-muted">Sin ítems asociados.</td></tr>');
            }


        }
      },
      error: function(xhr) {
        alert("No se pudo obtener el detalle de la compra.");
      }
    });
}
function limpiarModalEmbarque() {
    // Limpiar todos los inputs (texto, número, fecha) y selects dentro del modal
    $("#modal-embarque").find("input[type='text'], input[type='number'], input[type='date'], textarea").val("");
    $("#modal-embarque").find("select").prop("selectedIndex", 0);

    // Desmarcar todos los radio buttons
    $("#modal-embarque").find("input[type='radio']").prop("checked", false);

    // Limpiar los spans y campos ocultos de la sección de "Seleccionado"
    $("#seleccionado-embarque").text("");
    $("#seleccionado-tipo").text("");
    $("#seleccionado-posicion").text("");
    $("#seleccionado-precio").val("0.00");
    $("#seleccionado-cliente").val("");
    $("#seleccionado-lugar").val("");

    // Limpiar la tabla de información lateral
    $("#guardado-tabla tbody").empty();

    // Limpiar la tabla de embarques (dentro de #tabla-embarque-container)
    $("#tabla-embarque-container table tbody").empty();
}
function cargarDatosComprasDetallePago(autogenerado) {
    $.ajax({
      url: '/admin_cont/obtener_detalle_pago/',  // Ajustalo según tu ruta
      type: 'GET',
      data: {
        autogenerado: autogenerado
      },
      success: function(response) {
        // Cargar los campos del formulario con los datos recibidos
        $('#formComprasDetallePago input[name="numero"]').val(response.numero);
        $('#formComprasDetallePago select[name="moneda"]').val(response.moneda);
        $('#formComprasDetallePago input[name="fecha"]').val(response.fecha);
        $('#formComprasDetallePago input[name="arbitraje"]').val(response.arbitraje);
        $('#formComprasDetallePago input[name="importe"]').val(response.importe);
        $('#formComprasDetallePago input[name="por_imputar"]').val(response.por_imputar);
        $('#formComprasDetallePago input[name="paridad"]').val(response.paridad);
        $('#formComprasDetallePago input[name="proveedor"]').val(response.proveedor);
        $('#formComprasDetallePago input[name="detalle"]').val(response.detalle);
        $('#formComprasDetallePago input[name="autogenerado"]').val(autogenerado);

        $('#tablaChequesMovimiento').empty();
        if (response.cheques && response.cheques.length > 0) {
          response.cheques.forEach(function (cheque) {
            const fila = `
              <tr>
                <td>${cheque.fecha}</td>
                <td>${cheque.banco}</td>
                <td>${cheque.numero}</td>
                <td>${cheque.moneda}</td>
                <td>${cheque.monto}</td>
                <td>${cheque.vencimiento}</td>
              </tr>
            `;
            $('#tablaChequesMovimiento').append(fila);
          });
        }else{
             $('#tablaChequesMovimiento').append('<tr><td colspan="5" class="text-center">No hay resultados.</td></tr>');
        }

        cargarDocumentosImputadosDesdeDetalle(response.detalle);
      },
      error: function() {
        alert('Error al cargar los datos del pago.');
      }
    });
  }
function cargarDocumentosImputadosDesdeDetalle(detalleStr) {
  if (!detalleStr) return;

  const boletas = detalleStr.split(';').map(b => b.trim()).filter(b => b !== '');

  if (boletas.length === 0) return;

  const datos = {
    boletas: boletas
  };

$.ajax({
  url: '/admin_cont/obtener_imputados_orden_compra/',
  type: 'POST',
  data: JSON.stringify(datos),
  contentType: 'application/json',
  headers: {
    'X-CSRFToken': csrf_token
  },
  success: function (response) {
    const tbody = $('#tablaDocumentosImputados');
    tbody.empty(); // Limpiar contenido anterior
    if(response.boletas.length==0){
        tbody.append('<tr><td colspan="5" class="text-center">No hay resultados.</td></tr>');
    return;
    }
    response.boletas.forEach(function (b) {
      const fila = `
        <tr>
          <td>${b.documento}</td>
          <td>${b.imputado}</td>
          <td>${b.moneda}</td>
          <td>${b.detalle}</td>
        </tr>`;
      tbody.append(fila);
    });
    //agregar la comprobacion de si no hay nada
  },
  error: function () {
    alert('Error al cargar las boletas imputadas.');
  }
});
}
function cargarImputacionesCompra_old(autogen) {
    fetch('/admin_cont/obtener_imputados_compra/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({ autogen: autogen })
    })
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('tablaImputaciones');
        tbody.innerHTML = '';  // Limpiar tabla antes de cargar

        if (data.documentos && data.documentos.length > 0) {
            data.documentos.forEach(doc => {
                const fila = document.createElement('tr');

                fila.innerHTML = `
                    <td class="oculto">${doc.autogenerado}</td>
                    <td>${doc.documento}</td>
                    <td>${doc.imputado}</td>
                `;

                tbody.appendChild(fila);
            });
        } else {
            const fila = document.createElement('tr');
            fila.innerHTML = `<td colspan="3" class="text-center">No se encontraron imputaciones.</td>`;
            tbody.appendChild(fila);
        }
    })
    .catch(error => {
        console.error('Error al cargar imputaciones:', error);
    });
}
function cargarImputacionesCompra(autogen) {
    $.ajax({
        url: '/admin_cont/obtener_imputados_compra/',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ autogen: autogen }),
        headers: {
            'X-CSRFToken': csrf_token  // Asegurate que esta variable exista
        },
        success: function (data) {
            const tbody = document.getElementById('tablaImputaciones');
            tbody.innerHTML = '';  // Limpiar tabla

            if (data.documentos && data.documentos.length > 0) {
                data.documentos.forEach(function (doc) {
                    const fila = document.createElement('tr');
                    fila.innerHTML = `
                        <td class="oculto">${doc.autogenerado}</td>
                        <td>${doc.documento}</td>
                        <td>${doc.imputado}</td>
                    `;
                    tbody.appendChild(fila);
                });
            } else {
                const fila = document.createElement('tr');
                fila.innerHTML = `<td colspan="3" class="text-center">No se encontraron imputaciones.</td>`;
                tbody.appendChild(fila);
            }
        },
        error: function (xhr, status, error) {
            console.error('Error al cargar imputaciones:', error);
        }
    });
}

function abrir_impucompra(){
    let nro = $('#nro_prov').val();
    $("#impucompra_nota").dialog('open');
    const filas = document.querySelectorAll('#tablaImputaciones tr');
    let total= $('#id_total').val();
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
function verificarEstadoImputaciones() {
    const filas = document.querySelectorAll('#tablaImputaciones tr');
    const totalElemento = document.getElementById('id_total');
    const btnRealizar = document.getElementById('realizarImputaciones');
    const btnEliminar = document.getElementById('eliminarImputaciones');

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

    const totalEsperado = parseFloat(totalElemento.value.replace(',', '.'));

    if (filas.length > 0) {
        btnEliminar.disabled = false;
    } else {
        btnEliminar.disabled = true;
    }

    if (Math.abs(sumaImputado - totalEsperado) < 0.01) {
        btnRealizar.disabled = false;
    } else {
        btnRealizar.disabled = true;
    }
}
function cargar_facturas_imputacion(nrocliente) {
    $.ajax({
        url: "/admin_cont/cargar_pendientes_imputacion/",
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
function guardarImputacionesCompra(autogen, cliente, facturasImputadas) {
  fetch('/admin_cont/procesar_imputaciones_compra/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrf_token
    },
    body: JSON.stringify({
      accion: 'guardar',
      autogen: autogen,
      cliente: cliente,
      facturas: facturasImputadas
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert("Imputaciones guardadas correctamente");
      cargarImputacionesCompra(autogen);
      $("#impucompra_nota").dialog('close');
    } else {
      alert("Error al guardar imputaciones:", data.error);
    }
  })
  .catch(error => {
    console.error("Error en la solicitud:", error);
  });
}
function eliminarImputacionCompra(autogen, autofac) {
  fetch('/admin_cont/procesar_imputaciones_compra/', {
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
      cargarImputacionesCompra(autogen);
    } else {
      alert("Error al eliminar imputación:", data.error);
    }
  })
  .catch(error => {
    console.error("Error en la solicitud:", error);
  });
}
function guardarCambiosFormulario_old() {
    const camposModificados = document.querySelectorAll(".bg-warning");
    const datos = {};

    // Obtener autogenerado y tipo (de inputs ocultos o lo que uses)
    const autogen = document.getElementById("autogen_detalle_compra").value;
    const tipo = document.getElementById("id_tipo").value;

    // Validación mínima
    if (!autogen || !tipo) {
        console.error("Faltan autogenerado o tipo.");
        return;
    }

    datos["autogen"] = autogen;
    datos["tipo"] = tipo;

    camposModificados.forEach(campo => {
        const name = campo.name;
        const value = campo.value;
        if (name) {
            datos[name] = value;
        }
    });

    fetch("/admin_cont/modificar_compra/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token  // si usás CSRF
        },
        body: JSON.stringify(datos)
    })
    .then(res => res.json())
    .then(response => {
        if (response.success) {
            alert("Cambios guardados correctamente.");
            $("#modalFacturaDetalle").dialog('close');
        } else {
            alert("Error al guardar: " + response.error);
        }
    })
    .catch(err => {
        console.error("Error al guardar cambios:", err);
    });
}
function guardarCambiosFormulario() {
    const camposModificados = document.querySelectorAll(".bg-warning");
    const datos = {};

    const autogen = document.getElementById("autogen_detalle_compra").value;
    const tipo = document.getElementById("id_tipo").value;

    if (!autogen || !tipo) {
        console.error("Faltan autogenerado o tipo.");
        return;
    }

    datos["autogen"] = autogen;
    datos["tipo"] = tipo;

    camposModificados.forEach(campo => {
        const name = campo.name;
        const value = campo.value;
        if (name) {
            datos[name] = value;
        }
    });

    // 🔄 Recolectar datos de la tabla directamente con nth-child
    const posiciones = [];
    document.querySelectorAll("#tabla_items_compra tbody tr").forEach(fila => {
        const nroserv = fila.querySelector("td:nth-child(1)")?.textContent.trim();
        const posicionCelda = fila.querySelector("td:nth-child(6)");

        if (nroserv && posicionCelda) {
            const input = posicionCelda.querySelector("input");
            const nuevaPos = input ? input.value.trim() : posicionCelda.textContent.trim();

            posiciones.push({
                nroserv: nroserv,
                nueva_posicion: nuevaPos
            });
        }
    });

    if (posiciones.length > 0) {
        datos["posiciones"] = posiciones;
    }

    fetch("/admin_cont/modificar_compra/", {
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
            $("#modalFacturaDetalle").dialog('close');
        } else {
            alert("Error al guardar: " + response.error);
        }
    })
    .catch(err => {
        console.error("Error al guardar cambios:", err);
    });
}

function anularFactura(autogen) {
    if (!autogen) {
        alert("No se ha proporcionado el autogenerado.");
        return;
    }

    if (!confirm("¿Estás seguro de que deseas anular esta factura? Esta acción no se puede deshacer.")) {
        return;
    }

    fetch('/admin_cont/anular_compra/', {
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
            alert("Factura anulada correctamente.");
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
function cargarDatosEmbarque(posicion) {
    $.ajax({
        url: '/admin_cont/detalle_conocimiento/',
        method: 'GET',
        data: { posicion: posicion },
        traditional: true,
        success: function (response) {
            if (response.resultados) {
                const datos = response.resultados[0];

                if (datos.success) {
                    const form = datos.formulario;

                    $("#id_cliente").val(form.cliente);
                    $("#id_embarcador").val(form.embarcador);
                    $("#id_consignatario").val(form.consignatario);
                    $("#id_agente").val(form.agente);
                    $("#id_transportista").val(form.transportista);
                    $("#id_vapor_vuelo").val(form.vapor_vuelo);
                    $("#id_etd_eta").val(form.etd_eta);
                    $("#id_embarque").val(form.embarque);
                    $("#id_posicion").val(form.posicion);
                    $("#id_mbl").val(form.mbl);
                    $("#id_hbl").val(form.hbl);
                    $("#id_origen").val(form.origen);
                    $("#id_destino").val(form.destino);

                    // Servicios
                    let htmlServicios = '';
                    if (datos.servicios.length > 0) {
                        datos.servicios.forEach(serv => {
                            htmlServicios += `
                                <tr>
                                    <td>${serv.servicio}</td>
                                    <td>${serv.moneda}</td>
                                    <td>${serv.precio}</td>
                                    <td>${serv.costo}</td>
                                </tr>`;
                        });
                    } else {
                        htmlServicios = `<tr><td colspan="4" class="text-center">No hay datos disponibles</td></tr>`;
                    }
                    console.log(htmlServicios);
                    $("#tablaServicios").html(htmlServicios);

                    // Productos
                    let htmlProductos = '';
                    if (datos.productos.length > 0) {
                        datos.productos.forEach(prod => {
                            htmlProductos += `
                                <tr>
                                    <td>${prod.producto__nombre}</td>
                                    <td>${prod.bultos}</td>
                                    <td>${prod.bruto}</td>
                                </tr>`;
                        });
                    } else {
                        htmlProductos = `<tr><td colspan="3" class="text-center">No hay datos disponibles</td></tr>`;
                    }
                    $("#tablaProductos").html(htmlProductos);

                    // Envases
                    let htmlEnvases = '';
                    if (datos.envases && datos.envases.length > 0) {
                        datos.envases.forEach(env => {
                            htmlEnvases += `
                                <tr>
                                    <td>${env.unidad}</td>
                                    <td>${env.tipo}</td>
                                    <td>${env.movimiento}</td>
                                    <td>${env.termino}</td>
                                    <td>${env.cantidad}</td>
                                    <td>${env.precio}</td>
                                    <td>${env.costo}</td>
                                    <td>${env.nrocontenedor}</td>
                                </tr>`;
                        });
                    } else {
                        htmlEnvases = `<tr><td colspan="8" class="text-center">No hay datos disponibles</td></tr>`;
                    }
                    $("#tablaEnvases").html(htmlEnvases);

                    // Mostrar modal
                    $("#modalDetalleEmbarque").dialog({
                        autoOpen: true,
                        modal: true,
                        width: 'auto',
                        position: { my: "top", at: "center", of: window },
                        title: 'Conocimiento: ' + posicion,
                        buttons: [
                            {
                                text: "Salir",
                                class: "btn btn-dark",
                                click: function () {
                                    $(this).dialog("close");
                                }
                            }
                        ]
                    });

                } else {
                    alert("Error: " + datos.error);
                }
            }
        },
        error: function () {
            alert("Error al consultar los datos del embarque.");
        }
    });
}



