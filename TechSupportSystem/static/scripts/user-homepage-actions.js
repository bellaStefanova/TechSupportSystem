document.addEventListener("DOMContentLoaded", function () {
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
    const tableRows = document.querySelectorAll('.table-row');
    optionsContainer.addEventListener("click", function (event) {
        if (event.target.classList.contains("option")) {
            selectedOptionValue.textContent = event.target.textContent;
            optionsContainer.style.display = "none";
            tbody.innerHTML = tbodyOriginal_content;
            // Filter the table per status
            tableRows = document.querySelectorAll('.table-row');
            tableRows.forEach(row => {
                const statusCell = row.querySelector('.table-data-status');
                
                if (statusCell.textContent === selectedOptionValue.textContent || selectedOptionValue.textContent === 'All') {
                    row.style.display = 'flex';
                } else {
                    row.remove()
                }
            });
            
        }
    });

    // Close options when clicking outside the dropdown
    document.addEventListener("click", function (event) {
        if (!dropdown.contains(event.target)) {
            optionsContainer.style.display = "none";
        }
    });

    // Handle search input placeholder to disappear on click inside and appear on click outside when empty
    const input = document.getElementById('perDetailsInput');

    input.addEventListener('blur', () => {
        if (!input.value) {
            input.placeholder = 'Search by Request ID or subject';
        }
    });

    input.addEventListener('focus', () => {
        input.placeholder = '';
    });

    // Handle per period selector buttons to change color on click - the are mutually exclusive
    const perPeriodSelectors = document.querySelectorAll('.perPeriodSelector');
    perPeriodSelectors.forEach(selector => {
        selector.addEventListener('click', function() {
            const isColored = this.style.backgroundColor == 'rgb(29, 59, 101)'
            // Reset color for all elements
            perPeriodSelectors.forEach(element => {
                element.style.backgroundColor = '#dbdbdb';
                element.style.color = '#7b7b7b'
            });
    
            // Set a different color for the clicked element
            this.style.backgroundColor = isColored ? '#dbdbdb' : '#1D3B65';
            this.style.color = isColored? '#7b7b7b' : 'white' 
    
        });
    });

    // Handle table row click to redirect to the specific request details page

    tableRows.forEach(row => {
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

