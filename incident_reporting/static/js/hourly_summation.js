let chart;
const hours = [];
for (let hour = 0; hour < 24; hour++) hours.push(hour);

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

async function getIncidents() {
  const response = await fetch("/incidents/hourly");
  return response.json();
}

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

  chart = Highcharts.chart("visual-container", {
    chart: {
      type: "column",
    },
    title: {
      text: "UCPD Incident Type Sums per Hour of the Day",
      align: "center",
    },
    subtitle: {
      text: "Based on Data From 2011 to the Most Recent Completed Year",
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
      },
    },
    tooltip: {
      headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
      pointFormat:
        '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}%</b> of total<br/>',
    },
    xAxis: {
      type: "category",
      categories: hours,
    },
    yAxis: {
      title: {
        text: "Frequency of Incident Type(s)",
      },
    },
    series: [
      {
        name: "Hour of Day",
        colorByPoint: true,
        data: [],
      },
    ],
    drilldown: {
      breadcrumbs: {
        position: {
          align: "right",
        },
      },
      series: {},
    },
  });
});
