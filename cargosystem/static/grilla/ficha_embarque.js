document.addEventListener('DOMContentLoaded', function () {
    const tipoBusquedaRadios = document.querySelectorAll('input[name="tipo_busqueda"]');
    const masterInput = document.getElementById('id_master');
    const houseInput = document.getElementById('id_house');
    const seguimientoInput = document.getElementById('id_seguimiento');

    const posicionInput = document.getElementById('id_posicion');
    const documentoInput = document.getElementById('id_documento');

    function actualizarVisibilidadBusqueda() {
        const tipoSeleccionado = document.querySelector('input[name="tipo_busqueda"]:checked').value;

        // Resetear todos
        masterInput.disabled = true;
        houseInput.disabled = true;
        seguimientoInput.disabled = true;
        masterInput.value = '';
        houseInput.value = '';
        seguimientoInput.value = '';


        if (tipoSeleccionado === 'master') {
            masterInput.disabled = false;
        } else if (tipoSeleccionado === 'house') {
            houseInput.disabled = false;
        } else if (tipoSeleccionado === 'seguimiento') {
            seguimientoInput.disabled = false;
        }
    }

    tipoBusquedaRadios.forEach(radio => {
        radio.addEventListener('change', actualizarVisibilidadBusqueda);
    });

    // masterInput.disabled = false;
    actualizarVisibilidadBusqueda();
});
