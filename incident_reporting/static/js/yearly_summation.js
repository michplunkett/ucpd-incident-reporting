async function getIncidents() {
  const response = await fetch("/incidents/yearly");
  return response.json();
}

function createVisual() {
  getIncidents().then((r) => {
    const counts = r["counts"];
    const types = r["types"];

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
        text: "Incident types with at least 20 occurrences",
        align: "center",
      },
      xAxis: {
        categories: types,
        crosshair: true,
        accessibility: {
          description: "Incident Types",
        },
      },
      yAxis: {
        min: 0,
        title: {
          text: "Frequency",
        },
      },
      plotOptions: {
        column: {
          pointPadding: 0.2,
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
}
