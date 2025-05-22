$(document).ready(function () {
    // Inicializar DataTable
    const table = $('#preview-table').DataTable();

    // Hacer sortable la lista
    $("#sortable-columns").sortable({
        update: function () {
            reorderSelected();
        }
    });

    // Asegurar que las columnas seleccionadas siempre estén arriba
    function reorderSelected() {
        const sortableList = $('#sortable-columns');
        const selectedItems = sortableList.find('li').filter(function () {
            return $(this).find('input[type="checkbox"]').is(':checked');
        }).addClass('selected');
        const unselectedItems = sortableList.find('li').filter(function () {
            return !$(this).find('input[type="checkbox"]').is(':checked');
        }).removeClass('selected');

        // Agregar los seleccionados al principio
        sortableList.append(selectedItems);
        sortableList.append(unselectedItems);
    }

    // Escuchar cambios en los checkboxes
    $('#sortable-columns').on('change', 'input[type="checkbox"]', function () {
        reorderSelected();
    });

    // Evento para generar el reporte
    $('#generate-report').on('click', function () {
        const selectedColumns = [];
        const columnOrder = [];

        // Obtener columnas seleccionadas y su orden
        $('#sortable-columns li').each(function () {
            const checkbox = $(this).find('input[type="checkbox"]');
            const columnName = $(this).data('column');
            const columnLabel = $(this).text().trim();

            if (checkbox.is(':checked')) {
                selectedColumns.push(columnName);
                columnOrder.push(columnLabel);
            }
        });

        if (selectedColumns.length === 0) {
            alert('Por favor, selecciona al menos una columna.');
            return;
        }

        // Simular generación de reporte (puedes reemplazarlo con lógica para exportar a XLS)
        alert(`Generando reporte con las columnas: ${columnOrder.join(', ')}`);
    });

    // Inicializar el orden inicial
    reorderSelected();

     // Inicializa el modal "Guardar Preferencia"
    $("#guardar-preferencia-modal").dialog({
        autoOpen: false,
        modal: true,
        width: 400,
        resizable: false
    });

    // Inicializa el modal "Cargar Preferencia"
    $("#cargar-preferencia-modal").dialog({
        autoOpen: false,
        modal: true,
        width: 600,
        resizable: false
    });

    // Acción para el botón "Guardar Seleccion" en el modal de guardar preferencia
    $("#btn-guardar-seleccion").click(function() {
        var nombre = $("#nombre-preferencia").val();
        if (nombre.trim() === "") {
            alert("Debes ingresar un nombre para la preferencia.");
            return;
        }

        const selectedColumns = [];
        $("#sortable-columns li").each(function () {
            const checkbox = $(this).find("input[type='checkbox']");
            if (checkbox.is(":checked")) {
                selectedColumns.push($(this).data("valor"));
            }
        });

        $.ajax({
            type: "POST",
            url: "/guardar_preferencia/",
            data: {
                nombre: nombre,
                selected_columns: JSON.stringify(selectedColumns)
            },
            headers: {
                'X-CSRFToken': csrf_token
            },
            success: function(response) {
                console.log("Preferencia guardada:", response);
                $("#guardar-preferencia-modal").dialog("close");
            },
            error: function(xhr, status, error) {
                console.error("Error al guardar la preferencia:", error);
            }
        });

        $("#guardar-preferencia-modal").dialog("close");
    });

    $("#tabla-preferencias").on("click", ".seleccionar-preferencia", function() {
        var $row = $(this).closest("tr");
        var prefId = $row.data("preferencia-id");

        var selectedColumnsStr = $row.find("td").eq(4).text().trim();


        var selectedArray = selectedColumnsStr.split(",").map(function(item) {
            return item.trim();
        });

        $("#sortable-columns li").each(function() {
            var dataValor = $(this).data("valor");
            if (selectedArray.includes(dataValor)) {
                $(this).find("input[type='checkbox']").prop("checked", true);
                $(this).addClass("selected");
            } else {
                $(this).find("input[type='checkbox']").prop("checked", false);
                $(this).removeClass("selected");
            }
        });

        reorderSelected();
        $("#cargar-preferencia-modal").dialog("close");
    });

    // Acción opcional para cerrar el modal de cargar preferencia
    $("#btn-cerrar-cargar-preferencia").click(function() {
        $("#cargar-preferencia-modal").dialog("close");
    });

    $("#btn-cerrar-guardar-preferencia").click(function() {
        $("#guardar-preferencia-modal").dialog("close");
    });

    $("#tabla-preferencias").on("click", ".eliminar-preferencia", function() {
        var $row = $(this).closest("tr");
        var prefId = $row.data("preferencia-id");

        if (confirm("¿Estás seguro de eliminar esta preferencia?")) {
            $.ajax({
                url: "/eliminar_preferencia/",
                type: "POST",
                data: { id: prefId },
                headers: {
                    'X-CSRFToken': csrf_token
                },
                success: function(response) {
                    if (response.success) {
                        $row.remove();
                    } else {
                        alert("Error al eliminar la preferencia: " + response.error);
                    }
                },
                error: function(xhr, status, error) {
                    alert("Error al eliminar la preferencia.");
                }
            });
        }
    });



});

function modal_columnas() {
    $("#config-modal").dialog({
        autoOpen: true,
        modal: true,
        width: 600,
        position: {
            my: "center top", // Centrar horizontalmente y posicionar desde la parte superior
            at: "center top", // Agregar desplazamiento de 20px desde la parte superior
            of: window // Referencia a la ventana del navegador
        },
        buttons: [
         {
            class: "btn btn-primary btn-sm",
            text: "Generar Reporte",
            click: function () {
                triggerFormSubmit();
            }
        },
        {
            class: "btn btn-dark btn-sm",
            style: "width:100px",
            text: "Cerrar",
            click: function () {
                $(this).dialog("close");
            }
        }]
    });
}

function triggerFormSubmit() {
    const selectedColumns = [];
    $("#sortable-columns li").each(function () {
        const checkbox = $(this).find("input[type='checkbox']");
        if (checkbox.is(":checked")) {
            selectedColumns.push($(this).data("valor"));
        }
    });

    $("#selected_columns").val(JSON.stringify(selectedColumns));

    document.getElementById('reporte_op_form').submit();
}

function guardar_preferencia() {
    $('#form-guardar-preferencia').trigger("reset");
    $("#guardar-preferencia-modal").dialog("open");
}

function cargar_preferencia() {
    $("#cargar-preferencia-modal").dialog("open");

    $("#tabla-preferencias tbody").empty();

    $.ajax({
        type: "GET",
        url: "/cargar_preferencias/",
        success: function(response) {
            if (response.preferencias && response.preferencias.length > 0) {
                $.each(response.preferencias, function(index, pref) {
                    var fila = '<tr class="preferencia-row" data-preferencia-id="' + pref.id + '">' +
                                '<td style="visibility:hidden;">' + pref.id + '</td>' +
                                '<td>' + pref.nombre + '</td>' +
                                '<td><button type="button" class="btn btn-success btn-sm seleccionar-preferencia">Seleccionar</button></td>' +
                                '<td><button type="button" class="btn btn-danger btn-sm eliminar-preferencia">Eliminar</button></td>' +
                                '<td style="display:none;">' + pref.selected_columns + '</td>' +
                               '</tr>';
                    $("#tabla-preferencias tbody").append(fila);
                });
            } else {
                $("#tabla-preferencias tbody").append('<tr><td colspan="3">No hay preferencias guardadas.</td></tr>');
            }
        },
        error: function(xhr, status, error) {
            console.error("Error al cargar las preferencias:", error);
        }
    });
}