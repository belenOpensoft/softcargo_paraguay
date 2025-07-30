$(document).ready(function () {
    alert('hola');

    $.ajaxSetup({
        beforeSend: function (xhr) {
            const rol = sessionStorage.getItem('rol_activo');
            if (rol) {
                xhr.setRequestHeader('X-Rol-Activo', rol);
            }
        }
    });

    let path = window.location.pathname;
    let partes = path.split('/').filter(p => p);
    let modulo = partes.length >= 1 ? partes[0] : null;
    let modulo2 = partes.length >= 1 ? partes[1] : null;
    if (modulo == 'exportacion_aerea') {
        $('#modulo_nombre').html('EXPORTACIÓN AÉREA');
    }
    else if (modulo == 'exportacion_maritima') {
        $('#modulo_nombre').html('EXPORTACIÓN MARÍTIMA');
    }
    else if (modulo == 'exportacion_terrestre') {
        $('#modulo_nombre').html('EXPORTACIÓN TERRESTRE');
    }
    else if (modulo == 'importacion_maritima') {
        $('#modulo_nombre').html('IMPORTACIÓN MARÍTIMA');
    }
    else if (modulo == 'importacion_aerea') {
        $('#modulo_nombre').html('IMPORTACIÓN AÉREA');
    }
    else if (modulo == 'importacion_terrestre') {
        $('#modulo_nombre').html('IMPORTACIÓN TERRESTRE');
    }
    else if (modulo == 'admin_cont') {
        if (modulo2 == 'facturacion') {
            $('#modulo_nombre').html('FACTURACIÓN');
        } else if (modulo2 == 'proveedores_gastos') {
            $('#modulo_nombre').html('PROVEEDORES Y GASTOS');
        } else if (modulo2 == 'cobranza') {
            $('#modulo_nombre').html('COBRANZA');
        } else if (modulo2 == 'orden_pago') {
            $('#modulo_nombre').html('ORDEN DE PAGO');
        } else if (modulo2 == 'editar_consultar_pagos') {
            $('#modulo_nombre').html('EDITAR Y CONSULTAR ORDENES DE PAGO');
        } else if (modulo2 == 'editar_consultar_ventas') {
            $('#modulo_nombre').html('EDITAR Y CONSULTAR VENTAS');
        } else if (modulo2 == 'editar_consultar_compras') {
            $('#modulo_nombre').html('EDITAR Y CONSULTAR COMPRAS');
        } else if (modulo2 == 'editar_consultar_cobranzas') {
            $('#modulo_nombre').html('EDITAR Y CONSULTAR COBRANZAS');
        } else if (modulo2 == 'ingresar_asientos') {
            $('#modulo_nombre').html('INGRESAR ASIENTOS');
        } else if (modulo2 == 'modificar_asientos') {
            $('#modulo_nombre').html('MODIFICAR Y CONSULTAR ASIENTOS');
        } else if (modulo2 == 'movimientos_bancarios') {
            $('#modulo_nombre').html('MOVIMIENTOS BANCARIOS');
        } else if (modulo2 == 'movimientos_caja') {
            $('#modulo_nombre').html('MOVIMIENTOS DE CAJA');
        } else if (modulo2 == 'ingresar_buscar_cheques') {
            $('#modulo_nombre').html('INGRESAR / BUSCAR CHEQUES');
        } else if (modulo2 == 'bajar_cheques') {
            $('#modulo_nombre').html('BAJAR CHEQUES A BANCO');
        }
    }
    else if (modulo == 'consultas_administrativas') {
        if (modulo2 == 'subdiario_ventas') {
            $('#modulo_nombre').html('SUBDIARIO DE VENTAS');
        } else if (modulo2 == 'balance_cobrar') {
            $('#modulo_nombre').html('BALANCE DE COBROS');
        }
        else if (modulo2 == 'reporte_cobranzas') {
            $('#modulo_nombre').html('REPORTE DE COBROS');
        }
        else if (modulo2 == 'antiguedad_saldos') {
            $('#modulo_nombre').html('ANTIGUEDAD DE SALDOS - VENTAS');
        }
        else if (modulo2 == 'estados_cuenta') {
            $('#modulo_nombre').html('ESTADOS DE CUENTA - VENTAS');
        }
        else if (modulo2 == 'subdiario_compras') {
            $('#modulo_nombre').html('SUBDIARIO DE COMPRAS');
        }
        else if (modulo2 == 'balance_pagos') {
            $('#modulo_nombre').html('BALANCE DE PAGOS');
        }
        else if (modulo2 == 'antiguedad_saldos_compras') {
            $('#modulo_nombre').html('ANTIGUEDAD DE SALDOS - COMPRAS');
        }
        else if (modulo2 == 'estados_cuenta_compras') {
            $('#modulo_nombre').html('ESTADOS DE CUENTA - COMPRAS');
        }
        else{
                $('#modulo_nombre').html(modulo.replace(/_/g, ' ').toUpperCase());

        }
    }
    else{
            $('#modulo_nombre').html(modulo.replace(/_/g, ' ').toUpperCase());

    }

    var alerts = document.querySelectorAll(".alert");
    // Itera a través de los elementos y oculta cada uno después de 5 segundos
    alerts.forEach(function (alertElement) {
        setTimeout(function () {
            alertElement.style.display = "none";
        }, 5000);
    });
    const miBoton = document.getElementById("btntoggle");
    // Verificar si la cookie existe
    const aux = getCookie('toggle');
    if (aux == null) {
        setCookieToggle();
        event.preventDefault();
        miBoton.click();
    }

    const items = document.querySelectorAll('.sidebar-item.has-submenu');
    items.forEach(item => {
        const link = item.querySelector('.sidebar-link');
        link.addEventListener('click', function (e) {
            e.preventDefault();
            item.classList.toggle('active');

            // Opcional: cerrar otros menús
            items.forEach(other => {
                if (other !== item) {
                    other.classList.remove('active');
                }
            });
        });
    });

});

