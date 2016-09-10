<example>
  <h2>This is { sample }</h2>
  <h3>{ hello }</h3>
  <p>Hello, I am Kamala Harris</p>

  <table class="table table-striped table-hover">
      <thead>
          <tr>
              <th>name</th>
              <th>age</th>
          </tr>
      </thead>
      <tbody>
        <tr each={ items }>
          <td>{ name }</td>
          <td>{ age }</td>
        </tr>
      </tbody>
  </table>

  <script>
    this.items = [
      {name: "David", age: 17},
      {name: "Bob", age: 18},
      {name: "Steve", age: 14}
    ];

    this.sample = 'example';
    let test = "David Skrenta";
    this.hello = `${test} is very excited to meet with you!`;
  </script>
</example>
