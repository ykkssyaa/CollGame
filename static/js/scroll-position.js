// Восстанавливаем позицию скролла после перезагрузки страницы
window.onload = function() {
    var savedScrollPosition = localStorage.getItem('scrollPosition');
    if (savedScrollPosition !== null) {
        window.scrollTo(0, savedScrollPosition);
        localStorage.removeItem('scrollPosition'); // Очищаем сохраненную позицию скролла
    }
};

// Сохраняем позицию скролла перед перезагрузкой страницы
window.onbeforeunload = function() {
    var scrollPosition = window.scrollY;
    localStorage.setItem('scrollPosition', scrollPosition);
};