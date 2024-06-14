
$("#toast").delay(2000).fadeOut('slow')

function showErrorMessage(message) {
    var toast = $('#toastX');
    toast.text(message);
    //toast.addClass('show');
    toast.removeClass('d-none');
    toast.fadeIn();
    setTimeout(function() {
        toast.fadeOut();
    }, 2000); // 2 秒后隐藏 toast
}

/**
 * Converts the value of an input field to uppercase.
 * @param {string} item - The ID of the input field.
 */
function convertToUppercase(item) {
    // Get the input field element by its ID
    var inputField = document.getElementById(item);

    // Convert the input field value to uppercase
    inputField.value = inputField.value.toUpperCase();
}

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});