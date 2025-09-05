// Estado
window.wizardMode = false;
window.wizardStep = 0;
window.wizCtx = { id:null, numero:null,modo:null };

let firstStepSaved = false;

const WIZ_STEPS = [
  {
    name: 'seguimiento',
    // este paso lo abre tu click actual; acá solo definimos cómo "cerrarlo"
    open: () => $('#impo_marit_modal').dialog('open'),
    close: () => $('#impo_marit_modal').dialog('close'),
    requireSavedToAdvance: true,
      allowBack: false, // 👉 solo este paso exige guardado
  },
  {
    name: 'cronologia',
    open: () => abrirCronologiaPorIdNumero(wizCtx.id, wizCtx.numero),
    close: () => $('#cronologia_modal').dialog('close'),
    requireSavedToAdvance: false,
      allowBack: false,
  },
  {
    name: 'rutas',
    open: () => abrirRutasPorIdNumero(wizCtx.id, wizCtx.numero, $('#id_modo').val()),
    close: () => $('#rutas_modal').dialog('close'),
    requireSavedToAdvance: false,
      allowBack: true,
  },
  {
    name: 'envases',
    open:  () => abrirEnvasesPorIdNumero(wizCtx.id, wizCtx.numero, wizCtx.modo),
    close: () => $('#envases_modal').dialog('close'),
    requireSavedToAdvance: false,
    allowBack: true,
    enabled: () => !(wizCtx.modo === 'IMPORT AEREO' || wizCtx.modo === 'EXPORT AEREO'),
  },
    {
  name: 'embarques',
  open:  () => abrirEmbarquesPorIdNumero(wizCtx.id, wizCtx.numero, wizCtx.modo),
  close: () => $('#embarques_modal').dialog('close'),
  requireSavedToAdvance: false,
  allowBack: true,
  // enabled: () => true,  // opcional; si no lo ponés, queda habilitado por defecto
},
{
  name: 'aplicable',
  open:  () => abrirAplicablePorIdNumero(wizCtx.id, wizCtx.numero, wizCtx.modo),
  close: () => $('#aplicable_modal').dialog('close'),
  requireSavedToAdvance: false,
  allowBack: true,
  enabled: () => wizCtx.modo === 'IMPORT AEREO',   // 👈 solo IMPORT AEREO
},
{
  name: 'gastos',
  open:  () => abrirGastosPorIdNumero(wizCtx.id, wizCtx.numero, wizCtx.modo),
  close: () => $('#gastos_modal').dialog('close'),
  requireSavedToAdvance: false,
  allowBack: true,
  // enabled: () => true  // por defecto habilitado
},

];

function isStepEnabled(idx){
  const st = WIZ_STEPS[idx];
  return !st.enabled || st.enabled();   // si no define enabled => habilitado
}
function nextEnabledIndex(fromIdx){
  let i = fromIdx;
  while (i < WIZ_STEPS.length && !isStepEnabled(i)) i++;
  return i; // si i == length, no hay siguiente habilitado
}
function prevEnabledIndex(fromIdx){
  let i = fromIdx;
  while (i >= 0 && !isStepEnabled(i)) i--;
  return i; // si i < 0, no hay anterior habilitado
}
function lastEnabledIndex(){
  for (let i = WIZ_STEPS.length - 1; i >= 0; i--){
    if (isStepEnabled(i)) return i;
  }
  return 0;
}


// Helpers

function renderWizardToolbar(){
  return $(`
    <div class="wiz-toolbar">
      <button type="button" class="btn btn-secondary wiz-prev">◀ Anterior</button>
      <button type="button" class="btn btn-primary wiz-next">Siguiente ▶</button>
      <button type="button" class="btn btn-success wiz-finish">Finalizar</button>
      <button type="button" class="btn btn-dark wiz-cancel">Salir</button>
    </div>
  `);
}

function updateHeaderToolbarButtons_old($bar){
  const isFirst = (window.wizardStep === 0);
  const isLast  = (window.wizardStep === WIZ_STEPS.length - 1);
  const canGoBack = WIZ_STEPS[window.wizardStep].allowBack && window.wizardStep > 0;

  // visibilidad base por posición/flags
  $bar.find('.wiz-prev').toggle(canGoBack);
  $bar.find('.wiz-next').toggle(!isLast);
  $bar.find('.wiz-finish').toggle(isLast);

  // Paso 0 sin guardar → solo “Cancelar”
  if (window.wizardStep === 0 && !firstStepSaved) {
    $bar.find('.wiz-prev').hide();
    $bar.find('.wiz-next').hide();
    $bar.find('.wiz-finish').hide();
  }
}

