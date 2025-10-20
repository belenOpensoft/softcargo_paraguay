
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
        $('#spinnerCarga').hide();
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
              <td class="oculto">${item.autogenerado}</td>
            </tr>`;
          tbody.append(row);

        });
        $('#spinnerCarga').hide();
      },
      error: function () {
        $('#spinnerCarga').hide();
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
          const autogenerado = $("#detalle_asiento_autogen").val();
          if (!autogenerado) {
            alert("Debe especificar un número de asiento para imprimir.");
            return;
          }

          fetch(`/admin_cont/reimprimir_asiento/?autogenerado=${encodeURIComponent(autogenerado)}`, {
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

  const r = {
    id:        tds.eq(12).text().trim(),
    autogenerado: tds.eq(13).text().trim(),
    asiento:   tds.eq(8).text().trim(),
    cuenta:    tds.eq(10).text().trim(),
    detalle:   tds.eq(1).text().trim(),
    // reconstruimos debe/haber y tipo desde las columnas de la grilla
    debe:      parseFloat(tds.eq(2).text().trim()) || 0,
    haber:     parseFloat(tds.eq(3).text().trim()) || 0,
    tipo:      (tds.eq(11).text().trim() == '1') ? 'D' : 'H',
    moneda:    tds.eq(7).text().trim(),
    posicion:  tds.eq(6).text().trim(),
    paridad:   tds.eq(5).text().trim(),
    arbitraje: tds.eq(4).text().trim(),
    fecha:     tds.eq(9).text().trim()
  };

  setDetalleAsientoFromObj(r);
  $('#detalle_asiento_autogen').val(r.autogenerado);

  // Cargar los otros del mismo autogenerado
  if (r.autogenerado) {
    cargarAsientosRelacionados(r.autogenerado, r.id);
  }

  $("#modalEditarAsiento").dialog('open');
});

  });

// function cargarAsientosRelacionados(autogenerado, excludeId) {
//   const $tbody = $('#tabla_asientos_rel_body');
//   $tbody.empty().append(
//     `<tr><td colspan="11" class="text-center">Cargando...</td></tr>`
//   );
//
//   $.getJSON('/admin_cont/asientos_relacionados/', { autogenerado, exclude_id: excludeId })
//     .done(function(resp){
//       const filas = (resp && resp.data) ? resp.data : [];
//       $tbody.empty();
//
//       if (!filas.length) {
//         $tbody.append(`<tr><td colspan="11" class="text-center">No hay otros asientos con este autogenerado.</td></tr>`);
//         return;
//       }
//
//       for (const r of filas) {
//         const fecha = (r.fecha || '').toString().substring(0,10); // YYYY-MM-DD
//         const debe  = (typeof r.debe  === 'number') ? r.debe.toFixed(2)  : (r.debe  ?? '');
//         const haber = (typeof r.haber === 'number') ? r.haber.toFixed(2) : (r.haber ?? '');
//
//         const tr = `
//           <tr>
//             <td>${fecha}</td>
//             <td>${r.asiento ?? ''}</td>
//             <td>${r.cuenta_nombre ?? r.cuenta ?? ''}</td>
//             <td>${r.detalle ?? ''}</td>
//             <td class="text-end">${debe}</td>
//             <td class="text-end">${haber}</td>
//             <td>${r.moneda ?? ''}</td>
//             <td>${r.posicion ?? ''}</td>
//             <td>${r.paridad ?? ''}</td>
//             <td>${r.arbitraje ?? ''}</td>
//             <td>${r.tipo ?? ''}</td>
//           </tr>`;
//         $tbody.append(tr);
//       }
//     })
//     .fail(function(){
//       $tbody.empty().append(
//         `<tr><td colspan="11" class="text-center text-danger">Error cargando relacionados.</td></tr>`
//       );
//     });
// }
function num(val) {
  const n = parseFloat(val);
  return isNaN(n) ? 0 : n;
}

