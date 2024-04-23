let incidents = [];
let infoWindow = undefined;
let map = undefined;
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
let markers = [];

async function getMapIncidents() {
  const response = await fetch("/incidents/map");
  return response.json();
}

function createMap() {
  map = new google.maps.Map(document.getElementById("map-container"), {
    zoom: 14,
    center: new google.maps.LatLng(41.794295, -87.590701),
    mapTypeId: "terrain",
    styles: mapStyles,
  });

  // Get incidents once the map is loaded
  getMapIncidents().then((r) => {
    incidents = r["incidents"];

    incidents.forEach((incident) => {
      let content = `
            <div id="content">
              <h3 class="incident-title">${incident.incident}</h3>
              <p class="incident-information"><b>Predicted Address:</b> ${incident.validated_address}</p>
              <p class="incident-information"><b>Listed Address:</b> ${incident.location}</p>
              <p class="incident-information"><b>Reported Time:</b> ${incident.occurred}</p>
              <p class="incident-information"><b>UCPD ID:</b> ${incident.ucpd_id}</p>
            </div>
        `;

      let marker = new google.maps.Marker({
        title: `${incident.incident} @ ${incident.occurred}`,
        position: new google.maps.LatLng(
          incident.validated_location[0],
          incident.validated_location[1],
        ),
        map: map,
      });

      // Add an info when a marker is clicked
      marker.addListener("click", () => {
        // If an info window is already open, close it
        if (infoWindow) {
          infoWindow.close();
        }

        infoWindow = new google.maps.InfoWindow({
          content: content,
          ariaLabel: "Uluru",
        });

        infoWindow.open({
          anchor: marker,
          map,
        });
      });

      markers.push(marker);
    });
  });

  document
    .getElementById("incident-type")
    .addEventListener("change", (event) => {
      // Close the open info window when changing incident types
      if (infoWindow) {
        infoWindow.close();
        infoWindow = undefined;
      }

      const selectValue = event.target.value;
      markers.forEach((marker) => {
        if (
          selectValue === "" ||
          (selectValue !== "" && marker.title.includes(selectValue))
        ) {
          marker.setMap(map);
        } else {
          marker.setMap(null);
        }
      });
    });
}

window.initMap = createMap;
