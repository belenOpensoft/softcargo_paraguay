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
        });

function modal_columnas() {
    $("#config-modal").dialog({
        autoOpen: true,
        modal: true,
        width: 600,
        position: {
            my: "center top", // Centrar horizontalmente y posicionar desde la parte superior
            at: "center top+20", // Agregar desplazamiento de 20px desde la parte superior
            of: window // Referencia a la ventana del navegador
        },
        buttons: [{
            class: "btn btn-dark",
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
