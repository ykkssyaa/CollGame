document.addEventListener('DOMContentLoaded', function() {
    const userAvatarBtn = document.querySelector('.user-avatar-btn');
    const userLinks = document.querySelector('.user-links');

    if (userAvatarBtn) {
        userAvatarBtn.addEventListener('click', function() {
            userLinks.classList.toggle('d-none');
        });
    }
});

