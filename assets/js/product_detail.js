function copyProductInfo() {
    var productInfoField = document.getElementById("productInfoField");
    productInfoField.select();
    document.execCommand("copy");

    // Изменение текста кнопки для обратной связи
    var copyButton = document.getElementById("copyButton");
    copyButton.innerHTML = '<i class="fa fa-check"></i> Скопировано';

    // Возвращаем оригинальный текст через 2 секунды
    setTimeout(function () {
        copyButton.innerHTML = '<i class="fa fa-copy"></i> Копировать';
    }, 2000);
}
