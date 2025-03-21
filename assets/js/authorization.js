$(document).ready(function () {
    // Функция для переключения видимости пароля
    window.togglePasswordVisibility = function(passwordFieldId, iconId) {
        const passwordField = document.getElementById(passwordFieldId);
        const toggleIcon = document.getElementById(iconId);

        if (passwordField.type === 'password') {
            passwordField.type = 'text';
            toggleIcon.classList.remove('fa-eye');
            toggleIcon.classList.add('fa-eye-slash');
        } else {
            passwordField.type = 'password';
            toggleIcon.classList.remove('fa-eye-slash');
            toggleIcon.classList.add('fa-eye');
        }
    };

    // Пример использования функции togglePasswordVisibility
    $('#togglePasswordButton').on('click', function () {
        togglePasswordVisibility('id_password', 'togglePasswordIcon');
    });
});