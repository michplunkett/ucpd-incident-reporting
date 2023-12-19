let typeCounts;
const yearlySummation = d3.select("#visual-container").append("svg");

async function getIncidents() {
  const response = await fetch("/incidents/yearly");
  return response.json();
}

getIncidents().then((r) => {
  typeCounts = r["counts"];

  console.log(typeCounts);
});
