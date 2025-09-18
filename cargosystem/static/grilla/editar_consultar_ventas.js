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

  $('#consultaVentasForm').on('submit', function (e) {
    e.preventDefault();
        $('#spinnerCarga').show();

    $.ajax({
      url: $(this).attr('action') || window.location.href,
      method: 'GET',
      data: $(this).serialize(),
      success: function (response) {
        const tbody = $('#tabla_consultar_ventas tbody');
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
  $(document).on('dblclick', '#tabla_consultar_ventas tbody tr', function () {
    const autogenerado = $(this).find('td:nth-child(5)').text().trim();
    const numero = $(this).find('td:nth-child(6)').text().trim();
    const nrocliente = $(this).find('td:nth-child(7)').text().trim();
    $('#autogen_detalle_venta').val(autogenerado);
    buscar_gastos(autogenerado);
    buscar_ordenes(nrocliente,numero,autogenerado);
    // Mostrar el modal con jQuery UI
    $("#modalFacturaDetalle").dialog({
      modal: true,
      width: 'auto',
      height: 600,
    buttons: [
      {
        text: "Modificar",
        style: "width:90px;",
        class: "btn btn-primary",
        click: function () {
          guardarCambiosFormularioVenta();
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

  $(document).on('dblclick', '#tablaRecibos tr', function () {
    var autogenerado = $(this).find('td.oculto').first().text().trim();
    $('#formVentasDetallePago input[name="autogenerado"]').val(autogenerado);
    $('#modalVentasDetallePago').dialog({
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
    $("#tabla_items_venta tbody").on("dblclick", "td:nth-child(6)", function () {
    filaSeleccionada = $(this).closest("tr");
    let embarqueValor = $(this).text().trim();
    if (embarqueValor!=='NO IMPUTABLE'){
       cargarDatosEmbarque(embarqueValor);
    }
});
 //seccion para modal de embarque
  // Detectar doble clic en la celda de la columna "Embarque"
  $("#tabla_items_venta tbody").on("dblclick", "td:nth-child(5)", function () {
    filaSeleccionada = $(this).closest("tr");
    let embarqueValor = $(this).text().trim();
    if (embarqueValor!=='NO IMPUTABLE'){
        let precioValor = filaSeleccionada.find("td:nth-child(3)").text().trim();
        localStorage.setItem("precio_item_imputar", precioValor);
        $("#modal-embarque").dialog("open");
    }
});
      // Inicialización del modal de embarque
    $("#modal-embarque").dialog({
        autoOpen: false,
        modal: true,
        width: "auto",
        height: "auto",
        maxWidth: $(window).width() * 0.90,
        minWidth: 600,
        maxHeight: $(window).height() * 0.90,
        position: { my: "center top", at: "center top+20", of: window },
        buttons: [
            {
    text: "Armar",
    class: "btn btn-warning",
    click: function () {
        if (!selectedRow) {
            alert("Debe seleccionar un embarque.");
            return;
        }

        const embarque = selectedRow.cells[0].textContent.trim();
        const tipo = selectedRow.cells[1].textContent.trim();
        const posicion = selectedRow.cells[3].textContent.trim();
        const cliente = selectedRow.cells[9].textContent.trim();
        const lugar = $("#seleccionado-lugar").val();  // ya cargado en doble click

        const precio = parseFloat($("#seleccionado-precio").val()) || 0;
        const total = parseFloat(localStorage.getItem('precio_item_imputar')) || 0;

        if (precio > total) {
            alert('El monto ingresado: ' + precio + ', es mayor al original: ' + total);
            return;
        }

        // Limpiar tabla de armado si ya existía
        $("#guardado-tabla tbody").empty();

        // Crear la nueva fila
        const nuevaFila = `
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

        // Marcar como embarque armado
        embarqueSeleccionado = embarque;
        embarqueArmado = true;

        // Habilitar botón guardar si está deshabilitado
        $("#btnGuardarEmbarque").prop("disabled", false);

        // Activar botón eliminar
        $(".eliminar-fila").off("click").on("click", function () {
            $(this).closest("tr").remove();
            embarqueArmado = false;
            embarqueSeleccionado = null;
            $("#btnGuardarEmbarque").prop("disabled", true);
        });

        // Limpiar campos seleccionados
        $("#seleccionado-posicion").text("");
        $("#seleccionado-embarque").text("");
        $("#seleccionado-precio").val("");
        $("#seleccionado-tipo").val("");
    }
},

            {
                text: "Seleccionar datos y modificar",
                class: "btn btn-primary",
                click: function() {
                     if (!embarqueArmado || !embarqueSeleccionado) {
                        alert("Debe armar el embarque antes de guardar.");
                        return;
                    }

                    const posicion = selectedRow.cells[3].textContent.trim();  // o donde corresponda

                    $.ajax({
                        url: "/admin_cont/get_datos_embarque/",
                        method: "POST",
                        headers: { 'X-CSRFToken': csrf_token },
                        data: { posicion: posicion },
                        success: function (response) {
                        let autogenerado = $('#autogen_detalle_venta').val();
                        modificar_embarque_imputado(autogenerado,response);
                        },
                        error: function () {
                            alert("Error al cargar los datos del embarque.");
                        }
                    });
                }
            },
            {
                text: "Salir",
                class: "btn btn-dark",
                click: function() {
                    $(this).dialog("close");
                }
            }
        ],
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

    });


function buscar_gastos(autogenerado){
    $.ajax({
      url: '/admin_cont/detalle_venta/',
      method: 'GET',
      data: {
        autogenerado: autogenerado
      },
      success: function(response) {
        if (response.success) {
          const data = response.data;
          $('#id_prefijo').val(data.prefijo);
          $('#id_serie').val(data.serie);
          $('#numero_detalle_venta').val(data.numero);
          $('#id_tipo').val(data.tipo);
          $('#id_moneda_detalle_venta').val(data.moneda);
          $('#id_fecha_detalle_venta').val(data.fecha);
          $('#id_fecha_ingreso').val(data.fecha_ingreso);
          $('#id_fecha_vencimiento').val(data.fecha_vencimiento);
          $('#id_cliente_detalle').val(data.cliente);
          $('#nro_cli').val(data.nrocliente);
          $('#id_detalle_detalle_venta').val(data.detalle);

        $('#id_paridad_detalle_venta').val(parseFloat(data.paridad || 0).toFixed(2));
        $('#id_arbitraje_detalle_venta').val(parseFloat(data.arbitraje || 0).toFixed(2));
        $('#id_total').val(parseFloat(data.total || 0).toFixed(2));
        $('#id_posicion_venta').val(data.posicion);
        $('#id_observaciones').val(data.observaciones);
        $('#id_cae').val(data.cae);


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
        alert("No se pudo obtener el detalle de la venta.");
      }
    });
}
function buscar_ordenes(cliente,numero,autogenerado){

        if (!cliente || !numero || !autogenerado) {
            alert('Faltan datos');
            return;
        }

        $.ajax({
            url: '/admin_cont/buscar_ordenes_por_boleta_ventas/',  // Cambia esto por tu URL real
            type: 'GET',
            data: {
                cliente: cliente,
                numero: numero,
                autogenerado: autogenerado,
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
function cargarDatosComprasDetallePago(autogenerado) {
    $.ajax({
      url: '/admin_cont/obtener_detalle_pago_ventas/',  // Ajustalo según tu ruta
      type: 'GET',
      data: {
        autogenerado: autogenerado
      },
      success: function(response) {
        // Cargar los campos del formulario con los datos recibidos
        $('#formVentasDetallePago input[name="numero"]').val(response.numero);
        $('#formVentasDetallePago select[name="moneda"]').val(response.moneda);
        $('#formVentasDetallePago input[name="fecha"]').val(response.fecha);
        $('#formVentasDetallePago input[name="arbitraje"]').val(response.arbitraje);
        $('#formVentasDetallePago input[name="importe"]').val(response.importe);
        $('#formVentasDetallePago input[name="por_imputar"]').val(response.por_imputar);
        $('#formVentasDetallePago input[name="paridad"]').val(response.paridad);
        $('#formVentasDetallePago input[name="cliente"]').val(response.cliente);
        $('#formVentasDetallePago input[name="detalle"]').val(response.detalle);
        $('#formVentasDetallePago input[name="autogenerado"]').val(autogenerado);
        $('#formVentasDetallePago input[name="efectivo_recibido"]').val(response.efectivo_recibido);
        $('#formVentasDetallePago input[name="status"]').val(response.status);

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
  url: '/admin_cont/obtener_imputados_orden_venta/',
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
function modificar_embarque_imputado(autogenerado, datos) {
    fetch('/admin_cont/modificar_embarque_imputado/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({
            autogenerado: autogenerado,
            datos: datos
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Respuesta del servidor:", data);
        if(data.success){
        alert('Embarque modificado correctamente');
        $("#modal-embarque").dialog('close');
        $("#modalFacturaDetalle").dialog('close');
        limpiarModalEmbarque();
        }else{
        alert('Ocurrió un error');
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
function guardarCambiosFormularioVenta() {
    const camposModificados = document.querySelectorAll(".bg-warning");
    const datos = {};

    const autogen = document.getElementById("autogen_detalle_venta").value;
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
    document.querySelectorAll("#tabla_items_venta tbody tr").forEach(fila => {
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

    fetch("/admin_cont/modificar_venta/", {
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
