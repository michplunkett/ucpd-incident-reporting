const dimension = 928;
const innerRadius = 180;
const outerRadius = Math.min(dimension, dimension) / 2;
const hourlySummation = d3.select("#visual-container").append("svg");

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

  console.log(fallSummary);
  console.log(springSummary);
  console.log(summerSummary);
  console.log(winterSummary);
});
