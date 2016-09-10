<main>
  <div class="container">
    <h1>{ title }</h1>
    <h3>By { name }</h3>

    <button onclick={ changeColor }>Change color</button>

    <div style="background:blue;height:50px;width:50px;" if={ color }></div>
    <div style="background:red;height:50px;width:50px;" if={ !color }></div>
  </div>

  <script>
  this.title = 'Color Change';
  this.name = 'Bryce';
  this.color = true;

  changeColor() {
    if(this.color) {
      this.color = !this.color;
    } else {
      this.color = true;
    }
    this.update();
  }
  </script>
</main>
