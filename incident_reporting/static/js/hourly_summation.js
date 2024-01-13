const hours = [];
let selectedSeason = [];
for (let hour = 0; hour < 10; hour++) hours.push(hour);

let fallSummary = [];
let springSummary = [];
let summerSummary = [];
let totalSummary = [];
let winterSummary = [];

async function getIncidents() {
  const response = await fetch("/incidents/hourly");
  return response.json();
}

getIncidents().then((r) => {
  fallSummary = r["fall"];
  springSummary = r["spring"];
  summerSummary = r["summer"];
  totalSummary = r["total"];
  winterSummary = r["winter"];

  function createVisual() {
    new Chart(document.getElementById("canvas-visual"), {
      type: "bar",
      data: {
        labels: hours,
        datasets: [
          {
            data: [86, 114, 106, 106, 107, 111, 133, 221, 783, 2478],
            label: "Africa",
            borderColor: "#3e95cd",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            align: "center",
            display: true,
            font: {
              size: 26,
            },
            position: "top",
            text: "Incident Types per Hour of the Day",
          },
        },
      },
    });
  }

  createVisual();
});
