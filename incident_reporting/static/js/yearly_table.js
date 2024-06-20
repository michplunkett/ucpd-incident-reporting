async function getIncidents() {
  const response = await fetch("/incidents/yearly");
  return response.json();
}

function createTable() {
  getIncidents().then((r) => {
    const incidents = JSON.parse(r["incidents"]);
    console.log(incidents[0]);
    const table = new DataTable("#previous-year-incidents", {
      columns: [
        { title: "UCPD ID", data: "ucpd_id" },
        { title: "Category", data: "incident" },
        { title: "Reported Time", data: "reported" },
        { title: "Location", data: "location" },
        { title: "Description", data: "comments" },
      ],
      columnDefs: [
        {
          className: "dt-left",
          targets: "_all",
        },
        {
          className: "col-category",
          target: 1,
        },
        {
          className: "col-location",
          target: 3,
        },
        {
          className: "col-description",
          target: 4,
        },
      ],
      data: incidents,
      fixedHeader: true,
      order: [[2]],
      paging: true,
      responsive: true,
    });

    table.draw();
  });
}
