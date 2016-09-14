<saferoute>
  <div class="container">
    <div class="columns col-gapless">
        <div class="column col-4 input-col">
          <div class="input-wrapper">
            <form class="input-form" onsubmit={handler}>
              <div class="form-group">
                <input type="text" class="form-input" value="79 Hudson River Greenway, New York, NY 10024" placeholder="Origin"></input>
                <input type="text" class="form-input" value="564-566 Hudson Street, New York, NY 10014" placeholder="Destination"></input>
                <button type="submit" class="btn btn-primary input-group-btn btn-block">Go</button>
              </div>
            </form>
          </div>

          <virtual each={results}>
            <div class="card">
              <div class="card-header">
                  <h4 class="card-title">{title} <small class="label">Safety: {safety}/10</small></h4>
                  <h6 class="card-meta">{time} &middot; {distance} &middot; {crimes} recent crimes &middot; {openNow} open places</h6>
              </div>
            </div>
          </virtual>
        </div>
        <div class="column col-8">
          <div id="map"></div>
        </div>
    </div>
  </div>

  <style>
    #map {
      height: 100%;
    }
    .input-col {
      background-color: #f8f8f8;
    }
    .input-wrapper {
      background-color: #4285F4;
      padding: 10px;
    }
    .container,.columns,.column {
      height: 100%;
      padding: 0px;
      margin: 0px;
    }
    .form-input {
      margin-bottom: 1em;
    }
    .label {
      float: right;
    }
  </style>

  <script>
    this.map;
    this.pinpoints;
    this.results = [
      {
        title: 'via Middlefield Rd',
        distance: '47 miles',
        time: '1 h 20 min',
        saftey: 7,
        openNow: 21,
        crimes: 1,
        waypoints: [
          {lat: 37.772, lng: -122.214},
          {lat: 21.291, lng: -157.821},
          {lat: -18.142, lng: 178.431},
          {lat: -27.467, lng: 153.027}
        ]
      },
      {
        title: 'via El Camino Real',
        distance: '29 miles',
        time: '4 h 37 min',
        saftey: 5,
        openNow: 9,
        crimes: 20,
        waypoints: [
          {lat: 37.772, lng: -122.214},
          {lat: 21.291, lng: -157.821},
          {lat: -18.142, lng: 178.431},
          {lat: -27.467, lng: 153.027}
        ]
      },
      {
        title: 'via E Bayshore Rd',
        distance: '98 miles',
        time: '2 h 40 min',
        saftey: 2,
        openNow: 5,
        crimes: 43,
        waypoints: [
          {lat: 37.772, lng: -122.214},
          {lat: 21.291, lng: -157.821},
          {lat: -18.142, lng: 178.431},
          {lat: -27.467, lng: 153.027}
        ]
      }
    ];
    const self = this;

    window.initMap = (zoom = 3, center = {lat: 0, lng: -180}) => {
      const bounds = new google.maps.LatLngBounds();

      self.map = new google.maps.Map(document.getElementById('map'), {
        zoom: 3,
        center: {lat: 0, lng: -180},
      });

      const colors = ['#ff0000', '#0000ff', '#800080'];

      for (let i = 0; i < self.results.length; i++) {
        let waypoints = self.results[i].waypoints;
        let numPoints = [];
        for (let i = 0; i < waypoints.length; i++) {
          const lat = Number(waypoints[i].lat);
          const lng = Number(waypoints[i].lng);
          const latLngObj = {lat: lat, lng: lng};
          numPoints.push(latLngObj);
          bounds.extend(latLngObj);
        }
        const path = new google.maps.Polyline({
          path: numPoints,
          geodesic: true,
          strokeColor: colors[i],
          strokeOpacity: 1.0,
          strokeWeight: 2
        });
        path.setMap(self.map);
        self.map.fitBounds(bounds);
      }

      for (let i = 0; i < self.pinpoints.length; i++) {
        const latLngObj = {lat: self.pinpoints[i].lat, lng: self.pinpoints[i].lng};
        const image = self.pinpoints[i].tag ? formatImage(self.pinpoints[i].tag) : '';

        const marker = new google.maps.Marker({
          position: latLngObj,
          map: self.map,
          icon: image
        });
      }
    };

    function formatImage (name) {
      return `${window.location}/images/${name}2.png`;
    }

    function request (url, callback)  {
      const xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
          callback(xhr.responseText);
        }
      }
      xhr.open("GET", url, true);
      xhr.send(null);
    }

    handler (event) {
      const origin = event.target[0].value;
      const destination = event.target[1].value;
      if (origin && destination) apiRequest(origin, destination);
    }

    function apiRequest (origin, destination) {
      const requestURL = `http:\/\/www.skrenta.com/safety/routes.cgi?origin=${encodeURIComponent(origin)}&destination=${encodeURIComponent(destination)}`;
        request(requestURL, (response) => {
          let result = JSON.parse(response);
          self.pinpoints = result.pinpoints;
          self.results = result.routes;
          window.initMap();
          self.update();
        });
    }

    this.on('mount', () => {
      let script = document.createElement('script');
      script.setAttribute('id', 'gmap_script');
		  script.type = 'text/javascript';
			script.src = 'https:\/\/maps.googleapis.com/maps/api/js?key=AIzaSyCnOa8LV_tSyvras9MrV33mGqtvil2c4H8&callback=window.initMap';
			document.body.appendChild(script);
    });
  </script>
</saferoute>
