function filterGuitars() {
    var brandFilter = document.getElementById("brand-filter").value;
    var pickupFilter = document.getElementById("pickup-filter").value;
    var shapeFilter = document.getElementById("shape-filter").value;

    var guitars = document.querySelectorAll(".guitar-preview");
    var visibleGuitarCount = 0;

    guitars.forEach(function (guitar) {
        var brand = guitar.getAttribute("data-brand");
        var pickup = guitar.getAttribute("data-pickup");
        var shape = guitar.getAttribute("data-shape");

        var matchesBrand = brandFilter === "" || brand === brandFilter;
        var matchesPickup = pickupFilter === "" || pickup === pickupFilter;
        var matchesShape = shapeFilter === "" || shape === shapeFilter;

        if (matchesBrand && matchesPickup && matchesShape) {
            guitar.style.display = "block";
            visibleGuitarCount++;
        } else {
            guitar.style.display = "none";
        }
    });

    notFound(visibleGuitarCount);
}

function notFound(visibleCount) {
    var notFound = document.querySelector(".not-found");
    if (visibleCount === 0) {
        notFound.style.display = "block";
    } else {
        notFound.style.display = "none";
    }
}