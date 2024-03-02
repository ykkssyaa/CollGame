document.querySelectorAll('.like-button').forEach(button => {
    button.addEventListener('click', function() {
        const reviewId = this.getAttribute('data-review-id');
        const likesSpan = document.getElementById('review_likes_' + reviewId);

        fetch('/activity/like-review/' + reviewId)
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    this.innerText = 'Liked';
                    likesSpan.innerText = parseInt(likesSpan.innerText) + 1;
                    this.classList.add('button_liked');
                    this.classList.remove('button_not_liked');
                } else {
                    this.innerText = 'Like';
                    likesSpan.innerText = parseInt(likesSpan.innerText) - 1;
                    this.classList.add('button_not_liked');
                    this.classList.remove('button_liked');
                }
            });
    });
});
