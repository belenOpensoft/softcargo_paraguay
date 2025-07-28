document.addEventListener("DOMContentLoaded", function() {
    //console.log("📦 DOM cargado: inicializando bloqueo de formularios");

    document.querySelectorAll("form").forEach(function(form) {
        form.addEventListener("submit", function(event) {
            //console.log("📨 Formulario enviado:", form);

            const botones = form.querySelectorAll("button, input[type='submit']");
            if (botones.length === 0) {
                //console.log("⚠️ No se encontraron botones en el formulario");
            }

            botones.forEach(function(boton) {
                //console.log("⛔ Desactivando botón:", boton);
                boton.disabled = true;

                if (boton.tagName.toLowerCase() === 'button') {
                    boton.dataset.originalText = boton.innerHTML;
                    boton.innerHTML = 'Procesando...';
                } else if (boton.tagName.toLowerCase() === 'input') {
                    boton.dataset.originalValue = boton.value;
                    boton.value = 'Procesando...';
                }
            });
        });
    });
});