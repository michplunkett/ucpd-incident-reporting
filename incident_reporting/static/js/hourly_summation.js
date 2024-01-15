const hours = [];
let selectedSeason = [];
for (let hour = 0; hour < 24; hour++) hours.push(hour);

let fallSummary = {};
let springSummary = {};
let summerSummary = {};
let totalSummary = {};
let winterSummary = {};

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
    Highcharts.chart("visual-container", {
      data: {
        table: "freq",
        startRow: 1,
        endRow: 17,
        endColumn: 7,
      },

      chart: {
        polar: true,
        type: "column",
      },

      title: {
        text: "UCPD Incident Type Sums per Hour of the Day",
        align: "center",
      },

      subtitle: {
        text: "Based on Data From 2011 to the Most Recent Completed Year",
        align: "center",
      },

      pane: {
          size: '90%'
      },

    });
  }

  createVisual();
});
