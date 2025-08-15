var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;
let filaSeleccionada = null;
let modoImputacionIndividual = false;
let mismaPosicionTodos = false;
$(document).ready(function() {

    const $iva = $('#id_iva');
    const $neto = $('#id_neto');
    const $total = $('#id_total');

    // Cuando se hace clic en "Ajustar IVA"
    $('#ajustarIVA').on('click', function () {
        $iva.prop('readonly', false);
        $iva.focus();
    });

    // Cuando se pierde el foco del campo IVA
    $iva.on('blur', function () {
        $iva.prop('readonly', true);
        recalcularTotalAjuste();
    });

    // Función para recalcular el total
    function recalcularTotalAjuste() {
        const iva = parseFloat($iva.val()) || 0;
        const neto = parseFloat($neto.val()) || 0;
        const total = neto + iva;
        $total.val(total.toFixed(2));
    }

    var buscar = '';
    var que_buscar = '';
    let contador = 0;

    $("#impucompra_nota").dialog({
        autoOpen: false,
        resizable: false,
        draggable: true,
        width: "auto",
        height: "auto",
        maxWidth: $(window).width() * 0.90,
        minWidth: 600,
        maxHeight: $(window).height() * 0.90,
        modal: true,
        position: { my: "center", at: "center", of: window },
        open: function () {
            resetModal("#impucompra_nota");
            $(this).dialog("option", "width", "auto");
            $(this).dialog("option", "height", "auto");
            $(this).dialog("option", "position", { my: "center", at: "center", of: window });
        },
         buttons: [
        {
            class: "btn btn-primary btn-sm",
            text: "Cerrar y finalizar factura",
            click: function() {
                guardar_factura();
                $(this).dialog("close");
            }
        }
    ],
    });

    // Selección de filas en la tabla
    $("#tabla-impucompra tbody").on("click", "tr", function () {
        $(this).toggleClass("table-secondary");
        actualizarMonto();
    });
    //boton de imputar
    $("#btn-imputar").on("click", function () {
        let montoDisponible = parseFloat($("#monto-imputar").val()) || 0;
        let saldoRestante = montoDisponible;

        // Recuperar el localStorage actual para no sobrescribir
        let facturasGuardadas = JSON.parse(localStorage.getItem("facturas_impucompra")) || [];

        // Recorremos solo las filas seleccionadas
        $("#tabla-impucompra tbody tr.table-secondary").each(function () {
            let idFactura = $(this).find("td:nth-child(1)").text().trim(); // ID autogenerado (columna oculta)
            let saldoFactura = parseFloat($(this).find("td:nth-child(6)").text().replace(",", ".")) || 0; // Columna 5
            let montoImputado = 0;

            if (saldoRestante > 0) {
                if (saldoRestante >= saldoFactura) {
                    montoImputado = saldoFactura;
                    saldoRestante -= saldoFactura;
                    saldoFactura = 0; // La factura queda totalmente imputada
                } else {
                    montoImputado = saldoRestante;
                    saldoFactura -= saldoRestante;
                    saldoRestante = 0; // Ya no hay saldo disponible
                }

                // Guardar el monto imputado en la celda de la columna 7 y aplicar color de fondo
                let celdaImputado = $(this).find("td:nth-child(7)");
                celdaImputado.text(montoImputado.toFixed(2));
                celdaImputado.css("background-color", "#fcec3f"); // Aplicar color amarillo

                // Guardar la factura imputada en el array, evitando duplicados
                let facturaExistente = facturasGuardadas.find(f => f.autogenerado === idFactura);
                if (facturaExistente) {
                    facturaExistente.monto_imputado = montoImputado.toFixed(2);
                } else {
                    facturasGuardadas.push({
                        autogenerado: idFactura,
                        monto_imputado: montoImputado.toFixed(2),
                    });
                }

                // Actualizar la celda de saldo restante en la columna 5
                $(this).find("td:nth-child(6)").text(saldoFactura.toFixed(2));

                // Quitar la clase `table-secondary` después de imputar
                $(this).removeClass("table-secondary");
            }
        });

        // Guardar el saldo restante en localStorage
        localStorage.setItem("saldo_nota_credito_compra", saldoRestante.toFixed(2));

        // Guardar las facturas imputadas en localStorage sin sobrescribir los datos previos
        localStorage.setItem("facturas_impucompra", JSON.stringify(facturasGuardadas));

        // Actualizar el monto a imputar con el saldo restante
        $("#monto-imputar").val(saldoRestante.toFixed(2));

        // Deshabilitar el botón si ya no hay saldo disponible
        $("#btn-imputar").prop("disabled", saldoRestante === 0);

        actualizarImputado();

    });

    $("#cerrar-modal").on("click", function () {
        $("#impucompra_nota").dialog("close");
    });


    let radioMasters = document.getElementById("imputar-masters");
    let radioHouses = document.getElementById("imputar-houses");

    radioMasters.addEventListener("change", actualizarPestañas);
    radioHouses.addEventListener("change", actualizarPestañas);

    actualizarPestañas();

    verificarTipoFactura();

    $("#modal-embarque").dialog({
        autoOpen: false,
        open: function () {
            if (modoImputacionIndividual) {
                $("#guardarCerrar").hide();
                $("#guardarImputacion").show();
            } else {
                $("#guardarCerrar").show();
                $("#guardarImputacion").hide();
            }
        },
        width: "auto",
        height: "auto",
        maxWidth: $(window).width() * 0.90,
        minWidth: 600,
        maxHeight: $(window).height() * 0.90,
        modal: true,
        position: { my: "center top", at: "center top+20", of: window },
        create: function () {
            var $buttons = $(this).parent().find(".ui-dialog-buttonpane button");
            $buttons.eq(0).addClass("btn btn-warning");
            $buttons.eq(1).addClass("btn btn-success").attr("id", "guardarCerrar");
            $buttons.eq(2).addClass("btn btn-dark");

            const $guardarParcial = $('<button>', {
                text: 'Continuar',
                class: 'btn btn-success',
                id: 'guardarImputacion',
                click: function () {
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
                    rellenar_tabla_sin_guardar();
                }
            });

            $guardarParcial.insertBefore($buttons.eq(2));
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
               // $(this).dialog("close");
            },
            "Cancelar": function () {
                $(this).dialog("close");
            }
        },
        beforeClose: function(event, ui) {
        limpiarModalEmbarque();
    }
    }).prev('.ui-dialog-titlebar').remove();


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
    document.querySelectorAll(".buscador").forEach(button => {
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
        if ($(this).val()) {
            cargar_arbitraje();
        }
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
                "targets": 0,  // Columna 0 (se mantiene pero oculta su contenido)
                "className": "",
                "searchable": false,
                "visible": true,
               render: function (data, type, row) {
                    return `<span class="badge bg-warning text-dark">${row[0] ?? ''}</span>`;
                }
            },
        {
            "targets": 1,  // Oculta completamente la columna 1
            "visible": false,
            "searchable": false
        },
                    {
                "targets": [6,7,8],
                "className": "text-end",
            },
        {
            "targets": 2,
            "type": "date-iso",
            "orderable": true
        }
    ],
    "columns": [
        { "visible": true },
        { "visible": false },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "visible": false },
        { "visible": false }
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
            var api = this.api();
            api.columns().every(function () {
                var that = this;
                $('.filter-input', this.footer()).on('keyup change', function () {
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
        appendTo: "#proveedoresModal",
        select: function(event, ui) {
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
                        gasto: servicio.gasto,
                        imputar: servicio.imputar,
                    });
                    $('#id_descripcion_item input').val(servicio.nombre);
                    $('#id_cobro select').val(cobroActual);
                    $('#id_precio input').val(precio);
                    $('#iva_item').val(servicio.iva);

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
    if(precio == 0 || precio == null){
        alert('Digite un precio');
        return;
    }
    if (item && descripcion && !isNaN(precio)) {
        const iva = $('#id_precio input').data('iva') || "";
        const cuenta = $('#id_precio input').data('cuenta') || "";
        const codigo = $('#id_precio input').data('codigo') || "";
        const imputar = $('#id_precio input').data('imputar') || "";
        let texto = (imputar === 'S') ? 'PENDIENTE' : 'NO IMPUTABLE';

        let montoIva, totalConIva;
        if (iva === 'Básico') {
            montoIva = precio * 0.22;
        } else {
            montoIva = 0;
        }
        totalConIva = precio + montoIva;

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
            $editingRow.find("td").eq(4).text(montoIva.toFixed(2));     // NUEVO
            $editingRow.find("td").eq(5).text(totalConIva.toFixed(2));  // NUEVO
            $editingRow.find("td").eq(6).text(iva);
            $editingRow.find("td").eq(7).text(cuenta);
            $editingRow.find("td").eq(8).text(texto);

            $editingRow.removeClass("editing");
        } else {
            // Agregar nueva fila
            itemCounter++;
            const rowId = `item-${itemCounter}`;
            const row = `
                <tr id="${rowId}" data-precio="${precio}" data-iva="${iva}" data-cuenta="${cuenta}">
                    <td style="display:none;">${codigo}</td>
                    <td>${item}</td>
                    <td>${descripcion}</td>
                    <td>${precio.toFixed(2)}</td>
                    <td>${montoIva.toFixed(2)}</td>      <!-- NUEVO -->
                    <td>${totalConIva.toFixed(2)}</td>   <!-- NUEVO -->
                    <td>${iva}</td>
                    <td>${cuenta}</td>
                    <td>${texto}</td>
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
        limpiarCampos();
    } else {
        alert('Por favor, completa todos los campos antes de agregar el item.');
    }
});

    $("#itemTable").on("dblclick", "tr", function() {
        let colIndex = $(e.target).closest('td').index();
        if (colIndex === 8) {
            return;
        }

        var $row = $(this);
        // Asume que la fila tiene las 6 celdas en el orden correcto
        var codigo = $row.find("td").eq(0).text().trim();    // Código (oculto)
        var item = $row.find("td").eq(1).text().trim();        // Item
        var descripcion = $row.find("td").eq(2).text().trim(); // Descripción
        var precio = $row.find("td").eq(3).text().trim();      // Precio
        var iva = $row.find("td").eq(6).text().trim();         // IVA
        var cuenta = $row.find("td").eq(7).text().trim();      // Cuenta

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
    $(document).on('click', function (e) {
            // Verificamos si el click fue fuera de la tabla
            if (!$(e.target).closest('#itemTable').length) {
                $('#itemTable tbody tr.table-primary').removeClass('table-primary');
            }
        });

    $('#itemTable tbody').on('click', 'tr', function() {
        $('#itemTable tbody tr').removeClass('table-active table-primary');

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



    // Detectar doble clic en la celda de la columna "Embarque" (índice 7)
    $("#itemTable tbody").on("dblclick", "td:nth-child(9)", function () {
        filaSeleccionada = $(this).closest("tr");

        let embarqueValor = $(this).text().trim();
        if (embarqueValor==='PENDIENTE'){
            let precioValor = filaSeleccionada.find("td:nth-child(4)").text().trim();
            localStorage.setItem("precio_item_imputar", precioValor);
            modoImputacionIndividual = true;
            $("#modal-embarque").dialog("open");
        }
    });

    // Botón para cerrar el modal
    $("#cerrar-modal").click(function () {
        $("#modal-embarque").dialog("close");
    });

    function rellenar_tabla_old() {
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
        let embarqueFinal = embarque + ' ' + lugar;

        //filaSeleccionada.find("td").eq(3).text(precio);           // Precio
        filaSeleccionada.find("td").eq(8).text(embarqueFinal);    // Embarque
        filaSeleccionada.find("td").eq(9).text(posicion);         // Posición
        filaSeleccionada.find("td").eq(10).text(cliente);         // Socio Comercial

    } else {
       let filaBase = filaSeleccionada.clone();
        filaSeleccionada.remove();

        guardadoFilas.forEach(fila => {
            let posicion = fila.querySelector("td:nth-child(1)")?.textContent.trim() || "";
            let precio = fila.querySelector("td:nth-child(2)")?.textContent.trim() || "";
            let embarque = fila.querySelector("td:nth-child(6)")?.textContent.trim() || "";
            let lugar = fila.querySelector("td:nth-child(5)")?.textContent.trim() || "";
            let cliente = fila.querySelector("td:nth-child(4)")?.textContent.trim() || "";
            let embarqueFinal = embarque + ' ' + lugar;

            let nuevaFila = filaBase.clone();
            nuevaFila.find("td").eq(3).text(precio);             // Precio
            nuevaFila.find("td").eq(8).text(embarqueFinal);      // Embarque
            nuevaFila.find("td").eq(9).text(posicion);           // Posición
            nuevaFila.find("td").eq(10).text(cliente);           // Socio Comercial

            $("#itemTable tbody").append(nuevaFila);
        });

    }

    // Cerramos el modal
    $("#modal-embarque").dialog("close");
    guardar_factura();
}

    function rellenar_tabla() {
    let guardadoFilas = document.querySelectorAll("#guardado-tabla tbody tr");

    if (guardadoFilas.length === 0) {
        alert("No hay registros en la tabla guardado-tabla.");
        return;
    }

    let posicion = guardadoFilas[0].querySelector("td:nth-child(1)")?.textContent.trim() || "";
    let precio = guardadoFilas[0].querySelector("td:nth-child(2)")?.textContent.trim() || "";
    let embarque = guardadoFilas[0].querySelector("td:nth-child(6)")?.textContent.trim() || "";
    let lugar = guardadoFilas[0].querySelector("td:nth-child(5)")?.textContent.trim() || "";
    let cliente = guardadoFilas[0].querySelector("td:nth-child(4)")?.textContent.trim() || "";
    let embarqueFinal = embarque + ' ' + lugar;

    if (mismaPosicionTodos) {
        // MODO GLOBAL: aplicar a todas las filas con estado 'PENDIENTE'
        $('#itemTable tbody tr').each(function () {
            let fila = $(this);
            let estado = fila.find('td:nth-child(9)').text().trim();
            if (estado.toUpperCase() === 'PENDIENTE') {
                fila.find("td").eq(8).text(embarqueFinal);   // Embarque
                fila.find("td").eq(9).text(posicion);        // Posición
                fila.find("td").eq(10).text(cliente);        // Socio Comercial
            }
        });
    } else {
        // MODO INDIVIDUAL
        if (!filaSeleccionada || filaSeleccionada.length === 0) {
            alert("No se ha seleccionado ninguna fila para actualizar.");
            return;
        }

        if (guardadoFilas.length === 1) {
            filaSeleccionada.find("td").eq(8).text(embarqueFinal);
            filaSeleccionada.find("td").eq(9).text(posicion);
            filaSeleccionada.find("td").eq(10).text(cliente);
        } else {
            let filaBase = filaSeleccionada.clone();
            filaSeleccionada.remove();

            guardadoFilas.forEach(fila => {
                let pos = fila.querySelector("td:nth-child(1)")?.textContent.trim() || "";
                let pre = fila.querySelector("td:nth-child(2)")?.textContent.trim() || "";
                let emb = fila.querySelector("td:nth-child(6)")?.textContent.trim() || "";
                let lug = fila.querySelector("td:nth-child(5)")?.textContent.trim() || "";
                let cli = fila.querySelector("td:nth-child(4)")?.textContent.trim() || "";
                let embFinal = emb + ' ' + lug;

                let nuevaFila = filaBase.clone();
                nuevaFila.find("td").eq(3).text(pre);          // Precio
                nuevaFila.find("td").eq(8).text(embFinal);     // Embarque
                nuevaFila.find("td").eq(9).text(pos);          // Posición
                nuevaFila.find("td").eq(10).text(cli);         // Socio Comercial

                $("#itemTable tbody").append(nuevaFila);
            });
        }
    }

    $("#modal-embarque").dialog("close");
    guardar_factura();
}

    function rellenar_tabla_sin_guardar() {
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
        let embarqueFinal = embarque + ' ' + lugar;

        //filaSeleccionada.find("td").eq(3).text(precio);           // Precio
        filaSeleccionada.find("td").eq(8).text(embarqueFinal);    // Embarque
        filaSeleccionada.find("td").eq(9).text(posicion);         // Posición
        filaSeleccionada.find("td").eq(10).text(cliente);         // Socio Comercial

    } else {
       let filaBase = filaSeleccionada.clone();
        filaSeleccionada.remove();

        guardadoFilas.forEach(fila => {
            let posicion = fila.querySelector("td:nth-child(1)")?.textContent.trim() || "";
            let precio = fila.querySelector("td:nth-child(2)")?.textContent.trim() || "";
            let embarque = fila.querySelector("td:nth-child(6)")?.textContent.trim() || "";
            let lugar = fila.querySelector("td:nth-child(5)")?.textContent.trim() || "";
            let cliente = fila.querySelector("td:nth-child(4)")?.textContent.trim() || "";
            let embarqueFinal = embarque + ' ' + lugar;

            let nuevaFila = filaBase.clone();
            nuevaFila.find("td").eq(3).text(precio);             // Precio
            nuevaFila.find("td").eq(8).text(embarqueFinal);      // Embarque
            nuevaFila.find("td").eq(9).text(posicion);           // Posición
            nuevaFila.find("td").eq(10).text(cliente);           // Socio Comercial

            $("#itemTable tbody").append(nuevaFila);
        });

    }

    // Cerramos el modal
    $("#modal-embarque").dialog("close");
}

    $("#tabla_proveedoresygastos tbody").on("dblclick", "tr", function () {
        const row = $('#tabla_proveedoresygastos').DataTable().row(this).data();
        const autogenerado = row[1];
        const nrocliente = row[9];
        const numero = row[10];


        $("#autogen_detalle_compra").val(autogenerado);
        buscar_gastos(autogenerado);
        buscar_ordenes(nrocliente, numero, autogenerado);
        cargarImputacionesCompra(autogenerado);

        $("#modalDetalleCompra").dialog({
          modal: true,
          width: '80%',
          height: 'auto',
          position: { my: "center top", at: "center top+20", of: window },
            autoOpen: true,
        });
    });

    $("#tabla_proveedoresygastos tbody").on("click", "tr", function () {
        $("#tabla_proveedoresygastos tbody tr").removeClass("table-secondary");
        $(this).addClass("table-secondary");
    });


});
function procesar_factura(){
        let tipo= $("#id_tipo").val();
        if(tipo==41){
            if(confirm('¿Desea imputar esta Nota?')){
                $("#impucompra_nota").dialog('open');
                let cliente = $('#proveedorTable tbody tr td').eq(0).text();
                $('#monto-imputar').val( $('#id_total').val());
                localStorage.removeItem('facturas_impucompra');
                cargar_facturas_imputacion(cliente);
                return;
            }else{

                guardar_factura();
            }
        }else{
            guardar_factura();
        }

}
function guardar_factura(){
    let pendientes = [];

    $('#itemTable tbody tr').each(function () {
        const estado = $(this).find('td:nth-child(9)').text().trim().toUpperCase();
        if (estado === 'PENDIENTE') {
            pendientes.push($(this));
        }
    });

    if (pendientes.length > 0) {
        if (pendientes.length === 1) {
            // Solo uno pendiente → Imputar directamente
            filaSeleccionada = pendientes[0];
            let precio = filaSeleccionada.find("td:nth-child(4)").text().trim();
            localStorage.setItem("precio_item_imputar", precio);
            modoImputacionIndividual = false;
            $("#modal-embarque").dialog("open");
            return;
        } else {
            // Varios pendientes → Consultar al usuario
            if (confirm("Se encontraron varios ítems sin imputar.\n¿Desea imputar el total completo a un solo embarque?\n(Si elige 'Cancelar', se imputará individualmente de a uno)")) {
                // Imputar total
                let total = $('#id_total').val();
                localStorage.setItem("precio_item_imputar", total);
                modoImputacionIndividual = false;
                mismaPosicionTodos=true;
                $("#modal-embarque").dialog("open");
                return;
            } else {
                // Imputar de a uno → tomar el precio del primero
                filaSeleccionada = pendientes[0];
                let precio = filaSeleccionada.find("td:nth-child(4)").text().trim();
                localStorage.setItem("precio_item_imputar", precio);
                modoImputacionIndividual = true;
                $("#modal-embarque").dialog("open");
                return;
            }
        }
    }
    if (!confirm('¿Está seguro de que desea guardar?')) {
        return;
    }

    let tipoFac = $('#id_tipo').val();
    let serie = $('#id_serie').val();
    let detalle = $('#id_detalle_ingreso_compra').val();
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
            id: $(this).find('td').eq(0).text().trim(),
            descripcion: $(this).find('td').eq(2).text().trim(),
            precio: $(this).find('td').eq(3).text().trim(),
            iva: $(this).find('td').eq(4).text().trim(),
            cuenta: $(this).find('td').eq(7).text().trim(),
            posicion: $(this).find('td').eq(9).text().trim(),
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
            detalle: detalle,
            numero: numero,
            cliente: cliente,
            arbitraje: arbitraje,
            paridad: paridad,
            imputar: imputar,
            moneda: moneda,
            saldo_nota_cred: localStorage.getItem('saldo_nota_credito_compra') || null,
            clienteData: JSON.stringify(clienteData),
            facturas_imputadas:localStorage.getItem('facturas_impucompra') || "[]",
            items: JSON.stringify(items),
            total:$('#id_total').val(),
            iva:$('#id_iva').val(),
            neto:$('#id_neto').val(),
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
function actualizarMonto() {
        let total = 0;
        $("#tabla-impucompra tbody tr.table-secondary").each(function () {
            let monto = parseFloat($(this).find("td:nth-child(6)").text().replace(",", ".")) || 0;
            total += monto;
        });

        $("#se-imputaran").val(total.toFixed(2));

        $("#btn-imputar").prop("disabled", total === 0);
    }
function actualizarImputado() {
        let totalImputado = 0;

        // Recorre solo las filas que tienen un imputado mayor a 0
        $("#tabla-impucompra tbody tr").each(function () {
            let celdaImputado = $(this).find("td:nth-child(7)");
            let monto = parseFloat(celdaImputado.text().replace(",", ".")) || 0;

            if (monto > 0) {
                totalImputado += monto;
                celdaImputado.css("background-color", "#fcec3f"); // Mantener el color amarillo
            }
        });

        // Actualiza el input `#se-imputaran` con el total imputado
        $("#se-imputaran").val(totalImputado.toFixed(2));
    }
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
    resizable: false,
    draggable: true,
    maxWidth: $(window).width() * 0.90,
    maxHeight: $(window).height() * 0.90,
    minWidth: 500,
    minHeight: 200,
    dialogClass: "custom-dialog",
    buttons: [
        {
            class: "btn btn-dark btn-sm",
            style: "width:90px; height:30px; font-size:14px;",
            text: "Salir",
            click: function() {
                $(this).dialog("close");
                existe_cliente = false;
            }
        }
    ],
    open: function() {
        // 🔹 Ajustar el tamaño dinámicamente según el contenido
        $(this).dialog("option", "width", "auto");
        $(this).dialog("option", "height", "auto");
        $(this).dialog("option", "position", { my: "center", at: "center", of: window });
    },
    beforeClose: function(event, ui) {
        limpiarModalProveedor();
        window.location.reload();
    }
}).prev('.ui-dialog-titlebar').remove();
cargar_arbitraje();
//traer_proximo_numero();
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
function limpiarModalProveedor() {
        // Limpiar todos los inputs dentro del formulario
        $('#facturaForm').trigger('reset');
        // Ocultar y vaciar la tabla del proveedor
        $('#proveedorTable').hide();
        $('#proveedorTable tbody').empty();
        // Vaciar la tabla de ítems
        $('#itemTable tbody').empty();
        // Ocultar botones condicionales
        $('#eliminarSeleccionados').hide();
        $('#clonarItem').hide();
    }
function limpiarModalEmbarque() {
    // Limpiar todos los inputs (texto, número, fecha) y selects dentro del modal
    $("#modal-embarque").find("input[type='text'], input[type='number'], input[type='date'], textarea").val("");
    $("#modal-embarque").find("select").prop("selectedIndex", 0);

    // Desmarcar todos los radio buttons
    $("#modal-embarque").find("input[type='radio']").prop("checked", false);

    // Limpiar los spans y campos ocultos de la sección de "Seleccionado"
    $("#seleccionado-embarque").text("");
    $("#seleccionado-tipo").text("");
    $("#seleccionado-posicion").text("");
    $("#seleccionado-precio").val("0.00");
    $("#seleccionado-cliente").val("");
    $("#seleccionado-lugar").val("");

    // Limpiar la tabla de información lateral
    $("#guardado-tabla tbody").empty();

    // Limpiar la tabla de embarques (dentro de #tabla-embarque-container)
    $("#tabla-embarque-container table tbody").empty();
}
function limpiarCampos() {
    $('#item').val('');
    $('#id_descripcion_item input').val('');
    $('#id_precio input').val('');
    $('#iva_item').val('');

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
    });

    $('#id_neto').val(neto.toFixed(2)).prop('readonly', true);

    $('#itemTable tbody tr').each(function() {
        const precio = parseFloat($(this).data('precio')) || 0;
        const iva = $(this).data('iva');

        // Calcular el precio final con IVA
        const precioFinal = iva === 'Básico' ? precio * 1.22 : precio;
        total += precioFinal;

    });

    $('#id_total').val(total.toFixed(2)).prop('readonly', true);

    const iva_t = total - neto;
    $('#id_iva').val(iva_t.toFixed(2)).prop('readonly', true);
}
$('#abrir_arbi').on('click', function (event) {
    $("#arbitraje_modal").dialog({
        autoOpen: true,
        modal: true,
        title: "Cargar un arbitraje para el día de hoy",
        height: 'auto',
        width: 'auto',
        position: { my: "top", at: "top+20", of: window },
        buttons: [
            {
                text: "Guardar",
                class: "btn btn-primary btn-sm",
                style: "",
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
                class: "btn btn-dark btn-sm",
                style: "",
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
        data: { fecha: hoy },
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
function traer_proximo_numero(){
     $.ajax({
        url: "/admin_cont/obtener_proximo_mboleta_compra/",
        method: "GET",
        success: function (data) {
            if (data.proximo_mboleta) {
                $('#id_numero').val(data.proximo_mboleta);  // Cambiá el ID si es otro
            }
        },
        error: function (xhr) {
            console.error("No se pudo obtener el número de boleta:", xhr.responseText);
        }
    });
}

function cargar_facturas_imputacion(nrocliente) {
    $.ajax({
        url: "/admin_cont/cargar_pendientes_imputacion/",
        type: "GET",
        data: { nrocliente: nrocliente },
        success: function (response) {
            let tbody = $("#tabla-impucompra tbody");
            tbody.empty();

            response.data.forEach(item => {
                let fila = `
                    <tr data-id="${item.autogenerado}">
                        <td style="display: none;">${item.autogenerado}</td>
                        <td>${item.vto}</td>
                        <td>${item.emision}</td>
                        <td>${item.num_completo}</td>
                        <td>${item.total.toFixed(2)}</td>
                        <td>${item.saldo.toFixed(2)}</td>
                        <td>${item.imputado.toFixed(2)}</td>
                        <td>${item.tipo_cambio.toFixed(2)}</td>
                        <td>${item.detalle}</td>
                    </tr>
                `;
                tbody.append(fila);
            });
        },
        error: function (xhr) {
            alert("Error al cargar las facturas: " + xhr.responseJSON.error);
        }
    });
}

function buscar_gastos(autogenerado){
    $.ajax({
      url: '/admin_cont/detalle_compra/',
      method: 'GET',
      data: {
        autogenerado: autogenerado
      },
      success: function(response) {
        if (response.success) {
          const data = response.data;
          $('#id_prefijo_detalle').val(data.prefijo);
          $('#id_serie_detalle').val(data.serie);
          $('#numero_detalle_compra').val(data.numero);
          $('#id_tipo_detalle').val(data.tipo);
          $('#id_moneda_detalle_compra').val(data.moneda);
          $('#id_fecha_detalle_compra').val(data.fecha);
          $('#id_fecha_ingreso').val(data.fecha_ingreso);
          $('#id_fecha_vencimiento').val(data.fecha_vencimiento);
          $('#id_proveedor_detalle').val(data.proveedor);
          $('#nro_prov').val(data.nroproveedor);
          $('#id_detalle_detalle_compra').val(data.detalle);

        $('#id_paridad_detalle_compra').val(parseFloat(data.paridad || 0).toFixed(2));
        $('#id_arbitraje_detalle_compra').val(parseFloat(data.arbitraje || 0).toFixed(2));
        $('#id_total_detalle').val(parseFloat(data.total || 0).toFixed(2));
        $('#id_imputable').val(parseFloat(data.imputable || 0).toFixed(2));

            if (data.items && data.items.length > 0) {
              $('#tablaItems').empty();

              data.items.forEach(function(item) {
                const fila = `
                  <tr>
                    <td>${item.concepto || ''}</td>
                    <td>${item.nombre || ''}</td>
                    <td class="text-right">${item.precio != null ? parseFloat(item.precio).toFixed(2) : ''}</td>
                    <td class="text-right">${item.iva != null ? parseFloat(item.iva).toFixed(2) : ''}</td>
                    <td>${item.embarque || ''}</td>
                    <td>${item.posicion || ''}</td>
                  </tr>
                `;
                $('#tablaItems').append(fila);
              });
            } else {
              // Si no hay items, opcionalmente podés mostrar una fila vacía o un mensaje
              $('#tablaItems').html('<tr><td colspan="6" class="text-center text-muted">Sin ítems asociados.</td></tr>');
            }

        }
      },
      error: function(xhr) {
        alert("No se pudo obtener el detalle de la compra.");
      }
    });
}
function buscar_ordenes(cliente,numero,autogenerado){

        if (!cliente || !numero || !autogenerado) {
            alert('Faltan datos');
            return;
        }

        $.ajax({
            url: '/admin_cont/buscar_ordenes_por_boleta/',  // Cambia esto por tu URL real
            type: 'GET',
            data: {
                cliente: cliente,
                numero: numero,
                autogenerado: autogenerado
            },
            success: function(response) {
                let tbody = $('#tabla_pago_factura tbody');
                tbody.empty();

                if (response.resultados.length === 0) {
                    tbody.append('<tr><td colspan="4">No se encontraron resultados</td></tr>');
                } else {
                    $.each(response.resultados, function(i, orden) {
                        let row = `
                            <tr>
                                <td class="oculto">${orden.autogenerado}</td>
                                <td>${orden.nro_documento}</td>
                                <td>${orden.fecha}</td>
                                <td>${orden.monto}</td>
                                <td>${orden.tipo}</td>
                            </tr>
                        `;
                        tbody.append(row);
                    });
                }
            },
            error: function(xhr) {
                console.error(xhr.responseText);
                alert('Error al buscar órdenes');
            }
        });
}
function cargarImputacionesCompra(autogen) {
    $.ajax({
        url: '/admin_cont/obtener_imputados_compra/',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ autogen: autogen }),
        headers: {
            'X-CSRFToken': csrf_token  // Asegurate que esta variable exista
        },
        success: function (data) {
            const tbody = document.getElementById('tablaImputaciones');
            tbody.innerHTML = '';  // Limpiar tabla

            if (data.documentos && data.documentos.length > 0) {
                data.documentos.forEach(function (doc) {
                    const fila = document.createElement('tr');
                    fila.innerHTML = `
                        <td class="oculto">${doc.autogenerado}</td>
                        <td>${doc.documento}</td>
                        <td>${doc.imputado}</td>
                    `;
                    tbody.appendChild(fila);
                });
            } else {
                const fila = document.createElement('tr');
                fila.innerHTML = `<td colspan="3" class="text-center">No se encontraron imputaciones.</td>`;
                tbody.appendChild(fila);
            }
        },
        error: function (xhr, status, error) {
            console.error('Error al cargar imputaciones:', error);
        }
    });
}

function cargar_arbitraje() {
    const fecha = $('#id_fecha_registro').val();

    $.ajax({
        url: "/admin_cont/cargar_arbitraje/",
        type: "GET",
        data: { fecha: fecha },
        dataType: "json",
        success: function (data) {
            $('#id_arbitraje').val(data.arbitraje);
            $('#id_paridad').val(data.paridad);
        },
        error: function (xhr, status, error) {
            alert("Error al cargar los datos iniciales: " + error);
        }
    });
}