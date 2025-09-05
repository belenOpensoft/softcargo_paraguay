$(function() {
    const table = $('#tbl-audit').DataTable({
      processing: true,
      serverSide: true,
      ajax: {
        url: "/admin_cont/source_logs_administracion/",
        type: "GET",
        data: function (d) {
          // Anexamos los filtros del formulario
          d.date_from = $('#id_date_from').val() || '';
          d.date_to   = $('#id_date_to').val()   || '';
          d.user      = $('#id_user').val()      || '';
        }
      },
      columns: [
        {
          data: null,
          orderable: false,
          className: 'text-center',
          defaultContent: '<button class="btn btn-sm btn-outline-primary btn-details">+</button>'
        },
        { data: "mautogen", title: "Factura" },
        { data: "tabla", title: "Tabla" },
        { data: "fecha", title: "Fecha" },
        { data: "usuario", title: "Usuario" }
      ],
      order: [[3, 'desc']],
      pageLength: 100,   // 👈 por defecto 100 filas
      lengthMenu: [[25, 50, 100, 250], [25, 50, 100, 250]], // 👈 menú de selección
        scrollY: '500px',   // alto fijo con scroll
  scrollCollapse: true,
  paging: true
    });

    // Toggle child row
    $('#tbl-audit tbody').on('click', 'button.btn-details', function() {
      let tr = $(this).closest('tr');
      let row = table.row(tr);

      if (row.child.isShown()) {
        row.child.hide();
        tr.removeClass('shown');
        $(this).text('+').removeClass('btn-outline-danger').addClass('btn-outline-primary');
      } else {
        let detalles = row.data().detalles || [];
        if (!detalles.length) {
          row.child('<em>No hay detalles</em>').show();
        } else {
          let html = '<table class="table table-sm table-bordered table-striped mb-0">';
          html += '<thead><tr><th>Tabla</th><th>Fecha</th><th>Usuario</th><th>Cambios</th></tr></thead><tbody>';
          detalles.forEach(d => {
            html += `<tr>
              <td>${d.tabla}</td>
              <td>${d.fecha}</td>
              <td>${d.usuario}</td>
              <td><pre class="mb-0 small">${d.cambios}</pre></td>
            </tr>`;
          });
          html += '</tbody></table>';
          row.child(html).show();
        }
        tr.addClass('shown');
        $(this).text('-').removeClass('btn-outline-primary').addClass('btn-outline-danger');
      }
    });

    // Filtros
    $('#filter-form').on('submit', function(e) { e.preventDefault(); table.ajax.reload(); });
    $('#btn-clear').on('click', function() {
      $('#id_date_from, #id_date_to, #id_user').val('');
      table.search('').draw();
      table.ajax.reload();
    });
  // Opcional: recargar al cambiar un filtro sin enviar el form
  $('#id_date_from, #id_date_to, #id_user').on('change', function() {
    table.ajax.reload(null, true);
  });

  $('#btn-excel').on('click', function () {
  const date_from = $('#id_date_from').val();
  const date_to   = $('#id_date_to').val();
  const user      = $('#id_user').val();

  if (!date_from && !date_to) {
    alert("Debes seleccionar al menos una fecha (desde o hasta).");
    return;
  }

  // Armamos la URL con parámetros GET
  const url = `/admin_cont/export_logs_administracion/?date_from=${encodeURIComponent(date_from)}&date_to=${encodeURIComponent(date_to)}&user=${encodeURIComponent(user)}`;

  // Forzamos la descarga
  window.location.href = url;
});

  });



