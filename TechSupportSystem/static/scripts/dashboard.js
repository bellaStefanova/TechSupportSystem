import { filterTableRows } from './user-homepage-actions.js';
import { replaceTableRows } from './user-homepage-actions.js';
let optionStatus=''
if (window.location.pathname === '/dashboard/') {
    document.addEventListener("DOMContentLoaded", function () {
        function redirectToRequests(optionStatus) {
            sessionStorage.setItem('optionStatus', optionStatus);
            const url = `/requests/`;
            window.location.href = url;
        }
        const allTicketsElement = document.getElementById('allTickets');
        const waitingTicketsElement = document.getElementById('waitingTickets');
        const assignedTicketsElement = document.getElementById('assignedTickets');
        const resolvedTicketsElement = document.getElementById('resolvedTickets');
        allTicketsElement.addEventListener('click', function() {
            optionStatus = 'All';
            redirectToRequests(optionStatus);
        });
        waitingTicketsElement.addEventListener('click', function() {
            optionStatus = 'Waiting';
            redirectToRequests(optionStatus);
        });
        assignedTicketsElement.addEventListener('click', function() {
            optionStatus = 'Assigned';
            redirectToRequests(optionStatus);
        });
        resolvedTicketsElement.addEventListener('click', function() {
            optionStatus = 'Resolved';
            redirectToRequests(optionStatus);
        });
    });

}

if (window.location.pathname === '/requests/') {
    document.addEventListener("DOMContentLoaded", function () {
        optionStatus = sessionStorage.getItem('optionStatus');
        const selectedOptionValue = document.querySelector(".initial-option");
        selectedOptionValue.textContent = optionStatus;
        console.log(optionStatus);
        const input = document.getElementById('perDetailsInput');
        let originalTableRows;
        if (!originalTableRows) {
            originalTableRows = Array.from(document.querySelectorAll('.table-row'));
        };
        let tableRows = filterTableRows(input, selectedOptionValue, originalTableRows);
        replaceTableRows(tableRows)
        // };
    });
};