function setDetalleAsientoFromObj(r) {
  // r viene del JSON de relacionados o armado desde la fila principal
  $('#detalle_cuenta').val((r.cuenta ?? '').toString().trim());
  $('#detalle_detalle').val((r.detalle ?? '').toString().trim());

  const debe  = num(r.debe);
  const haber = num(r.haber);
  $('#detalle_monto').val(debe > 0 ? debe : haber);

  // tipo: 'D' o 'H'
  if ((r.tipo ?? '').toString().toUpperCase() === 'D') {
    $('#id_tipo_0').prop('checked', true);
  } else {
    $('#id_tipo_1').prop('checked', true);
  }

  $('#detalle_moneda').val((r.moneda ?? '').toString().trim());
  $('#detalle_posicion').val((r.posicion ?? '').toString().trim());
  $('#detalle_paridad').val((r.paridad ?? '').toString().trim());
  $('#detalle_arbitraje').val((r.arbitraje ?? '').toString().trim());
  $('#detalle_asiento').val((r.asiento ?? '').toString().trim());

  const fecha = (r.fecha ?? '').toString().trim();
  $('#detalle_fecha').val(fecha.includes('T') ? fecha.split('T')[0] : fecha);

  $('#detalle_id').val((r.id ?? '').toString().trim());
}
function cargarAsientosRelacionados(autogenerado, excludeId) {
  const $tbody = $('#tabla_asientos_rel_body');
  $tbody.empty().append(
    `<tr><td colspan="11" class="text-center">Cargando...</td></tr>`
  );

  $.getJSON('/admin_cont/asientos_relacionados/', { autogenerado, exclude_id: excludeId })
    .done(function(resp){
      const filas = (resp && resp.data) ? resp.data : [];
      $tbody.empty();

      if (!filas.length) {
        $tbody.append(`<tr><td colspan="11" class="text-center">No hay otros asientos con este autogenerado.</td></tr>`);
        return;
      }

      for (const r of filas) {
        const fecha = (r.fecha || '').toString().substring(0,10);
        const debe  = (typeof r.debe  === 'number') ? r.debe.toFixed(2)  : (r.debe  ?? '');
        const haber = (typeof r.haber === 'number') ? r.haber.toFixed(2) : (r.haber ?? '');

        const tr = $(`
          <tr
            data-id="${r.id ?? ''}"
            data-autogenerado="${r.autogenerado ?? ''}"
            data-asiento="${r.asiento ?? ''}"
            data-cuenta="${r.cuenta ?? ''}"
            data-detalle="${(r.detalle ?? '').toString().replace(/"/g,'&quot;')}"
            data-debe="${r.debe ?? 0}"
            data-haber="${r.haber ?? 0}"
            data-moneda="${r.moneda ?? ''}"
            data-posicion="${r.posicion ?? ''}"
            data-paridad="${r.paridad ?? ''}"
            data-arbitraje="${r.arbitraje ?? ''}"
            data-tipo="${r.tipo ?? ''}"
            data-fecha="${r.fecha ?? ''}"
          >
            <td>${fecha}</td>
            <td>${r.asiento ?? ''}</td>
            <td>${r.cuenta_nombre ?? r.cuenta ?? ''}</td>
            <td>${r.detalle ?? ''}</td>
            <td class="text-end">${debe}</td>
            <td class="text-end">${haber}</td>
            <td>${r.moneda ?? ''}</td>
            <td>${r.posicion ?? ''}</td>
            <td>${r.paridad ?? ''}</td>
            <td>${r.arbitraje ?? ''}</td>
            <td>${r.tipo ?? ''}</td>
          </tr>
        `);
        $tbody.append(tr);
      }
    })
    .fail(function(){
      $tbody.empty().append(
        `<tr><td colspan="11" class="text-center text-danger">Error cargando relacionados.</td></tr>`
      );
    });
}

// Delegado: click en una fila relacionada
$('#tabla_asientos_rel_body').on('dblclick', 'tr', function() {
  const $tr = $(this);
  const r = {
    id: $tr.data('id'),
    autogenerado: $tr.data('autogenerado'),
    asiento: $tr.data('asiento'),
    cuenta: $tr.data('cuenta'),
    detalle: $tr.data('detalle'),
    debe: $tr.data('debe'),
    haber: $tr.data('haber'),
    moneda: $tr.data('moneda'),
    posicion: $tr.data('posicion'),
    paridad: $tr.data('paridad'),
    arbitraje: $tr.data('arbitraje'),
    tipo: $tr.data('tipo'),
    fecha: $tr.data('fecha')
  };

  // Cargar el formulario con ese asiento
  setDetalleAsientoFromObj(r);

  // Volver a cargar “los otros” del mismo autogenerado, excluyendo ahora este id
  const nuevoAuto = (r.autogenerado ?? '').toString().trim();
  const nuevoId   = (r.id ?? '').toString().trim();
  if (nuevoAuto) {
    cargarAsientosRelacionados(nuevoAuto, nuevoId);
  }
});


