document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.querySelector(".profile-options");
    const profileNav = document.querySelector(".profile-nav-bar");

    const profileDynamicDropdownActivate = document.querySelector(".profile-dynamic-dropdown-activate");
    profileDynamicDropdownActivate.addEventListener("click", function () {
        if (dropdown.style.display === "block") {
            dropdown.style.display = "none";
        } else {
            dropdown.style.display = "block";
            };

    });
    window.addEventListener('click', function(){
        if (event.target !== profileDynamicDropdownActivate && event.target !== dropdown) {
            dropdown.style.display = "none";
        };
        
    });
});