function updateHeaderToolbarButtons($bar){
  const lastIdx   = lastEnabledIndex();
  const isLast    = (window.wizardStep === lastIdx);
  const canGoBack = WIZ_STEPS[window.wizardStep].allowBack && (prevEnabledIndex(window.wizardStep - 1) >= 0);

  $bar.find('.wiz-prev').toggle(canGoBack);
  $bar.find('.wiz-next').toggle(!isLast);
  $bar.find('.wiz-finish').toggle(isLast);

  // Paso 0 sin guardar → solo “Cancelar”
  if (window.wizardStep === 0 && !firstStepSaved) {
    $bar.find('.wiz-prev,.wiz-next,.wiz-finish').hide();
  }
}

function attachWizardToolbarToDialog($dialogEl){
  if (!window.wizardMode) return;
  const $widget   = $dialogEl.dialog('widget');
  const $titlebar = $widget.find('.ui-dialog-titlebar');

  $titlebar.css('position','relative');
    $widget.addClass('wiz-on');
  $titlebar.find('.wiz-toolbar').remove();

  const $bar = renderWizardToolbar();
  $titlebar.append($bar);

  // dejá aire al título si hace falta
  $widget.find('.ui-dialog-title').css('padding-right','340px');

  updateHeaderToolbarButtons($bar);
}

function refreshCurrentToolbar(){
  const $open = $('.ui-dialog:visible .ui-dialog-content').first();
  if ($open.length) attachWizardToolbarToDialog($open);
}


// Anterior
$(document).on('click', '.wiz-prev', function(){
  const step = WIZ_STEPS[window.wizardStep];
  if (!(step.allowBack && window.wizardStep > 0)) {
    alert('No se puede volver al paso anterior en esta etapa.');
    return;
  }
  step.close();
  const prevIdx = prevEnabledIndex(window.wizardStep - 1);
  if (prevIdx < 0) return;
  window.wizardStep = prevIdx;
  WIZ_STEPS[window.wizardStep].open();
  setTimeout(()=> refreshCurrentToolbar(), 0);
});

// Siguiente
$(document).on('click', '.wiz-next', function(){
  const step = WIZ_STEPS[window.wizardStep];
  if (step.requireSavedToAdvance && !firstStepSaved) return;

  step.close();
  const nextIdx = nextEnabledIndex(window.wizardStep + 1);
  if (nextIdx >= WIZ_STEPS.length) return;  // safety
  window.wizardStep = nextIdx;
  WIZ_STEPS[window.wizardStep].open();
  setTimeout(()=> refreshCurrentToolbar(), 0);
});


// Finalizar (no obligamos a guardar pasos > 0)
$(document).on('click', '.wiz-finish', function(){
  if (window.wizardStep !== WIZ_STEPS.length - 1) return;
  try { WIZ_STEPS[window.wizardStep].close(); } catch(e){}
  window.wizardMode = false;
  wizardReset({ restoreRowNumber: true });
});

// Cancelar
$(document).on('click', '.wiz-cancel', function(){
  // cerrá todo lo que pueda estar abierto
  try { $('#impo_marit_modal').dialog('close'); } catch(e){}
  try { $('#cronologia_modal').dialog('close'); } catch(e){}
  try { $('#rutas_modal').dialog('close'); } catch(e){}
  window.wizardMode = false;
  wizardReset({ restoreRowNumber: true });
});

$(document).on('seguimiento:guardado', function(evt, payload){
  firstStepSaved = true;            // ✅ ya puede avanzar
  wizCtx.id     = payload.id;
  wizCtx.numero = payload.numero;
  wizCtx.modo = payload.modo;
  // row_number=payload.numero;
  localStorage.setItem('id_seguimiento_seleccionado',payload.id);
  refreshCurrentToolbar();
    $("#id_id").val(payload.id);
});
// Post-guardado de Cronología (solo efecto en wizard)
$(document).on('cronologia:guardada', function(){
  if (!window.wizardMode) return;
  // no cerramos; dejamos que el usuario toque “Siguiente”
  refreshCurrentToolbar();
});

