import { createServer } from 'node:http';

const server = createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('This is My Now it should work\n');
});

server.listen(3000, '0.0.0.0', () => {
  console.log('Listening on 127.0.0.1:3000');
});

