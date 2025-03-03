INSERT INTO Genres (name) VALUES 
('Rock'),
('Pop'),
('Hip-Hop');

INSERT INTO Artists (name, nickname) VALUES
('John Smith', 'Johnny Rock'),
('Lisa Carter', 'Lisa Pop'),
('Mike Johnson', 'MC Mike'),
('Emma Williams', 'DJ Em'),
('Marchall Bruce Mathers III', 'Eminem');

INSERT INTO Genres_Artists (genre_id, artist_id) VALUES
(1, 1),  -- Johnny -> Rock
(2, 2),  -- Lisa Pop -> Pop
(3, 3),  -- MC Mike -> Hip-Hop
(2, 4),  -- DJ Em -> Pop
(3, 4),  -- DJ Em -> Hip-Hop
(3, 5);  -- Eminem -> Hip-Hop

INSERT INTO Albums (title, release_year) VALUES
('Rocking My World', 2018),
('Pop Sensation', 2019),
('Hip-Hop Beats', 2020),
('The Slim Shady', 1999);

INSERT INTO Albums_Artists (album_id, artist_id) VALUES
(1, 1),  -- Johnny -> Rocking My World
(2, 2),  -- Lisa Pop -> Pop Sensation
(3, 3),  -- MC Mike -> Hip-Ho Beats
(2, 4),  -- DJ Em -> Pop Sensation
(3, 4),  -- DJ Em -> Hip-Hop Beats
(4, 5);  -- Eminem -> The Slim Shady

INSERT INTO Tracks (title, durations, album_id) VALUES
('My Rock Anthem', 220, 1),
('Powerful Guitar', 210, 1),
('Love in the Air', 180, 2),
('Dance Forever', 230, 2),
('Rap Revolution', 250, 3),
('Beats Drop', 200, 3),
('My Name Is', 268, 4),
('Lose Yourself', 326, 4);

INSERT INTO Compilations (title, release_year) VALUES
('Best of Rock 2018', 2018),
('Pop Hits 2019', 2019),
('Hip-Hop Vibes', 2020),
('Mega Mix 2020', 2020);

INSERT INTO Compilations_Tracks (compilation_id, track_id) VALUES
(1, 1),  -- My Rock Anthem in Best of Rock 2018
(1, 2),  -- Powerful Guitar in Best of Rock 2018
(2, 3),  -- Love in the Air in Pop Hits 2019
(2, 4),  -- Dance Forever in Pop Hits 2019
(3, 5),  -- Rap Revolution in Hip-Hop Vibes
(3, 6),  -- Beats Drop in Hip-Hop Vibes
(3, 7),  -- My Name Is in Hip-Hop Vibes
(4, 1),  -- My Rock Anthem also in Mega Mix 2020
(4, 5);  -- Rap Revolution also in Mega Mix 2020
