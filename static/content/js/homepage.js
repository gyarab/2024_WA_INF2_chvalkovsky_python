function filterGuitars() {
    var pickupFilter = document.getElementById("pickup-filter").value;
    var shapeFilter = document.getElementById("shape-filter").value;

    var guitars = document.querySelectorAll(".guitar-preview");
    var visibleGuitarCount = 0;

    guitars.forEach(function (guitar) {
        var pickup = guitar.getAttribute("data-pickup");
        var shape = guitar.getAttribute("data-shape");

        var matchesPickup = pickupFilter === "" || pickup === pickupFilter;
        var matchesShape = shapeFilter === "" || shape === shapeFilter;

        if (matchesPickup && matchesShape) {
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
function resetFilters() {
    document.querySelectorAll('.filter').forEach(function(filter) {
        filter.value = "All";
    });
    filterGuitars();
}