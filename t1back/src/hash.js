/* eslint-disable no-console */
const { argv } = require('node:process');
const bcrypt = require('bcrypt');

const saltRounds = 10;

if (argv.length === 3) {
  const password = argv[2];

  console.log(password);
  bcrypt.hash(password, saltRounds).then((hash) => console.log(hash));
}
