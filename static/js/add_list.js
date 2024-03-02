document.addEventListener('DOMContentLoaded', function() {
    const createListBtn = document.getElementById('createListBtn');
    const createListForm = document.getElementById('createListForm');
    const listForm = document.getElementById('listForm');

    createListBtn.addEventListener('click', function() {
        createListForm.style.display = 'block';
    });

});
