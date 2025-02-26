var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;

$(document).ready(function() {
    var buscar = '';
    var que_buscar = '';
    let contador = 0;

       // Evento cuando se cambia de pestaña

    let radioMasters = document.getElementById("imputar-masters");
    let radioHouses = document.getElementById("imputar-houses");

    radioMasters.addEventListener("change", actualizarPestañas);
    radioHouses.addEventListener("change", actualizarPestañas);

    actualizarPestañas();

    verificarTipoFactura();

    $("#modal-embarque").dialog({
        autoOpen: false,
        width: wWidth * 0.90,
        height: wHeight,
        modal: true,
        position: { my: "center top", at: "center top+20", of: window }, // Ajusta la posición
        create: function () {
            var $buttons = $(this).parent().find(".ui-dialog-buttonpane button");
            $buttons.eq(0).addClass("btn btn-warning"); // Botón Guardar
            $buttons.eq(1).addClass("btn btn-success"); // Botón Guardar
            $buttons.eq(2).addClass("btn btn-dark"); // Botón Cerrar
        },
        buttons: {
            "Armar": function () {
                // Lógica para guardar los cambios
                let precio = parseFloat($("#seleccionado-precio").val()) || 0;
                let cliente = $("#seleccionado-cliente").val();
                let lugar = $("#seleccionado-lugar").val();
                let embarque = $("#seleccionado-embarque").text();
                let total = parseFloat(localStorage.getItem('precio_item_imputar')) || 0;

                if (precio>total){
                alert('El monto ingresado: ' +precio+', es mayor al original: '+total);
                return;
                }

                let nuevaFila = `
                    <tr>
                        <td>${posicion}</td>
                        <td>${precio}</td>
                        <td><button class="btn btn-danger btn-sm eliminar-fila">Eliminar</button></td>
                        <td style="display:none;">${cliente}</td>
                        <td style="display:none;">${lugar}</td>
                        <td style="display:none;">${embarque}</td>
                    </tr>
                `;

                $("#guardado-tabla tbody").append(nuevaFila);

                // Agregar evento para eliminar fila al botón generado dinámicamente
                $(".eliminar-fila").off("click").on("click", function () {
                    $(this).closest("tr").remove();
                });

                // Limpiar los valores seleccionados después de agregar la fila
                $("#seleccionado-posicion").text("");
                $("#seleccionado-embarque").text("");
                $("#seleccionado-precio").val("");
                $("#seleccionado-tipo").val("");
                //$(this).dialog("close");
            },
            "Guardar y Cerrar": function () {
                let total= localStorage.getItem('precio_item_imputar');
                let total_tabla = 0;
                let filas = document.querySelectorAll("#guardado-tabla tbody tr");
                if(filas.length==0){
                alert('No se ha armado nada.');
                return;
                }
                filas.forEach(fila => {
                    let montoCelda = fila.querySelector("td:nth-child(2)");

                    if (montoCelda) {
                        let monto = parseFloat(montoCelda.textContent.trim().replace(',', '.')) || 0;
                        total_tabla += monto;
                    }
                });
                if(total!=total_tabla){
                alert('Los montos armados: '+ total_tabla+', difieren del ingresado: '+total);
                return;
                }

                //guardar_impucompra();
                rellenar_tabla();
                $(this).dialog("close");
            },
            "Cancelar": function () {
                $(this).dialog("close");
            }
        }
    });

    let table = document.querySelector("#tabla-embarque-container tbody");
    let selectedRow = null;

    table.addEventListener("click", function (event) {
        let row = event.target.closest("tr");
        if (!row) return;

        if (selectedRow) {
            selectedRow.classList.remove("table-secondary");
        }

        row.classList.add("table-secondary");
        selectedRow = row;
    });
    //rellenar seleccionados
    table.addEventListener("dblclick", function (event) {
        let row = event.target.closest("tr");
        if (!row) return;

        let embarque = row.cells[0].textContent.trim();
        let tipo = row.cells[1].textContent.trim();
        posicion = row.cells[3].textContent.trim();
        cliente = row.cells[9].textContent.trim();

        let selectedRadio = $('input[name="imputar"]:checked').attr('id');
        let impucompra_tipo;
        if(selectedRadio=='imputar-masters'){
            impucompra_tipo='M';
        }else{
            impucompra_tipo='H';
        }

        document.querySelector("#seleccionado-embarque").textContent = embarque;
        document.querySelector("#seleccionado-tipo").textContent = tipo === "CONSOLIDADO" ? "C" : "D";
        document.querySelector("#seleccionado-posicion").textContent = posicion;
        $("#seleccionado-cliente").val(cliente);
        $("#seleccionado-precio").val(localStorage.getItem('precio_item_imputar'));
        $("#seleccionado-lugar").val(impucompra_tipo);

    });
    //buscadores
    document.querySelectorAll("button.btn-primary").forEach(button => {
        button.addEventListener("click", function () {
            let selectedRadio = $('input[name="imputar"]:checked').attr('id');
            let impucompra_tipo;
            if(selectedRadio=='imputar-masters'){
                impucompra_tipo='master';
            }else{
                impucompra_tipo='house';
            }
            let departamento = document.getElementById("departamento").value;
            if(departamento==''){
                alert('Seleccione una Operativa');
                return;
            }
            let fechaDesde = document.getElementById("fecha-desde")?.value || "";
            let fechaHasta = document.getElementById("fecha-hasta")?.value || "";
            let posicion = document.getElementById("posicion-input")?.value || "";
            let tipoEmbarque = document.querySelector('input[name="tipo-embarque"]:checked')?.value || "todos";
            let conocimiento = document.getElementById("contenedor-input")?.value || "";
            let transportista = document.getElementById("transportista-input")?.value || "";
            let agente = document.getElementById("agente-input")?.value || "";
            let status = document.getElementById("status-input")?.value || "";
            let contenedor = document.getElementById("contenedor-input")?.value || "";
            let vapor = document.getElementById("vapor-input")?.value || "";
            let seguimiento = document.getElementById("seguimiento-input")?.value || "";
            let master = document.getElementById("master-input")?.value || "";
            let house = document.getElementById("house-input")?.value || "";
            let embarque = document.getElementById("embarque-input-buscar")?.value || "";

            let params = new URLSearchParams({
                departamento: departamento,
                fecha_desde: fechaDesde,
                fecha_hasta: fechaHasta,
                posicion: posicion,
                tipo_embarque: tipoEmbarque,
                conocimiento: conocimiento,
                transportista: transportista,
                agente: agente,
                status: status,
                contenedor: contenedor,
                vapor: vapor,
                seguimiento: seguimiento,
                master: master,
                house: house,
                embarque:embarque,
                cual:impucompra_tipo
            });

            fetch(`/admin_cont/buscar_embarques/?${params}`)
                .then(response => response.json())
                .then(data => {
                    let tbody = document.querySelector("#tabla-embarque-container tbody");
                    tbody.innerHTML = "";  // Limpiar la tabla antes de cargar nuevos datos

                    data.resultados.forEach(item => {
                        let row = `<tr>
                            <td>${item.embarque}</td>
                            <td>${item.tipo}</td>
                            <td>${item.fecha}</td>
                            <td>${item.posicion}</td>
                            <td>${item.conocimiento}</td>
                            <td>${item.transportista}</td>
                            <td>${item.agente}</td>
                            <td>${item.tarifa}</td>
                            <td>${item.status}</td>
                            <td>${item.cliente}</td>
                        </tr>`;
                        tbody.innerHTML += row;
                    });
                })
                .catch(error => console.error("Error al buscar embarques:", error));
     });
     });


    $("#modal-embarque").tabs();
    $("#id_fecha_registro").change(function () {
        actualizarFechas(this, "#id_fecha_documento");  // Copia la fecha al segundo campo
        actualizarFechas(this, "#id_vencimiento");  // Copia la fecha al tercer campo
    });

    $("#id_fecha_documento").change(function () {
        actualizarFechas(this, "#id_vencimiento");  // Copia la fecha al tercer campo
    });
    $('#tabla_proveedoresygastos tfoot th').each(function(index) {
        let title = $('#tabla_proveedoresygastos thead th').eq(index).text();

        if (index === 0) {
            // Si es la primera columna, colocar el botón de limpiar filtros
            $(this).html('<button class="btn btn-danger" title="Borrar filtros" id="clear"><span class="glyphicon glyphicon-erase"></span> Limpiar</button>');
        } else if (title !== '') {
            // Agregar inputs de búsqueda en las demás columnas
            $(this).html('<input type="text" class="form-control filter-input" autocomplete="off" id="buscoid_' + index + '" placeholder="Buscar ' + title + '" />');
        }
    });
    // Evento para limpiar todos los filtros
    $(document).on("click", "#clear", function() {
        awbRegex='';
        $(".filter-input").val("").trigger("keyup"); // Limpia los inputs y activa la búsqueda
        $(".filter-input").removeClass("is-invalid"); // Se quita el rojo si se vacía
        table.ajax.reload();
    });
    // Evento para resaltar los inputs cuando tienen contenido
    $(document).on("input", ".filter-input", function() {
        if ($(this).val().trim() !== "") {
            $(this).addClass("is-invalid"); // Se pone en rojo
        } else {
            $(this).removeClass("is-invalid"); // Se quita el rojo si se vacía
        }
    });
    table = $('#tabla_proveedoresygastos').DataTable({
    "dom": 'Btlipr',
    "scrollX": true,
    "bAutoWidth": false,
    "scrollY": wHeight * 0.60,
    "columnDefs": [
        {
            "targets": [0],  // Ocultamos ambas columnas en una sola configuración
            "visible": true,
            "searchable": false ,
            "className": "invisible-column",
             "render": function(data, type, row) {
            return "";  // Devuelve una celda vacía
        }
        },
    ],
    "order": [[2, "desc"]],
    "processing": true,
    "serverSide": true,
    "pageLength": 100,
    "ajax": {
        "url": "/admin_cont/source_proveedoresygastos/",
        'type': 'GET',
        "data": function (d) {
            return $.extend({}, d, {
                "buscar": buscar,
                "que_buscar": que_buscar,
            });
        }
    },
    "language": {
        url: "/static/datatables/es_ES.json"
    },
    initComplete: function () {
        let api = this.api();
        api.columns().every(function () {
            var that = this;
            $('input', this.footer()).on('keyup change', function () {
                if (that.search() !== this.value) {
                    that.search(this.value).draw();
                }
            });
        });
    },
    "rowCallback": function (row, data) {}
});
    const valorInicial = $('#id_tipo').find('option:selected').text();

    $('#tipoSeleccionado').text(valorInicial);

    $('#id_tipo').change(function() {
        const valorSeleccionado = $(this).find('option:selected').text();
        $('#tipoSeleccionado').text(valorSeleccionado);
        verificarTipoFactura();
    });

    // Verificar el estado inicial de tercerizado
        toggleProveedor2();

    // Detectar cambios en el campo tercerizado
    $('#id_tercerizado').change(function() {
        toggleProveedor2();
    });

    // Autocomplete proveedor
    $('#proveedor').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/admin_cont/buscar_proveedor",
                dataType: 'json',
                data: { term: request.term },
                success: function(data) {
                    response(data.map(proveedor => ({
                        label: proveedor.text,
                        value: proveedor.text,
                        codigo: proveedor.codigo
                    })));
                },
                error: xhr => console.error('Error al buscar proveedores:', xhr)
            });
        },
        minLength: 2,
        appendTo: "#proveedoresModal",
        select: function(event, ui) {
            let codigo = ui.item['codigo'];
            $.ajax({
                url: "/admin_cont/buscar_proveedores",
                data: { 'codigo': codigo, },
                dataType: 'json',
                success: proveedor => {
                    const row = `
                        <tr id="proveedor-${codigo}">
                            <td class="d-none">${proveedor.codigo}</td>
                            <td>${proveedor.empresa}</td>
                            <td>${proveedor.ruc}</td>
                        </tr>`;
                    $('#proveedorTable tbody').html(row);
                    $('#proveedorTable').show();
                },
                error: xhr => console.error('Error al obtener los detalles del proveedor:', xhr)
            });
        }
    });

    // Autocomplete proveedor2
    $('#proveedor2').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/admin_cont/buscar_proveedor",
                dataType: 'json',
                data: { term: request.term },
                success: function(data) {
                    response(data.map(proveedor => ({
                        label: proveedor.text,
                        value: proveedor.text,
                        id: proveedor.id
                    })));
                },
                error: xhr => console.error('Error al buscar proveedores:', xhr)
            });
        },
        minLength: 2,
        select: function(event, ui) {
            const { id } = ui.item;

            $.ajax({
                url: "/admin_cont/buscar_proveedores",
                data: { id },
                dataType: 'json',
                success: proveedor => {
                    const row = `
                        <tr id="proveedor-${id}">
                            <td class="d-none">${proveedor.codigo}</td>
                            <td>${proveedor.empresa}</td>
                        </tr>`;
                    $('#proveedor2Table tbody').html(row);
                    $('#proveedor2Table').show();
                },
                error: xhr => console.error('Error al obtener los detalles del proveedor:', xhr)
            });
        }
    });

    let itemCounter = 0;

    // Autocomplete para el input "item"
    $('#item').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/admin_cont/buscar_item_c",
                dataType: 'json',
                data: {
                    term: request.term
                },
                success: data => response(data.map(item => ({
                    label: item.text,
                    value: item.text,
                    id: item.id
                }))),
                error: xhr => console.error('Error al buscar items:', xhr)
            });
        },
        minLength: 2,
        select: function(event, ui) {
            const tipoCobroActual = $('#id_tipo_cobro select').val();
            const cobroActual = $('#id_cobro select').val();
            const precio = parseFloat($('#id_precio input').val());


            $.ajax({
                url: "/admin_cont/buscar_items_c",
                data: { id: ui.item.id },
                dataType: 'json',
                success: servicio => {
                    $('#id_precio input').val(servicio.precio).data({
                        iva: servicio.iva,
                        cuenta: servicio.cuenta,
                        codigo: servicio.item,
                        embarque: servicio.embarque,
                        gasto: servicio.gasto
                    });
                    $('#id_descripcion_item input').val(servicio.nombre);
                    $('#id_tipo_cobro select').val(tipoCobroActual);
                    $('#id_cobro select').val(cobroActual);
                    $('#id_precio input').val(precio);
                },
                error: xhr => console.error('Error al obtener los detalles del item:', xhr)
            });
        }
    });

    // Al hacer clic en "Agregar Item" se agrega una nueva fila o se actualiza la fila en edición
    $('#agregarItem').on('click', function() {
        const item = $('#item').val();
        const descripcion = $('#id_descripcion_item input').val();
        const precio = parseFloat($('#id_precio input').val());

        if (item && descripcion && !isNaN(precio)) {
            const iva = $('#id_precio input').data('iva') || "";   // puede estar vacío en un nuevo item
            const cuenta = $('#id_precio input').data('cuenta') || "";
            const codigo = $('#id_precio input').data('codigo') || "";

            // Si hay una fila en edición, se actualiza en lugar de agregar
            if ($("#itemTable tr.editing").length > 0) {
                var $editingRow = $("#itemTable tr.editing");
                // Actualiza los atributos data del <tr>
                $editingRow.data("precio", precio);
                $editingRow.data("iva", iva);
                $editingRow.data("cuenta", cuenta);

                // Actualiza el contenido de cada celda
                $editingRow.find("td").eq(0).text(codigo);
                $editingRow.find("td").eq(1).text(item);
                $editingRow.find("td").eq(2).text(descripcion);
                $editingRow.find("td").eq(3).text(precio.toFixed(2));
                $editingRow.find("td").eq(4).text(iva);
                $editingRow.find("td").eq(5).text(cuenta);

                $editingRow.removeClass("editing");
            }else {
                // Agregar nueva fila
                itemCounter++;
                const rowId = `item-${itemCounter}`;
                const row = `
                    <tr id="${rowId}" data-precio="${precio}" data-iva="${iva}" data-cuenta="${cuenta}">
                        <td style="display:none;">${codigo}</td>
                        <td>${item}</td>
                        <td>${descripcion}</td>
                        <td>${precio.toFixed(2)}</td>
                        <td>${iva}</td>
                        <td>${cuenta}</td>
                        <td>PENDIENTE</td>
                        <td>S/I</td>
                        <td>S/I</td>
                    </tr>`;
                $('#itemTable tbody').append(row);
                $('#itemTable').show();

            }
            $('#eliminarSeleccionados').show();
            $('#clonarItem').css('display','block');
            $('#itemTable').css('visibility', 'visible');
            actualizarTotal();
            $('#totales').show();
            limpiarCampos();
        } else {
            alert('Por favor, completa todos los campos antes de agregar el item.');
        }
    });
    $("#itemTable").on("dblclick", "tr", function() {
        var $row = $(this);
        // Asume que la fila tiene las 6 celdas en el orden correcto
        var codigo = $row.find("td").eq(0).text().trim();    // Código (oculto)
        var item = $row.find("td").eq(1).text().trim();        // Item
        var descripcion = $row.find("td").eq(2).text().trim(); // Descripción
        var precio = $row.find("td").eq(3).text().trim();      // Precio
        var iva = $row.find("td").eq(4).text().trim();         // IVA
        var cuenta = $row.find("td").eq(5).text().trim();      // Cuenta

        // Cargar los datos en los campos de entrada
        $("#item").val(item);
        $("#id_descripcion_item input").val(descripcion);
        $("#id_precio input").val(precio);

        // Guardar datos adicionales en el input de precio (por si se necesitan al actualizar)
        $("#id_precio input").data("iva", iva);
        $("#id_precio input").data("cuenta", cuenta);
        $("#id_precio input").data("codigo", codigo);

        // Marcar la fila como "editing" para que se actualice en lugar de agregar una nueva
        $("#itemTable tr").removeClass("editing");
        $row.addClass("editing");
    });
    // Botón para clonar la fila seleccionada
    $("#clonarItem").on("click", function() {
        var $selected = $("#itemTable tr.table-active");
        if ($selected.length > 0) {
            itemCounter++;
            var $clone = $selected.clone();
            $clone.attr("id", "item-" + itemCounter);
            $clone.removeClass("selected editing");
            $clone.removeClass("table-active");
            $clone.removeClass("table-primary");
            $("#itemTable tbody").append($clone);
            actualizarTotal();
        } else {
            alert("Selecciona una fila para clonar.");
        }
    });

    $('#itemTable tbody').on('click', 'tr', function() {
        $(this).toggleClass('table-active table-primary');
    });

    $('#eliminarSeleccionados').on('click', function() {
        if (confirm('¿Está seguro de que desea eliminar la selección?')) {
            $('#itemTable tbody tr.table-active').remove();
            actualizarTotal();

            if ($('#itemTable tbody tr').length === 0) {
                $('#itemTable').hide();
                $('#eliminarSeleccionados').hide();
                $('#totales').hide();
            }
        }
    });

    $('#facturaForm').submit(function(event) {
        event.preventDefault();
        if (confirm('¿Está seguro de que desea facturar?')) {
            let tipoFac = $('#id_tipo').val();
            let serie = $('#id_serie').val();
            let prefijo = $('#id_prefijo').val();
            let numero = $('#id_numero').val();
            let cliente = $('#cliente').val();
            let fecha = $('#id_fecha_registro').val();
            let paridad = $('#id_paridad').val();
            let arbitraje = $('#id_arbitraje').val();
            let imputar = $('#id_imputar').val();
            let moneda = $('#id_moneda').val();
            let clienteData = {
                codigo: $('#proveedorTable tbody tr td').eq(0).text(),
                empresa: $('#proveedorTable tbody tr td').eq(1).text(),
                rut: $('#proveedorTable tbody tr td').eq(2).text(),
            };

            if (!clienteData.codigo.trim() || !clienteData.empresa.trim() || !clienteData.rut.trim()) {
                alert('Faltan datos del proveedor.');
                return;
            }


            let items = [];
            $('#itemTable tbody tr').each(function() {
                const itemData = {
                    id: $(this).find('td').eq(0).text(),
                    descripcion: $(this).find('td').eq(1).text(),
                    precio: $(this).find('td').eq(3).text(),
                    iva: $(this).find('td').eq(4).text(),
                    cuenta: $(this).find('td').eq(5).text(),
                    posicion: $(this).find('td').eq(7).text(),
                };
                items.push(itemData);
            });
            let data=[];
                data={
                    csrfmiddlewaretoken: csrf_token,
                    fecha: fecha,
                    tipoFac: tipoFac,
                    serie: serie,
                    prefijo: prefijo,
                    numero: numero,
                    cliente: cliente,
                    arbitraje: arbitraje,
                    paridad: paridad,
                    imputar: imputar,
                    moneda: moneda,
                    clienteData: JSON.stringify(clienteData),
                    items: JSON.stringify(items),
                    total:$('#id_total input').val(),
                    iva:$('#id_iva input').val(),
                    neto:$('#id_neto input').val(),
                }
            $.ajax({
                url: "/admin_cont/procesar_factura_proveedor/",
                dataType: 'json',
                type: 'POST',
                data: data,
                headers: { 'X-CSRFToken': csrf_token },
                success: function(data) {
                    $('#proveedoresModal').dialog('close');
                    $('#facturaForm').trigger('reset');
                    total=0;
                    iva=0;
                    neto=0;
                    //window.location.reload();
                },
                error: function(xhr) {
                    console.error('Error al facturar:', xhr);
                    alert('Error al procesar la factura');
                }
            });
        }
    });

    let filaSeleccionada = null;

    // Detectar doble clic en la celda de la columna "Embarque" (índice 7)
    $("#itemTable tbody").on("dblclick", "td:nth-child(7)", function () {
        filaSeleccionada = $(this).closest("tr"); // Guardar la fila completa

        let embarqueValor = $(this).text().trim(); // Obtener el valor de la celda "Embarque"
        let precioValor = filaSeleccionada.find("td:nth-child(4)").text().trim(); // Obtener "Precio"

        // Guardar el precio en localStorage
        localStorage.setItem("precio_item_imputar", precioValor);

        // Colocar el valor en un campo dentro del modal
        $("#modal-embarque #embarque-input").val(embarqueValor);

        // Abrir el modal
        $("#modal-embarque").dialog("open");
    });

    // Botón para cerrar el modal
    $("#cerrar-modal").click(function () {
        $("#modal-embarque").dialog("close");
    });

    function rellenar_tabla() {
    if (!filaSeleccionada || filaSeleccionada.length === 0) {
        alert("No se ha seleccionado ninguna fila para actualizar.");
        return;
    }

    let guardadoFilas = document.querySelectorAll("#guardado-tabla tbody tr");

    if (guardadoFilas.length === 0) {
        alert("No hay registros en la tabla guardado-tabla.");
        return;
    }

    if (guardadoFilas.length === 1) {
        let fila = guardadoFilas[0];
        let posicion = fila.querySelector("td:nth-child(1)")?.textContent.trim() || "";
        let precio = fila.querySelector("td:nth-child(2)")?.textContent.trim() || "";
        let embarque = fila.querySelector("td:nth-child(6)")?.textContent.trim() || "";
        let lugar = fila.querySelector("td:nth-child(5)")?.textContent.trim() || "";
        let cliente = fila.querySelector("td:nth-child(4)")?.textContent.trim() || "";
        let embarqueFinal = embarque + lugar;

        filaSeleccionada.find("td").eq(7).text(posicion);
        filaSeleccionada.find("td").eq(8).text(cliente);
        filaSeleccionada.find("td").eq(6).text(embarqueFinal);

    } else {
        let filaBase = filaSeleccionada.clone();

        filaSeleccionada.remove();

        guardadoFilas.forEach(fila => {
            let posicion = fila.querySelector("td:nth-child(1)")?.textContent.trim() || "";
            let precio = fila.querySelector("td:nth-child(2)")?.textContent.trim() || "";
            let embarque = fila.querySelector("td:nth-child(6)")?.textContent.trim() || "";
            let lugar = fila.querySelector("td:nth-child(5)")?.textContent.trim() || "";
            let cliente = fila.querySelector("td:nth-child(4)")?.textContent.trim() || "";
            let embarqueFinal = embarque + lugar;

            let nuevaFila = filaBase.clone();
            nuevaFila.find("td").eq(7).text(posicion);
            nuevaFila.find("td").eq(8).text(cliente);
            nuevaFila.find("td").eq(6).text(embarqueFinal);
            nuevaFila.find("td").eq(3).text(precio);

            $("#itemTable tbody").append(nuevaFila);
        });
    }

    // Cerramos el modal
    $("#modal-embarque").dialog("close");
    console.log("Tabla actualizada con registros del guardado-tabla.");
}

});

