let map = undefined;
let incidents = [];
const mapStyles = [
  {
    featureType: "poi.attraction",
    stylers: [
      {
        visibility: "off",
      },
    ],
  },
  {
    featureType: "poi.business",
    stylers: [
      {
        visibility: "off",
      },
    ],
  },
  {
    featureType: "poi.government",
    stylers: [
      {
        visibility: "simplified",
      },
    ],
  },
  {
    featureType: "poi.medical",
    stylers: [
      {
        visibility: "simplified",
      },
    ],
  },
  {
    featureType: "poi.park",
    stylers: [
      {
        visibility: "simplified",
      },
    ],
  },
  {
    featureType: "poi.place_of_worship",
    stylers: [
      {
        visibility: "off",
      },
    ],
  },
  {
    featureType: "poi.school",
    stylers: [
      {
        visibility: "simplified",
      },
    ],
  },
  {
    featureType: "poi.sports_complex",
    stylers: [
      {
        visibility: "off",
      },
    ],
  },
];

async function getMapIncidents() {
  const response = await fetch("/incidents/map");
  return response.json();
}

function createMap() {
  map = new google.maps.Map(document.getElementById("incident-map"), {
    zoom: 14,
    center: new google.maps.LatLng(41.794295, -87.590701),
    mapTypeId: "terrain",
    styles: mapStyles,
  });
}

window.initMap = createMap;

getMapIncidents().then((r) => {
  console.log(r);
  incidents = r["incidents"];

  for (let i = 0; i < incidents.length; i++) {
    let incident = incidents[i];

    let content = `
            <div id="content">
              <h3 class="incident-title">${incident.incident}</h3>
              <p class="incident-information">${incident.validated_address}</p>
              <p class="incident-information">${incident.occurred}</p>
              <p class="incident-information"><b>UCPD ID:</b> ${incident.ucpd_id}
            </div>
        `;

    const infoWindow = new google.maps.InfoWindow({
      content: content,
      ariaLabel: "Uluru",
    });

    let marker = new google.maps.Marker({
      title: `${incident.incident} @ ${incident.occurred}`,
      position: new google.maps.LatLng(
        incident.validated_location[0],
        incident.validated_location[1],
      ),
      map: map,
    });

    marker.addListener("click", () => {
      infoWindow.open({
        anchor: marker,
        map,
      });
    });
  }
});
