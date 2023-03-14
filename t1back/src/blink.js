/* eslint-disable no-console */
const { spawn } = require('node:child_process');

const blink = () => {
  const subprocess = spawn('/usr/bin/python3', ['blink.py'], {
    stdio: 'ignore',
  });

  subprocess.on('close', async (code) => {
    console.log(`blink.py exited with code ${code}`);
  });
};

module.exports = { blink };
