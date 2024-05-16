CREATE TABLE IF NOT EXISTS players(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    p_name TEXT NOT NULL,
    position TEXT NOT NULL,
    college TEXT NOT NULL,
    country TEXT NOT NULL,
    grade TEXT NOT NULL,
    number TEXT NOT NULL
);

CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL
    );

CREATE TABLE IF NOT EXISTS drafts(
    user_id INTEGER,
    slot TEXT NOT NULL,
    p_name TEXT NOT NULL,
    position TEXT NOT NULL,
    college TEXT NOT NULL,
    country TEXT NOT NULL,
    grade TEXT NOT NULL,
    number TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE playerpoints (
    name TEXT NOT NULL,
    points INTEGER NOT NULL
);


CREATE TABLE UserRatings (
    username TEXT NOT NULL,
    teamRating REAL NOT NULL
);


