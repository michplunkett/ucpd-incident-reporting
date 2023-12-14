function titleCase(str) {
  return str.replace(/\w\S*/g, function (txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  });
}

const incidents = [];

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

function createMap() {
  let map = new google.maps.Map(document.getElementById("graph-container"), {
    zoom: 14,
    center: new google.maps.LatLng(41.794295, -87.590701),
    mapTypeId: "terrain",
    styles: mapStyles,
  });

  for (let i = 0; i < incidents.length; i++) {
    let incident = incidents[i];
    incident.titleAddress = titleCase(incident.address);

    let content = `
            <div id="content">
                <h3 style="margin-top:2px; margin-bottom: 8px;">${incident.incident}</h3>
                <p class="incident-information">${incident.titleAddress}</p>
                <p class="incident-information">${incident.occurred}</p>
                <p class="incident-information"><b>Number of Victims:</b> ${incident.numberOfVictims}</p>
                 <p class="incident-information"><b>UCPD ID:</b> ${incident.ucpdID}
                 </div>
        `;

    const infoWindow = new google.maps.InfoWindow({
      content: content,
      ariaLabel: "Uluru",
    });

    let marker = new google.maps.Marker({
      title: `${incident.incident} @ ${incident.occurred}`,
      position: new google.maps.LatLng(incident.coords[0], incident.coords[1]),
      map: map,
    });

    marker.addListener("click", () => {
      infoWindow.open({
        anchor: marker,
        map,
      });
    });
  }
}

window.initMap = createMap;
