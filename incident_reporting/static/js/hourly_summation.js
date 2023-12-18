const hourlySummation = d3.select("#graph-container").append("svg");
let seasonSummaries = {};

async function getIncidents() {
  const response = await fetch("/incidents/hourly");
  return response.json();
}

getIncidents().then((r) => {
  seasonSummaries = r["season_summaries"];
  console.log(seasonSummaries);
});
