document.addEventListener('DOMContentLoaded', function () {
    $("#modalStock").dialog({
        autoOpen: false,
        modal: true,
        width: 400,
        buttons: [
            {
                text: "Guardar",
                class: "btn btn-primary",
                click: function () {
                    guardar_cheques();
                    $(this).dialog("close");
                }
            },
            {
                text: "Salir",
                class: "btn btn-dark",
                click: function () {
                    resetearCamposModalStock();
                    $(this).dialog("close");
                }
            }
        ]
    });
    $('table tbody').on('click', 'tr', function () {
        $('table tbody tr').removeClass('table-secondary');
        $(this).toggleClass('table-secondary');
      });

    $("#btn-stock").click(function () {
        $("#modalStock").dialog("open");
    });
});

function guardar_cheques() {
    const bancoText = $("#banco_modal option:selected").text();
    const bancoNumero = bancoText.split(" - ")[0].trim();
    const primer_cheque = $("#primer_cheque").val();
    const total_cheques = $("#total_cheques_stock").val();
    const diferido = $("#diferidos").is(":checked");

    fetch("/admin_cont/guardar_stock_cheques/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        },
        body: JSON.stringify({
            bancoNumero,
            primer_cheque,
            total_cheques,
            diferido: diferido ? 'S' : 'N'
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Cheques generados correctamente.");
                resetearCamposModalStock();
                // podés recargar tabla aquí
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => alert("Error al guardar: " + error));
}

function resetearCamposModalStock() {
    $('#banco_modal').val('');
    $('#primer_cheque').val('');
    $('#total_cheques_stock').val('');
    $('#diferidos').prop('checked', false);
}
$("#btnBuscar").on("click", function() {
    let banco_validar=$('#id_banco').val();
    if(banco_validar==null){
        alert('Debe seleccionar un banco.');
        return;
    }
    const bancoText = $("#id_banco option:selected").text();
    const banco_id = bancoText.split(" - ")[0].trim();
    const cheque_desde = $("#id_cheque_desde").val();
    const cheque_hasta = $("#id_cheque_hasta").val();
    const ver_utilizados = $("#id_ver_utilizados").is(":checked");
    fetch("/admin_cont/buscar_cheques/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        },
        body: JSON.stringify({
            banco_id,
            cheque_desde,
            cheque_hasta,
            ver_utilizados,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "ok") {
            const tbody = $("#tablaChequeras").empty();
            data.cheques.forEach(chq => {
                tbody.append(`
                    <tr>
                        <td>${chq.numero}</td>
                        <td>${chq.estado}</td>
                        <td>${chq.referencia}</td>
                        <td>${chq.fecha}</td>
                        <td>${chq.diferido}</td>
                    </tr>
                `);
            });

            // Cargar resumen
            $("#disponibles").val(data.resumen.disponibles);
            $("#utilizados").val(data.resumen.utilizados);
            $("#anulados").val(data.resumen.anulados);
            $("#total_cheques").val(data.resumen.total);

        } else {
            alert("Error: " + data.mensaje);
        }
    });
});
$("#btnEliminar").on("click", function () {
    const fila = document.querySelector("#tablaChequeras tr.table-secondary");
    if (!fila) {
        alert("Selecciona una fila para eliminar.");
        return;
    }

    let numero = fila.querySelector("td:nth-child(1)")?.textContent.trim() || "";
    if (!numero) {
        alert("No se pudo obtener el número de cheque.");
        return;
    }

    if (!confirm("¿Estás seguro de que deseas eliminar el cheque " + numero + "?")) {
        return;
    }

    fetch("/admin_cont/eliminar_cheque/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token,
        },
        body: JSON.stringify({ numero: numero }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "ok") {
            fila.remove();
        } else {
            alert("Error: " + data.mensaje);
        }
    })
    .catch(error => {
        alert("Error de red o servidor: " + error);
    });
});
$("#btnHabilitar").on("click", function () {
    const fila = document.querySelector("#tablaChequeras tr.table-secondary");
    if (!fila) {
        alert("Selecciona una fila.");
        return;
    }

    let numero = fila.querySelector("td:nth-child(1)")?.textContent.trim() || "";
    if (!numero) {
        alert("No se pudo obtener el número de cheque.");
        return;
    }

    if (!confirm("¿Estás seguro de que deseas habilitar el cheque " + numero + "?")) {
        return;
    }

    fetch("/admin_cont/habilitar_deshabilitar/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token,
        },
        body: JSON.stringify({ numero: numero,habilitar_deshabilitar:0 }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status != "ok") {
            alert("Error: " + data.mensaje);
        }
    })
    .catch(error => {
        alert("Error de red o servidor: " + error);
    });
    $('#btnBuscar').trigger('click');

});
$("#btnBloquear").on("click", function () {
    const fila = document.querySelector("#tablaChequeras tr.table-secondary");
    if (!fila) {
        alert("Selecciona una fila.");
        return;
    }

    let numero = fila.querySelector("td:nth-child(1)")?.textContent.trim() || "";
    if (!numero) {
        alert("No se pudo obtener el número de cheque.");
        return;
    }

    if (!confirm("¿Estás seguro de que deseas bloquear el cheque " + numero + "?")) {
        return;
    }

    fetch("/admin_cont/habilitar_deshabilitar/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token,
        },
        body: JSON.stringify({ numero: numero,habilitar_deshabilitar:2 }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status != "ok") {
            alert("Error: " + data.mensaje);
        }
    })
    .catch(error => {
        alert("Error de red o servidor: " + error);
    });

    $('#btnBuscar').trigger('click');
});
