<saferoute>
  <div class="container">
    <div class="columns col-gapless">
        <div class="column col-4 input-col">
          <div class="input-wrapper">
            <form class="input-form" onsubmit={handler}>
              <div class="form-group">
                <input type="text" class="form-input" placeholder="Origin"></input>
                <input type="text" class="form-input" placeholder="Destination"></input>
                <button type="submit" class="btn btn-primary input-group-btn btn-block">Go</button>
              </div>
            </form>
          </div>

          <virtual each={results}>
            <div class="card">
              <div class="card-header">
                  <h4 class="card-title">{title} <small class="label">Safety: {saftey}/10</small></h4>
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
    this.results = [
      {
        title: 'via Middlefield Rd',
        distance: '47 miles',
        time: '1 h 20 min',
        saftey: 7,
        openNow: 21,
        crimes: 1
      },
      {
        title: 'via El Camino Real',
        distance: '29 miles',
        time: '4 h 37 min',
        saftey: 5,
        openNow: 9,
        crimes: 20
      },
      {
        title: 'via E Bayshore Rd',
        distance: '98 miles',
        time: '2 h 40 min',
        saftey: 2,
        openNow: 5,
        crimes: 43
      }
    ];
    const self = this;

    window.initMap = () => {
      self.map = new google.maps.Map(document.getElementById('map'), {
        zoom: 3,
        center: {lat: 0, lng: -180},
      });

      const flightPlanCoordinates = [
          {lat: 37.772, lng: -122.214},
          {lat: 21.291, lng: -157.821},
          {lat: -18.142, lng: 178.431},
          {lat: -27.467, lng: 153.027}
        ];

      const flightPath = new google.maps.Polyline({
        path: flightPlanCoordinates,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
      });

      flightPath.setMap(self.map);
    };

    function request (method, url) {
      return new Promise((resolve, reject) => {
        const XHR = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.onload = () => {
          if (this.status >= 200 && this.status < 300) {
            resolve(xhr.response);
          } else {
            reject({
              status: this.status,
              statusText: xhr.statusText
            });
          }
        };
        xhr.onerror = () => {
          reject({
            status: this.status,
            statusText: xhr.statusText
          });
          xhr.send();
        };
      });
    }

    handler (event) {
      const origin = event.target[0].value;
      const destination = event.target[1].value;
    }

    this.on('mount', () => {
      let script = document.createElement('script');
      script.setAttribute('id', 'gmap_script');
		  script.type = 'text/javascript';
			script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyCnOa8LV_tSyvras9MrV33mGqtvil2c4H8&callback=window.initMap';
			document.body.appendChild(script);
    });
  </script>
</saferoute>
