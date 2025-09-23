let table_fac;

$(document).ready(function () {


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

    let total = 0;
    let neto = 0;
    let iva = 0;

    var buscar = '';
    var que_buscar = '';

    $('#id_fecha').on('change', function () {
            if ($(this).val()) {
                cargar_arbitraje();
            }
        });

    const valorInicial = $('#id_tipo').find('option:selected').text();
    $('#tipoSeleccionado').text(valorInicial);

    $('#id_tipo').change(function () {
        const valorSeleccionado = $(this).find('option:selected').text();
        $('#tipoSeleccionado').text(valorSeleccionado);
    });

    $('#cliente').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "/admin_cont/buscar_cliente",
                dataType: 'json',
                data: {term: request.term},
                success: function (data) {
                    response(data.map(cliente => ({
                        label: cliente.text,
                        value: cliente.text,
                        id: cliente.id
                    })));
                },
                error: xhr => console.error('Error al buscar clientes:', xhr)
            });
        },
        minLength: 2,
        appendTo: "#facturaM",
        select: function (event, ui) {
            const {id} = ui.item;
            $.ajax({
                url: "/admin_cont/buscar_clientes",
                data: {id},
                dataType: 'json',
                success: cliente => {
                    const row = `
                        <tr id="cliente-${id}">
                            <td class="d-none">${cliente.codigo}</td>
                            <td>${cliente.empresa}</td>
                            <td>${cliente.ruc}</td>
                            <td>${cliente.direccion}</td>
                            <td>${cliente.localidad}</td>
                            <td>${cliente.telefono}</td>
                            <td>${cliente.pais}</td>
                        </tr>`;
                    $('#clienteTable tbody').html(row);
                    $('#clienteTable').show();
                },
                error: xhr => console.error('Error al obtener los detalles del cliente:', xhr)
            });
        }
    });

    // // Debounce + abort de requests previas
    // let xhrCliente = null;
    //
    // $("#cliente").autocomplete({
    //   minLength: 2,
    //   delay: 300,                  // reduce el “spamming” de requests
    //   appendTo: "#facturaM",
    //   source: function(request, response) {
    //     // abortar la búsqueda anterior
    //     if (xhrCliente && xhrCliente.readyState !== 4) {
    //       xhrCliente.abort();
    //     }
    //     xhrCliente = $.ajax({
    //       url: "/admin_cont/buscar_cliente/",   // ← con “/” final para evitar 301
    //       type: "GET",
    //       dataType: "json",
    //       timeout: 7000,                        // no dejar colgada la pestaña
    //       data: { term: request.term },
    //       success: function(data) {
    //         response($.map(data, function(item) {
    //           return {
    //             label: item.empresa + " — " + (item.ruc || ""),
    //             value: item.empresa,
    //             id:    item.codigo
    //           };
    //         }));
    //       },
    //       error: function(xhr, status) {
    //         if (status !== "abort") {
    //           console.error("Autocomplete cliente error:", status);
    //           response([]); // vaciar sugerencias en error
    //         }
    //       }
    //     });
    //   },
    //   select: function(event, ui) {
    //     $("#cliente").data("selected-id", ui.item.id);
    //     // cargar ficha del cliente (cuidá también la barra final)
    //     $.ajax({
    //       url: "/admin_cont/buscar_clientes/",
    //       type: "GET",
    //       dataType: "json",
    //       data: { id: ui.item.id },
    //       success: function(cliente) {
    //         const row = `
    //           <tr id="cliente-${ui.item.id}">
    //             <td class="d-none">${cliente.codigo}</td>
    //             <td>${cliente.empresa}</td>
    //             <td>${cliente.ruc || ""}</td>
    //             <td>${cliente.direccion || ""}</td>
    //             <td>${cliente.localidad || ""}</td>
    //             <td>${cliente.telefono || ""}</td>
    //           </tr>`;
    //         $("#clienteTable tbody").html(row);
    //         $("#clienteTable").show();
    //       }
    //     });
    //   }
    // });


    // Autocomplete para el input "item"
    $('#item').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "/admin_cont/buscar_item_v",
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
        appendTo: "#facturaM",
        select: function (event, ui) {
            $.ajax({
                url: "/admin_cont/buscar_items_v",
                data: {id: ui.item.id},
                dataType: 'json',
                success: servicio => {
                    $('#id_precio input').data({
                        iva: servicio.iva,
                        cuenta: servicio.cuenta,
                        codigo: servicio.item,
                        embarque: servicio.embarque,
                        gasto: servicio.gasto,
                        imputar: servicio.imputar,
                    });
                    $('#id_descripcion_item input').val(servicio.nombre);
                    $('#iva_item').val(servicio.iva);
                },
                error: xhr => console.error('Error al obtener los detalles del item:', xhr)
            });
        }
    });

    let itemCounter = 0;
    // Editar fila: al hacer doble clic sobre una fila, se cargan los datos en los campos de entrada
    $("#itemTable").on("dblclick", "tr", function () {
        var $row = $(this);
        // Ajustar índices según las nuevas columnas agregadas
        var codigo = $row.find("td").eq(0).text().trim();       // Código (oculto)
        var item = $row.find("td").eq(1).text().trim();         // Item
        var descripcion = $row.find("td").eq(2).text().trim();  // Descripción
        var precio = $row.find("td").eq(3).text().trim();       // Precio
        var iva = $row.find("td").eq(6).text().trim();          // IVA (columna 7 ahora)
        var cuenta = $row.find("td").eq(7).text().trim();       // Cuenta (columna 8 ahora)

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

    // Al hacer clic en "Agregar Item" se agrega una nueva fila o se actualiza la fila en edición
    $('#agregarItem').on('click', function () {
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

            if ($("#itemTable tr.editing").length > 0) {
                var $editingRow = $("#itemTable tr.editing");
                $editingRow.data("precio", precio);
                $editingRow.data("iva", iva);
                $editingRow.data("cuenta", cuenta);
                 let montoIva, totalConIva;
                    if (iva === 'Básico') {
                        montoIva = precio * 0.22;
                    } else {
                        montoIva = 0;
                    }
                    totalConIva = precio + montoIva;

                $editingRow.find("td").eq(0).text(codigo);           // Código
                $editingRow.find("td").eq(1).text(item);             // Nombre del item
                $editingRow.find("td").eq(2).text(descripcion);      // Descripción
                $editingRow.find("td").eq(3).text(precio.toFixed(2));// Precio
                $editingRow.find("td").eq(4).text(montoIva.toFixed(2));  // IVA
                $editingRow.find("td").eq(5).text(totalConIva.toFixed(2)); // Total con IVA
                $editingRow.find("td").eq(6).text(iva);              // Tipo de IVA
                $editingRow.find("td").eq(7).text(cuenta);           // Cuenta
                $editingRow.find("td").eq(8).text(texto);            // Estado
                $editingRow.removeClass("editing");
            } else {
                itemCounter++;
                let montoIva;
                let totalConIva;
                const rowId = `item-${itemCounter}`;
                if(iva==='Básico'){
                    montoIva = parseFloat(precio) * (22 / 100);
                    totalConIva = parseFloat(precio) + montoIva;
                }else{
                    montoIva = 0;
                    totalConIva = parseFloat(precio) + montoIva;
                }


                const row = `
                    <tr id="${rowId}" data-precio="${precio}" data-iva="${iva}" data-cuenta="${cuenta}">
                        <td style="display:none;">${codigo}</td>
                        <td>${item}</td>
                        <td>${descripcion}</td>
                        <td>${precio.toFixed(2)}</td>
                        <td>${montoIva.toFixed(2)}</td>
                        <td>${totalConIva.toFixed(2)}</td>
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
            $('#itemTable').css('visibility', 'visible');
            $('#clonarItem').show();
            actualizarTotal();
            $('#totales').show();
            limpiarCampos();
        } else {
            alert('Por favor, completa todos los campos antes de agregar el item.');
        }
    });

    // Botón para clonar la fila seleccionada
    $("#clonarItem").on("click", function () {
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

    // Seleccionar/Deseleccionar fila
    $('#itemTable tbody').on('click', 'tr', function () {
        $('#itemTable tbody tr').removeClass('table-active table-primary');
        $(this).toggleClass('table-active table-primary');
    });

    $('#eliminarSeleccionados').on('click', function () {
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

    //buscadores tabla facturas
    let contador = 0;


    $('#tabla_facturas tfoot th').each(function (index) {
        let title = $('#tabla_facturas thead th').eq(index).text();

        if (index === 0) {
            // Si es la primera columna, colocar el botón de limpiar filtros
            $(this).html('<button class="btn btn-danger" title="Borrar filtros" id="clear"><span class="glyphicon glyphicon-erase"></span> Limpiar</button>');
        } else if (title !== '') {
            // Agregar inputs de búsqueda en las demás columnas
            $(this).html('<input type="text" class="form-control filter-input" autocomplete="off" id="buscoid_' + index + '" placeholder="Buscar ' + title + '" />');
        }
    });

    // Evento para limpiar todos los filtros
    $(document).on("click", "#clear", function () {
        awbRegex = '';
        $(".filter-input").val("").trigger("keyup"); // Limpia los inputs y activa la búsqueda
        $(".filter-input").removeClass("is-invalid"); // Se quita el rojo si se vacía
        table.ajax.reload();
    });
    // Evento para resaltar los inputs cuando tienen contenido
    $(document).on("input", ".filter-input", function () {
        if ($(this).val().trim() !== "") {
            $(this).addClass("is-invalid"); // Se pone en rojo
        } else {
            $(this).removeClass("is-invalid"); // Se quita el rojo si se vacía
        }
    });
    table_fac = $('#tabla_facturas').DataTable({
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
                "targets": 2,  // Asignamos la columna de fecha
                "type": "date-iso", // Indica que esta columna es de tipo fecha
                "orderable": true // Habilita el ordenamiento
            },
            {
                "targets": [6,7,8],
                "className": "text-end",
            }
        ],
        "columns": [
            {"visible": true}, // Columna 0
            {"visible": false}, // Columna 1
            {"orderable": true}, // Columna 2 (Ordenable)
            {"orderable": true},
            {"orderable": true},
            {"orderable": true},
            {"orderable": true},
            {"orderable": true},
            {"orderable": true},
            {"visible": false},
            {"visible": false},
        ],
        "order": [[2, "desc"]],
        "processing": true,
        "serverSide": true,
        "pageLength": 100,
        "ajax": {
            "url": "/admin_cont/source_facturacion/",
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
        "rowCallback": function (row, data) {
        }
    });

//seccion para modal de embarque

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
        if (selectedRadio == 'imputar-masters') {
            impucompra_tipo = 'M';
        } else {
            impucompra_tipo = 'H';
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
            if (selectedRadio == 'imputar-masters') {
                impucompra_tipo = 'master';
            } else {
                impucompra_tipo = 'house';
            }
            let departamento = document.getElementById("departamento").value;
            if (departamento == '') {
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
                embarque: embarque,
                cual: impucompra_tipo
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
    let embarqueSeleccionado = null;
    let embarqueArmado = false;

    // Inicialización del modal de embarque
    $("#modal-embarque").dialog({
        autoOpen: false,
        modal: true,
        width: "auto",
        height: "auto",
        maxWidth: $(window).width() * 0.90,
        minWidth: 600,
        maxHeight: $(window).height() * 0.90,
        position: {my: "center top", at: "center top+20", of: window},
        buttons: [
            {
                text: "Armar",
                class: "btn btn-warning",
                click: function () {
                    if (!selectedRow) {
                        alert("Debe seleccionar un embarque.");
                        return;
                    }

                    const embarque = selectedRow.cells[0].textContent.trim();
                    const tipo = selectedRow.cells[1].textContent.trim();
                    const posicion = selectedRow.cells[3].textContent.trim();
                    const cliente = selectedRow.cells[9].textContent.trim();
                    const lugar = $("#seleccionado-lugar").val();  // ya cargado en doble click

                    const precio = parseFloat($("#seleccionado-precio").val()) || 0;
                    const total = parseFloat(localStorage.getItem('precio_item_imputar')) || 0;

                    if (precio > total) {
                        alert('El monto ingresado: ' + precio + ', es mayor al original: ' + total);
                        return;
                    }

                    // Limpiar tabla de armado si ya existía
                    $("#guardado-tabla tbody").empty();

                    // Crear la nueva fila
                    const nuevaFila = `
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

                    // Marcar como embarque armado
                    embarqueSeleccionado = embarque;
                    embarqueArmado = true;

                    // Habilitar botón guardar si está deshabilitado
                    $("#btnGuardarEmbarque").prop("disabled", false);

                    // Activar botón eliminar
                    $(".eliminar-fila").off("click").on("click", function () {
                        $(this).closest("tr").remove();
                        embarqueArmado = false;
                        embarqueSeleccionado = null;
                        $("#btnGuardarEmbarque").prop("disabled", true);
                    });

                    // Limpiar campos seleccionados
                    $("#seleccionado-posicion").text("");
                    $("#seleccionado-embarque").text("");
                    $("#seleccionado-precio").val("");
                    $("#seleccionado-tipo").val("");
                }
            },

            {
                text: "Seleccionar datos",
                class: "btn btn-primary",
                click: function () {
                    if (!embarqueArmado || !embarqueSeleccionado) {
                        alert("Debe armar el embarque antes de guardar.");
                        return;
                    }

                    const posicion = selectedRow.cells[3].textContent.trim();  // o donde corresponda

                    $.ajax({
                        url: "/admin_cont/get_datos_embarque/",
                        method: "POST",
                        headers: {'X-CSRFToken': csrf_token},
                        data: {posicion: posicion},
                        success: function (response) {
                            // Llenar modal de carga
                            Object.keys(response).forEach(key => {
                                const campo = $("#modalRegistroCarga [name='" + key + "']");
                                if (campo.length) {
                                    campo.val(response[key]);
                                }
                            });

                            $("#modalRegistroCarga").dialog("open");
                        },
                        error: function () {
                            alert("Error al cargar los datos del embarque.");
                        }
                    });
                }
            },
            {
                text: "Salir",
                class: "btn btn-dark",
                click: function () {
                    $(this).dialog("close");
                }
            }
        ],
        beforeClose: function (event, ui) {
            limpiarModalEmbarque();
        }
    }).prev('.ui-dialog-titlebar').remove();

    $("#modalRegistroCarga").dialog({
        autoOpen: false,
        modal: true,
        width: 'auto',
        position: {
            my: "center top",
            at: "center top+20",
            of: window
        },
        buttons: [
            {
                text: "Procesar",
                class: "btn btn-primary",
                click: function () {
                    procesar_complementarios();
                }
            },

            {
                text: "Salir",
                class: "btn btn-dark",
                click: function () {
                    $(this).dialog("close");
                }
            }
        ]
    });

    $("#modal-embarque").tabs();

    let radioMasters = document.getElementById("imputar-masters");
    let radioHouses = document.getElementById("imputar-houses");

    radioMasters.addEventListener("change", actualizarPestanias);
    radioHouses.addEventListener("change", actualizarPestanias);

    actualizarPestanias();


    $("#tabla_facturas tbody").on("dblclick", "tr", function () {
        const row = $('#tabla_facturas').DataTable().row(this).data();
        const autogenerado = row[1];
        const nrocliente = row[9];
        const numero = row[10];


        $("#autogen_detalle_venta").val(autogenerado);
        buscar_gastos(autogenerado);
        buscar_ordenes(nrocliente, numero, autogenerado);

        $("#modalFacturaDetalle").dialog({
            modal: true,
            width: '80%',
            height: 'auto',
            position: {my: "center top", at: "center top+20", of: window},
            autoOpen: true,
        });

    });

    $("#tabla_facturas tbody").on("click", "tr", function () {
        $("#tabla_facturas tbody tr").removeClass("table-secondary");
        $(this).addClass("table-secondary");
    });

    //formulario de nueva nota de credito
    $('#nota_credito_form').on('submit', function (e) {
        e.preventDefault();
        let numero = $('#numero_nota').val();
        let arbitraje_cambio = $('#arbitraje_cambio').val();
        let autogenerado = $('#autogen_detalle_venta').val();
        if(numero==null || arbitraje_cambio==null || autogenerado == null){
            alert('Ingrese Numero y Cambio.');
            return;
        }
        $.post("/admin_cont/hacer_nota_credito/", {
            numero: numero,
            arbitraje: arbitraje_cambio,
            autogenerado: autogenerado,
            csrfmiddlewaretoken: csrf_token
        }, function(resp) {
            alert(resp.mensaje);
            $('#notaCreditoDialog').dialog("close");
            //location.reload();
        });
    });

    //imputacion de notas de credito:

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
                procesar_factura_nota();
                $(this).dialog("close");
            }
        }
    ],
    });

    $("#tabla-impucompra tbody").on("click", "tr", function () {
        $(this).toggleClass("table-secondary");
        actualizarMonto();
    });
    //boton de imputar
    $("#btn-imputar").on("click", function () {
        let montoDisponible = parseFloat($("#monto-imputar").val()) || 0;
        let saldoRestante = montoDisponible;

        // Recuperar el localStorage actual para no sobrescribir
        let facturasGuardadas = JSON.parse(localStorage.getItem("facturas_impuvta")) || [];

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
        localStorage.setItem("saldo_nota_credito_venta", saldoRestante.toFixed(2));

        // Guardar las facturas imputadas en localStorage sin sobrescribir los datos previos
        localStorage.setItem("facturas_impuvta", JSON.stringify(facturasGuardadas));

        // Actualizar el monto a imputar con el saldo restante
        $("#monto-imputar").val(saldoRestante.toFixed(2));

        // Deshabilitar el botón si ya no hay saldo disponible
        $("#btn-imputar").prop("disabled", saldoRestante === 0);

        actualizarImputado();

    });

    $("#cerrar-modal").on("click", function () {
        $("#impucompra_nota").dialog("close");
    });

    $('#reenviar_uruware').on('click', function () {
        let autogenerado= $('#autogen_detalle_venta').val()
            $.ajax({
          url: "/admin_cont/refacturar_uruware/",
          method: "POST",
          data: {
            csrfmiddlewaretoken: csrf_token,
            autogenerado: autogenerado,
          },
          dataType: "json" // jQuery parsea resp a objeto
        })
          .done(function (resp) {
              console.log(resp);
              alert(resp.mensaje);

            $('#modalFacturaDetalle').dialog("close");

          })
          .fail(function (xhr) {
            let msg = "error";
            try {
              const r = JSON.parse(xhr.responseText);
              if (r.mensaje) msg = r.mensaje;
            } catch (e) {}
            alert(msg);
          })
          .always(function (resp) {
          });
    });

    $('#descargar_uruware').on('click', function () {
        let autogenerado= $('#autogen_detalle_venta').val()

        fetch("/admin_cont/descargar_pdf_uruware/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf_token // asegurate de tener csrf_token definido
            },
            body: new URLSearchParams({ autogenerado: autogenerado,csrfmiddlewaretoken: csrf_token,
     })
        })
        .then(response => {
            if (!response.ok) throw new Error("Error al descargar el PDF");
            return response.blob();
        })
        // .then(blob => {
        //     const url = window.URL.createObjectURL(blob);
        //     const a = document.createElement("a");
        //     a.href = url;
        //     a.download = "descarga_"+autogenerado+".pdf"; // nombre de archivo en la descarga
        //     document.body.appendChild(a);
        //     a.click();
        //     a.remove();
        //     window.URL.revokeObjectURL(url);
        // })

        .then(async response => {
        const contentType = response.headers.get("Content-Type");

        if (contentType && contentType.includes("application/pdf")) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "descarga_" + autogenerado + ".pdf";
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } else {
            const data = await response.json();
            alert(data.mensaje || "Ocurrió un error");
        }
        })
        .catch(error => {
            alert("Error: " + error.message);
        });
    });

});

