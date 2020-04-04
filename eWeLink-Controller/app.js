const http = require('http');
const ewelink = require('ewelink-api');

const hostname = '127.0.0.1';
const port = 2137;

const eweLinkConnection = new ewelink({
    email: 'marcin93w@gmail.com',
    password: process.argv[2],
    region: 'eu',
  });

const server = http.createServer(async (req, res) => {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');

    if (req.url === '/toggleLight') {
        await eweLinkConnection.toggleDevice('10005f2197');
        res.end('OK');
    }

    res.end('Server is running');
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});