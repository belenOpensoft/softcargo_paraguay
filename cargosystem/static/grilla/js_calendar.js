
//document.addEventListener('DOMContentLoaded', function () {
//alert();
//    var calendarEl = document.getElementById('calendar');
//
//    var calendar = new Calendar(calendarEl, {
//        plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
//        initialView: 'dayGridMonth',
//        events: [
//            { title: 'Evento 1', start: '2024-10-01' },
//            { title: 'Evento 2', start: '2024-10-05', end: '2024-10-07' }
//        ],
//        locale: 'es',
//        headerToolbar: {
//            left: 'prev,next today',
//            center: 'title',
//            right: 'dayGridMonth,timeGridWeek,timeGridDay'
//        }
//    });
//
//    calendar.render();
//
////    var calendar = new FullCalendar.Calendar(calendarEl, {
////    initialView: 'dayGridMonth',
////    events: function (fetchInfo, successCallback, failureCallback) {
////        $.ajax({
////            url: '/mi-api-de-eventos/',  // URL para obtener eventos
////            type: 'GET',
////            dataType: 'json',
////            success: function (data) {
////                successCallback(data);  // Devuelve los eventos
////            },
////            error: function () {
////                failureCallback();
////            }
////        });
////    },
////    locale: 'es',
////    headerToolbar: {
////        left: 'prev,next today',
////        center: 'title',
////        right: 'dayGridMonth,timeGridWeek,timeGridDay'
////    }
////});
////
////calendar.render();
//
//});

document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    locale: 'es',  // Puedes cambiar esto al idioma que prefieras
    events: '/ruta/a/tu/api/para/obtener/eventos/',  // URL para tus eventos
  });

  calendar.render();
});


