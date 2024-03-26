if (window.location.pathname === '/home') {

    document.addEventListener("DOMContentLoaded", function () {
        // Get all table rows from the requests table initially
        let originalTableRows;
        if (!originalTableRows) {
            originalTableRows = Array.from(document.querySelectorAll('.table-row'));
        };

        const input = document.getElementById('perDetailsInput');


        // colorize status cells in requests table
        const statusCells = document.querySelectorAll('.table-data-status');
        statusCells.forEach(cell => {
            if (cell.textContent === 'Waiting') {
                cell.style.backgroundColor = '#BE3A3A';
            } else if (cell.textContent === 'Assigned') {
                cell.style.backgroundColor = '#BD9037';
            } else if (cell.textContent === 'Resolved') {
                cell.style.backgroundColor = '#279127';
            }
        });

        // Handle status dropdown filter
        const dropdown = document.querySelector(".per-status");
        const selectedOption = document.querySelector(".initial-option-container");
        const selectedOptionValue = document.querySelector(".initial-option");
        const optionsContainer = document.querySelector(".filter-per-status-options");
        var tbody = document.getElementById('tableBody');
        var tbodyOriginal_content;

        // Initial setup to store original tbody content so it can be dinamically reloaded on status filter selection
        if (!tbodyOriginal_content) {
            tbodyOriginal_content = tbody.innerHTML;
        }

        // Toggle options visibility on click status dropdown
        selectedOption.addEventListener("click", function () {
            optionsContainer.style.display =
                optionsContainer.style.display === "none" ? "block" : "none";
        });

        // Handle option selection
        optionsContainer.addEventListener("click", function (event) {
            if (event.target.classList.contains("option")) {
                selectedOptionValue.textContent = event.target.textContent;
                optionsContainer.style.display = "none";

                // Filter the table per status and search input
                filterTableRows();
                // Replace the table rows with the filtered ones
                replaceTableRows()

            }
        });


        // Close options when clicking outside the dropdown
        document.addEventListener("click", function (event) {
            if (!dropdown.contains(event.target)) {
                optionsContainer.style.display = "none";
            }
        });

        // Handle search input placeholder to disappear on click inside and appear on click outside when empty
        input.addEventListener('blur', () => {
            if (!input.value) {
                input.placeholder = 'Search by Request ID or subject';
            }
        });

        input.addEventListener('focus', () => {
            input.placeholder = '';
        });

        // Handle search input to filter the table rows
        input.addEventListener('input', () => {
            // Filter the table per status and search input
            filterTableRows();
            // Replace the table rows with the filtered ones
            replaceTableRows()
        });

        // Function to filter the table rows
        function filterTableRows() {

            const searchValue = input.value.toLowerCase();
            if (selectedOptionValue.textContent === 'All' || selectedOptionValue.textContent === 'Status') {
                if (input.value === '') {
                    tableRows = originalTableRows;
                } else {
                    tableRows = originalTableRows.filter(row => {
                        const titleCell = row.querySelector('.table-data-subject');
                        const idCell = row.querySelector('.table-data-request-id');
                        return titleCell.textContent.toLowerCase().includes(searchValue) || idCell.textContent.toLowerCase().includes(searchValue);
                    });
                }
            } else {
                if (input.value === '') {
                    tableRows = originalTableRows.filter(row => {
                        const statusCell = row.querySelector('.table-data-status');
                        return statusCell.textContent === selectedOptionValue.textContent;
                    });
                } else {
                    tableRows = originalTableRows.filter(row => {
                        const statusCell = row.querySelector('.table-data-status');
                        const titleCell = row.querySelector('.table-data-subject');
                        const idCell = row.querySelector('.table-data-request-id');
                        return statusCell.textContent === selectedOptionValue.textContent && (titleCell.textContent.toLowerCase().includes(searchValue) || idCell.textContent.toLowerCase().includes(searchValue));
                    });
                }
            }
        }

        // Function to replace the table rows
        function replaceTableRows() {

            const table = document.querySelector('#tableBody');

            // Remove all existing table rows from the table
            while (table.firstChild) {
                table.removeChild(table.firstChild);
            }

            // Append the filtered rows to the table
            tableRows.forEach(row => {
                table.appendChild(row);
            });
            if (tableRows.length === 0) {
                const noRequestsRow = document.createElement('tr');
                noRequestsRow.classList.add('table-row-no-requests');
                noRequestsRow.innerHTML = '<td class="no-requests-found" colspan="3">No requests</td>';
                table.appendChild(noRequestsRow);
            }
        };

        // Handle per period selector buttons to change color on click - the are mutually exclusive
        const perPeriodSelectors = document.querySelectorAll('.perPeriodSelector');
        perPeriodSelectors.forEach(selector => {
            selector.addEventListener('click', function () {
                const isColored = this.style.backgroundColor == 'rgb(29, 59, 101)'
                // Reset color for all elements
                perPeriodSelectors.forEach(element => {
                    element.style.backgroundColor = '#dbdbdb';
                    element.style.color = '#7b7b7b'
                });

                // Set a different color for the clicked element
                this.style.backgroundColor = isColored ? '#dbdbdb' : '#1D3B65';
                this.style.color = isColored ? '#7b7b7b' : 'white'

            });
        });

        // Handle table row click to redirect to the specific request details page
        let newTableRows = document.querySelectorAll('.table-row');
        // console.log(newTableRows);
        newTableRows.forEach(row => {
            row.addEventListener("click", function (event) {
                var target = event.target.parentNode;
                if (target.tagName === "TBODY") {
                    target = target.children[0];
                };
                if (target.tagName === "TD" && target.className === "table-data-status-cell") {
                    target = target.parentNode;
                };
                if (target.tagName === "TR") {
                    target = target.children[0];
                };

                if (target.tagName === "TD" && target.className === "table-data-request-id") {
                    var id = target.getAttribute("data-id");
                    // Redirect to the edit page with the specific ID
                    window.location.href = "/view-request/" + id;
                }
            });
        })
    });
}
