// eslint-disable-next-line no-undef
const socket = io();

const loginForm = document.getElementById('loginForm');
const username = document.getElementById('username');
const password = document.getElementById('password');
const cameraForm = document.getElementById('cameraForm');
const doorForm = document.getElementById('doorForm');
const image = document.getElementById('image');
const messages = document.getElementById('messages');

loginForm.addEventListener('submit', (e) => {
  e.preventDefault();
  if (username.value && password.value) {
    socket.emit('login', {
      username: username.value,
      password: password.value,
    });
    username.value = '';
    password.value = '';
  }
});

cameraForm.addEventListener('submit', (e) => {
  e.preventDefault();
  socket.emit('camera');
});

doorForm.addEventListener('submit', (e) => {
  e.preventDefault();
  socket.emit('door');
});

socket.on('image', (data) => {
  image.src = data;
});

socket.on('message', (msg) => {
  messages.textContent = msg;
});