/* INITIAL CONTROL PAGE */
var wWidth = $(window).width();
var dWidth = wWidth * 0.40;
var wHeight = $(window).height();
var dHeight = wHeight * 0.30;

function abrir_modalfactura() {
    $('#facturaForm').trigger('reset');
    $('#itemTable tbody').empty();
    $('#clienteTable tbody').empty();
    $('#clienteTable').hide();

    $("#facturaM").dialog({
        autoOpen: true,
        modal: true,
        width: wWidth * 0.90,
        height: wHeight * 0.85,
        dialogClass: "custom-dialog",
        buttons: [{
            text: "Salir",
            class: "btn btn-dark btn-sm",
            style: "width:90px; height:30px; font-size:14px;",
            click: function () {
                $(this).dialog("close");
                localStorage.removeItem('preventa');
                localStorage.removeItem('gastos');

            },
        }],
        open: function() {
            // 🔹 Ajustar el tamaño dinámicamente según el contenido
        },
        beforeClose: function (){

        window.location.reload();
        }
    }).prev('.ui-dialog-titlebar').remove();
    cargar_arbitraje();

}

$('#preventa').on('click', function () {

    $("#preventa_modal").dialog({
        autoOpen: true,
        modal: true,
        draggable: true,
        width: wWidth*0.90,  // Se ajusta al contenido
        height: 'auto', // Se ajusta al contenido
        minWidth: 500,  // Evita que sea demasiado pequeño
        minHeight: 200, // Evita que sea demasiado pequeño
        position: {my: "top", at: "top+20", of: window},
        beforeClose: function(event, ui) {
            limpiar_modal_preventa();
        }
    }).prev(".ui-dialog-titlebar").hide();
    cargar_preventas();

});
function limpiar_modal_preventa() {
    // Limpiar todos los inputs dentro del modal
    $('#preventa_modal input').val('');

    // Limpiar las tablas (excepto el thead)
    $('#preventa_table tbody').empty();
    $('#tabla_gastos_preventa_factura tbody').empty();

}


