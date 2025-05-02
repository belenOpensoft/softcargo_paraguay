$(document).ready(function() {
const dataDiv = document.getElementById('entregaDocsData');

const hayResultados = parseInt(document.getElementById('entregaDocsData').dataset.resultados);
const clienteEntrega = JSON.parse(document.getElementById('cliente-data').textContent);
const despachanteEntrega = JSON.parse(document.getElementById('despachante-data').textContent);


  function cargarDatosEntrega(tipo) {
    const datos = tipo === 'cliente' ? clienteEntrega : despachanteEntrega;
    $('#id_nombre_entrega').val(datos.nombre);
    $('#id_direccion_entrega').val(datos.direccion);
    $('#id_ciudad_entrega').val(datos.ciudad);
    $('#id_telefono_entrega').val(datos.telefono);
  }

  if (hayResultados > 0) {
    $("#modalEntregaDocumentacion").dialog({
      modal: true,
      width: "60%",
      height: 'auto',
        buttons: [
        {
          text: "Imprimir",
          click: function () {
             $("#formEntregaDocumentacion").attr("action", "/importacion_maritima/generar_entrega_documentacion_pdf/").attr("target", "_blank").submit();
          },
          class: "btn btn-warning"
        },
        {
          text: "Cerrar",
          click: function () {
            $(this).dialog("close");
          },
          class: "btn btn-dark"
        }
      ],
    });
  } else {
    alert("No se encontraron resultados.");
  }
      // Inicial
    cargarDatosEntrega($('input[name="entregar_a"]:checked').val());

    // Al cambiar la opción
    $('input[name="entregar_a"]').change(function () {
      cargarDatosEntrega($(this).val());
    });

});

