let counts, types;

async function getIncidents() {
  const response = await fetch("/incidents/yearly");
  return response.json();
}

getIncidents().then((r) => {
  types = r["types"];
  counts = r["counts"];

  Highcharts.chart("container", {
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
        text: "1000 metric tons (MT)",
      },
    },
    tooltip: {
      valueSuffix: " (1000 MT)",
    },
    plotOptions: {
      column: {
        pointPadding: 0.2,
        borderWidth: 0,
      },
    },
    series: [
      {
        name: "Corn",
        data: [406292, 260000, 107000, 68300, 27500, 14500],
      },
      {
        name: "Wheat",
        data: [51086, 136000, 5500, 141000, 107180, 77000],
      },
    ],
  });
});
