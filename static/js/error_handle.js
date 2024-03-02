// Функция для получения значения параметра из URL
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

// Получаем значение параметра error из URL
var errorMessage = getParameterByName('error');

// Если параметр error был найден, выводим его в alert
if (errorMessage) {
    alert(errorMessage);

    // Удаляем параметр error из URL и перенаправляем пользователя
    var newUrl = window.location.href.split('?')[0];
    window.history.replaceState({}, document.title, newUrl);
}