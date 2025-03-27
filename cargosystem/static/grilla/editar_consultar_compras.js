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

  $('#consultaComprasForm').on('submit', function (e) {
    e.preventDefault();

    $.ajax({
      url: $(this).attr('action') || window.location.href,
      method: 'GET',
      data: $(this).serialize(),
      success: function (response) {
        const tbody = $('table tbody');
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
            </tr>`;
          tbody.append(row);
        });
      },
      error: function () {
        alert('Hubo un error al consultar los datos.');
      }
    });
  });

  });

