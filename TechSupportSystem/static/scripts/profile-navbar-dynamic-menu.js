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


    const adminDropdown = document.querySelector(".admin-options");
    const adminNav = document.querySelector(".admin-nav-bar");

    const adminDynamicDropdownActivate = document.querySelector(".admin-dynamic-dropdown-activate");
    adminDynamicDropdownActivate.addEventListener("click", function () {
        if (adminDropdown.style.display === "block") {
            adminDropdown.style.display = "none";
        } else {
            adminDropdown.style.display = "block";
            };

    });
    window.addEventListener('click', function(){
        if (event.target !== adminDynamicDropdownActivate && event.target !== adminDropdown) {
            adminDropdown.style.display = "none";
        };
        
    });
});