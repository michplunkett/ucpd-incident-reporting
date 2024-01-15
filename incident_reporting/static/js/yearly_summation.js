let counts, types;

async function getIncidents() {
  const response = await fetch("/incidents/yearly");
  return response.json();
}

getIncidents().then((r) => {
  types = r["types"];
  counts = r["counts"];

  Highcharts.chart("visual-container", {
    colors: ["#800000"],
    chart: {
      type: "column",
    },
    title: {
      text: "Frequency of UCPD Incident Types Over the Last Year",
      align: "center",
    },
    subtitle: {
      text: "This Graphic Pulls From the Last 365 Days",
      align: "center",
    },
    xAxis: {
      categories: types,
      crosshair: true,
      accessibility: {
        description: "Countries",
      },
    },
    yAxis: {
      min: 0,
      title: {
        text: "Category Frequency",
      },
    },
    plotOptions: {
      column: {
        pointPadding: 0.2,
        borderWidth: 0,
      },
    },
    legend: {
      enabled: false,
    },
    series: [
      {
        name: "Incidents",
        data: counts,
      },
    ],
  });
});
