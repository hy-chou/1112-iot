// eslint-disable-next-line no-undef
const socket = io();

const loginSection = document.getElementById('login-section');
const loginForm = document.getElementById('loginForm');
const username = document.getElementById('username');
const password = document.getElementById('password');

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
  loginSection.classList += ' hidden';
  // loginSection.setAttribute('class', 'hidden');
});