// Post-guardado de Rutas (solo efecto en wizard)
$(document).on('rutas:guardada', function(){
  if (!window.wizardMode) return;
  refreshCurrentToolbar();
});

// Post-guardado de Envases (solo efecto en wizard)
$(document).on('envases:guardado', function(){
  if (!window.wizardMode) return;
  refreshCurrentToolbar();
});
// Post-guardado de Embarques (solo efecto en wizard)
$(document).on('embarques:guardado', function(){
  if (!window.wizardMode) return;
  refreshCurrentToolbar();
});

// Post-guardado de "Aplicable" (solo tiene efecto en wizard)
$(document).on('aplicable:guardado', function(){
  if (!window.window.wizardMode) return;
  if (typeof refreshCurrentToolbar === 'function') refreshCurrentToolbar();
});

// Post-guardado de Gastos (solo efecto en wizard)
$(document).on('gastos:guardado', function(){
  if (!window.wizardMode) return;
  refreshCurrentToolbar();
});


function abrirCronologiaPorIdNumero(id, numero) {
  $('#cronologia_form').trigger("reset");
  console.log(id);
  get_datos_cronologia(id, function (ok) {
    if (!ok) return;
    $("#cronologia_modal").dialog({
      autoOpen: true,
        open: function(){
    if (window.wizardMode) {
      $(this).dialog('option','closeOnEscape', false);
      $('.ui-widget-overlay').off('click');
      attachWizardToolbarToDialog($(this));
    }
  },
      modal: true,
      title: "Fechas de cronologia para el seguimiento N°: " + numero,
      height: wHeight * 0.50,
      width:  wWidth * 0.40,
      class: 'modal fade',
      buttons: [
        {
          text: "Guardar",
          class: "btn btn-primary",
          style: "width:100px",
          click: function () {
            let formData = $("#cronologia_form").serializeArray();
            let data = JSON.stringify(formData);
            $.ajax({
              type: "POST",
              url: "/guardar_cronologia/",
              data: { id: id, data: data, csrfmiddlewaretoken: csrf_token },
              async: true,
            success: function (resultado) {
              if (resultado['resultado'] === 'exito') {
                mostrarToast("¡Cronologia guardada correctamente!", 'success');
                table.ajax.reload();
               //$("#cronologia_modal").dialog("close");
                // >>> evento para wizard
                $(document).trigger('cronologia:guardada');
               if (window.wizardMode) {
                 // en wizard: NO cerramos; dejamos que el usuario use “Siguiente”
                 refreshCurrentToolbar(); // por si querés refrescar botones
               } else {
                 $("#cronologia_modal").dialog("close"); // fuera del wizard: comportamiento normal
               }
              } else {
                alert(resultado['resultado']);
                $(document).trigger('cronologia:error', resultado['resultado']);
              }
            },
              error: function(e){
                alert(e);
                $(document).trigger('cronologia:error', e);
              }
            });
          },
        }
      ],

    });
  });
}

