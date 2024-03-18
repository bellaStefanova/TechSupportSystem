document.addEventListener("DOMContentLoaded", function () {
    const takeRequestButton = document.getElementById('take-request');
    let requestId = document.getElementById('request-id').getAttribute('request-id');
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
});