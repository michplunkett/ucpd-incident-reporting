let chart;

const loadingContainer = "#loading-visual-container";

let fallHours = [];
let fallHourBreakdown = [];
let springHours = [];
let springHourBreakdown = [];
let summerHours = [];
let summerHourBreakdown = [];
let totalHours = [];
let totalHourBreakdown = [];
let winterHours = [];
let winterHourBreakdown = [];

let selectedHours = [];
let selectedHoursBreakdown = [];

function showLoadingContainer(inputStr) {
  document.querySelector("#loading-content").innerText = inputStr;
  // Using a setTimeout to trigger a DOM redraw

  setTimeout(() => {
    document.querySelector(loadingContainer).classList.add("loading");
  }, 0);
}

function hideLoadingContainer() {
  // Using a setTimeout to trigger a DOM redraw
  document.querySelector(loadingContainer).classList.remove("loading");
  setTimeout(() => {}, 0);
}

async function getIncidents() {
  const response = await fetch("/incidents/hourly");
  return response.json();
}

Highcharts.setOptions({
  chart: {
    style: {
      fontFamily: "Georgia, serif",
    },
  },
});

function createVisual() {
  chart = Highcharts.chart("visual-container", {
    colors: ["#800000"],
    chart: {
      type: "column",
    },
    loading: {
      style: {
        backgroundColor: "#ffffff",
        opacity: 0.9,
        textAlign: "center",
      },
    },
    lang: {
      thousandsSep: ",",
    },
    title: {
      text: "Frequency of Criminal Incidents Reported to UCPD by Hour",
      align: "center",
    },
    subtitle: {
      text: "Click the hour to see a breakdown by incident type",
      align: "center",
    },
    accessibility: {
      announceNewData: {
        enabled: true,
      },
    },
    legend: {
      enabled: false,
    },
    plotOptions: {
      series: {
        borderWidth: 0,
        dataLabels: {
          enabled: false,
        },
        events: {
          click: function (e) {
            if (e.point.drilldown) {
              chart.addSeriesAsDrilldown(
                e.point,
                selectedHoursBreakdown[e.point.index],
              );
            }
          },
        },
      },
    },
    tooltip: {
      headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      pointFormat: "{point.name}: <b>{point.y:.f}</b> Incidents<br/>",
    },
    xAxis: {
      type: "category",
    },
    yAxis: {
      title: {
        text: "Frequency of Incident Type(s)",
      },
    },
    drilldown: {
      breadcrumbs: {
        position: {
          align: "right",
        },
      },
    },
  });

  showLoadingContainer("Loading all season incident data...");

  getIncidents().then((r) => {
    fallHours = r["fall_hour_counts"];
    fallHourBreakdown = r["fall_breakdown_counts"];
    springHours = r["spring_hour_counts"];
    springHourBreakdown = r["spring_breakdown_counts"];
    summerHours = r["summer_hour_counts"];
    summerHourBreakdown = r["summer_breakdown_counts"];
    totalHours = r["total_hour_counts"];
    totalHourBreakdown = r["total_breakdown_counts"];
    winterHours = r["winter_hour_counts"];
    winterHourBreakdown = r["winter_breakdown_counts"];

    selectedHours = totalHours;
    selectedHoursBreakdown = totalHourBreakdown;

    chart.addSeries({
      name: "Hour of Day",
      colorByPoint: true,
      data: selectedHours,
    });

    hideLoadingContainer();

    document
      .getElementById("season-select")
      .addEventListener("change", (event) => {
        const selectSeason = event.target.value;
        if (selectSeason === "fall") {
          selectedHours = fallHours;
          selectedHoursBreakdown = fallHourBreakdown;
        } else if (selectSeason === "spring") {
          selectedHours = springHours;
          selectedHoursBreakdown = springHourBreakdown;
        } else if (selectSeason === "summer") {
          selectedHours = summerHours;
          selectedHoursBreakdown = summerHourBreakdown;
        } else if (selectSeason === "winter") {
          selectedHours = winterHours;
          selectedHoursBreakdown = winterHourBreakdown;
        } else if (selectSeason === "all season") {
          selectedHours = totalHours;
          selectedHoursBreakdown = totalHourBreakdown;
        }

        showLoadingContainer(`Loading ${selectSeason} incident data...`);

        setTimeout(() => {
          chart.drillUp();
          // TODO: Setting the data to empty is a hack that allows me to
          //  reset the drilldown.
          chart.series[0].setData([]);
          chart.series[0].setData(selectedHours);
          hideLoadingContainer();
        }, 1500);
      });
  });
}