function abrirRutasPorIdNumero(id, numero, modo) {
    $.ajax({
        url: '/get_data_seguimiento/' + id + '/',
        type: 'GET',
        success: function (data) {
            if (data.bloqueado) {
                alert(data.mensaje);
                return;
            }
            get_datos_rutas();

            $('#rutas_form').trigger("reset");
            $("#id_origen").val('');   // opcional: podés precargar como hacías con row
            $("#id_destino").val('');
            $("#id_cia").val('');
            $("#id_viaje").val('');
            $("#id_vapor").val('');

            $("#rutas_modal").dialog({
                autoOpen: true,
                open: function(){
                    if (window.wizardMode) {
                      $(this).dialog('option','closeOnEscape', false);
                      $('.ui-widget-overlay').off('click');
                      attachWizardToolbarToDialog($(this)); // <<< importante
                    }
                  },
                modal: true,
                title: "Ingreso de datos para transbordos en el seguimiento N°: " + numero,
                height: 'auto',
                width: 'auto',
                position: { my: "top", at: "top+20", of: window },
                class: 'modal fade',
                buttons: [
                    {
                        text: "Eliminar",
                        class: "btn btn-danger",
                        style: "width:100px",
                        click: function () {
                            if (confirm('¿Confirma eliminar?')) {
                                row = table_rutas.rows('.table-secondary').data();
                                if (row.length === 1) {
                                    miurl = "/eliminar_ruta/";
                                    var toData = {
                                        'id': row[0][0],
                                        'csrfmiddlewaretoken': csrf_token,
                                    };
                                    $.ajax({
                                        type: "POST",
                                        url: miurl,
                                        data: toData,
                                        success: function (resultado) {
                                            aux = resultado['resultado'];
                                            if (aux === 'exito') {
                                                var idx = table.cell('.table-secondary', 0).index();
                                                table_rutas.$("tr.table-secondary").removeClass('table-secondary');
                                                table_rutas.row(idx).remove().draw(true);
                                                $('#tabla_rutas').DataTable().ajax.reload();
                                                $('#tabla_seguimiento').DataTable().ajax.reload();
                                                mostrarToast('¡Ruta eliminada correctamente!', 'success');
                                            } else {
                                                alert(aux);
                                            }
                                        }
                                    });
                                } else {
                                    alert('Debe seleccionar un unico registro');
                                }
                            }
                        },
                    },],
                beforeClose: function (event, ui) {
                    try {
                        desbloquearDatos();
                    } catch (error) {
                        console.error("⚠️ Error en desbloquearDatos:", error);
                    }
                    const $ciaInput = $("#id_cia");
                    if ($ciaInput.data("autocomplete-initialized")) {
                        $ciaInput.autocomplete("destroy");
                        $ciaInput.removeData("autocomplete-initialized");
                    }

                }
            });

            if (modo != 'IMPORT AEREO' && modo != 'EXPORT AEREO') {
                const $ciaInput = $("#id_cia");
                if (!$ciaInput.data("autocomplete-initialized")) {
                    $ciaInput.autocomplete({
                        source: '/autocomplete_clientes/',
                        minLength: 2,
                        select: function (event, ui) {
                            $(this).attr('data-id', ui.item['id']);
                        },
                        change: function (event, ui) {
                            if (ui.item) {
                                $(this).css({
                                    "border-color": "#3D9A37",
                                    'box-shadow': '0 0 0 0.1rem #3D9A37'
                                });
                                $('#id_cia').val(ui.item['value']).css({
                                    "border-color": "#3D9A37",
                                    'box-shadow': '0 0 0 0.1rem #3D9A37'
                                });
                            } else {
                                $(this).val('');
                                $('#id_cia').val('');
                                $(this).css({"border-color": "", 'box-shadow': ''});
                                $('#id_cia').css({"border-color": "", 'box-shadow': ''});
                            }
                        }
                    });
                    $ciaInput.data("autocomplete-initialized", true);
                }
            }
        }
    });
}

function abrirEnvasesPorIdNumero(id, numero, modo) {
  // si el modo es aéreo, este paso no aplica
  if (modo === 'IMPORT AEREO' || modo === 'EXPORT AEREO') {
    alert('No puede agregar envases a las operaciones aéreas.');
    return; // en wizard, el botón Siguiente ya salteará este paso
  }

  $.ajax({
    url: '/get_data_seguimiento/' + id + '/',
    type: 'GET',
    success: function (data) {
      if (data.bloqueado) {
        alert(data.mensaje);
        return;
      }
      get_datos_envases();
    }
  });

  $('#envases_form').trigger("reset");

  $("#envases_modal").dialog({
    autoOpen: true,
    open: function () {
      if (window.wizardMode) {
        $(this).dialog('option','closeOnEscape', false);
        $('.ui-widget-overlay').off('click');
        attachWizardToolbarToDialog($(this)); // barra en la titlebar
      }
    },
    modal: true,
    title: "Envases para el seguimiento N°: " + numero,
    height: wHeight * 0.80,
    width:  wWidth * 0.80,
    class: 'modal fade',
    buttons: [
      {
        text: "Eliminar",
        class: "btn btn-danger",
        style: "width:100px",
        click: function () {
          if (!confirm('¿Confirma eliminar?')) return;
          const row = table_envases.rows('.table-secondary').data();
          if (row.length !== 1) { alert('Debe seleccionar un unico registro'); return; }

          $.ajax({
            type: "POST",
            url: "/eliminar_envase/",
            data: { id: row[0][0], csrfmiddlewaretoken: csrf_token },
            success: function (resultado) {
              const aux = resultado['resultado'];
              if (aux === 'exito') {
                const idx = table.cell('.table-secondary', 0).index();
                table_envases.$("tr.table-secondary").removeClass('table-secondary');
                table_envases.row(idx).remove().draw(true);
                $('#tabla_seguimiento').DataTable().ajax.reload();
                mostrarToast('¡Envase eliminado correctamente!', 'success');
              } else {
                alert(aux);
              }
            }
          });
        },
      },
    ],
    beforeClose: function () {
      try { desbloquearDatos(); } catch(e){ console.error(e); }
    }
  });

  // si tenés sugerencias:
  try { get_sugerencias_envases(numero); } catch(e){}
}

