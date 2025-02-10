
function toggle_collapse_menu(targetId, linkElement) {
    // Obtén el elemento objetivo usando el id
    var targetElement = document.getElementById(targetId);
    var icon = linkElement.querySelector('.toggle-icon'); // Obtén el ícono de la flecha

    // Verifica si el elemento está actualmente colapsado o no
    if (targetElement.classList.contains('show')) {
        // Si está expandido, colápaselo
        var bsCollapse = bootstrap.Collapse.getInstance(targetElement);
        if (bsCollapse) {
            bsCollapse.hide();
        } else {
            new bootstrap.Collapse(targetElement).hide();
        }
        // Cambia la flecha a hacia abajo
        icon.classList.remove('fa-chevron-up');
        icon.classList.add('fa-chevron-down');
    } else {
        // Si está colapsado, expándelo
        var bsCollapse = bootstrap.Collapse.getInstance(targetElement);
        if (bsCollapse) {
            bsCollapse.show();
        } else {
            new bootstrap.Collapse(targetElement).show();
        }
        // Cambia la flecha a hacia arriba
        icon.classList.remove('fa-chevron-down');
        icon.classList.add('fa-chevron-up');
    }
}
