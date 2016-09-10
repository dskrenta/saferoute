<todo>
  <h1>Todo</h1>

  <div each={ items }>
    <h3>{ title }</h3>
    <button class="btn btn-default" onclick={ parent.remove }>Remove</button>
  </div>

  <form onsubmit={ add }>
    <input type="text" class="form-input" placeholder="todo item" name="item" />
    <button class="btn btn-primary input-group-btn">Add Item</button>
  </form>

  <style scoped>
    div {
      padding-bottom: 10px;
    }
  </style>

  <script>
    this.items = [{title: 'homework'}, {title: 'wash clothes'}];

    add (event) {
      this.items.push({title: this.item.value});
      this.item.value = '';
    }

    remove (event) {
      const item = event.item;
      const index = this.items.indexOf(item);
      this.items.splice(index, 1);
    }
  </script>
</todo>
