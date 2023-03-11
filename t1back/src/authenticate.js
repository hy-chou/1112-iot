const bcrypt = require('bcrypt');

const hashOfUsername = {
  username: '$2b$10$PTeEym1mHpivsQ2Rg0p60.o.0fxf13PK89Fv2IcICOG.MPKgYehvm',
};

const authenticate = async (credentials) => {
  const hash = hashOfUsername[credentials.username];

  if (hash === undefined) {
    return false;
  }

  return bcrypt.compare(credentials.password, hash);
};

module.exports = { authenticate };
