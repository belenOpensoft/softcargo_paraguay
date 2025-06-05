document.addEventListener('DOMContentLoaded', function () {
    $('table tbody').on('click', 'tr', function () {
        $('table tbody tr').removeClass('table-secondary');
        $(this).toggleClass('table-secondary');
      });
    $("#btnBuscar").on("click", function() {
    let banco_validar=$('#id_banco').val();
    if(banco_validar==null){
        alert('Debe seleccionar un banco.');
        return;
    }
    const bancoText = $("#id_banco option:selected").text();
    const banco_id = bancoText.split(" - ")[0].trim();
    const fecha = $("#id_fecha").val();
    fetch("/admin_cont/buscar_cheques_bajar/", {
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
});