CREATE TABLE IF NOT EXISTS kicks (
    id SERIAL PRIMARY KEY,
    player VARCHAR(100),
    competition VARCHAR(50),
    distance FLOAT,
    angle FLOAT,
    success BOOLEAN
);
