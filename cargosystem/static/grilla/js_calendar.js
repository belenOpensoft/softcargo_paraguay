document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    // Inicializar el calendario con FullCalendar
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'es',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: function(fetchInfo, successCallback, failureCallback) {
            // Llamada AJAX para obtener los eventos con los filtros aplicados
            $.ajax({
                url: '/importacion_maritima/eventos-calendario/',
                data: {
                    modo_filtro: $('#modo_filtro').val(),  // Filtrar por modo (aéreo, marítimo, etc.)
                    filtro_cliente: $('#filtro_cliente').val()  // Filtrar por consignatario
                },
                success: function(data) {
                    successCallback(data);  // Devolver los eventos al calendario
                },
                error: function() {
                    failureCallback();  // Manejar el error si ocurre
                }
            });
        },
        eventClick: function (info) {
            // Crear el contenido del modal con los datos del evento
            var modalContent = `
                <p><strong>Transportista:</strong> ${info.event.extendedProps.transportista}</p>
                <p><strong>Consignatario:</strong> ${info.event.extendedProps.consignatario}</p>
                <p><strong>AWB:</strong> ${info.event.extendedProps.awb}</p>
                <p><strong>HAWB:</strong> ${info.event.extendedProps.hawb}</p>
                <p><strong>Status:</strong> ${info.event.extendedProps.status}</p>
                <p><strong>Origen:</strong> ${info.event.extendedProps.origen}</p>
                <p><strong>Destino:</strong> ${info.event.extendedProps.destino}</p>
                <p><strong>Tipo:</strong> ${info.event.extendedProps.source_formatted}</p>
                <p><strong>Posición:</strong> ${info.event.extendedProps.posicion}</p>
            `;

            // Mostrar el contenido en un modal (usando jQuery UI)
            $("#modal-content").html(modalContent);
            $("#myModal").dialog({
                title: "Detalles del Evento",
                width: 400,
                modal: true
            });
        }
    });

    calendar.render();

    // Botón para cerrar el modal
    $("#close-modal-btn").click(function() {
        $("#myModal").dialog("close");
    });

    // Autocompletado del filtro de consignatario
    $("#filtro_cliente").autocomplete({
        source: '/autocomplete_clientes/',  // Ruta para obtener las sugerencias
        minLength: 2,
        select: function (event, ui) {
            $(this).attr('data-id', ui.item['id']);  // Guardar el id del consignatario seleccionado
        },
        change: function (event, ui) {
            if (!ui.item) {
                $(this).val('');
                $('#filtro_cliente').val('');  // Limpiar el input si no se selecciona una opción válida
            }
        }
    });

    // Evento para aplicar los filtros
    $('#filtrar_seguimientos').click(function() {
        calendar.refetchEvents();  // Recargar eventos con los filtros aplicados
    });

    // Evento para limpiar los filtros
    $('#limpiar_filtros').click(function() {
        $('#modo_filtro').val('');  // Limpiar el filtro de modo
        $('#filtro_cliente').val('');  // Limpiar el filtro de consignatario
        calendar.refetchEvents();  // Recargar los eventos sin filtros
    });

    $("#reporte_excel_filtrado").click(function () {
        var modoFiltro = $("#modo_filtro").val();
        var filtroCliente = $("#filtro_cliente").val();

        // Mostrar los filtros aplicados en el párrafo
        var filtrosTexto = [];
        if (modoFiltro) {
            filtrosTexto.push("Modo: " + ($("#modo_filtro option:selected").text()));
        }
        if (filtroCliente) {
            filtrosTexto.push("Consignatario: " + filtroCliente);
        }

        if (filtrosTexto.length > 0) {
            $("#que_filtra").text("El reporte mantendrá los filtros: " + filtrosTexto.join(", "));
            $("#que_filtra").show();
        } else {
            $("#que_filtra").hide();
        }

        $("#reporte").dialog({
            title: "Generar Reporte de Eventos",
            width: 400,
            modal: true,
            position: { my: "top", at: "top+50", of: window }  // Posiciona el modal en la parte superior, con un margen de 50px
        });

    });

    // Cerrar el modal
    $("#close-modal-btn_r").click(function() {
        $("#reporte").dialog("close");
    });

    // Cuando el usuario hace clic en "Descargar reporte"
    $("#reporte_fechas").click(function () {
        var desde = $("#desde_filtro").val();
        var hasta = $("#hasta_filtro").val();
        var modoFiltro = $("#modo_filtro").val();
        var filtroCliente = $("#filtro_cliente").val();

        if (desde && hasta) {
            // Redirigir para descargar el reporte con los filtros de fecha, modo y consignatario
            window.location.href = `/importacion_maritima/generar_reporte_excel/?desde=${desde}&hasta=${hasta}&modo_filtro=${modoFiltro}&filtro_cliente=${filtroCliente}`;
        } else {
            alert("Por favor, seleccione un rango de fechas.");
        }
    });

});


