document.addEventListener('DOMContentLoaded', function () {

const hoy = new Date().toISOString().split('T')[0];
    $.ajax({
        url: "/admin_cont/cargar_arbitraje/",
        type: "GET",
        data: { fecha: hoy },
        dataType: "json",
        success: function (data) {
            // Cargar los valores en los campos
            $('#id_arbitraje').val(data.arbitraje);
        },
        error: function (xhr, status, error) {
            alert("Error al cargar los datos iniciales: " + error);
        }
    });

    const inputDetalle = document.getElementById('id_detalle');
    const inputDetalleCuenta = document.getElementById('id_detalle_cuenta');

    if (inputDetalle && inputDetalleCuenta) {
        inputDetalle.addEventListener('input', function () {
            const valorMayuscula = this.value.toUpperCase();
            this.value = valorMayuscula;
            inputDetalleCuenta.value = valorMayuscula;
        });
    }
    $('table tbody').on('click', 'tr', function () {
        $('table tbody tr').removeClass('table-secondary');
        $(this).toggleClass('table-secondary');
      });

    $('#id_caja').on('change', function () {
      const banco = parseInt($(this).val(), 10);

      let nueva_moneda = null;
      if (banco === 90 || banco === 92) {
        nueva_moneda = 1;
      } else if (banco === 91 || banco === 93) {
        nueva_moneda = 2;
      }

      if (nueva_moneda !== null) {
        $('#id_moneda').val(nueva_moneda).change();
      }
    });
    document.getElementById("btnGuardar").addEventListener("click", function () {
      const cuenta = document.getElementById("id_cuenta");
      const detalle = document.getElementById("id_detalle_cuenta").value;
      const monto = parseFloat(document.getElementById("id_monto").value) || 0;
      //const tipo = document.querySelector('input[name="tipo_movimiento"]:checked')?.value;


      if (!cuenta || !monto) return;

      const cuentaText = cuenta.options[cuenta.selectedIndex].text;


      const nuevaFila = `
        <tr>
          <td>${cuentaText}</td>
          <td class="col-total">${monto}</td>
          <td>${detalle}</td>
        </tr>
      `;

      document.getElementById("tablaCaja").insertAdjacentHTML("beforeend", nuevaFila);
      $('#id_cuenta').val('');
      $('#id_monto').val('');

      calcularTotales();
    });
    document.getElementById("btnClonar").addEventListener("click", function () {
      const fila = document.querySelector("#tablaCaja tr.table-secondary");
      if (!fila) {
        alert("Selecciona una fila para clonar.");
        return;
      }

      const celdas = fila.querySelectorAll("td");

      const cuentaTexto = celdas[0].textContent.trim();
      const detalle = celdas[2].textContent.trim();
      const monto = parseFloat(celdas[1].textContent.trim()) || 0;

      document.getElementById("id_detalle_cuenta").value = detalle;
      document.getElementById("id_monto").value = monto;

      const cuentaSelect = document.getElementById("id_cuenta");
      for (let i = 0; i < cuentaSelect.options.length; i++) {
        if (cuentaSelect.options[i].text.trim() === cuentaTexto) {
          cuentaSelect.selectedIndex = i;
          break;
        }
      }
});
    document.getElementById("btnEliminar").addEventListener("click", function () {
      const fila = document.querySelector("#tablaCaja tr.table-secondary");
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
        let orden = 0;
        if(confirm('¿Desea generar una orden de pago?')){
            orden=1;
        }
      //const tipo = document.querySelector('input[name="tipo_movimiento"]:checked')?.value;

      const filas = document.querySelectorAll("#tablaCaja tr");
      const data = [];
      let fecha = $('#id_fecha').val();
      let moneda = $('#id_moneda').val();
      let arbitraje = $('#id_arbitraje').val();
      let paridad = $('#id_paridad').val();
      let detalle_general = $('#id_detalle').val();
      let banco = $('#id_caja option:selected').text();
      let acumulado = $('#acumulado').val();

      filas.forEach(fila => {
        const celdas = fila.querySelectorAll("td");

        const cuenta = celdas[0].textContent.trim();
        const detalle = celdas[2].textContent.trim();
        const monto = parseFloat(celdas[1].textContent.trim()) || 0;

        data.push({
          cuenta,
          detalle,
          monto,
        });
      });



    const general = {
      fecha: fecha,
      moneda: moneda,
      arbitraje: arbitraje,
      detalle: detalle_general,
      banco: banco,
      acumulado: acumulado,
      orden: orden,
    };

      if (data.length === 0) {
        alert("No hay datos para enviar.");
        return;
      }

    fetch("/admin_cont/guardar_movimiento_caja/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token
      },
      body: JSON.stringify({ asientos: data, general:general })
    })
    .then(response => response.json())
    .then(data => {
      if(data.numero_orden!=0){
        descargar_op(data.numero_orden);
      }else{
          resetear_form();
      }
      if (!data.success && !data.status) {
        console.error("Error del servidor:", data.error || data);
        throw new Error("Error al guardar.");
      }
      alert("Movimientos guardados correctamente.");
    })
    .catch(error => {
      console.error("Error en la petición:", error);
      alert("Ocurrió un error al enviar los datos.");
    });

    });
});

function calcularTotales() {
  let total = 0;
  document.querySelectorAll('#tablaCaja .col-total').forEach(function (td) {
    const valor = parseFloat(td.textContent.trim()) || 0;
    total += valor;
  });

  // Mostrar el resultado en el campo acumulado
  document.getElementById('acumulado').value = total.toFixed(2);
}
function descargar_op(op){
      let fecha= $('#id_fecha').val();
      let moneda = $('#id_moneda option:selected').text();
      let banco = $('#id_caja option:selected').text();
      let total= $('#acumulado').val();
      let detalle= $('#id_detalle').val();
      let data=[];
      const filas = document.querySelectorAll("#tablaCaja tr");
      filas.forEach(fila => {
        const celdas = fila.querySelectorAll("td");

        const cuenta = celdas[0].textContent.trim();
        const detalle = celdas[2].textContent.trim();
        const monto = parseFloat(celdas[1].textContent.trim()) || 0;

        data.push({
          cuenta,
          detalle,
          monto,
        });

      });

      const formData = new FormData();

      formData.append('data', JSON.stringify(data));
      formData.append('fecha_pago',fecha);
      formData.append('vto',fecha);
      formData.append('numero',0);
      formData.append('moneda',moneda);
      formData.append('monto_total',total);
      formData.append('banco',banco);
      formData.append('detalle',detalle);
      formData.append('orden',op);
      formData.append('modo','S/I');

      fetch("/admin_cont/generar_orden_pago_pdf/", {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": csrf_token,  // Asegurate de tener el token CSRF si estás usando Django
        }
      })
      .then(response => {
        if (!response.ok) throw new Error("Error al generar el PDF");
        return response.blob();
      })
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "orden_pago.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
        resetear_form();

      })
      .catch(error => {
        alert("Hubo un error al generar el PDF");
        console.error(error);
      });

  }
function resetear_form(){
  $('#formMovCaja').trigger('reset');
  $('#tablaCaja').empty();
const hoy = new Date().toISOString().split('T')[0];
    $.ajax({
        url: "/admin_cont/cargar_arbitraje/",
        type: "GET",
        data: { fecha: hoy },
        dataType: "json",
        success: function (data) {
            // Cargar los valores en los campos
            $('#id_arbitraje').val(data.arbitraje);
        },
        error: function (xhr, status, error) {
            alert("Error al cargar los datos iniciales: " + error);
        }
    });
}