document.addEventListener('DOMContentLoaded', function () {
    $('table tbody').on('click', 'tr', function () {
        $('table tbody tr').removeClass('table-secondary');
        $(this).toggleClass('table-secondary');
      });
    $("#btnBuscar").on("click", function() {
    let banco_validar=$('#banco_baja').val();
    if(banco_validar==null){
        alert('Debe seleccionar un banco.');
        return;
    }
    const bancoText = $("#banco_baja option:selected").text();
    const fecha = $("#fecha_baja").val();
    fetch("/admin_cont/buscar_cheques_bajar/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        },
        body: JSON.stringify({
            bancoText,
            fecha
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "ok") {
            const tbody = $("#tablaChequesBaja").empty();
            data.cheques.forEach(chq => {
                tbody.append(`
                    <tr>
                        <td>${chq.vto}</td>
                        <td>${chq.emision}</td>
                        <td>${chq.numero}</td>
                        <td>${chq.detalle}</td>
                        <td>${chq.total}</td>
                        <td>${chq.bajar}</td>
                        <td>${chq.mov}</td>
                        <td>${chq.tipo_cambio}</td>
                        <td>${chq.paridad}</td>
                    </tr>
                `);
            });


        } else {
            alert("Error: " + data.mensaje);
        }
    });
});
});