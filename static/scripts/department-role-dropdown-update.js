if (window.location.pathname === '/edit-profile') {

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

    document.addEventListener('DOMContentLoaded', function () {
        const departmentSelector = document.getElementById('id_department');


        const departmentId = departmentSelector.value;
            if (departmentId) {
                var url = '/get-roles-for-department/';
                fetch(url, {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest',
                    },
                    body: JSON.stringify({ 'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest' ,
                    'department_id': departmentId})
                })
                    
                    .then(response => response.json())
                    .then(data => {
                        var roleSelect = document.getElementById('id_role');
                        var roles = roleSelect.querySelectorAll('option');
                        let selectedName;
                        for (let child of roles) {
                            if (!child.selected) {
                                child.remove();
                            } else {
                                selectedName = child.textContent;
                            }
                        }
                        let basicOption = document.createElement('option');
                        basicOption.value = '';
                        basicOption.textContent = '---------';
                        roleSelect.prepend(basicOption);
                        data.roles.forEach(role => {
                            if (role.name !== selectedName) {
                                var option = document.createElement('option');
                                option.value = role.id;
                                option.textContent = role.name;
                                roleSelect.appendChild(option);
                            }
                        });
                    })
                    .catch(error => console.error('Error fetching roles:', error));
            }



        departmentSelector.addEventListener('change', function (e) {
            const departmentId = e.target.value;
            if (departmentId) {
                var url = '/get-roles-for-department/';
                fetch(url, {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest',
                    },
                    body: JSON.stringify({ 'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest' ,
                    'department_id': departmentId})
                })
                    
                    .then(response => response.json())
                    .then(data => {
                        var roleSelect = document.getElementById('id_role');
                        var roles = roleSelect.querySelectorAll('option');
                        for (let child of roles) {
                            child.remove();
                        }
                        let basicOption = document.createElement('option');
                        basicOption.value = '';
                        basicOption.textContent = '---------';
                        roleSelect.appendChild(basicOption);
                        data.roles.forEach(role => {
                            var option = document.createElement('option');
                            option.value = role.id;
                            option.textContent = role.name;
                            roleSelect.appendChild(option);
                        });
                    })
                    .catch(error => console.error('Error fetching roles:', error));
            }
        });
});
}