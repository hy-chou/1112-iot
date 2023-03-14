/* eslint-disable no-console */
const { spawn } = require('node:child_process');

const capture = (socket) => {
  const subprocess = spawn(
    '/usr/bin/python3',
    ['capture.py'],
    { stdio: ['ignore', 'pipe', 'ignore'] },
  );
  let image = '';

  subprocess.stdout.on('data', (data) => {
    image += data;
  });

  subprocess.on('close', async (code) => {
    if (code === 0) {
      socket.emit('image', `data:image/png;base64,${image.slice(2, -2)}`);
    }
    console.log(`capture.py exited with code ${code}`);
  });
};

module.exports = { capture };
