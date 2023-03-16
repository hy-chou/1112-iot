// eslint-disable-next-line no-undef
const socket = io();

const loginStep = document.getElementById('login-step');
const loginForm = document.getElementById('loginForm');
const username = document.getElementById('username');
const password = document.getElementById('password');

const image = document.getElementById('image');

const cameraButton = document.getElementById('camera-button');
const doorButton = document.getElementById('door-button');

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

socket.on('loginOK', () => {
  loginStep.classList += ' hidden';
});

socket.on('image', (data) => {
  image.src = data;
});

cameraButton.addEventListener('click', () => {
  socket.emit('camera');
});

doorButton.addEventListener('click', () => {
  socket.emit('door');
});