function cargar_preventas(){
    $('#preventa_table tbody').empty();
    $.ajax({
        url: "/admin_cont/source_infofactura",
        type: "GET",
        success: function(response) {
            const data = response.data;
            const tbody = $('#preventa_table tbody');
            tbody.empty();  // Limpia la tabla

            if (data.length === 0) {
                tbody.append('<tr><td colspan="10" class="text-center">Sin registros</td></tr>');
                return;
            }

            data.forEach(item => {
                const fila = `
                    <tr>
                        <td>${item.numero}</td>
                        <td>${item.cliente}</td>
                        <td>${item.posicion}</td>
                        <td>${item.master}</td>
                        <td>${item.house}</td>
                        <td>${item.vapor_vuelo}</td>
                        <td>${item.contenedor}</td>
                        <td>${item.clase}</td>
                        <td>${item.referencia}</td>
                        <td>${item.fecha || ''}</td>
                    </tr>
                `;
                tbody.append(fila);
            });

            $('#preventa_table tbody').off('click').on('click', 'tr', function () {
        let preventa = $(this).find('td').eq(0).text();
        let clase = $(this).find('td').eq(7).text();

        if ($(this).hasClass('table-secondary')) {
            $(this).removeClass('table-secondary');
            localStorage.removeItem('preventa_id');
            localStorage.removeItem('preventa_clase');
        } else {
            $('#preventa_table tbody tr.table-secondary').removeClass('table-secondary');
            $(this).addClass('table-secondary');
            localStorage.setItem('preventa_id', preventa);
            localStorage.setItem('preventa_clase', clase);
        }
    });

            $('#preventa_table tbody').off('dblclick').on('dblclick', 'tr', function () {
                $('#pararesetear').trigger('reset');
                $('#pararesetear2').trigger('reset');

                let referencia = $(this).find('td').eq(8).text();
                let clase = $(this).find('td').eq(7).text();
                let preventa = $(this).find('td').eq(0).text();

                $.ajax({
                    url: "/admin_cont/cargar_preventa_infofactura/",
                    method: 'POST',
                    data: {
                        'referencia': referencia,
                        'clase': clase,
                        'preventa': preventa
                    },
                    headers: {'X-CSRFToken': csrf_token},
                    success: function (response) {
                        if (response.bloqueo) {
                            alert(response.bloqueo.mensaje);
                            return;
                        }
                        let preventa = response.data_preventa;
                        let gastos = response.data;

                        localStorage.setItem('gastos_preventa', JSON.stringify(gastos));
                        localStorage.setItem('preventa', JSON.stringify(preventa));

                        $('#moneda').val(preventa.moneda);
                        $('#total_con_iva').val(preventa.total_con_iva);
                        $('#total_sin_iva').val(preventa.total_sin_iva);
                        $('#cliente_i').val(preventa.cliente_i);
                        $('#peso').val(preventa.peso);
                        $('#direccion').val(preventa.direccion);
                        $('#localidad').val(preventa.localidad);
                        $('#aplic').val(preventa.aplic);
                        $('#bultos').val(preventa.bultos);
                        $('#volumen').val(preventa.volumen);
                        $('#commodity').val(preventa.commodity);
                        $('#inconterms').val(preventa.inconterms);
                        $('#flete').val(preventa.flete);
                        $('#deposito').val(preventa.deposito);
                        $('#wr').val(preventa.wr);
                        $('#referencia').val(preventa.referencia);
                        $('#llegada_salida').val(preventa.llegada_salida);
                        $('#origen').val(preventa.origen);
                        $('#destino').val(preventa.destino);
                        $('#transportista').val(preventa.transportista);
                        $('#consignatario').val(preventa.consignatario);
                        $('#embarcador').val(preventa.embarcador);
                        $('#agente').val(preventa.agente);
                        $('#vuelo_vapor').val(preventa.vuelo_vapor);
                        $('#seguimiento').val(preventa.seguimiento);
                        $('#mawb_mbl_mcrt').val(preventa.mawb_mbl_mcrt);
                        $('#hawb_hbl_hcrt').val(preventa.hawb_hbl_hcrt);
                        $('#posicion').val(preventa.posicion);
                        $('#status').val(preventa.status);
                        $('#orden').val(preventa.orden);
                        $('#modo').val(preventa.modo);

                        // Cargar gastos en DataTable como ya hacías
                        if ($.fn.DataTable.isDataTable("#tabla_gastos_preventa_factura")) {
                            $('#tabla_gastos_preventa_factura').DataTable().clear().destroy();
                        }

                        $('#tabla_gastos_preventa_factura').DataTable({
                            info: false,
                            lengthChange: false,
                            data: gastos,
                            columns: [
                                {data: 'descripcion', title: 'Descripcion'},
                                {data: 'total', title: 'Total'},
                                {data: 'iva', title: 'IVA'},
                                {data: 'original', title: 'Original'},
                                {data: 'moneda', title: 'Moneda'}
                            ],
                            paging: false,
                            searching: true,
                            ordering: true,
                            responsive: true,
                            language: {
                                url: "//cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json"
                            },
                            columnDefs: [
                                {
                                    targets: 0,
                                    className: "dt-body-left"
                                },
                                {
                                    targets: 1,
                                    className: "dt-body-right",
                                    render: function (data) {
                                        return '$' + parseFloat(data).toFixed(2);
                                    }
                                },
                                {
                                    targets: [2, 3, 4],
                                    className: "dt-body-center"
                                }
                            ]
                        });
                    },
                    error: function () {
                        alert('Error al realizar la consulta.');
                    }
                });
            });
            },
            error: function(xhr) {
                alert("Error al cargar la tabla de preventas.");
            }
            });
}

