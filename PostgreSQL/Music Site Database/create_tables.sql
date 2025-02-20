-- Создание таблицы Genres
CREATE TABLE Genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Создание таблицы Artists
CREATE TABLE Artists (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    nickname VARCHAR(255)
);

-- Создание таблицы Genres_Artists (связь "многие ко многим" между Genres и Artists)
CREATE TABLE Genres_Artists (
    genre_id INT NOT NULL,
    artist_id INT NOT NULL,
    PRIMARY KEY (genre_id, artist_id),
    FOREIGN KEY (genre_id) REFERENCES Genres(id) ON DELETE CASCADE,
    FOREIGN KEY (artist_id) REFERENCES Artists(id) ON DELETE CASCADE
);

-- Создание таблицы Albums
CREATE TABLE Albums (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT NOT NULL,
    CHECK (release_year BETWEEN 1900 AND 2999)
);

-- Создание таблицы Albums_Artists (связь "многие ко многим" между Albums и Artists)
CREATE TABLE Albums_Artists (
    album_id INT NOT NULL,
    artist_id INT NOT NULL,
    PRIMARY KEY (album_id, artist_id),
    FOREIGN KEY (album_id) REFERENCES Albums(id) ON DELETE CASCADE,
    FOREIGN KEY (artist_id) REFERENCES Artists(id) ON DELETE CASCADE
);

-- Создание таблицы Tracks
CREATE TABLE Tracks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration INT NOT NULL,
    album_id INT NOT NULL,
    CHECK (duration > 0),
    FOREIGN KEY (album_id) REFERENCES Albums(id) ON DELETE CASCADE
);

-- Создание таблицы Compilations
CREATE TABLE Compilations (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_year INT NOT NULL
);

-- Создание таблицы Compilations_Tracks (связь "многие ко многим" между Compilations и Tracks)
CREATE TABLE Compilations_Tracks (
    compilation_id INT NOT NULL,
    track_id INT NOT NULL,
    PRIMARY KEY (compilation_id, track_id),
    FOREIGN KEY (compilation_id) REFERENCES Compilations(id) ON DELETE CASCADE,
    FOREIGN KEY (track_id) REFERENCES Tracks(id) ON DELETE CASCADE
);
