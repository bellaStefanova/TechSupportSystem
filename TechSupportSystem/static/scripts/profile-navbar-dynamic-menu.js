document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.querySelector(".profile-options");
    const profileNav = document.querySelector(".profile-nav-bar");

    profileNav.addEventListener("mouseenter", function () {
        dropdown.style.display = "block";
        // dropdown.style.transition = "max-height 0.3s ease";
    });
    profileNav.addEventListener("mouseleave", function () {
        dropdown.style.display = "none";
    });
});