function facturar_preventa() {
    $("#preventa_modal").dialog('close');

    const gastos = JSON.parse(localStorage.getItem('gastos_preventa')) || [];
    const preventa = JSON.parse(localStorage.getItem('preventa')) || [];

    $("#cliente").val(preventa.cliente_i);
    $("#cliente").attr('data-id', preventa.nrocliente);

    if (preventa.nrocliente) {
        $.ajax({
            url: "/admin_cont/buscar_clientes",
            data: { id: preventa.nrocliente },
            dataType: 'json',
            success: cliente => {
                const row = `
                    <tr id="cliente-${cliente.codigo}">
                        <td class="d-none">${cliente.codigo}</td>
                        <td>${cliente.empresa}</td>
                        <td>${cliente.ruc}</td>
                        <td>${cliente.direccion}</td>
                        <td>${cliente.localidad}</td>
                        <td>${cliente.telefono}</td>
                    </tr>`;
                $('#clienteTable tbody').html(row);
                $('#clienteTable').show();
            },
            error: xhr => console.error('Error al obtener los detalles del cliente:', xhr)
        });
    }

    if (gastos.length > 0) {
        gastos.forEach(gasto => {
            const partes = gasto.descripcion.split(' - ');
            const codigo = gasto.codigo;
            const desc = partes[1] || '';
            agregarItem(desc, codigo, gasto.total, gasto.posicion);
        });
    }
}


function agregarItem(desc, codigo, precio, posicion = null) {
    const item = desc;
    const descripcion = desc;
    let itemCounter=0;
    const preventa = JSON.parse(localStorage.getItem('preventa')) || [];

    if (item && descripcion && !isNaN(precio)) {
        $.ajax({
            url: "/admin_cont/buscar_items_v_codigo",
            data: { id: codigo },
            dataType: 'json',
            success: servicio => {
                const iva = servicio.iva;
                const cuenta = servicio.cuenta;
                const codigo = servicio.item;
                const imputar = servicio.imputar || ""

                itemCounter++;
                const rowId = `item-${itemCounter}`;
                let montoIva, totalConIva;
                    if (iva === 'Básico' || iva == 'Basico') {
                        montoIva = precio * 0.22;
                    } else {
                        montoIva = 0;
                    }
                    totalConIva = precio + montoIva;

                let row = `
                    <tr id="${rowId}" data-precio="${precio}" data-iva="${iva}" data-cuenta="${cuenta}">
                        <td style="display:none;">${codigo}</td>
                        <td>${item}</td>
                        <td>${descripcion}</td>
                        <td>${precio.toFixed(2)}</td>
                        <td>${montoIva.toFixed(2)}</td>
                        <td>${totalConIva.toFixed(2)}</td>
                        <td>${iva}</td>
                        <td>${cuenta}</td>
                        <td>${preventa.posicion}</td>
                        <td>${preventa.posicion}</td>
                        <td>${preventa.cliente_i}</td>
                    </tr>`;

                $('#itemTable tbody').append(row);
                $('#itemTable').show();
                $('#eliminarSeleccionados').show();
                actualizarTotal();
                $('#totales').show();
            },
            error: xhr => console.error('Error al obtener los detalles del item:', xhr)
        });
    } else {
        alert('Por favor, completa todos los campos antes de agregar el item.');
    }
}

function limpiarCampos() {
    $('#item').val('');
    $('#id_descripcion_item input').val('');
    $('#id_precio input').val('');
    $('#iva_item').val('');

}

