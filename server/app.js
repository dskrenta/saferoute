'use strict';
import Koa from 'koa';
import serveStatic from 'koa-serve-static';

const app = new Koa();
const PORT = 3000;

app
  .use(serveStatic(`${__dirname}/../public`));

app.listen(PORT, () => console.log(`Server started on *:${PORT}`));

export default app;