function abrirEmbarquesPorIdNumero(id, numero, modo) {
  $.ajax({
    url: '/get_data_seguimiento/' + id + '/',
    type: 'GET',
    success: function (data) {
      if (data.bloqueado) {
        alert(data.mensaje);
        return;
      }
      get_datos_embarques();
      $('#embarques_form').trigger("reset");

      $("#embarques_modal").dialog({
        autoOpen: true,
        open: function () {
          if (window.wizardMode) {
            $(this).dialog('option','closeOnEscape', false);
            $('.ui-widget-overlay').off('click');
            attachWizardToolbarToDialog($(this));      // barra del wizard
          }
        },
        modal: true,
        title: "Embarques para el seguimiento N°: " + numero,
        height: wHeight * 0.80,
        width:  wWidth * 0.80,
        class: 'modal fade',
        buttons: [
          {
            text: "Eliminar",
            class: "btn btn-danger",
            style: "width:100px",
            click: function () {
              if (!confirm('¿Confirma eliminar?')) return;
              const row = table_embarques.rows('.table-secondary').data();
              let formDataExtra = $("#embarques_extra_form").serializeArray();
              let data_extra = JSON.stringify(formDataExtra);
              if (row.length !== 1) { alert('Debe seleccionar un unico registro'); return; }

              $.ajax({
                type: "POST",
                url: "/eliminar_embarque/",
                data: { id: row[0][0], data_extra: data_extra, csrfmiddlewaretoken: csrf_token },
                success: function (resultado) {
                  const aux = resultado['resultado'];
                  if (aux === 'exito') {
                    const idx = table.cell('.table-secondary', 0).index();
                    table_embarques.$("tr.table-secondary").removeClass('table-secondary');
                    table_embarques.row(idx).remove().draw(true);

                    try { $('#tabla_embarques').DataTable().ajax.reload(null, false); } catch(e){}
                    try { $('#tabla_seguimiento').DataTable().ajax.reload(null, false); } catch(e){}
                    try { table.ajax.reload(null, false); } catch(e){}

                    mostrarToast('¡Embarque eliminado correctamente!', 'success');
                  } else {
                    alert(aux);
                  }
                }
              });
            },
          },
        ],
        beforeClose: function () {
          try { desbloquearDatos(); } catch (error) { console.error("⚠️ Error en desbloquearDatos:", error); }
          try { $("#tabla_embarques").dataTable().fnDestroy(); } catch(e){}
        }
      });

      // por si necesitás usar el número luego:
      try { localStorage.setItem('numero_embarque', numero); } catch(e){}
    }
  });
}

function abrirAplicablePorIdNumero(id, numero, modo) {
  // si no es IMPORT AEREO y esto viene del wizard, simplemente no abrir
  if (window.wizardMode && modo !== 'IMPORT AEREO') return;

  $.ajax({
    url: '/get_data_seguimiento/' + id + '/',
    type: 'GET',
    success: function (data) {
      if (data.bloqueado) {
        alert(data.mensaje);
        return;
      }
      $('#form_aplicable').trigger("reset");
      cargar_datos_aplicables(numero);

      $("#aplicable_modal").dialog({
        autoOpen: true,
        modal: true,
        title: "Editar datos aplicables del seguimiento N°: " + numero,
        height: 'auto',
        width: wWidth * 0.50,
        open: function(){
          if (window.wizardMode) {
            $(this).dialog('option','closeOnEscape', false);
            $('.ui-widget-overlay').off('click');
            attachWizardToolbarToDialog($(this)); // barra del wizard en la titlebar
          }
        },
        buttons: [
          {
            text: "Guardar",
            class: "btn btn-primary",
            click: function () {
              // usa tu función actual — ver #3 para adaptar su success
              // si tu guardar_aplicable espera el número, pasalo directo:
              guardar_aplicable(numero);
            }
          },
        ],
        beforeClose: function () {
          try { desbloquearDatos(); } catch (e) { console.error(e); }
        }
      });
    }
  });
}

