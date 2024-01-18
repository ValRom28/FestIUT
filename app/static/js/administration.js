document.addEventListener("DOMContentLoaded", function() {
    var close1 = document.getElementById("close1");
    var close2 = document.getElementById("close2");
    var close3 = document.getElementById("close3");

    close1.addEventListener('click', function () {
        var modal = document.getElementById('popup');
        modal.style.display = 'none';
    });

    close2.addEventListener('click', function () {
        var modal = document.getElementById('popup2');
        modal.style.display = 'none';
    });

    close3.addEventListener('click', function () {
        var modal = document.getElementById('popup3');
        modal.style.display = 'none';
    });

    document.querySelector('.gestionGroupe').addEventListener('click', function () {
        var modal = document.getElementById('popup');
        modal.style.display = 'block';
    });

    document.querySelector('.gestionConcert').addEventListener('click', function () {
        var modal = document.getElementById('popup2');
        modal.style.display = 'block';
    });

    document.querySelector('.gestionEvenement').addEventListener('click', function () {
        var modal = document.getElementById('popup3');
        modal.style.display = 'block';
    });
});
