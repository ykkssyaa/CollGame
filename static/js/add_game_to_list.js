document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('addToListButton').addEventListener('click', function () {
        var userLists = document.getElementById('userLists');
        if (userLists.style.display === 'none') {
            userLists.style.display = 'block';
        } else {
            userLists.style.display = 'none';
        }
    });

    var listButtons = document.querySelectorAll('.userListButton');
    listButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            var listId = this.getAttribute('data-listid');
            var gameId = "{{ game.id }}"; // замените на соответствующий идентификатор вашей игры
            addToUserList(listId, gameId);
        });
    });

    function addToUserList(listId, gameId) {

        fetch('/add-to-list/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({
                list_id: listId,
                game_id: gameId
            })
        }).then(function (response) {
            if (response.ok) {
                // обработка успешного добавления игры в список
                console.log('Игра успешно добавлена в список');
            } else {
                // обработка ошибки
                console.error('Ошибка при добавлении игры в список');
            }
        }).catch(function (error) {
            console.error('Ошибка при отправке запроса:', error);
        });
    }
});

