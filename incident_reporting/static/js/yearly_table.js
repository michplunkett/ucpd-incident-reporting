async function getIncidents() {
  const response = await fetch("/incidents/yearly");
  return response.json();
}

function createTable() {
  getIncidents().then((r) => {
    const incidents = r["incidents"];
    const types = r["types"];
    console.log(incidents);
    console.log(types);
    const table = new DataTable("#visual-container", {
      columns: [
        { title: "UCPD ID" },
        { title: "Category" },
        { title: "Reported Time" },
        { title: "Address" },
        { title: "Description" },
      ],
      fixedHeader: true,
      paging: true,
      responsive: true,
    });

    table.draw();
  });
}
