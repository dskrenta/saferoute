<saferoute>
  <form onsubmit={handler}>
    <input type="text" name="origin" placeholder="Origin"></input>
    <input type="text" name="destination" placeholder="Destination"></input>
    <button type="submit">Submit</button>
  </form>

  <div id="map"></div>

  <style>
  #map {
    height: 100%;
  }
  .navbar {
    
  }
  </style>

  <script>
    this.map;
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
      let script = document.createElement('script');
      script.setAttribute('id', 'gmap_script');
		  script.type = 'text/javascript';
			script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyCnOa8LV_tSyvras9MrV33mGqtvil2c4H8&callback=window.initMap';
			document.body.appendChild(script);
    });
  </script>
</saferoute>
