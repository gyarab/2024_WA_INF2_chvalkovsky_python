function redirect() {
    window.location.href = "/";
}

document.addEventListener("DOMContentLoaded", function() {
    var guitarImage = document.querySelector(".guitar-image");
        guitarImage.onclick = function() {
            this.classList.toggle("large");
        };
});