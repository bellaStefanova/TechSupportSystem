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

document.addEventListener("DOMContentLoaded", function () {
    const unreadNotifications = document.querySelectorAll('.unread-notification');

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
                    let requestId = child.getAttribute('request-id');
                    console.log(notificationId);
                    console.log(requestId);
                                        fetch('/mark-notification-as-read/' + notificationId + '/', {
                                            method: 'POST',
                                            headers: {
                                                'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token
                                                'Content-Type': 'application/json'
                                            },
                                        })
                                        .then(response => {
                                            if (response.ok) {
                                                window.location.href = "/view-request/" + requestId;
                                            } else {
                                                console.log(response);
                                            }
                                        })
                                        .catch(error => {
                                            console.log('Error marking notification as read');
                                            // console.log(error);
                                            // console.log(requestId)
                                        });
                    };
            };
        });
    });
});

