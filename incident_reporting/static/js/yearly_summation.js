let typeCounts;

async function getIncidents() {
  const response = await fetch("/incidents/yearly");
  return response.json();
}

getIncidents().then((r) => {
  typeCounts = r["counts"];
});
