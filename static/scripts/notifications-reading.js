if (window.location.pathname === '/view-notifications/') {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    document.addEventListener('DOMContentLoaded', function () {
        const unreadNotifications = document.querySelectorAll('.unread-notification');
        const readAllNotificationsButton = document.getElementById('readAllNotifications');

        // Reading the notification - making it not bold font
        unreadNotifications.forEach(notification => {
            notification.addEventListener('click', function() {
                const unreadNotificationChildren = notification.children;
                for (let child of unreadNotificationChildren) {
                    if (child.tagName === 'P') {
                        child.style.fontWeight = 'normal';
                        if (child.classList.contains('unread-notification')) {
                            child.classList.remove('unread-notification');
                        };
                    };

                };
            });
        });

        // Redirecting to the view-request page when clicking on the notification
        const readNotifications = document.querySelectorAll('.read-notification');
        const allNotifications = [...unreadNotifications, ...readNotifications];

        allNotifications.forEach(notification => {
            notification.addEventListener('click', function() {
                const allNotificationChildren = notification.children;
                for (let child of allNotificationChildren) {
                    if (child.tagName === 'P' && child.classList.contains('notification-id')) {
                        let notificationId = child.getAttribute('notification-id');
                        let userId = child.getAttribute('user-id');
                        let requestId = child.getAttribute('request-id');
                        if (requestId !== null) {
                            windowLocationHref = '/view-request/' + requestId + '/';
                        } else if (userId !== null && userId !== 'myId') {
                            windowLocationHref = '/edit-user/' + userId;
                        } else if (userId === 'myId') {
                            windowLocationHref = '/profile' + '/';
                        }
                                            fetch('/mark-notification-as-read/' + notificationId + '/', {
                                                method: 'POST',
                                                headers: {
                                                    'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token
                                                    'Content-Type': 'application/json'
                                                },
                                            })
                                            .then(response => {
                                                if (response.ok) {
                                                    window.location.href = windowLocationHref;
                                                } else {
                                                    console.log(response);
                                                }
                                            })
                                            .catch(error => {
                                                console.log('Error marking notification as read');
                                            });
                        };
                };
            });
        });
        readAllNotificationsButton.addEventListener('click', function() {
            fetch('/mark-all-notifications-as-read/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token
                    'Content-Type': 'application/json'
                },
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/view-notifications' + '/';
                } else {
                    console.log(response);
                }
            })
            .catch(error => {
                console.log('Error marking notification as read');
            });
        });


    });
};
