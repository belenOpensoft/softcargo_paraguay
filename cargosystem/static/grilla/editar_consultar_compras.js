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

  $('#consultaComprasForm').on('submit', function (e) {
    e.preventDefault();

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
    buscar_gastos(autogenerado);
    buscar_ordenes(nrocliente,numero);
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
          console.log("Acción: Anular factura");
          // Agregá tu lógica de anulación aquí
        }
      },
      {
        text: "Modificar",
        style: "width:90px;",
        class: "btn btn-warning",
        click: function () {
          console.log("Acción: Modificar factura");
          // Agregá tu lógica de modificación aquí
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
console.log(filaSeleccionada);
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
function buscar_ordenes(cliente,numero){

        if (!cliente || !numero) {
            alert('Faltan datos');
            return;
        }

        $.ajax({
            url: '/admin_cont/buscar_ordenes_por_boleta/',  // Cambia esto por tu URL real
            type: 'GET',
            data: {
                cliente: cliente,
                numero: numero
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
          $('#id_numero').val(data.numero);
          $('#id_tipo').val(data.tipo);
          $('#id_moneda').val(data.moneda);
          $('#id_fecha').val(data.fecha);
          $('#id_fecha_ingreso').val(data.fecha_ingreso);
          $('#id_fecha_vencimiento').val(data.fecha_vencimiento);
          $('#id_proveedor_detalle').val(data.proveedor);
          $('#id_detalle').val(data.detalle);

        $('#id_paridad').val(parseFloat(data.paridad || 0).toFixed(2));
        $('#id_arbitraje').val(parseFloat(data.arbitraje || 0).toFixed(2));
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