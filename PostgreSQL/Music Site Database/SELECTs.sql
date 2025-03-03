-- 2.1 Название и продолжительность самого длительного трека.
SELECT title, durations
FROM Tracks
WHERE durations = (SELECT MAX(durations) FROM Tracks);

-- 2.2 Название треков, продолжительность которых не менее 3,5 минут.
SELECT title
FROM Tracks
WHERE durations >= 210;

-- 2.3 Названия сборников, вышедших в период с 2018 по 2020 год включительно.
SELECT title
FROM Compilations
WHERE release_year BETWEEN 2018 AND 2020;

-- 2.4 Исполнители, чей псевдоним состоит из одного слова.
SELECT id, name, nickname
FROM Artists
WHERE nickname NOT LIKE '% %';

-- 2.5 Название треков, которые содержат слово «my».
SELECT title
FROM Tracks
WHERE title ~* '\ymy\y';

-- 3.1 Количество исполнителей в каждом жанре.
SELECT g.name AS genre, COUNT(ga.artist_id) AS artist_count
FROM Genres g
LEFT JOIN Genres_Artists ga ON ga.genre_id = g.id
GROUP BY g.name
ORDER BY artist_count DESC;

-- 3.2.1 Количество треков, вошедших в альбомы 2019–2020 годов.
SELECT COUNT(title) AS track_count
FROM Tracks
WHERE album_id IN (SELECT id FROM Albums WHERE release_year BETWEEN 2019 AND 2020);

-- 3.2.2 Количество треков, вошедших в альбомы 2019–2020 годов.
SELECT COUNT(t.title) AS track_count
FROM Tracks t
JOIN Albums a ON t.album_id = a.id
WHERE a.release_year BETWEEN 2019 AND 2020;

-- 3.3 Средняя продолжительность треков по каждому альбому.
SELECT a.title AS album_title, AVG(t.durations) AS avg_durations
FROM Albums a
JOIN Tracks t ON a.id = t.album_id
GROUP BY a.title
ORDER BY avg_durations DESC;

-- 3.4.1 Все исполнители, которые не выпустили альбомы в 2020 году.
SELECT ar.nickname
FROM Artists ar
LEFT JOIN Albums_Artists aa ON ar.id = aa.artist_id
LEFT JOIN Albums al ON al.id = aa.album_id AND al.release_year = 2020
WHERE al.id IS NULL;

-- 3.4.2 Все исполнители, которые не выпустили альбомы в 2020 году.
SELECT ar.nickname AS artist
FROM Artists ar
WHERE NOT EXISTS (
    SELECT 1 
    FROM Albums_Artists aa
    JOIN Albums al ON aa.album_id = al.id
    WHERE aa.artist_id = ar.id 
    AND al.release_year = 2020
);

-- 3.4.3 Все исполнители, которые не выпустили альбомы в 2020 году.
SELECT ar.nickname AS artist
FROM Artists ar
WHERE ar.id NOT IN (
    SELECT aa.artist_id
    FROM Albums_Artists aa
    JOIN Albums al ON aa.album_id = al.id AND al.release_year = 2020
);

-- 3.5 Названия сборников, в которых присутствует Eminem
SELECT DISTINCT c.title AS compilation_title
FROM Compilations c
JOIN Compilations_Tracks ct ON c.id = ct.compilation_id
JOIN Tracks tr ON ct.track_id = tr.id
JOIN Albums al ON tr.album_id = al.id
JOIN Albums_Artists aa ON al.id = aa.album_id
JOIN Artists ar ON aa.artist_id = ar.id
WHERE ar.nickname = 'Eminem'; -- Здесь указываем нужного исполнителя

-- 4.1.1 Названия альбомов, в которых присутствуют исполнители более чем одного жанра.
SELECT al.title
FROM Albums al
JOIN Albums_Artists aa ON al.id = aa.album_id AND 
aa.artist_id IN (
				 SELECT artist_id
				 FROM Genres_Artists
				 GROUP BY artist_id
				 HAVING count(artist_id) > 1
				);

-- 4.1.2 Названия альбомов, в которых присутствуют исполнители более чем одного жанра.
SELECT al.title
FROM Albums al
JOIN Albums_Artists aa ON al.id = aa.album_id
JOIN Genres_Artists ga ON ga.artist_id = aa.artist_id
GROUP BY al.title
HAVING COUNT(DISTINCT ga.genre_id) > 1;

-- 4.2 Наименования треков, которые не входят в сборники.
SELECT t.title
FROM Tracks t
LEFT JOIN Compilations_Tracks ct ON t.id = ct.track_id
WHERE ct.compilation_id IS NULL;

-- 4.3 Исполнитель или исполнители, написавшие самый короткий по продолжительности трек
SELECT DISTINCT ar.nickname
FROM Artists ar
JOIN Albums_Artists aa ON ar.id = aa.artist_id
JOIN Albums al ON al.id = aa.album_id
JOIN Tracks tr ON tr.album_id = al.id
WHERE tr.durations = (SELECT MIN(durations) FROM Tracks);

-- 4.4 Названия альбомов, содержащих наименьшее количество треков.
SELECT a.title AS album_title
FROM Albums a
JOIN Tracks t ON a.id = t.album_id
GROUP BY a.id, a.title
HAVING COUNT(t.id) = (
    SELECT MIN(track_count)
    FROM (
        SELECT COUNT(t.id) AS track_count
        FROM Albums a
        JOIN Tracks t ON a.id = t.album_id
        GROUP BY a.id
    ) AS album_track_counts
);

