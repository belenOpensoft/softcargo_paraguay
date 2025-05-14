
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


  $('#formFiltroAsientos').on('submit', function (e) {
    e.preventDefault();
$('#spinnerCarga').show();
    $.ajax({
      url: $(this).attr('action') || window.location.href,
      method: 'GET',
      data: $(this).serialize(),
      success: function (response) {
        const tbody = $('#tabla_asientos tbody');
        tbody.empty();

        if (response.resultados.length === 0) {
          tbody.append('<tr><td colspan="5" class="text-center">No hay resultados.</td></tr>');
          return;
        }

        response.resultados.forEach(function (item) {
        let haber = 0;
        let deber = 0;

        if(item.imputacion == 1){
            deber = item.monto;
        }else{
            haber = item.monto;
        }
          const row = `
            <tr>
              <td>${item.cuenta}</td>
              <td>${item.detalle}</td>
              <td>${deber}</td>
              <td>${haber}</td>
              <td>${item.tipo_cambio}</td>
              <td>${item.paridad}</td>
              <td>${item.posicion}</td>
              <td class="oculto">${item.moneda}</td>
              <td class="oculto">${item.asiento}</td>
              <td class="oculto">${item.fecha}</td>
              <td class="oculto">${item.nrocuenta}</td>
              <td class="oculto">${item.imputacion}</td>
              <td class="oculto">${item.id}</td>
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
  $("#modalEditarAsiento").dialog({
    autoOpen: false,
    modal: true,
    width:'auto',
    position: { my: "top", at: "top+70", of: window },
    buttons: [
      {
        text: "Imprimir",
        class: "btn btn-warning btn-sm",
        click: function () {
          const nro_asiento = $("#detalle_asiento").val();
          if (!nro_asiento) {
            alert("Debe especificar un número de asiento para imprimir.");
            return;
          }

          fetch(`/admin_cont/reimprimir_asiento/?asiento=${encodeURIComponent(nro_asiento)}`, {
            method: "GET",
            headers: {
              "X-CSRFToken": csrf_token
            }
          })
          .then(response => {
            const contentType = response.headers.get("Content-Type") || "";
            if (!contentType.includes("application/pdf")) {
              return response.text().then(text => {
                try {
                  const json = JSON.parse(text);
                  throw new Error(json.error || json.status || "Error desconocido del servidor.");
                } catch (e) {
                  throw new Error("Respuesta inválida del servidor: " + text);
                }
              });
            }
            return response.blob();
          })
          .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = "asiento_contable.pdf";
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
          })
          .catch(error => {
            alert("Error: " + error.message);
            console.error("Error en la petición:", error);
          });

          $(this).dialog("close");
        }
      },
      {
        text: "Guardar modificación",
        class: "btn btn-success btn-sm",
        click: function () {
        let editar=false;
        if(confirm('¿Desea editar todos los asientos para este numero? Cancelar= Editar solo el asiento en pantalla, Aceptar= Editar todos los asientos bajo este numero')){
        editar=true;
        }
        const data = {
            cuenta: $("#detalle_cuenta").val(),
            moneda: $("#detalle_moneda").val(),
            arbitraje: $("#detalle_arbitraje").val(),
            paridad: $("#detalle_paridad").val(),
            detalle: $("#detalle_detalle").val(),
            tipo: $("input[name='detalle_tipo']:checked").val(),
            monto: $("#detalle_monto").val(),
            posicion: $("#detalle_posicion").val(),
            asiento: $("#detalle_asiento").val(),
            id: $("#detalle_id").val(),
            editar: editar,
          };

          fetch("/admin_cont/guardar_asiento_editado/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrf_token
            },
            body: JSON.stringify(data)
          })
          .then(res => res.json())
          .then(res => {
            if (!res.success) {
              console.error("Error en backend:", res.error || res);
              alert("Hubo un error al guardar. "+res.error || res);
            } else {
              alert("Modificación guardada correctamente.");
              $("#modalEditarAsiento").dialog("close");
              $("#formEditarAsiento").trigger("reset");
            }
          })
          .catch(err => {
            console.error("Error en la petición:", err);
            alert("Error de conexión o de servidor.");
          });
          $(this).dialog("close");
        }
      },
      {
        text: "Eliminar",
        class: "btn btn-danger btn-sm",
        click: function () {
        let editar=false;
        if(confirm('¿Desea eliminar todos los asientos para este numero? Cancelar= Eliminar solo el asiento en pantalla, Aceptar= Eliminar todos los asientos bajo este numero')){
        editar=true;
        }
        const data = {
            asiento: $("#detalle_asiento").val(),
            id: $("#detalle_id").val(),
            editar: editar,
          };

          fetch("/admin_cont/eliminar_asiento/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrf_token
            },
            body: JSON.stringify(data)
          })
          .then(res => res.json())
          .then(res => {
            if (!res.success) {
              console.error("Error en backend:", res.error || res);
              alert("Hubo un error al guardar. "+res.error || res);
            } else {
              alert("Eliminado correctamente.");
              $("#modalEditarAsiento").dialog("close");
              $("#formEditarAsiento").trigger("reset");
            }
          })
          .catch(err => {
            console.error("Error en la petición:", err);
            alert("Error de conexión o de servidor.");
          });
          $(this).dialog("close");
        }
      },
      {
        text: "Salir",
        class: "btn btn-dark btn-sm",
        click: function () {
          $(this).dialog("close");
        }
      },
    ]
  });

  $('#tabla_asientos tbody').on('dblclick', 'tr', function () {
  const tds = $(this).find('td');

  $('#detalle_cuenta').val(tds.eq(10).text().trim());
  $('#detalle_detalle').val(tds.eq(1).text().trim());
  const debe = parseFloat(tds.eq(2).text().trim());
  const haber = parseFloat(tds.eq(3).text().trim());
  $('#detalle_monto').val(debe > 0 ? debe : haber);
  if (tds.eq(11).text().trim() == 1) {
    $('#id_tipo_0').prop('checked', true);  // debe
  } else {
    $('#id_tipo_1').prop('checked', true);  // haber
  }
  $('#detalle_moneda').val(tds.eq(7).text().trim());
  $('#detalle_posicion').val(tds.eq(6).text().trim());
  $('#detalle_paridad').val(tds.eq(5).text().trim());
  $('#detalle_arbitraje').val(tds.eq(4).text().trim());
  $('#detalle_asiento').val(tds.eq(8).text().trim());
  $('#detalle_fecha').val(tds.eq(9).text().trim());
  $('#detalle_id').val(tds.eq(12).text().trim());

  $("#modalEditarAsiento").dialog('open');
});

  });