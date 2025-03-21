$(document).ready(function () {
    // Функция для копирования информации о товаре
    window.copyProductInfo = function() {
        var productInfoField = document.getElementById("productInfoField");
        productInfoField.select();
        document.execCommand("copy");

        // Изменение текста кнопки для обратной связи
        var copyButton = document.getElementById("copyButton");
        copyButton.innerHTML = '<i class="fas fa-check"></i> Скопировано';

        // Возвращаем оригинальный текст через 2 секунды
        setTimeout(function () {
            copyButton.innerHTML = '<i class="fas fa-copy"></i> Копировать';
        }, 2000);
    };
});