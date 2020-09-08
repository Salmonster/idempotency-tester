DROP TABLE IF EXISTS balance;
DROP TABLE IF EXISTS idempotency_keys;

CREATE TABLE balance (
  id SERIAL PRIMARY KEY,
  universal_balance INTEGER NOT NULL
);

CREATE TABLE idempotency_keys (
  id SERIAL PRIMARY KEY,
  key VARCHAR NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
