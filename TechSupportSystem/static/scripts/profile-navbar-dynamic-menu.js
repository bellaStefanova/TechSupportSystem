document.addEventListener("DOMContentLoaded", function () {
    if (window.location.pathname === "/signin/" || window.location.pathname === "/signup/") {
        // Accessing sign up URL from navbar
        const signUpNavElement = document.getElementById("signupNavBar");
        signUpNavElement.addEventListener("click", function () {
            window.location.href = "/signup";
        });

        // Accessing sign in URL from navbar
        const signInNavElement = document.getElementById("signinNavBar");
        signInNavElement.addEventListener("click", function () {
            window.location.href = "/signin";
        });
    } else {

        // Accessing home URL from navbar
        const homeNavElement = document.getElementById("homeNavBar");
        if (homeNavElement) {
            homeNavElement.addEventListener("click", function () {
                window.location.href = "/home";
            });
        };

        // Accessing dashboard URL from navbar
        const dashboardNavElement = document.getElementById("dashboardNavBar");
        if (dashboardNavElement) {
            dashboardNavElement.addEventListener("click", function () {
                window.location.href = "/dashboard";
            });
        }

        // Accessing notifications URL from navbar
        const notificationsNavElement = document.getElementById("notificationsNavBar");
        notificationsNavElement.addEventListener("click", function () {
            window.location.href = "/view-notifications";
        });

        // Accessing profile sub navbar URL from navbar
        const dropdown = document.querySelector(".profile-options");
        const profileNavElement = document.getElementById("profileNavBar");
        profileNavElement.addEventListener("click", function () {
            if (dropdown.style.display === "block") {
                dropdown.style.display = "none";
            } else {
                dropdown.style.display = "block";
                const profileDetailsElement = document.getElementById("profileDetails");
                profileDetailsElement.addEventListener("click", function () {
                    window.location.href = "/profile";
                });
                const changePasswordElement = document.getElementById("changePassword");
                changePasswordElement.addEventListener("click", function () {
                    window.location.href = "/change-password";
                });
                const signOutElement = document.getElementById("signOut");
                signOutElement.addEventListener("click", function () {
                    window.location.href = "/signout";
                });
            };
        });
        window.addEventListener('click', function(){
            if (event.target !== profileNavElement && !profileNavElement.contains(event.target) && event.target !== dropdown) {
                dropdown.style.display = "none";
            };
        });

        // Accessing admin sub navbar URL from navbar
        const adminNavElement = document.getElementById("adminNavBar");
        const adminDropdown = document.querySelector(".admin-options");

        if (adminNavElement) {
            adminNavElement.addEventListener("click", function () {
                if (adminDropdown.style.display === "block") {
                    adminDropdown.style.display = "none";
                } else {
                    adminDropdown.style.display = "block";
                    const manageDepartmentsElement = document.getElementById("manageDepartments");
                    manageDepartmentsElement.addEventListener("click", function () {
                        window.location.href = "/departments";
                    });
                    const manageRolesElement = document.getElementById("manageRoles");
                    manageRolesElement.addEventListener("click", function () {
                        window.location.href = "/roles";
                    });
                    const manageUsersElement = document.getElementById("manageUsers");
                    manageUsersElement.addEventListener("click", function () {
                        window.location.href = "/users";
                    });
                };

            });
            window.addEventListener('click', function(){
                if (event.target !== adminNavElement && !adminNavElement.contains(event.target) && event.target !== adminDropdown) {
                    adminDropdown.style.display = "none";
                };
            });
        };

        // const myTeamDropdown = document.querySelector(".my-team-options");
        // const myTeamNav = document.querySelector(".my-team-nav-bar");

        // const myTeamDynamicDropdownActivate = document.querySelector(".my-team-dynamic-dropdown-activate");
        //     if (myTeamDynamicDropdownActivate) {
        //     myTeamDynamicDropdownActivate.addEventListener("click", function () {
        //         if (myTeamDropdown.style.display === "block") {
        //             myTeamDropdown.style.display = "none";
        //         } else {
        //             myTeamDropdown.style.display = "block";
        //             };

        //     });
        //     window.addEventListener('click', function(){
        //         if (event.target !== myTeamDynamicDropdownActivate && event.target !== myTeamDropdown) {
        //             myTeamDropdown.style.display = "none";
        //         };
                
        //     });
        // };
    };
});