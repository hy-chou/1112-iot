/* eslint-disable no-console */
const http = require('node:http');

const express = require('express');
const { Server } = require('socket.io');

const { authenticate } = require('./src/authenticate');
const { capture } = require('./src/capture');
const { blink } = require('./src/blink');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

const legalUsers = new Set();

app.use(express.static('public'));

io.on('connection', (socket) => {
  console.log(`${socket.id} connected`);

  socket.on('login', async (credentials) => {
    const isLegal = await authenticate(credentials);

    if (isLegal) {
      legalUsers.add(socket.id);
      console.log(legalUsers);

      socket.emit('message', 'login OK');
      socket.emit('loginOK');
    } else {
      socket.emit('message', 'login KO');
    }
  });

  socket.on('camera', () => {
    if (legalUsers.has(socket.id)) {
      capture(socket);

      socket.emit('message', 'camera OK');
    } else {
      socket.emit('message', 'camera KO');
    }
  });

  socket.on('door', () => {
    if (legalUsers.has(socket.id)) {
      // openTheDoor();
      blink();

      socket.emit('message', 'door OK');
    } else {
      socket.emit('message', 'door KO');
    }
  });

  socket.on('disconnect', () => {
    legalUsers.delete(socket.id);
    console.log(legalUsers);

    console.log(`${socket.id} disconnected`);
  });
});

server.listen(3000, () => {
  console.log('listening on *:3000');
});
