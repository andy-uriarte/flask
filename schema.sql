DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS reviews;

CREATE TABLE user (
	id SERIAL PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL
);

CREATE TABLE reviews (
	id SERIAL PRIMARY KEY,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  rating INTEGER NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
