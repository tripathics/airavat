CREATE TABLE bus (
    id INTEGER,
    license_plate TEXT NOT NULL,
    long REAL,
    lat REAL,
    in_campus_location TEXT,
    PRIMARY KEY(id)   
);

CREATE TABLE users (
    id INTEGER, 
    username TEXT NOT NULL, 
    password TEXT NOT NULL, 
    PRIMARY KEY(id)
);

