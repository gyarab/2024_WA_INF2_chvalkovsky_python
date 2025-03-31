document.addEventListener("DOMContentLoaded", function() {
    var guitarImage = document.querySelector(".guitar-image");
        guitarImage.onclick = function() {
            this.classList.toggle("large");
        };
});
function redirectToBrand(id) {
    window.location.href = "/brand/" + id;
}