// Aplicar a cualquier cierre de modal jQuery UI
$(document).on("dialogclose", ".ui-dialog-content", function () {
    const numeroEmbarque = $("#id_numero_embarque").length ? $("#id_numero_embarque").val() : null;
    const numeroMaster = $("#id_numero_master").length ? $("#id_numero_master").val() : null;

    if (numeroEmbarque || numeroMaster) {
        enviarDesbloqueo(numeroEmbarque, numeroMaster);
    }
});
function enviarDesbloqueo(numeroEmbarque, numeroMaster) {
            const ruta = window.location.pathname;

            $.ajax({
                type: "POST",
                url: "/desbloquear/",
                data: {
                    numero_embarque: numeroEmbarque,
                    numero_master: numeroMaster,
                    ruta: ruta,
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                },
                success: function(response) {
                    console.log("Desbloqueo:", response);
                },
                error: function(xhr, status, error) {
                    console.error("Error desbloqueando:", error);
                }
            });
        }

//usa ren varias pestañas
function setRolActivo(rol) {
    sessionStorage.setItem('rol_activo', rol);
}

function getRolActivo() {
    return sessionStorage.getItem('rol_activo');
}

function cambiarRol(modulo, baseUrl) {
    setRolActivo(modulo);

    // Verifica si ya hay parámetros en la URL
    var url = baseUrl.includes('?') ? baseUrl + '&rol=' + encodeURIComponent(modulo)
        : baseUrl + '?rol=' + encodeURIComponent(modulo);

    window.location.href = url;
}

function redirectConRol(urlBase) {
    const rol = sessionStorage.getItem('rol_activo');
    if (!rol) {
        window.location.replace(urlBase);
        return;
    }

    try {
        let url = new URL(urlBase, window.location.origin);
        if (!url.searchParams.has("rol")) {
            url.searchParams.set("rol", rol);
        }
        window.location.replace(url.toString());
    } catch (error) {
        console.log(error);
        window.location.replace(urlBase);
    }

}


function setCookieToggle() {
    aux = getCookie('toggle');
    if (aux == null) {
        document.cookie = 'toggle=true'; // Establecer la cookie con el valor booleano "true"
    } else {
        deleteCookie('toggle');
    }
}

function deleteCookie(cookieName) {
    // Establece la fecha de caducidad en el pasado
    const pastDate = new Date(0);

    // Crea la cookie con la fecha de caducidad en el pasado
    document.cookie = cookieName + "=; expires=" + pastDate.toUTCString() + "; path=/";

    // También puedes especificar el dominio si es necesario
    // document.cookie = cookieName + "=; expires=" + pastDate.toUTCString() + "; path=/; domain=example.com";
}

function getCookie(cookieName) {
    const name = cookieName + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookieArray = decodedCookie.split(';');

    for (let i = 0; i < cookieArray.length; i++) {
        let cookie = cookieArray[i];
        while (cookie.charAt(0) === ' ') {
            cookie = cookie.substring(1);
        }
        if (cookie.indexOf(name) === 0) {
            return cookie.substring(name.length, cookie.length);
        }
    }

    return null; // Devuelve null si la cookie no se encuentra
}

function imprimirPDF() {
    var contenido = $('#pdf_add_input').summernote('code');
    var elemento = document.createElement('div');
    elemento.innerHTML = contenido;

    var opt = {
        margin: 0.1,
        filename: 'documento.pdf',
        image: {type: 'jpeg', quality: 0.98},
        html2canvas: {scale: 2},
        jsPDF: {unit: 'in', format: 'a4', orientation: 'portrait'}
    };

    html2pdf().set(opt).from(elemento).outputPdf('bloburl').then(function (url) {
        var nuevaVentana = window.open(url, '_blank');
        nuevaVentana.onload = function () {
            nuevaVentana.focus();
            nuevaVentana.print();
        };
    });
}

function agregarRolActivoALinks() {
        const rol = getRolActivo();
        if (!rol) return;

        document.querySelectorAll('a[href^="/"]:not([href^="//"])').forEach(link => {
            const href = link.getAttribute('href');

            // Evita modificar enlaces externos, anclas o JavaScript
            if (!href || href.startsWith('javascript:') || href.startsWith('#')) return;

            const url = new URL(href, window.location.origin);

            if (!url.searchParams.has('rol')) {
                url.searchParams.set('rol', rol);
                link.setAttribute('href', url.pathname + url.search + url.hash);
            }
        });
    }

document.addEventListener('DOMContentLoaded', agregarRolActivoALinks);