let total=0;
function actualizarPestañas() {
    let radioMasters = document.getElementById("imputar-masters");
    let radioHouses = document.getElementById("imputar-houses");
    let tabMaster = document.querySelector('a[href="#master"]').parentElement;
    let tabHouse = document.querySelector('a[href="#house"]').parentElement;

    // Mostrar todas las pestañas antes de aplicar restricciones
    tabMaster.style.display = "block";
    tabHouse.style.display = "block";

    if (radioMasters.checked) {
        tabMaster.style.display = "none"; // Ocultar Master
        tabHouse.style.display = "none"; // Ocultar Master
    } else if (radioHouses.checked) {
        tabHouse.style.display = "none"; // Ocultar House
    }
}
// Mostrar u ocultar tipo_factura
function verificarTipoFactura() {
    const valorSeleccionado = $('#id_tipo').find('option:selected').val();
    if (valorSeleccionado === 'devolucion_contado') {
        $('#id_tipo_factura').hide();
    } else {
        $('#id_tipo_factura').show();
    }
}
function abrir_modal() {
    $("#proveedoresModal").dialog({
        autoOpen: true,
        modal: true,
        width: wWidth * 0.90,
        height: wHeight * 0.95,
        buttons: [
            {
                class: "btn btn-dark",
                style: "width:100px",
                text: "Salir",
                click: function() {
                    $(this).dialog("close");
                    existe_cliente=false;
                    resetModal("#proveedoresModal");
                }
            }
        ]
    }).prev('.ui-dialog-titlebar').remove();
    $.ajax({
        url: "/admin_cont/cargar_arbitraje/",
        type: "GET",
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
function resetModal(modalId) {
    const modal = $(modalId);

    // Reinicia el formulario
    modal.find("form").each(function () {
        this.reset();
    });

    // Limpia tablas
    modal.find("table").each(function () {
        if ($.fn.DataTable.isDataTable(this)) {
            $(this).DataTable().clear().draw();
        } else {
            $(this).find("tbody").empty();
        }
    });
}
function limpiarCampos() {
    $('#item').val('');
    $('#id_descripcion_item input').val('');
    $('#id_precio input').val('');
}
// Función para mostrar u ocultar el campo proveedor2
function toggleProveedor2() {
        if ($('#id_tercerizado').is(':checked')) {
            $('#proveedor2').show();
        } else {
            $('#proveedor2').hide();
        }
}
function actualizarTotal() {
    let neto = 0;
    let total = 0; // Inicializar total aquí

    $('#itemTable tbody tr').each(function() {
        const precio = parseFloat($(this).data('precio')) || 0;
        neto += precio;
        console.log($(this));
    });

    $('#id_neto input').val(neto.toFixed(2)).prop('readonly', true);

    $('#itemTable tbody tr').each(function() {
        const precio = parseFloat($(this).data('precio')) || 0;
        const iva = $(this).data('iva');

        // Calcular el precio final con IVA
        const precioFinal = iva === 'Basico' ? precio * 1.22 : precio;
        total += precioFinal;

    });

    $('#id_total input').val(total.toFixed(2)).prop('readonly', true);

    const iva_t = total - neto;
    $('#id_iva input').val(iva_t.toFixed(2)).prop('readonly', true);
}
$('#abrir_arbi_prov').on('click', function (event) {
    $("#arbitraje_modal").dialog({
        autoOpen: true,
        modal: true,
        title: "Cargar un arbitraje para el día de hoy",
        height: 300,
        width: 500,
        position: { my: "top", at: "top+20", of: window },
        buttons: [
            {
                text: "Guardar",
                class: "btn btn-primary",
                style: "width:100px",
                click: function () {
                    let arbDolar = $('#valor_arbitraje').val();
                    let parDolar = $('#valor_paridad').val();
                    let tipoMoneda = $('#moneda_select').val();
                    let pizDolar = $('#valor_pizarra').val();
                    let fecha = $('#fecha_arbi').val();

                    $.ajax({
                        url: "/admin_cont/guardar_arbitraje/",
                        dataType: 'json',
                        type: 'POST',
                        headers: { 'X-CSRFToken': csrf_token },
                        data: {
                            arbDolar: arbDolar,
                            parDolar: parDolar,
                            tipoMoneda: tipoMoneda,
                            pizDolar: pizDolar,
                            fecha:fecha
                        },
                        success: function(data) {
                            if(data['status'].length == 0){
                                alert("Valores guardados correctamente");
                                $("#arbitraje_modal").dialog("close");
                            }else{
                                alert(data['status']);
                            }
                        },
                        error: function(xhr, status, error) {
                            alert("Error al guardar los datos: " + error);
                        }
                    });
                },
            },
            {
                text: "Salir",
                class: "btn btn-dark",
                style: "width:100px",
                click: function () {
                    $(this).dialog("close");
                },
            },
        ],
    });
        const hoy = new Date().toISOString().split('T')[0];
    // Establecer el valor predeterminado del campo de fecha
    document.getElementById('fecha_arbi').value = hoy;
        $.ajax({
        url: "/admin_cont/cargar_arbitraje/",
        type: "GET",
        dataType: "json",
        success: function (data) {
            // Cargar los valores en los campos
            $('#valor_arbitraje').val(data.arbitraje);
            $('#valor_pizarra').val(data.pizarra);
            $('#valor_paridad').val(data.paridad);
            $('#moneda_select').val(data.moneda);
        },
        error: function (xhr, status, error) {
            alert("Error al cargar los datos iniciales: " + error);
        }
    });
});
function actualizarFechas(origen, destino) {
    let fechaSeleccionada = $(origen).val();
    if (fechaSeleccionada) {
        $(destino).val(fechaSeleccionada);
    }
}