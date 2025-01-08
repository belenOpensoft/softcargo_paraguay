document.addEventListener('DOMContentLoaded', function() {
alert();
    // Mapa para almacenar ID internacional de cada país
    var paisesIdInternacional = {
        {% for pais in paises %}
        "{{ pais.nombre }}": "{{ pais.idinternacional }}",
        {% endfor %}
    };

    // Obtén el campo select y el input ID País
    var selectPais = document.getElementById('pais-select');
    var inputIdInternacional = document.getElementById('idinternacional');
    var pais = document.getElementById('nombrepais');


     for (var i = 0; i < selectPais.options.length; i++) {
        var optionText = selectPais.options[i].text;
        if (optionText === pais.value) {
            selectPais.selectedIndex = i;
            var selectedPais = selectPais.value;
            inputIdInternacional.value = paisesIdInternacional[selectedPais] || '';
            break;
        }
    }

    // Maneja el evento de cambio en el select
    selectPais.addEventListener('change', function() {
        var selectedPais = selectPais.value;
        inputIdInternacional.value = paisesIdInternacional[selectedPais] || '';
    });
});