function actualizarPestanias() {
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

function actualizarTotal() {
    let precio = 0;
    let neto_fun = 0;
    total = 0;  // Asegúrate de inicializar total aquí
    iva = 0;

// Recorre cada fila y calcula el neto
    $('#itemTable tbody tr').each(function () {
        precio = parseFloat($(this).data('precio')) || 0;
        neto_fun += precio;
    });

    $(document).on('click', function (e) {
        // Verificamos si el click fue fuera de la tabla
        if (!$(e.target).closest('#itemTable').length) {
            $('#itemTable tbody tr.table-primary').removeClass('table-primary');
        }
    });

    neto = neto_fun;

// Actualiza el valor del neto en el campo correspondiente
    $('#id_neto').val(neto.toFixed(2)).prop('readonly', true);

// Recorre cada fila y calcula el total con IVA
    $('#itemTable tbody tr').each(function () {
        precio = parseFloat($(this).data('precio')) || 0;
        iva = $(this).data('iva');

        const precioFinal = iva === 'Básico' ? precio * 1.22 : precio;
        total += precioFinal;
    });


// Actualiza el valor del total en el campo correspondiente
    $('#id_total').val(total.toFixed(2)).prop('readonly', true);

// Calcula y actualiza el IVA
    iva = total - neto;
    $('#id_iva').val(iva.toFixed(2)).prop('readonly', true);
}

function cancelar_preventa() {
//agregar a formularios los demas bloques para poder resetearlos
    $('#pararesetear').trigger('reset');
    $('#pararesetear2').trigger('reset');
    if ($.fn.DataTable.isDataTable("#tabla_gastos_preventa_factura")) {
        $('#tabla_gastos_preventa_factura').DataTable().clear().destroy();
    }
}

function borrar_preventa() {
    id = localStorage.getItem('preventa_id');

    $.ajax({
        url: '/admin_cont/eliminar_preventa/',
        method: 'POST',
        headers: {'X-CSRFToken': csrf_token},
        data: JSON.stringify({id: id}),
        contentType: 'application/json',
        success: function (response) {
            if (response.resultado === "éxito") {
                alert("Preventa eliminada correctamente");
                cargar_preventas();
            } else {
                alert(response.mensaje);
            }
        },
        error: function (xhr) {
            alert("Error al eliminar la preventa: " + xhr.responseText);
        }
    });
}


//imprimir caratula house
function imprimir_preventa() {
    id = localStorage.getItem('preventa_id');
    $("#pdf_add_input").html('');
    $('#pdf_add_input').summernote('destroy');
    get_datos_pdf();
    if (id != null) {
        $("#pdf_modal").dialog({
            autoOpen: true,
            open: function (event, ui) {
                $('#pdf_add_input').summernote('destroy');

                $('#pdf_add_input').summernote({
                    placeholder: '',
                    title: 'PDF con el detalle del seguimiento',
                    tabsize: 10,
                    fontNames: ['Arial', 'Arial Black', 'Comic Sans MS', 'Courier New', 'Merriweather'],
                    height: wHeight * 0.65,
                    width: wWidth * 0.55,
                    toolbar: [
                        ['style', ['style']],
                        ['font', ['bold', 'underline', 'clear']],
                        ['color', ['color']],
                        ['para', ['ul', 'ol', 'paragraph']],
                        ['table', ['table']],
                        ['insert', ['link', 'picture', 'video']],
                        ['view', ['fullscreen', 'codeview']]
                    ]
                });
            },
            modal: true,
            title: "Preventa N°: " + id,
            height: wHeight * 0.70,
            width: wWidth * 0.60,
            class: 'modal fade',
            buttons: [
                {
                    // text:"Imprimir",
                    html: '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-printer" viewBox="0 0 16 16">\n' +
                        '  <path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/>\n' +
                        '  <path d="M5 1a2 2 0 0 0-2 2v2H2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v1a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1h1a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3a2 2 0 0 0-2-2H5zM4 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2H4V3zm1 5a2 2 0 0 0-2 2v1H2a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v-1a2 2 0 0 0-2-2H5zm7 2v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1z"/>\n' +
                        '</svg> Imprimir',
                    class: "btn btn-warning ",
                    style: "width:100px",
                    icons: {primary: "bi bi-star"},
                    click: function () {
                        imprimirPDF();
                    },
                }, {
                    text: "Salir",
                    class: "btn btn-dark",
                    style: "width:100px",
                    click: function () {
                        $(this).dialog("close");
                    },
                },
            ],
            beforeClose: function (event, ui) {
                // table.ajax.reload();
            }
        })
    } else {
        alert('Debe seleccionar al menos un registro');
    }
}

function imprimirPDF() {
    var contenido = $('#pdf_add_input').summernote('code');
    var ventanaImpresion = window.open('', '_blank');

    ventanaImpresion.document.write('<html><head><title>Impresión</title>');
    ventanaImpresion.document.write('<style>');
    ventanaImpresion.document.write(`
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            line-height: 1.5;
            font-size:12px;
        }
        @media print {
            @page {
                size: portrait; /* Establece la orientación en vertical (portrait) */
                margin: 20mm;   /* Márgenes alrededor del contenido */
            }
            body {
                width: 100%;
                margin: 0;
                padding: 0;
            }
            .container {
                display: block;
                width: 100%;
                text-align: left;
            }
        }
        .container {
            margin: 20px; /* Margen interior para el contenido */
        }
        h1, h2 {
            text-align: center;
        }
        p {
            text-align: left;
        }
        hr {
            border: 1px solid #000;
        }
    `);
    ventanaImpresion.document.write('</style></head><body>');
    ventanaImpresion.document.write('<div class="container">');
    ventanaImpresion.document.write(contenido);
    ventanaImpresion.document.write('</div></body></html>');
    ventanaImpresion.document.close();

    ventanaImpresion.onload = function () {
        ventanaImpresion.focus(); // Asegurarse de que la ventana esté en foco
        ventanaImpresion.print(); // Iniciar la impresión
        ventanaImpresion.close(); // Cerrar la ventana después de la impresión
    };
}

function get_datos_pdf() {
    id = localStorage.getItem('preventa_id');
    clase = localStorage.getItem('preventa_clase');
    let modo = '';
    if (clase == 'IM' || clase == 'EM') {
        modo = 'MARITIMO';
    } else if (clase == 'IA' || clase == 'EA') {
        modo = 'AEREO';
    } else if (clase == 'IT' || clase == 'ET') {
        modo = 'TERRESTRE';
    } else {
        modo = 'SINMODO';
    }

    miurl = "/admin_cont/get_datos_pdf_preventa/";
    var toData = {
        'clase': clase,
        'modo': modo,
        'id': id,
        'csrfmiddlewaretoken': csrf_token,
    };
    $.ajax({
        type: "POST",
        url: miurl,
        data: toData,
        async: false,
        success: function (resultado) {
            if (resultado['resultado'] === 'exito') {
                $("#pdf_add_input").html(resultado['texto']);
            } else {
                alert(resultado['resultado']);
            }
        }
    });
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

//multiples preventas

//$('#infofacturaTable').DataTable().ajax.reload();
function multiples_preventas() {
    $("#prev_multiple_modal").dialog({
        autoOpen: true,
        modal: true,
        width: 'auto',
        height: 'auto',
        "scrollX": true,
        "scrollCollapse": true,
        position: {my: "top", at: "top+20", of: window},
        buttons: [{
            text: "Salir",
            class: "btn btn-dark btn-sm",
            style: "width:90px:font-size:14px;height:30px;",
            click: function () {
                $(this).dialog("close");
                $('#pendientes_tabla').DataTable().destroy();
                $('#preventa_unificada_tabla').DataTable().destroy();
                $('#conceptos_unificar_tabla').DataTable().destroy();
                $('#socio_com_filtro').val();

            },
        }],
    }).prev('.ui-dialog-titlebar').remove();
}

$('#socio_com_filtro').autocomplete({
    source: function (request, response) {
        $.ajax({
            url: "/admin_cont/buscar_cliente",
            dataType: 'json',
            data: {term: request.term},
            success: function (data) {
                response(data.map(cliente => ({
                    label: cliente.text,
                    value: cliente.text,
                    id: cliente.text
                })));
            },
            error: xhr => console.error('Error al buscar clientes:', xhr)
        });
    },
    minLength: 2,
    select: function (event, ui) {
        tabla_pendientes();

    }
});

function tabla_pendientes() {
    $('#pendientes_tabla').DataTable({
        info: false,        // Oculta "Mostrando X a Y de Z registros"
        lengthChange: false,
        "stateSave": false,
        "dom": 'Btlipr',
        "scrollX": true,
        "bAutoWidth": false,
        "scrollY": true,
        "lengthMenu": [5, 10, 25],
        "columnDefs": [
            {
                "targets": [0],
                "className": 'text-left',
                "data": 'numero',
                "title": 'Número'
            },
            {
                "targets": [1],
                "className": 'text-left',
                "data": 'sale_llega',
                "title": 'Sale/Llega'
            },
            {
                "targets": [2],
                "className": 'text-left',
                "data": 'referencia',
                "title": 'Ref.'
            },
            {
                "targets": [3],
                "className": 'text-left',
                "data": 'consignatario',
                "title": 'Consignatario'
            },
            {
                "targets": [4],
                "className": 'text-left',
                "data": 'master',
                "title": 'Máster'
            },
            {
                "targets": [5],
                "className": 'text-left',
                "data": 'house',
                "title": 'House'
            },
            {
                "targets": [6],
                "className": 'text-center',
                "orderable": false,
                "data": null,
                "defaultContent": '',
                "render": function (data, type, row) {
                    return `<input type="checkbox" value="${row.numero}">`;
                },
                "title": 'Seleccionar'
            },
            {
                "targets": [7],
                "className": 'text-left',
                "data": 'vapor_vuelo',
                "title": 'Vuelo/Vapor'
            },
            {
                "targets": [8],
                "className": 'text-left',
                "data": 'clase',
                "title": 'Clase'
            }
        ],
        "order": [[0, "desc"]], // Ordena inicialmente por la columna 'Número'
        "processing": true,
        "serverSide": true,
        "pageLength": 5,
        "ajax": {
            "url": "/admin_cont/source_infofactura_cliente/",
            'type': 'GET',
            "data": function (d) {
                return $.extend({}, d, {
                    "cliente": $('#socio_com_filtro').val() // Se pasa el valor del cliente
                });
            }
        },
        "language": {
            "url": "/static/datatables/es_ES.json" // Ruta de traducción al español
        }
    });
}

function unificar(x) {
// 1 es unificados, 0 es originales
    $('#guardar_preventa_unificada').attr('data-id', x);

    let seleccionados = [];

    $('#pendientes_tabla input[type="checkbox"]:checked').each(function () {
        let fila = $(this).closest('tr');
        let numero = $(this).val();
        let referencia = fila.find('td').eq(2).text().trim();
        let clase = fila.find('td').eq(8).text().trim();
        seleccionados.push({numero: numero, referencia: referencia, clase: clase});
    });

    if (seleccionados.length === 0) {
        alert('Por favor, seleccione al menos una fila.');
        return;
    }

    $.ajax({
        url: "/admin_cont/cargar_preventa_infofactura_multiple/",
        method: 'POST',
        data: {
            'seleccionados': JSON.stringify(seleccionados)
        },
        headers: {'X-CSRFToken': csrf_token},
        success: function (response) {
            let todo = response.data;

            let resultado = unificarPreventas(todo);
            let gastos = resultado.gastosUnificados;
            let preventa = resultado.preventaUnificada.data_preventa;
            let gastos_originales = resultado.preventaUnificada.gastos_originales;
            let gastos_mostrar;

            if ($.fn.DataTable.isDataTable("#conceptos_unificar_tabla")) {
                $('#conceptos_unificar_tabla').DataTable().clear().destroy();
            }
            if ($.fn.DataTable.isDataTable("#gastos_no_unificados")) {
                $('#gastos_no_unificados').DataTable().clear().destroy();
            }

            if ($.fn.DataTable.isDataTable("#preventa_unificada_tabla")) {
                $('#preventa_unificada_tabla').DataTable().clear().destroy();
            }

            if (x == 1) {
                gastos_mostrar = gastos;
            } else {
                gastos_mostrar = gastos_originales;
            }


            var tabla = $('#preventa_unificada_tabla tbody');
            tabla.empty();
            var fila = $('<tr>');
            fila.append('<td class="editable">' + preventa.llegada_salida + '</td>');
            fila.append('<td class="">' + preventa.referencia + '</td>');
            fila.append('<td class="">' + preventa.consignatario + '</td>');
            fila.append('<td class="">' + preventa.master + '</td>');
            fila.append('<td class="editable">' + preventa.house + '</td>');
            fila.append('<td class="">' + preventa.posicion + '</td>');
            fila.append('<td class="">' + preventa.seguimiento + '</td>');
            fila.append('<td class="">' + preventa.cliente_i + '</td>');
            fila.append('<td class="editable">' + preventa.vuelo_vapor + '</td>');
            fila.append('<td class="">' + resultado.preventaUnificada.clase + '</td>');
            tabla.append(fila);

            $('.editable').on('dblclick', function () {
                var celda = $(this);
                var valorActual = celda.text();
                var input = $('<input type="text" class="form-control">').val(valorActual);

                // Reemplazar el contenido de la celda con el input
                celda.html(input);

                // Enfocar el input y seleccionar el texto
                input.focus().select();

                // Manejar el evento blur (cuando el usuario sale del campo)
                input.on('blur', function () {
                    var nuevoValor = $(this).val(); // Obtener el nuevo valor
                    celda.html(nuevoValor); // Reemplazar el input con el nuevo valor
                });

                // Manejar el evento Enter para confirmar la edición
                input.on('keypress', function (e) {
                    if (e.which === 13) { // Enter key
                        $(this).blur(); // Simular blur para confirmar el cambio
                    }
                });
            });

            $('#conceptos_unificar_tabla').DataTable({
                info: false,        // Oculta "Mostrando X a Y de Z registros"
                lengthChange: false,
                data: gastos_mostrar,
                columns: [
                    {data: 'descripcion', title: 'Descripcion'},
                    {data: 'total', title: 'Total'},
                    {data: 'iva', title: 'IVA'},
                    {data: 'original', title: 'Original'},
                    {data: 'moneda', title: 'Moneda'},

                ],
                paging: true,
                searching: true,
                ordering: true,
                responsive: true,
                language: {
                    url: "//cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json"
                },
                "columnDefs": [
                    {
                        targets: 0,
                        className: "dt-body-left",
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                    {
                        targets: 1,
                        className: "dt-body-right",
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: 2,
                        className: "dt-body-center",
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                    {
                        targets: 3,
                        className: "dt-body-center",
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: 4,
                        className: "dt-body-center",
                        render: function (data, type, row) {
                            return data;
                        }
                    }
                ],
                "lengthMenu": [5, 10, 25],
                "pageLength": 5,
            });
            $('#gastos_no_unificados').DataTable({
                info: false,        // Oculta "Mostrando X a Y de Z registros"
                lengthChange: false,
                data: gastos_originales,
                columns: [
                    {data: 'descripcion', title: 'Descripcion'},
                    {data: 'total', title: 'Total'},
                    {data: 'iva', title: 'IVA'},
                    {data: 'original', title: 'Original'},
                    {data: 'moneda', title: 'Moneda'},

                ],
                paging: true,
                searching: true,
                ordering: true,
                responsive: true,
                language: {
                    url: "//cdn.datatables.net/plug-ins/1.10.25/i18n/Spanish.json"
                },
                "columnDefs": [
                    {
                        targets: 0,
                        className: "dt-body-left",
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                    {
                        targets: 1,
                        className: "dt-body-right",
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: 2,
                        className: "dt-body-center",
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                    {
                        targets: 3,
                        className: "dt-body-center",
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: 4,
                        className: "dt-body-center",
                        render: function (data, type, row) {
                            return data;
                        }
                    }
                ],
                "lengthMenu": [5, 10, 25],
                "pageLength": 5,
            });

        },
        error: function () {
            alert('Error al realizar la consulta.');
        }
    });

}

function unificarPreventas(preventas) {
    let ids = [];
    const gastosOriginales = preventas.flatMap(preventa => preventa.gastos);

    const gastosUnificados = gastosOriginales.reduce((acumulador, actual) => {
        const existente = acumulador.find(
            gasto => gasto.descripcion === actual.descripcion && gasto.moneda === actual.moneda
        );

        if (existente) {
            existente.total += parseFloat(actual.total) || 0;
            existente.original += parseFloat(actual.original) || 0;
        } else {
            acumulador.push({
                ...actual,
                total: parseFloat(actual.total) || 0,
                original: parseFloat(actual.original) || 0
            });
        }

        return acumulador;
    }, []);

    const preventaUnificada = JSON.parse(JSON.stringify(preventas[0]));

    preventaUnificada.data_preventa.total_con_iva = 0;
    preventaUnificada.data_preventa.total_sin_iva = 0;
    preventaUnificada.data_preventa.bultos = 0;
    preventaUnificada.data_preventa.peso = 0;

    preventas.forEach(preventa => {
        preventaUnificada.data_preventa.total_con_iva += parseFloat(preventa.data_preventa.total_con_iva) || 0;
        preventaUnificada.data_preventa.total_sin_iva += parseFloat(preventa.data_preventa.total_sin_iva) || 0;
        preventaUnificada.data_preventa.bultos += parseInt(preventa.data_preventa.bultos, 10) || 0;
        preventaUnificada.data_preventa.peso += parseFloat(preventa.data_preventa.peso) || 0;
        ids.push(preventa.numero);
    });

    preventaUnificada.data_preventa.total_con_iva = preventaUnificada.data_preventa.total_con_iva.toFixed(4);
    preventaUnificada.data_preventa.total_sin_iva = preventaUnificada.data_preventa.total_sin_iva.toFixed(4);

    preventaUnificada.gastos = gastosUnificados;
    preventaUnificada.gastos_originales = gastosOriginales;
    preventaUnificada.ids = ids;
    preventaUnificada.data_preventa.referencia = generarNumero();
    //preventaUnificada.referencia = preventaUnificada.data_preventa.referencia;

    const datosParaGuardar = {
        preventaUnificada,
        gastosUnificados
    };
    const datosJSON = JSON.stringify(datosParaGuardar);
    localStorage.setItem('preventaUnificada', datosJSON);

    return {
        preventaUnificada,
        gastosUnificados
    };
}

function guardar_preventa_unificada() {
    let x = $('#guardar_preventa_unificada').attr('data-id');
    let preventaUnificada = JSON.parse(localStorage.getItem('preventaUnificada')) || [];
    let preventa = preventaUnificada.preventaUnificada.data_preventa;
    preventa.numero = preventaUnificada.preventaUnificada.numero;
    let clase = preventaUnificada.preventaUnificada.clase;
    let referencia = preventaUnificada.preventaUnificada.data_preventa.referencia;

    let gastos = preventaUnificada.gastosUnificados;
    let gastos_originales = preventaUnificada.preventaUnificada.gastos_originales;
    let gastos_mostrar;
    let ids = preventaUnificada.preventaUnificada.ids;

    if (x == 1) {
        gastos_mostrar = gastos;
    } else {
        gastos_mostrar = gastos_originales;
    }

    $.ajax({
        type: "POST",
        url: "/admin_cont/preventa/",
        data: JSON.stringify(preventa),
        contentType: "application/json",
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (response) {
            if (response.resultado === 'exito') {
                guardar_gastos_uni(gastos_mostrar, clase, referencia);
                borrar_preventas_multiples(ids);
                alert("Los datos se han enviado correctamente.");
            } else {
                alert("Error al enviar los datos.");
            }
        },
        error: function () {
            alert("Error en la solicitud.");
        }
    });
}

function guardar_gastos_uni(gastos, clase, referencia) {
    $.ajax({
        method: "POST",
        url: "/admin_cont/guardar_gasto_unificado/",
        data: JSON.stringify({
            gastos: gastos,  // Asegúrate de que los datos sean un objeto JavaScript
            clase: clase,
            referencia: referencia
        }),
        contentType: "application/json",
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (response) {
        },
        error: function () {
            alert("Error en la solicitud.");
        }
    });
}

function borrar_preventas_multiples(preventas) {

    preventas.forEach(function (p) {
        $.ajax({
            url: '/admin_cont/eliminar_preventa/',
            method: 'POST',
            headers: {'X-CSRFToken': csrf_token},
            data: JSON.stringify({id: p}),
            contentType: 'application/json',
            success: function (response) {
            },
            error: function (xhr) {
                alert("Error al eliminar la preventa: " + xhr.responseText);
            }
        });
    });
}

function generarNumero() {
    const now = new Date();

    const segundos = now.getSeconds();

    const milisegundos = now.getMilliseconds();

    const numero = `${segundos % 100}${milisegundos % 100}`.padStart(4, '0');

    return -parseInt(numero);
}


$('#abrir_arbi').on('click', function (event) {
    $("#arbitraje_modal").dialog({
        autoOpen: true,
        modal: true,
        title: "Cargar un arbitraje para el día de hoy",
        height: 'auto',
        width: 'auto',
        position: {my: "top", at: "top+20", of: window},
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
                        headers: {'X-CSRFToken': csrf_token},
                        data: {
                            arbDolar: arbDolar,
                            parDolar: parDolar,
                            tipoMoneda: tipoMoneda,
                            pizDolar: pizDolar,
                            fecha: fecha
                        },
                        success: function (data) {
                            if (data['status'].length == 0) {
                                alert("Valores guardados correctamente");
                                $("#arbitraje_modal").dialog("close");
                            } else {
                                alert(data['status']);
                            }
                        },
                        error: function (xhr, status, error) {
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
}

function validarRucUyDeTabla() {
    let selector = '#clienteTable', idxRuc = 2, idxPais = 6;
  const tr = document.querySelector(`${selector} tbody tr`);
  if (!tr) return false;

  const tds = tr.children;
  const ruc = (tds[idxRuc]?.textContent || '').trim();
  const paisRaw = (tds[idxPais]?.textContent || '').trim();

  const pais = paisRaw.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const esUruguay = pais === 'uruguay' || pais.endsWith('uruguay') ||
                    paisRaw.toUpperCase() === 'UY' || paisRaw.toUpperCase() === 'URY';

  const rucEs12Digitos = /^\d{12}$/.test(ruc);

  return esUruguay ? rucEs12Digitos : false;
}

function procesar_factura() {
    let tipo = $('#id_tipo').val();
    if(tipo==21 || tipo == 23){
        if(confirm('¿Desea imputar esta Nota?')){
            $("#impucompra_nota").dialog('open');
            let cliente = $('#clienteTable tbody tr td').eq(0).text();
            $('#monto-imputar').val( $('#id_total').val());
            localStorage.removeItem('facturas_impuvta');
            cargar_facturas_imputacion(cliente);
            return;
        }
    }

    if(!validarRucUyDeTabla()){
        console.log(tipo);
        if(tipo!=23 && tipo !=24){
            alert('El cliente es del exterior, seleccione Eticket o Eticket N/C');
            return;
        }
    }

    let pendienteEncontrado = false;

    $('#itemTable tbody tr').each(function () {
        // Antes: columna 7 (index 6)
        const estado = $(this).find('td:nth-child(9)').text().trim();  // Ahora es la 8.ª columna (estado)
        if (estado.toUpperCase() === 'PENDIENTE') {
            pendienteEncontrado = true;
            return false; // cortar el .each
        }
    });

    if (pendienteEncontrado) {
        let total = $('#id_total').val();
        localStorage.setItem("precio_item_imputar", total);
        $("#modal-embarque").dialog("open");
        return; // cortar la función, no continuar con el procesamiento
    }

    if (confirm('¿Está seguro de que desea facturar?')) {

        let tipoFac = $('#id_tipo').val();
        let serie = $('#id_serie').val();
        let prefijo = $('#id_prefijo').val();
        let numero = $('#id_numero').val();
        let cliente = $('#cliente').val();
        let fecha = $('#id_fecha').val();
        let paridad = $('#id_paridad').val();
        let arbitraje = $('#id_arbitraje').val();
        let imputar = $('#id_imputar').val();
        let moneda = $('#id_moneda select').val();
        let clienteData = {
            codigo: $('#clienteTable tbody tr td').eq(0).text(),
            empresa: $('#clienteTable tbody tr td').eq(1).text(),
            rut: $('#clienteTable tbody tr td').eq(2).text(),
            direccion: $('#clienteTable tbody tr td').eq(3).text(),
            localidad: $('#clienteTable tbody tr td').eq(4).text(),
            telefono: $('#clienteTable tbody tr td').eq(5).text()
        };
        let items = [];
        $('#itemTable tbody tr').each(function () {
            const tds = $(this).children('td'); // Incluye todos, incluso ocultos
            //console.log("Columnas:", tds.length, tds.map((i, td) => `(${i}) ${$(td).text().trim()}`).get());

            const itemData = {
                id: tds.eq(0).text().trim(),           // Id (oculto)
                item: tds.eq(1).text().trim(),         // Item
                descripcion: tds.eq(2).text().trim(),  // Descripción
                precio: parseFloat(tds.eq(3).text().trim()),       // Precio base
                precio_iva: parseFloat(tds.eq(4).text().trim()),   // IVA calculado
                total: parseFloat(tds.eq(5).text().trim()),        // Total (precio + IVA)
                iva: tds.eq(6).text().trim(),           // % IVA
                cuenta: tds.eq(7).text().trim(),        // Cuenta contable
                estado: tds.eq(8).text().trim(),        // Estado (PENDIENTE / NO IMPUTABLE)
                embarque: tds.eq(9).text().trim(),      // Embarque
                posicion: tds.eq(10).text().trim(),     // Posición
                socio: tds.eq(11).text().trim()         // Socio Comercial
            };

            items.push(itemData);
        });

        let preventa = JSON.parse(localStorage.getItem('preventa')) || [];
        let data = [];
        if (preventa != null) {
            data = {
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
                saldo_nota_cred: localStorage.getItem('saldo_nota_credito_venta') || null,
                facturas_imputadas:localStorage.getItem('facturas_impuvta') || "[]",
                clienteData: JSON.stringify(clienteData),
                items: JSON.stringify(items),
                total: total,
                iva: iva,
                neto: neto,
                preventa: JSON.stringify(preventa),
            }
        } else {
            data = {
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
                saldo_nota_cred: localStorage.getItem('saldo_nota_credito_venta') || null,
                facturas_imputadas:localStorage.getItem('facturas_impuvta') || "[]",
                clienteData: JSON.stringify(clienteData),
                items: JSON.stringify(items),
                total: total,
                iva: iva,
                neto: neto,
                preventa: 0,
            }
        }

        $.ajax({
            url: "/admin_cont/procesar_factura/",
            dataType: 'json',
            type: 'POST',
            data: data,
            headers: {'X-CSRFToken': csrf_token},
            success: function (data) {
                if (data.success) {
                    $('#facturaM').dialog('close');
                    $('#facturaForm').trigger('reset');

                    total = 0;
                    iva = 0;
                    neto = 0;
                    table_fac.ajax.reload();
                } else {
                   const msg = data.mensaje || 'Ocurrió un error';
                    alert(msg);
                }

                //window.location.reload();
            },
            error: function (xhr) {
                console.error('Error al facturar:', xhr);
                alert('Error al procesar la factura');
            }
        });

    }
}

function procesar_factura_nota() {
    console.log('entra');

    let pendienteEncontrado = false;

    $('#itemTable tbody tr').each(function () {
        // Antes: columna 7 (index 6)
        const estado = $(this).find('td:nth-child(9)').text().trim();  // Ahora es la 8.ª columna (estado)
        if (estado.toUpperCase() === 'PENDIENTE') {
            pendienteEncontrado = true;
            return false; // cortar el .each
        }
    });

    if (pendienteEncontrado) {
        let total = $('#id_total').val();
        localStorage.setItem("precio_item_imputar", total);
        $("#modal-embarque").dialog("open");
        return; // cortar la función, no continuar con el procesamiento
    }

    if (confirm('¿Está seguro de que desea facturar?')) {

        let tipoFac = $('#id_tipo').val();
        let serie = $('#id_serie').val();
        let prefijo = $('#id_prefijo').val();
        let numero = $('#id_numero').val();
        let cliente = $('#cliente').val();
        let fecha = $('#id_fecha').val();
        let paridad = $('#id_paridad').val();
        let arbitraje = $('#id_arbitraje').val();
        let imputar = $('#id_imputar').val();
        let moneda = $('#id_moneda select').val();
        let clienteData = {
            codigo: $('#clienteTable tbody tr td').eq(0).text(),
            empresa: $('#clienteTable tbody tr td').eq(1).text(),
            rut: $('#clienteTable tbody tr td').eq(2).text(),
            direccion: $('#clienteTable tbody tr td').eq(3).text(),
            localidad: $('#clienteTable tbody tr td').eq(4).text(),
            telefono: $('#clienteTable tbody tr td').eq(5).text()
        };
        let items = [];
        $('#itemTable tbody tr').each(function () {
            const tds = $(this).children('td'); // Incluye todos, incluso ocultos
            //console.log("Columnas:", tds.length, tds.map((i, td) => `(${i}) ${$(td).text().trim()}`).get());

            const itemData = {
                id: tds.eq(0).text().trim(),           // Id (oculto)
                item: tds.eq(1).text().trim(),         // Item
                descripcion: tds.eq(2).text().trim(),  // Descripción
                precio: parseFloat(tds.eq(3).text().trim()),       // Precio base
                precio_iva: parseFloat(tds.eq(4).text().trim()),   // IVA calculado
                total: parseFloat(tds.eq(5).text().trim()),        // Total (precio + IVA)
                iva: tds.eq(6).text().trim(),           // % IVA
                cuenta: tds.eq(7).text().trim(),        // Cuenta contable
                estado: tds.eq(8).text().trim(),        // Estado (PENDIENTE / NO IMPUTABLE)
                embarque: tds.eq(9).text().trim(),      // Embarque
                posicion: tds.eq(10).text().trim(),     // Posición
                socio: tds.eq(11).text().trim()         // Socio Comercial
            };

            items.push(itemData);
        });

        let preventa = JSON.parse(localStorage.getItem('preventa')) || [];
        let data = [];
        if (preventa != null) {
            data = {
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
                saldo_nota_cred: localStorage.getItem('saldo_nota_credito_venta') || null,
                facturas_imputadas:localStorage.getItem('facturas_impuvta') || "[]",
                clienteData: JSON.stringify(clienteData),
                items: JSON.stringify(items),
                total: total,
                iva: iva,
                neto: neto,
                preventa: JSON.stringify(preventa),
            }
        } else {
            data = {
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
                saldo_nota_cred: localStorage.getItem('saldo_nota_credito_venta') || null,
                facturas_imputadas:localStorage.getItem('facturas_impuvta') || "[]",
                clienteData: JSON.stringify(clienteData),
                items: JSON.stringify(items),
                total: total,
                iva: iva,
                neto: neto,
                preventa: 0,
            }
        }

        $.ajax({
            url: "/admin_cont/procesar_factura/",
            dataType: 'json',
            type: 'POST',
            data: data,
            headers: {'X-CSRFToken': csrf_token},
            success: function (data) {
                if (data.success) {
                    $('#facturaM').dialog('close');
                    $('#facturaForm').trigger('reset');

                    total = 0;
                    iva = 0;
                    neto = 0;
                    table_fac.ajax.reload();
                } else {
                    const msg = data.mensaje || 'Ocurrió un error';
                    alert(msg);
                }

                //window.location.reload();
            },
            error: function (xhr) {
                console.error('Error al facturar:', xhr);
                alert('Error al procesar la factura');
            }
        });

    }
}

function procesar_complementarios() {

    let formCarga = {
        referencia: $('#id_referencia').val(),
        seguimiento: $('#id_seguimiento').val(),
        peso: $('#id_peso').val(),
        aplicable: $('#id_aplicable').val(),
        volumen: $('#id_volumen').val(),
        transportista: $('#id_transportista').val(),
        posicion: $('#id_posicion').val(),
        vuelo_vapor: $('#id_vuelo_vapor').val(),
        mawb: $('#id_mawb').val(),
        hawb: $('#id_hawb').val(),
        origen: $('#id_origen').val(),
        destino: $('#id_destino').val(),
        fecha_llegada_salida: $('#id_fecha_llegada_salida').val(),
        consignatario: $('#id_consignatario').val(),
        commodity: $('#id_commodity').val(),
        wr: $('#id_wr').val(),
        shipper: $('#id_shipper').val(),
        incoterms: $('#id_incoterms').val(),
        pago: $('#id_pago').val(),
        agente: $('#id_agente').val(),
        observaciones: $('#id_observaciones').val(),
        transportista_nro: $('#id_transportista_nro').val(),
        consignatario_nro: $('#id_consignatario_nro').val(),
        agente_nro: $('#id_agente_nro').val(),
        shipper_nro: $('#id_shipper_nro').val(),
        servicio: $("input[name='servicio']:checked").val()
    };

    procesar_factura_finalizada(formCarga);

}

function procesar_factura_finalizada(datos_complementarios) {

    if (confirm('¿Está seguro de que desea facturar?')) {
        let tipoFac = $('#id_tipo').val();
        let serie = $('#id_serie').val();
        let prefijo = $('#id_prefijo').val();
        let numero = $('#id_numero').val();
        let cliente = $('#cliente').val();
        let fecha = $('#id_fecha').val();
        let paridad = $('#id_paridad').val();
        let arbitraje = $('#id_arbitraje').val();
        let imputar = $('#id_imputar').val();
        let moneda = $('#id_moneda select').val();
        let clienteData = {
            codigo: $('#clienteTable tbody tr td').eq(0).text(),
            empresa: $('#clienteTable tbody tr td').eq(1).text(),
            rut: $('#clienteTable tbody tr td').eq(2).text(),
            direccion: $('#clienteTable tbody tr td').eq(3).text(),
            localidad: $('#clienteTable tbody tr td').eq(4).text(),
            telefono: $('#clienteTable tbody tr td').eq(5).text()
        };

        let items = [];
        $('#itemTable tbody tr').each(function () {
            const tds = $(this).children('td'); // Incluye todos, incluso ocultos
            //console.log("Columnas:", tds.length, tds.map((i, td) => `(${i}) ${$(td).text().trim()}`).get());

            const itemData = {
                id: tds.eq(0).text().trim(),           // Id (oculto)
                item: tds.eq(1).text().trim(),         // Item
                descripcion: tds.eq(2).text().trim(),  // Descripción
                precio: parseFloat(tds.eq(3).text().trim()),       // Precio base
                precio_iva: parseFloat(tds.eq(4).text().trim()),   // IVA calculado
                total: parseFloat(tds.eq(5).text().trim()),        // Total (precio + IVA)
                iva: tds.eq(6).text().trim(),           // % IVA
                cuenta: tds.eq(7).text().trim(),        // Cuenta contable
                estado: tds.eq(8).text().trim(),        // Estado (PENDIENTE / NO IMPUTABLE)
                embarque: tds.eq(9).text().trim(),      // Embarque
                posicion: tds.eq(10).text().trim(),     // Posición
                socio: tds.eq(11).text().trim()         // Socio Comercial
            };

            items.push(itemData);
        });


        let preventa = JSON.parse(localStorage.getItem('preventa')) || [];
        let data = [];
        if (preventa != null) {
            //es preventa
            data = {
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
                facturas_imputadas:localStorage.getItem('facturas_impuvta') || "[]",
                clienteData: JSON.stringify(clienteData),
                items: JSON.stringify(items),
                total: total,
                iva: iva,
                neto: neto,
                preventa: JSON.stringify(preventa),
            }
        } else {
            data = {
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
                facturas_imputadas:localStorage.getItem('facturas_impuvta') || "[]",
                clienteData: JSON.stringify(clienteData),
                items: JSON.stringify(items),
                total: total,
                iva: iva,
                neto: neto,
                preventa: 0,
            }
        }
        data["registroCarga"] = JSON.stringify(datos_complementarios);
        $.ajax({
            url: "/admin_cont/procesar_factura/",
            dataType: 'json',
            type: 'POST',
            data: data,
            headers: {'X-CSRFToken': csrf_token},
            success: function (data) {
                if (data.success) {
                    $('#facturaM').dialog('close');
                    $('#modalRegistroCarga').dialog('close');
                    $('#modal-embarque').dialog('close');
                    limpiarModalEmbarque();
                    $('#facturaForm').trigger('reset');
                    $('#formRegistroCarga').trigger('reset');
                    table_fac.ajax.reload();
                    total = 0;
                    iva = 0;
                    neto = 0;

                } else {
                    const msg = data.mensaje || 'Ocurrió un error';
                    alert(msg);
                }
                //window.location.reload();
            },
            error: function (xhr) {
                console.error('Error al facturar:', xhr);
                alert('Error al procesar la factura');
            }
        });
    }

}

function cargar_arbitraje() {
    const fecha = $('#id_fecha').val();

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


function buscar_gastos(autogenerado) {
    $.ajax({
        url: '/admin_cont/detalle_venta/',
        method: 'GET',
        data: {
            autogenerado: autogenerado
        },
        success: function (response) {
            if (response.success) {
                const data = response.data;
                $('#id_prefijo_detalle').val(data.prefijo);
                $('#id_serie_detalle').val(data.serie);
                $('#numero_detalle_venta').val(data.numero);
                $('#id_tipo_detalle').val(data.tipo);
                $('#id_moneda_detalle_venta').val(data.moneda);
                $('#id_fecha_detalle_venta').val(data.fecha);
                $('#id_fecha_ingreso').val(data.fecha_ingreso);
                $('#id_fecha_vencimiento').val(data.fecha_vencimiento);
                $('#id_cliente_detalle').val(data.cliente);
                $('#nro_cli').val(data.nrocliente);
                $('#id_detalle_detalle_venta').val(data.detalle);

                $('#id_paridad_detalle_venta').val(parseFloat(data.paridad || 0).toFixed(2));
                $('#id_arbitraje_detalle_venta').val(parseFloat(data.arbitraje || 0).toFixed(2));
                $('#id_total_detalle').val(parseFloat(data.total || 0).toFixed(2));
                $('#id_posicion_venta').val(data.posicion);
                $('#id_observaciones').val(data.observaciones);
                $('#id_cae').val(data.cae);
                $('#id_cae').removeClass('is-valid is-invalid');

                // validar si es número y existe
                if (data.cae && !isNaN(data.cae)) {
                    // correcto → verde (success)
                    $('#id_cae').addClass('is-valid');
                    $('#reenviar_uruware').prop('disabled',true);
                    $('#descargar_uruware').prop('disabled',false);

                } else {
                    // error → rojo (danger)
                    $('#id_cae').addClass('is-invalid');
                    $('#reenviar_uruware').prop('disabled',false);
                    $('#descargar_uruware').prop('disabled',true);

                }
                const tipo = data.tipo.trim().toUpperCase();
                if (tipo === 'FACTURA' || tipo === 'E-TICKET') {
                    $('#nota_credito_clonar').prop('disabled',false);
                }else{
                    $('#nota_credito_clonar').prop('disabled',true);
                }


                if (data.items && data.items.length > 0) {
                    $('#tablaItems').empty();

                    data.items.forEach(function (item) {
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
        error: function (xhr) {
            alert("No se pudo obtener el detalle de la venta.");
        }
    });
}

function buscar_ordenes(cliente, numero, autogenerado) {

    if (!cliente || !numero || !autogenerado) {
        alert('Faltan datos');
        return;
    }

    $.ajax({
        url: '/admin_cont/buscar_ordenes_por_boleta_ventas/',  // Cambia esto por tu URL real
        type: 'GET',
        data: {
            cliente: cliente,
            numero: numero,
            autogenerado: autogenerado,
        },
        success: function (response) {
            let tbody = $('#tabla_pago_factura tbody');
            tbody.empty();

            if (response.resultados.length === 0) {
                tbody.append('<tr><td colspan="4">No se encontraron resultados</td></tr>');
            } else {
                $.each(response.resultados, function (i, orden) {
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
        error: function (xhr) {
            console.error(xhr.responseText);
            alert('Error al buscar órdenes');
        }
    });
}

function cerrar_modal_preventa() {
    $('#preventa_modal').dialog('close');
}

function abrirDialogoNotaCredito() {
    let autogenerado= $('#autogen_detalle_venta').val()
    $('#nota_credito_form').trigger('reset');
    $('#notaCreditoDialog').dialog({
        modal: true,
        title: "Crear Nota de Crédito a partir de esta factura",
        buttons: {
            "Cancelar": function() {
                $(this).dialog("close");
            },
            "Confirmar": function() {
                let numero = $('#numero_nota').val();
                let arbitraje_cambio = $('#arbitraje_cambio').val();
                if(numero==null || arbitraje_cambio==null || autogenerado == null){
                    alert('Ingrese Numero y Cambio.');
                    return;
                }
                // $.post("/admin_cont/hacer_nota_credito/", {
                //     numero: numero,
                //     arbitraje: arbitraje_cambio,
                //     autogenerado: autogenerado,
                //     csrfmiddlewaretoken: csrf_token
                // }, function(resp) {
                //     alert(resp.mensaje);
                //     //location.reload();
                // });
                $.ajax({
                  url: "/admin_cont/hacer_nota_credito/",
                  method: "POST",
                  data: {
                    numero: numero,
                    arbitraje: arbitraje_cambio,
                    autogenerado: autogenerado,
                    csrfmiddlewaretoken: csrf_token
                  },
                  dataType: "json" // jQuery parsea resp a objeto
                })
                  .done(function (resp) {
                    if (resp.success) {
                      alert(resp.mensaje || "OK");
                    } else {
                      alert(resp.mensaje || "Ocurrió un error.");
                    }
                $('#modalFacturaDetalle').dialog("close");

                  })
                  .fail(function (xhr) {
                    let msg = "Ocurrió un error";
                    try {
                      const r = JSON.parse(xhr.responseText);
                      if (r.mensaje) msg = r.mensaje;
                    } catch (e) {}
                    alert(msg);
                  })
                  .always(function () {
                  });

                $(this).dialog("close");
            },

        },
        open: function () {
            const buttons = $(this).parent().find(".ui-dialog-buttonpane button");
            buttons.eq(1).addClass("btn btn-sm btn-primary"); // Confirmar
            buttons.eq(0).addClass("btn btn-sm btn-dark");    // Cancelar
        }
    });
}

function cargar_facturas_imputacion(nrocliente) {
    $.ajax({
        url: "/admin_cont/cargar_pendientes_imputacion_venta/",
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

