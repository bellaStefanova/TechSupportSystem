if (window.location.pathname === '/dashboard/') {
  document.addEventListener("DOMContentLoaded", function () {
    // Doughnut chart with requests count per status
      const waitingRequestsCount = document.getElementById('waitingRequestsCount').innerText;
      const assignedRequestsCount = document.getElementById('assignedRequestsCount').innerText;
      const resolvedRequestsCount = document.getElementById('resolvedRequestsCount').innerText;

      const sValues = ["Waiting", "Assigned", "Resolved"];
      const sData = [waitingRequestsCount, assignedRequestsCount, resolvedRequestsCount];
      const sColors = [
        "#be3a3a",
        "#bd9037",
        "#279127",
      ];

      let stx = document.getElementById('statusDiagram').getContext('2d'); // node

      let statusDiagram = new Chart(stx, {
        type: "doughnut",
        data: {
          labels: sValues,
          datasets: [{
            backgroundColor: sColors,
            data: sData,
          }]
        },
        options: {
          plugins: {
            legend: {
              display: false,
            },
          },
          cutout: '70%',
          maintainAspectRatio: true,
          aspectRatio: 1,
          responsive: true,
        }
      });

      // Pie chart with requests count per priority
      let lowUrgency = document.getElementById('lowUrgencyRequestsCount').attributes.number.value;
      let mediumUrgency = document.getElementById('mediumUrgencyRequestsCount').attributes.number.value;
      let highUrgency = document.getElementById('highUrgencyRequestsCount').attributes.number.value;
      let criticalUrgency = document.getElementById('criticalUrgencyRequestsCount').attributes.number.value;
      

      const pValues = ["Critical", "High", "Medium", "Low"];
      const pData = [criticalUrgency, highUrgency, mediumUrgency, lowUrgency];
      const pColors = [
        "#323232",
        "#777777",
        "#A2A2A2",
        "#E6E6E6",
      ];

      let ptx = document.getElementById('priorityDiagram').getContext('2d'); // node

      let priorityDiagram = new Chart(ptx, {
        type: "pie",
        data: {
          labels: pValues,
          datasets: [{
            backgroundColor: pColors,
            data: pData,
          }]
        },
        options: {
          plugins: {
            legend: {
              display: false,
            },
          },
          maintainAspectRatio: true,
          aspectRatio: 1,
          responsive: true,
        }
      });

      const prValues = ["Product1", "Product2", "Product3", "Product4"];
      const prData = [[5, null, null, null], [null, 10, null, null], [null, null, 35, null], [null, null, null, 50]];
      const prColors = [
        "#323232",
        "#777777",
        "#A2A2A2",
        "#E6E6E6",
      ];

      let prtx = document.getElementById('productDiagram').getContext('2d'); // node

      let productDiagram = new Chart(prtx, {
        type: "bar",
        data: {
          labels: prValues,
          datasets: [{
            backgroundColor: prColors[0],
            label: prValues[0],
            data: prData[0],
          }, {
            backgroundColor: prColors[1],
            label: prValues[1],
            data: prData[1],
          }, {
            backgroundColor: prColors[2],
            label: prValues[2],
            data: prData[2],
          }, {
            backgroundColor: prColors[3],
            label: prValues[3],
            data: prData[3],
          }]
        },
        options: {
          indexAxis: 'x',
          skipNull: true,
          maintainAspectRatio: true,
          responsive: true,
          plugins: {
            legend: {
              display: false,
              position: 'top', // Adjust legend position as needed
            },
          },
          scales: {
            x: {
              grid: {
                display: false,
              }
            },
            y: {
              grid: {
                display: false,
              }
            }
          }
        }
      });
      
      // Bar chart with requests count per department
      const topDepartmentElements = document.querySelectorAll('#topDepartment');
      const topDeparmentNames = Array.from(topDepartmentElements).map(element => element.attributes.name.value);
      const topDeparmentValues = Array.from(topDepartmentElements).map(element => element.attributes.number.value);

      const dColors = ["#323232", "#777777", "#A2A2A2", "#E6E6E6",];

      let dataset = [];
      for (let i = 0; i < topDeparmentValues.length; i++) {
        let data = Array.from({ length: topDeparmentValues.length }, () => null);
        data[i] = topDeparmentValues[i];
        dataset.push(
          {
            backgroundColor: dColors[i],
            label: topDeparmentNames[i],
            data: data,
          }
        );
      }

      let dtx = document.getElementById('departmentDiagram').getContext('2d'); // node

      let departmentDiagram = new Chart(dtx, {
        type: "bar",
        data: {
          labels: topDeparmentNames,
          datasets: dataset
        },
        options: {
          indexAxis: 'x',
          skipNull: true,
          maintainAspectRatio: true,
          responsive: true,
          plugins: {
            legend: {
              display: false,
              position: 'top', // Adjust legend position as needed
            },
          },
          scales: {
            x: {
              grid: {
                display: false,
              }
            },
            y: {
              grid: {
                display: false,
              }
            }
          }
        }
      });
    });
  }