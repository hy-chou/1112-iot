/* eslint-disable no-console */
const { spawn } = require('node:child_process');

class Camera {
  static stream(socket) {
    const subprocess = spawn(
      '/usr/bin/python3',
      ['capture.py'],
      { stdio: ['ignore', 'pipe', process.stderr] },
    );
    let image = '';

    subprocess.stdout.on('data', (data) => {
      image += data;
    });

    subprocess.on('close', async (code) => {
      if (code === 0) {
        socket.emit('image', `data:image/png;base64,${image.slice(2, -2)}`);
      }
      console.log(`child process exited with code ${code}`);
      this.stream(socket);
    });
  }
}

module.exports = Camera;
