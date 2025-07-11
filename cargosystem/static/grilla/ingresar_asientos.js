$(document).ready(function () {
    arbitraje_carga();

  $('table tbody').on('click', 'tr', function () {
    $('table tbody tr').removeClass('table-secondary');
    $(this).toggleClass('table-secondary');
  });
    const detalle = document.getElementById("detalle");
      if (detalle) {
        detalle.addEventListener("input", function () {
          this.value = this.value.toUpperCase();
        });
      }

    document.getElementById("btnGuardar").addEventListener("click", function () {
      const cuenta = document.getElementById("cuenta");
      const detalle = document.getElementById("detalle").value;
      const posicion = document.getElementById("posicion").value;
      const moneda = document.getElementById("moneda").value;
      //const asiento = document.getElementById("asiento").value;
      const monto = parseFloat(document.getElementById("monto").value) || 0;
      const tipo = document.querySelector('input[name="tipo_movimiento"]:checked')?.value;
      const arbitraje = document.getElementById("arbitraje").value || "0.00";
      const paridad = document.getElementById("paridad").value || "0.0000";

      if (!cuenta || !tipo) return;

      const cuentaText = cuenta.options[cuenta.selectedIndex].text;

      let debe = tipo === 'debe' ? monto.toFixed(2) : "0.00";
      let haber = tipo === 'haber' ? monto.toFixed(2) : "0.00";
          //<td class="oculto">${asiento}</td>
      const nuevaFila = `
        <tr>
          <td>${cuentaText}</td>
          <td>${detalle}</td>
          <td class="col-debe">${debe}</td>
          <td class="col-haber">${haber}</td>
          <td>${arbitraje}</td>
          <td>${paridad}</td>
          <td>${posicion}</td>
          <td class="oculto">${moneda}</td>
        </tr>
      `;

      document.getElementById("tablaMovimientos").insertAdjacentHTML("beforeend", nuevaFila);
      document.getElementById("formIngresarAsiento").reset();

      arbitraje_carga();
      calcularTotales();
    });
    document.getElementById("btnClonar").addEventListener("click", function () {
      const fila = document.querySelector("#tablaMovimientos tr.table-secondary");
      if (!fila) {
        alert("Selecciona una fila para clonar.");
        return;
      }

      const celdas = fila.querySelectorAll("td");

      const cuentaTexto = celdas[0].textContent.trim();
      const detalle = celdas[1].textContent.trim();
      const debe = parseFloat(celdas[2].textContent.trim()) || 0;
      const haber = parseFloat(celdas[3].textContent.trim()) || 0;
      const arbitraje = celdas[4].textContent.trim();
      const paridad = celdas[5].textContent.trim();
      const posicion = celdas[6].textContent.trim();
      //const asiento = celdas[8].textContent.trim();
      const moneda = celdas[7].textContent.trim();

      document.getElementById("detalle").value = detalle;
      document.getElementById("arbitraje").value = arbitraje;
      document.getElementById("paridad").value = paridad;
      document.getElementById("posicion").value = posicion;
      document.getElementById("moneda").value = moneda;
      //document.getElementById("asiento").value = asiento;
      document.getElementById("monto").value = debe > 0 ? debe : haber;

      const tipo = debe > 0 ? 'debe' : 'haber';
      const radioTipo = document.querySelectorAll('input[name="tipo_movimiento"]');
      radioTipo.forEach(r => r.checked = (r.value === tipo));

      const cuentaSelect = document.getElementById("cuenta");
      for (let i = 0; i < cuentaSelect.options.length; i++) {
        if (cuentaSelect.options[i].text.trim() === cuentaTexto) {
          cuentaSelect.selectedIndex = i;
          break;
        }
      }
});
    document.getElementById("btnEliminar").addEventListener("click", function () {
      const fila = document.querySelector("#tablaMovimientos tr.table-secondary");
      if (!fila) {
        alert("Selecciona una fila para eliminar.");
        return;
      }

      if (confirm("¿Estás seguro que deseas eliminar esta fila?")) {
        fila.remove();
        calcularTotales(); // actualiza acumulados automáticamente
      }
    });
    document.getElementById("btnFinalizar").addEventListener("click", function () {
      const filas = document.querySelectorAll("#tablaMovimientos tr");
      const data = [];
      const monedas = new Set();

      filas.forEach(fila => {
        const celdas = fila.querySelectorAll("td");

        const cuenta = celdas[0].textContent.trim();
        const detalle = celdas[1].textContent.trim();
        const debe = parseFloat(celdas[2].textContent.trim()) || 0;
        const haber = parseFloat(celdas[3].textContent.trim()) || 0;
        const tipo_cambio = parseFloat(celdas[4].textContent.trim()) || 0;
        const paridad = parseFloat(celdas[5].textContent.trim()) || 0;
        const posicion = celdas[6].textContent.trim();
        const moneda = celdas[7].textContent.trim();
        monedas.add(moneda);
        data.push({
          cuenta,
          detalle,
          debe,
          haber,
          tipo_cambio,
          paridad,
          posicion,
          moneda
        });
      });

      if (monedas.size > 1) {
          alert("Error: no se pueden combinar monedas distintas en un mismo asiento.");
          return;
        }
      if (data.length === 0) {
        alert("No hay datos para enviar.");
        return;
      }
/*
    fetch("/admin_cont/guardar_asientos/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token
      },
      body: JSON.stringify({ asientos: data })
    })
    .then(response => response.json())
    .then(data => {
      if (!data.success && !data.status) {
        console.error("Error del servidor:", data.error || data);
        throw new Error("Error al guardar.");
      }
      $('#formIngresarAsiento').trigger('reset');
      $('#tablaMovimientos').empty();
      alert("Asientos guardados correctamente.");
    })
    .catch(error => {
      console.error("Error en la petición:", error);
      alert("Ocurrió un error al enviar los datos.");
    });
*/
      fetch("/admin_cont/guardar_asientos/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrf_token
        },
        body: JSON.stringify({ asientos: data }),
      })
      .then(response => {
        const contentType = response.headers.get("Content-Type") || "";
        if (!contentType.includes("application/pdf")) {
          // No es PDF: leer como texto y parsear como JSON
          return response.text().then(text => {
            try {
              const json = JSON.parse(text);
              throw new Error(json.error || json.status || "Error desconocido del servidor.");
            } catch (e) {
              throw new Error("Respuesta inválida del servidor: " + text);
            }
          });
        }
        return response.blob(); // Es PDF
      })
      .then(blob => {
        // Crear y descargar el PDF
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "asiento_contable.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        // Resetear formulario y limpiar
        $('#formIngresarAsiento').trigger('reset');
        $('#tablaMovimientos').empty();
        arbitraje_carga();

      })
      .catch(error => {
        alert("Error: " + error.message);
        console.error("Error en la petición:", error);
      });


    });
});


function calcularTotales() {
  let totalDebe = 0;
  let totalHaber = 0;

  const filas = document.querySelectorAll("#tablaMovimientos tr");

  filas.forEach(fila => {
    const debe = parseFloat(fila.querySelector(".col-debe")?.textContent || "0");
    const haber = parseFloat(fila.querySelector(".col-haber")?.textContent || "0");
    totalDebe += debe;
    totalHaber += haber;
  });

  document.getElementById("totalDebe").value = totalDebe.toFixed(2);
  document.getElementById("totalHaber").value = totalHaber.toFixed(2);
  document.getElementById("saldo").value = (totalDebe - totalHaber).toFixed(2);
}
function arbitraje_carga(){
const hoy = new Date().toISOString().split('T')[0];
    $.ajax({
        url: "/admin_cont/cargar_arbitraje/",
        type: "GET",
        data: { fecha: hoy },
            dataType: "json",
            success: function (data) {
                // Cargar los valores en los campos
                $('#arbitraje').val(data.arbitraje);
                $('#paridad').val(data.paridad);
            },
            error: function (xhr, status, error) {
                alert("Error al cargar los datos iniciales: " + error);
            }
        });
}