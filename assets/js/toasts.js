document.addEventListener('DOMContentLoaded', function () {
    // Инициализация всех тостов
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl, {
            autohide: true,
            delay: 5000
        });
    });

    // Автоматическое скрытие тостов через 5 секунд
    setTimeout(function () {
        toastList.forEach(toast => toast.hide());
    }, 5000);
});
