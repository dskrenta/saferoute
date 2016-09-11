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
                  <h4 class="card-title">{title} <small class="label">{time}</small></h4>
                  <h6 class="card-meta">{distance}</h6>
              </div>
              <div class="card-body">
                  To make a contribution to the world by making tools for the mind that advance humankind.
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
  </style>

  <script>
    this.map;
    this.results = [
      {
        title: 'via Middlefield Rd',
        distance: '47 miles',
        time: '1 h 20 min',
        snippet: ''
      },
      {
        title: 'via El Camino Real',
        distance: '29 miles',
        time: '4 h 37 min'
      },
      {
        title: 'via E Bayshore Rd',
        distance: '98 miles',
        time: '2 h 40 min'
      }
    ];
    const self = this;

    window.initMap = () => {
      self.map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -34.397, lng: 150.644},
        zoom: 8
      });
    };

    handler (event) {
      const origin = event.target[0].value;
      const destination = event.target[1].value;
    }

    this.on('mount', () => {
      /*
      let script = document.createElement('script');
      script.setAttribute('id', 'gmap_script');
		  script.type = 'text/javascript';
			script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyCnOa8LV_tSyvras9MrV33mGqtvil2c4H8&callback=window.initMap';
			document.body.appendChild(script);
      */
    });
  </script>
</saferoute>