function abrirGastosPorIdNumero(id, numero, modo) {
  $.ajax({
    url: '/get_data_seguimiento/' + id + '/',
    type: 'GET',
    success: function (data) {
      if (data.bloqueado) {
        alert(data.mensaje);
        return;
      }
      get_datos_gastos();
      $('#gastos_form').trigger("reset");

      $("#gastos_modal").dialog({
        autoOpen: true,
        open: function () {
          // // setear socio por defecto si lo tenés disponible
          // if (typeof wizCtx.socio !== 'undefined') {
          //   $('#id_socio').val(wizCtx.socio);
          // } else {
          //   // fuera del wizard, si abriste desde la tabla podés mantener tu lógica previa
          //   try {
          //     const row = table.rows('.table-secondary').data();
          //     if (row && row.length === 1) $('#id_socio').val(row[0][54]);
          //   } catch(e){}
          // }

          // barra del wizard en la titlebar
          if (window.wizardMode) {
            $(this).dialog('option','closeOnEscape', false);
            $('.ui-widget-overlay').off('click');
            attachWizardToolbarToDialog($(this));
          }
        },
        modal: true,
        title: "Gastos para el seguimiento N°: " + numero,
        height: wHeight * 0.90,
        width:  wWidth * 0.90,
        class: 'modal fade',
        buttons: [
          {
            text: "Eliminar",
            class: "btn btn-danger",
            style: "width:100px",
            click: function () {
              if (!confirm('¿Confirma eliminar el gasto seleccionado?')) return;
              const row_g = table_gastos.rows('.table-secondary').data();
              if (row_g.length !== 1) { alert('Debe seleccionar un único registro'); return; }

              $.ajax({
                type: "POST",
                url: "/eliminar_gasto/",
                data: { id: row_g[0][0], csrfmiddlewaretoken: csrf_token },
                success: function (resultado) {
                  const aux = resultado['resultado'];
                  if (aux === 'exito') {
                    try { $('#tabla_gastos').DataTable().ajax.reload(null, false); } catch(e){}
                    try { $('#tabla_seguimiento').DataTable().ajax.reload(null, false); } catch(e){}
                    try { table.ajax.reload(null, false); } catch(e){}
                    mostrarToast('¡Gasto eliminado correctamente!', 'success');

                    // Si querés mantener el socio por defecto tras eliminación:
                    if (typeof data.socio_default !== 'undefined') {
                      $('#id_socio').val(data.socio_default);
                    }
                  } else {
                    alert(aux);
                  }
                }
              });
            },
          },
        ],
        beforeClose: function () {
          try { desbloquearDatos(); } catch (error) { console.error("⚠️ Error en desbloquearDatos:", error); }
        }
      });
    }
  });
}

function wizardReset(opts = {}) {
  const { restoreRowNumber = true } = opts;

  // 1) flags/estado
  window.wizardMode  = false;
  window.wizardStep  = 0;
  window.wizCtx      = { id:null, numero:null, modo:null };
  if (typeof firstStepSaved !== 'undefined') firstStepSaved = false;

  // 2) UI: quita toolbars del título en cualquier diálogo abierto
  try {
    $('.ui-dialog').removeClass('wiz-on')
      .find('.ui-dialog-titlebar .wiz-toolbar').remove();
  } catch(e){}

  // 3) Rehabilitá cierres “normales” de jQuery UI
  try {
    $('.ui-dialog-content:visible').each(function(){
      $(this).dialog('option', 'closeOnEscape', true);
    });
  } catch(e){}

  // 4) LocalStorage u otras cachés temporales
  // try { localStorage.removeItem('id_seguimiento_seleccionado'); } catch(e){}
  // try { localStorage.removeItem('numero_embarque'); } catch(e){}

  // 5) row_number (si usás el shim)
  //    - si querés que el sistema vuelva a usar el seleccionado en la grilla:
  if (restoreRowNumber) {
    try {
      // Si hay una fila seleccionada, restaurá ese numero; si no, dejalo null.
      const sel = (typeof table !== 'undefined') ? table.rows('.table-secondary').data() : null;
      if (sel && sel.length === 1) {
        // IMPORTANTE: asignación SIMPLE (sin var/let/const) para que pegue en el shim
        row_number = sel[0][1];
      } else {
        // o dejalo nulo
        row_number = null;
      }
    } catch(e){
      // si algo falla, al menos liberalo
      row_number = null;
    }
  }
}
