CREATE TABLE bus (
    id INTEGER,
    name TEXT DEFAULT "Bus" NOT NULL,
    license_plate TEXT NOT NULL,
    status INTEGER DEFAULT 1 NOT NULL,
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

