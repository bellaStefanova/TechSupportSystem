if (window.location.pathname.indexOf('/view-request') !== -1) {
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
    };

    document.addEventListener("DOMContentLoaded", function () {
        const takeRequestButton = document.getElementById('take-request');
        let requestId = document.getElementById('request-id').getAttribute('request-id');
        if (takeRequestButton) {
            takeRequestButton.addEventListener('click', function () {
                fetch('/take-request/' + requestId + '/', {
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
                        console.log('');
                    });

            });
        };

        const markRequestDoneButton = document.getElementById('markRequestDone');
        if (markRequestDoneButton) {
            markRequestDoneButton.addEventListener('click', function () {
                fetch('/mark-request-done/' + requestId + '/', {
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
                        console.log('');
                    });

            });
        };
    });
}