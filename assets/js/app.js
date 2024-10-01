$(document).ready(function () {
    // Обработчик для изменения input[type="file"]
    $('input[type="file"]').on('change', function () {
        var fileInput = $(this)[0];
        if (fileInput.files && fileInput.files[0]) {
            var file = fileInput.files[0];
            var url = URL.createObjectURL(file);
            $('.custom-file-label').html(file.name); // Обновляем метку файла
        }
    });

    // Обработчик для клика на изображение товара
    $('.product-image').on('click', function () {
        var images = $(this).data('images').split(','); // Получаем список всех изображений
        var carouselInner = $('#carouselInner'); // Обращаемся к контейнеру для слайдов карусели
        carouselInner.empty(); // Очищаем карусель перед вставкой новых слайдов

        // Проверяем, есть ли изображения
        if (images.length > 0) {
            // Динамически добавляем изображения в карусель
            $.each(images, function (index, image) {
                var activeClass = index === 0 ? 'active' : ''; // Первый слайд активен
                carouselInner.append(`
                    <div class="carousel-item ${activeClass}">
                        <img class="d-block img-fluid" src="${image}" alt="Product Image">
                    </div>
                `);
            });

            // Открываем модальное окно с каруселью
            $('#imageModal').modal('show');
        } else {
            alert('Изображения не найдены для этого товара.');
        }

        // Реинициализация карусели (если необходимо)
        $('#imageModal .carousel').carousel(0); // Перемещаем карусель на первый элемент
    });
});
