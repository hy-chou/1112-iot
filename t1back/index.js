/* eslint-disable no-console */
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');

const { authenticate } = require('./src/authenticate');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.get('/', (_, res) => {
  res.sendFile(`${__dirname}/public/index.html`);
});

io.on('connection', (socket) => {
  console.log('a user connected');

  socket.on('login', async (credentials) => {
    const isAuthenticated = await authenticate(credentials);

    if (isAuthenticated) {
      socket.emit('message', 'OK');
    } else {
      socket.emit('message', 'KO');
    }
  });

  socket.on('disconnect', () => {
    console.log('user disconnected');
  });
});

server.listen(3000, () => {
  console.log('listening on *:3000');
});
