$(function() {
    const table = $('#tbl-audit-historico').DataTable({
      processing: true,
      serverSide: true,
      ajax: {
        url: "/admin_cont/source_logs_administracion_historico/",
        type: "GET",
        data: function (d) {
          // Anexamos los filtros del formulario
          d.date_from = $('#id_date_from').val() || '';
          d.date_to   = $('#id_date_to').val()   || '';
          d.user      = $('#id_user').val()      || '';
          d.modulo      = $('#id_modulo').val()      || '';
          d.accion      = $('#id_accion').val()      || '';
        }
      },
      columns: [
        { data: "detalle_col", title: "Detalle" },
        { data: "modulo_col", title: "Modulo" },
      {
        data: "fecha",
        title: "Fecha",
        render: function (data, type, row) {
          if (!data) return "";
          let d = new Date(data);
          let day = String(d.getDate()).padStart(2, '0');
          let month = String(d.getMonth() + 1).padStart(2, '0');
          let year = d.getFullYear();
          return `${day}/${month}/${year}`;  // formato d/m/Y
        }
      },
        { data: "nomusuario_col", title: "Usuario" },
        { data: "clave_col", title: "Accion" }
      ],
      order: [[3, 'desc']],
      pageLength: 100,   // 👈 por defecto 100 filas
      lengthMenu: [[25, 50, 100, 250], [25, 50, 100, 250]], // 👈 menú de selección
      scrollY: '500px',   // alto fijo con scroll
      scrollCollapse: true,
      paging: true,

    });


    // Filtros
    $('#filter-form').on('submit', function(e) { e.preventDefault(); table.ajax.reload(); });
    $('#btn-clear').on('click', function() {
      $('#id_date_from, #id_date_to, #id_user').val('');
      table.search('').draw();
      table.ajax.reload();
    });
  $('#id_date_from, #id_date_to, #id_user,#id_modulo,#id_accion').on('change', function() {
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



