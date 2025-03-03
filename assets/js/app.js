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
        var images = $(this).data('images').split(',').map(img => img.trim()); // Получаем список всех изображений и удаляем лишние пробелы
        var carouselInner = $('#carouselInner'); // Обращаемся к контейнеру для слайдов карусели
        carouselInner.empty(); // Очищаем карусель перед вставкой новых слайдов

        // Определение индекса текущего изображения в массиве изображений
        var currentImage = $(this).attr('src');
        var currentIndex = images.findIndex(img => img === currentImage);
        if (currentIndex === -1) currentIndex = 0; // Если изображение не найдено, используем первое

        // Проверяем, есть ли изображения
        if (images.length > 0) {
            // Динамически добавляем изображения в карусель
            $.each(images, function (index, image) {
                var activeClass = index === currentIndex ? 'active' : ''; // Активным будет выбранное изображение
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
    });
});

