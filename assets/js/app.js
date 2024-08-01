$(document).ready(function () {
	$('input[type="file"]').on('change', function () {
		var fileInput = $(this)[0];
		if (fileInput.files && fileInput.files[0]) {
			var file = fileInput.files[0];
			var url = URL.createObjectURL(file);
			$('.custom-file-label').html(file.name); // Обновляем метку файла
		}
	});
});