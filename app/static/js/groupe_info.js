document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.sup').addEventListener('click', function () {
        var modal = document.getElementById('popup');
        modal.style.display = 'block';
    });
    document.getElementById('non').addEventListener('click', function() {
        var modal = document.getElementById('popup');
        modal.style.display = 'none';
    });
});


