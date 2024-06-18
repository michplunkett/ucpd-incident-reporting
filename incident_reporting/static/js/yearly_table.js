async function getIncidents() {
  const response = await fetch("/incidents/yearly");
  return response.json();
}

function createTable() {
  getIncidents().then((r) => {
    const incidents = r["incidents"];
    const types = r["types"];
  });
}
