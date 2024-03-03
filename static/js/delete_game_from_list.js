// Получаем все кнопки удаления
var deleteButtons = document.querySelectorAll('.delete-btn');
var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

deleteButtons.forEach(function (button) {
    button.addEventListener('click', function () {
        // Получаем идентификатор игры из атрибута data-game-id
        var gameId = button.getAttribute('data-game-id');
        var list_id = getParameterByName('list');

        var requestBody = {
            game_id: gameId,
            list_id: list_id
        };

        // Отправляем запрос на сервер для удаления игры
        fetch('/users/delete-from-list', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(requestBody),
        })
            .then(response => {
                if (response.ok) {
                    console.log('Успешное удаление игры');
                    window.location.reload();
                } else {
                    console.error('Ошибка удаления игры');
                }
            })
            .catch(error => {
                console.error('Ошибка удаления игры:', error);
            });
    });
});