const sValues = ["Waiting", "Assigned", "Resolved"];
const sData = [15, 35, 50];
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


const pValues = ["Critical", "High", "Medium", "Low"];
const pData = [5, 10, 35, 50];
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
        display: true,
      },
    },
    maintainAspectRatio: true,
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

const dValues = ["Product1", "Product2", "Product3", "Product4"];
const dData = [[5, null, null, null], [null, 10, null, null], [null, null, 35, null], [null, null, null, 50]];
const dColors = [
  "#323232",
  "#777777",
  "#A2A2A2",
  "#E6E6E6",
];

let dtx = document.getElementById('departmentDiagram').getContext('2d'); // node

let departmentDiagram = new Chart(dtx, {
  type: "bar",
  data: {
    labels: dValues,
    datasets: [{
      backgroundColor: dColors[0],
      label: dValues[0],
      data: dData[0],
    }, {
      backgroundColor: dColors[1],
      label: dValues[1],
      data: dData[1],
    }, {
      backgroundColor: dColors[2],
      label: dValues[2],
      data: dData[2],
    }, {
      backgroundColor: dColors[3],
      label: dValues[3],
      data: dData[3],
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