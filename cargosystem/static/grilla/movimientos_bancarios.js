function actualizarDetalleMovimiento() {
    const seleccionado = document.querySelector('input[name="tipo_movimiento"]:checked');
    if (seleccionado) {
      const texto = seleccionado.nextElementSibling.innerText.trim().toUpperCase();
      document.getElementById('id_detalle').value = texto;
      document.getElementById('id_detalle_cuenta').value = texto;
      if (seleccionado.value=='cheque_comun' || seleccionado.value=='cheque_diferido'){
        $('#busqueda_cheques').prop('disabled', false);
      }else{
        $('#busqueda_cheques').prop('disabled', true);
      }

      if(seleccionado.value=='depositar'){
        $('#cheques_disponibles_clientes').prop('disabled', false);
      }else{
        $('#cheques_disponibles_clientes').prop('disabled', true);
      }
    }
  }
function calcularTotales() {
  let total = 0;

  const filas = document.querySelectorAll("#tablaCheques tr");

  filas.forEach(fila => {
    const monto = parseFloat(fila.querySelector(".col-total")?.textContent || "0");
    total += monto;
  });

  document.getElementById("acumulado").value = total.toFixed(2);
}

document.addEventListener('DOMContentLoaded', function () {

    $('#id_detalle').on('input', function () {
        const texto = $(this).val().toUpperCase();
        $(this).val(texto);
        $('#id_detalle_cuenta').val(texto);
    });


    $('#id_banco').on('change', function () {
  const banco = parseInt($(this).val(), 10);

  let nueva_moneda = null;
  if (banco === 95 || banco === 97) {
    nueva_moneda = 1;
  } else if (banco === 96 || banco === 98 || banco === 99) {
    nueva_moneda = 2;
  } else if (banco === 94) {
    nueva_moneda = 4;
  }

  if (nueva_moneda !== null) {
    $('#id_moneda').val(nueva_moneda).change();
  }
});

    actualizarDetalleMovimiento();

    document.querySelectorAll('input[name="tipo_movimiento"]').forEach(radio => {
      radio.addEventListener('change', actualizarDetalleMovimiento);
    });

    $('table tbody').on('click', 'tr', function () {
        $('table tbody tr').removeClass('table-secondary');
        $(this).toggleClass('table-secondary');
      });

    const hoy = new Date().toISOString().split('T')[0];
    $.ajax({
        url: "/admin_cont/cargar_arbitraje/",
        type: "GET",
        data: { fecha: hoy },
        dataType: "json",
        success: function (data) {
            // Cargar los valores en los campos
            $('#id_arbitraje').val(data.arbitraje);
            $('#id_paridad').val(data.paridad);
        },
        error: function (xhr, status, error) {
            alert("Error al cargar los datos iniciales: " + error);
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

      document.getElementById("tablaCheques").insertAdjacentHTML("beforeend", nuevaFila);
      $('#id_cuenta').val('');
      $('#id_monto').val('');

      calcularTotales();
    });
    document.getElementById("btnClonar").addEventListener("click", function () {
      const fila = document.querySelector("#tablaCheques tr.table-secondary");
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
      const fila = document.querySelector("#tablaCheques tr.table-secondary");
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
      let orden=0;
      const tipo = document.querySelector('input[name="tipo_movimiento"]:checked')?.value;

      if(tipo=='cheque_comun'||tipo=='cheque_diferido'||tipo=='egresos'||tipo=='transferencia'){
        if(confirm('Desea generar una Orden de Pago?')){
            orden =1;
          }
      }

      const filas = document.querySelectorAll("#tablaCheques tr");
      const data = [];
      let documento = $('#id_nro_documento').val();
      let vencimiento = $('#id_vto_cheque').val();
      let fecha = $('#id_fecha').val();
      let moneda = $('#id_moneda').val();
      let arbitraje = $('#id_arbitraje').val();
      let paridad = $('#id_paridad').val();
      let detalle_general = $('#id_detalle').val();
      let banco = $('#id_banco option:selected').text();
      let cheque = $('#id_escheque').val();
      let chequera = $('#id_chequera').val();
      let acumulado = $('#acumulado').val();


      if(cheque==1){
      filas.forEach(fila => {
        const celdas = fila.querySelectorAll("td");

        const cuenta = celdas[0].textContent.trim();
        const detalle = celdas[2].textContent.trim();
        const autogen = celdas[3].textContent.trim();
        const monto = parseFloat(celdas[1].textContent.trim()) || 0;

        data.push({
          cuenta,
          detalle,
          monto,
          autogen,
        });
      });

      }else{
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

      }


    const general = {
      documento: documento,
      vencimiento: vencimiento,
      fecha: fecha,
      moneda: moneda,
      arbitraje: arbitraje,
      paridad: paridad,
      detalle: detalle_general,
      banco: banco,
      tipo: tipo,
      cheque: cheque,
      chequera: chequera,
      acumulado: acumulado,
      orden: orden,
    };


      if (data.length === 0) {
        alert("No hay datos para enviar.");
        return;
      }

    fetch("/admin_cont/guardar_movimiento_bancario/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token
      },
      body: JSON.stringify({ asientos: data, general:general })
    })
    .then(response => response.json())
    .then(data => {
      if(tipo=='depositar'){
          if (confirm('¿Desea imprimir el comprobante de deposito?')){
            descargar_depo();
          }
      }
      if(data.numero_orden!=0){
          if (confirm('¿Desea imprimir el comprobante de pago?')){
            descargar_op(data.numero_orden);
          }
      }
      if (!data.success && !data.status) {
        console.error("Error del servidor:", data.error || data);
        throw new Error("Error al guardar.");
      }
        resetear_form();
      alert("Movimientos guardados correctamente.");
    })
    .catch(error => {
      console.error("Error en la petición:", error);
      alert("Ocurrió un error al enviar los datos.");
    });

    });

/*
    document.getElementById("btnGenerarPDF").addEventListener("click", function () {
     let documento= $('#id_nro_documento').val();
      let fecha= $('#id_fecha').val();
      let vto= $('#id_vto_cheque').val();
      let moneda = $('#id_moneda option:selected').text();
      let banco = $('#id_banco option:selected').text();
      let total= $('#acumulado').val();
      let detalle= $('#id_detalle').val();
      let data=[];
      const filas = document.querySelectorAll("#tablaCheques tr");
      let cheque = $('#id_escheque').val();
      if(cheque==1){
        filas.forEach(fila => {
        const celdas = fila.querySelectorAll("td");

        const banco = celdas[6].textContent.trim();
        const cliente = celdas[5].textContent.trim();
        const numero = celdas[4].textContent.trim();
        const monto = parseFloat(celdas[1].textContent.trim()) || 0;

        data.push({
          banco,
          cliente,
          numero,
          monto,
        });

      });
      }


      const formData = new FormData();

      formData.append('data', JSON.stringify(data));
      formData.append('fecha',fecha);
      formData.append('vto',vto);
      formData.append('numero',$('#id_nro_documento').val());
      formData.append('moneda',moneda);
      formData.append('monto_total',total);
      formData.append('banco',banco);
      formData.append('detalle',detalle);

      fetch("/admin_cont/generar_comprobante_deposito_pdf/", {
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
        a.download = "comprobante_deposito.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      })
      .catch(error => {
        alert("Hubo un error al generar el PDF");
        console.error(error);
      });
});
*/
    $("#modalChequesDisponibles").dialog({
        autoOpen: false,
        modal: true,
        width: 800,
        height: 400,
        buttons:  [{
                        text: "Salir",
                        class: "btn btn-dark",
                        style: "width:80px;font-size:12px",
                        click: function () {
                            $(this).dialog("close");
                        },
                    }],
        close: function () {
          const filasSeleccionadas = $('#tablaChequesDisponibles tr').has('input.cheque-seleccionado:checked');
          const tabla = document.getElementById("tablaCheques");
          const detalleGeneral = document.getElementById("id_detalle_cuenta").value;

          let monedaUnica = null;
          let monedasValidas = true;

          // Verificación de monedas consistentes
          filasSeleccionadas.each(function () {
            const moneda = $(this).find('td').eq(7).text().trim();
            if (monedaUnica === null) {
              monedaUnica = moneda;
            } else if (monedaUnica !== moneda) {
              monedasValidas = false;
              return false;
            }
          });

          if (!monedasValidas) {
            alert("Todos los cheques seleccionados deben tener la misma moneda.");
            return;
          }

          // Insertar filas con cuenta correspondiente
          filasSeleccionadas.each(function () {
            const celdas = $(this).find('td');
            const total = parseFloat(celdas.eq(5).text().trim()) || 0;
            const moneda = celdas.eq(7).text().trim();
            const id = celdas.eq(6).text().trim();
            const numero = celdas.eq(3).text().trim();
            const cliente = celdas.eq(4).text().trim();
            const banco = celdas.eq(2).text().trim();

            let cuentaId = null;
            if (moneda === "1") {
              cuentaId = "92";
            } else if (["2", "3"].includes(moneda)) {
              cuentaId = "93";
            }

            let cuentaText = "";
            if (cuentaId) {
              const option = $('#id_cuenta option[value="' + cuentaId + '"]');
              if (option.length) {
                cuentaText = option.text();
              }
            }

            const nuevaFila = `
              <tr>
                <td>${cuentaText}</td>
                <td class="col-total">${total.toFixed(2)}</td>
                <td>${detalleGeneral}</td>
                <td class='oculto'>${id}</td>
                <td class='oculto'>${numero}</td>
                <td class='oculto'>${cliente}</td>
                <td class='oculto'>${banco}</td>
              </tr>
            `;
            tabla.insertAdjacentHTML("beforeend", nuevaFila);
          });


          $('#id_escheque').val('1');

          // Limpiar campos
          $('#id_monto').val('');
          $('#id_detalle_cuenta').val('');

          // Desmarcar los checkboxes
          $('#tablaChequesDisponibles input.cheque-seleccionado').prop('checked', false);

          calcularTotales();
        }

      });

    $("#cheques_disponibles_clientes").on("click", function () {
      const tbody = $("#tablaChequesDisponibles");
      tbody.empty();
      $("#modalChequesDisponibles").dialog("open");
      $("#loadingSpinner").show();

      fetch("/admin_cont/cheques_disponibles_clientes/")
        .then(response => response.json())
        .then(data => {
          if (data.mensaje) {
            tbody.append('<tr><td colspan="7" class="text-center">No hay cheques disponibles.</td></tr>');
             $("#loadingSpinner").hide();
            return;
          }

          if (data.success) {
            if (data.cheques.length === 0) {
             $("#loadingSpinner").hide();
              tbody.append('<tr><td colspan="7" class="text-center">No hay cheques disponibles.</td></tr>');

            } else {
            $("#loadingSpinner").hide();
              data.cheques.forEach(c => {
                const row = `
                  <tr>
                    <td>${c.vencimiento}</td>
                    <td>${c.emision}</td>
                    <td>${c.banco}</td>
                    <td>${c.numero}</td>
                    <td>${c.cliente}</td>
                    <td>${c.total}</td>
                    <td class="oculto">${c.id}</td>
                    <td class="oculto">${c.moneda}</td>
                    <td><input type="checkbox" class="cheque-seleccionado"></td>
                  </tr>
                `;
                tbody.append(row);
              });

            }
          } else {
            alert(data.error);
          }
        })
        .catch(err => {
          console.error("Error al cargar cheques:", err);
          alert("No se pudieron cargar los cheques.");
          $("#loadingSpinner").hide(); // Ocultar en caso de error
        });
});

    $(document).on('click', function (e) {
      if (!$(e.target).closest('#lista_cheques, #busqueda_cheques').length) {
        $('#lista_cheques').hide();
      }
    });

    $('#busqueda_cheques').on('click', function (e) {
      const boton = $(this);
      const offset = boton.offset();

      const tipoMovimiento = $('input[name="tipo_movimiento"]:checked').val();
      let url = "/admin_cont/cheques_disponibles_listado";

      if (tipoMovimiento === "cheque_diferido") {
        url += "_diferidos";
      }

      fetch(url + '/', {
        method: "GET",
        headers: {
          "X-CSRFToken": csrf_token
        }
      })
      .then(response => response.json())
      .then(cheques => {
        const ul = $('#cheques_lista_ul');
        ul.empty();

        if (cheques.length === 0) {
          ul.append(`<li class="list-group-item text-muted">No hay cheques disponibles</li>`);
        } else {
          cheques.forEach(chq => {
            ul.append(`<li class="list-group-item" data-numero="${chq.numero}"><strong>${chq.numero}</strong> - ${chq.fecha}</li>`);
          });
        }

        // Doble clic para usar el cheque
        $('#cheques_lista_ul').off('dblclick').on('dblclick', 'li', function () {
          const numeroCheque = $(this).data('numero');
          if (numeroCheque) {
            $('#id_nro_documento').val(numeroCheque);
            $('#lista_cheques').hide();
            $('#id_chequera').val('1');
          }
        });

        $('#lista_cheques').css({
          top: offset.top + boton.outerHeight(),
          left: offset.left
        }).toggle();
      })
      .catch(error => {
        console.error("Error al cargar cheques:", error);
      });
});

  });

  function descargar_op(op){
      let fecha= $('#id_fecha').val();
      let vto= $('#id_vto_cheque').val();
      let moneda = $('#id_moneda option:selected').text();
      let banco = $('#id_banco option:selected').text();
      let total= $('#acumulado').val();
      let detalle= $('#id_detalle').val();
      let data=[];
      const filas = document.querySelectorAll("#tablaCheques tr");
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

      const tipo = document.querySelector('input[name="tipo_movimiento"]:checked')?.value;
        let modo_asiento = "";

        if (tipo === 'cheque_comun' || tipo === 'cheque_diferido') {
          modo_asiento = 'CHEQUE';
        } else if (tipo === 'depositar') {
          modo_asiento = 'DEPOSITO';
        } else if (tipo === 'transferencia') {
          modo_asiento = 'TRANSFER';
        } else if (tipo === 'egresos') {
          modo_asiento = 'EGRESO';
        } else if (tipo === 'ingresos') {
          modo_asiento = 'INGRESO';
        }


      const formData = new FormData();

      formData.append('data', JSON.stringify(data));
      formData.append('fecha_pago',fecha);
      formData.append('vto',vto);
      formData.append('numero',$('#id_nro_documento').val());
      formData.append('moneda',moneda);
      formData.append('monto_total',total);
      formData.append('banco',banco);
      formData.append('detalle',detalle);
      formData.append('orden',op);
      formData.append('modo',modo_asiento);

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
          /*
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "orden_pago.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);*/
        const url = window.URL.createObjectURL(blob);
        const ventana = window.open(url);
        ventana.onload = function () {
            ventana.focus();
            ventana.print();
        };
        resetear_form();
      })
      .catch(error => {
        alert("Hubo un error al generar el PDF");
        console.error(error);
      });
  }
  function descargar_depo(){
  let documento= $('#id_nro_documento').val();
      let fecha= $('#id_fecha').val();
      let vto= $('#id_vto_cheque').val();
      let moneda = $('#id_moneda option:selected').text();
      let banco = $('#id_banco option:selected').text();
      let total= $('#acumulado').val();
      let detalle= $('#id_detalle').val();
      let data=[];
      const filas = document.querySelectorAll("#tablaCheques tr");
      let cheque = $('#id_escheque').val();
      if(cheque==1){
        filas.forEach(fila => {
        const celdas = fila.querySelectorAll("td");

        const banco = celdas[6].textContent.trim();
        const cliente = celdas[5].textContent.trim();
        const numero = celdas[4].textContent.trim();
        const monto = parseFloat(celdas[1].textContent.trim()) || 0;

        data.push({
          banco,
          cliente,
          numero,
          monto,
        });

      });
      }


      const formData = new FormData();

      formData.append('data', JSON.stringify(data));
      formData.append('fecha',fecha);
      formData.append('vto',vto);
      formData.append('numero',$('#id_nro_documento').val());
      formData.append('moneda',moneda);
      formData.append('monto_total',total);
      formData.append('banco',banco);
      formData.append('detalle',detalle);

      fetch("/admin_cont/generar_comprobante_deposito_pdf/", {
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
          /*
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "comprobante_deposito.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
           */
        const url = window.URL.createObjectURL(blob);
        const ventana = window.open(url);
        ventana.onload = function () {
            ventana.focus();
            ventana.print();
        };
        resetear_form();
      })
      .catch(error => {
        alert("Hubo un error al generar el PDF");
        console.error(error);
      });
  }
  function resetear_form(){
    $('#formMovBancarios').trigger('reset');
    $('#tablaCheques').empty();
    $('#id_escheque').val('0');
    actualizarDetalleMovimiento();
const hoy = new Date().toISOString().split('T')[0];
    $.ajax({
        url: "/admin_cont/cargar_arbitraje/",
        type: "GET",
        data: { fecha: hoy },
        dataType: "json",
        success: function (data) {
            // Cargar los valores en los campos
            $('#id_arbitraje').val(data.arbitraje);
            $('#id_paridad').val(data.paridad);
        },
        error: function (xhr, status, error) {
            alert("Error al cargar los datos iniciales: " + error);
        }
    });
}