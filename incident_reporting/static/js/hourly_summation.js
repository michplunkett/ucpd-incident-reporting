const hourlySummation = d3.select("#visual-container").append("svg");
let fallSummary = {};
let springSummary = {};
let summerSummary = {};
let winterSummary = {};

async function getIncidents() {
  const response = await fetch("/incidents/hourly");
  return response.json();
}

getIncidents().then((r) => {
  fallSummary = r["fall"];
  springSummary = r["spring"];
  summerSummary = r["summer"];
  winterSummary = r["winter"];

  console.log(fallSummary);
  console.log(springSummary);
  console.log(summerSummary);
  console.log(winterSummary);
});
