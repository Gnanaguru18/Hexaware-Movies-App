INSERT INTO Directors (Name) VALUES
('Christopher Nolan'),
('S.S. Rajamouli'),
('Mani Ratnam'),
('David Fincher'),
('Shankar'),
('Quentin Tarantino');

INSERT INTO Movies (Title, Year, DirectorId) VALUES
('Inception', 2010, 1),
('The Dark Knight', 2008, 1),
('Baahubali', 2015, 2),
('RRR', 2022, 2),
('Ponniyin Selvan', 2022, 3),
('Guru', 2007, 3),
('Fight Club', 1999, 4),
('Se7en', 1995, 4),
('Enthiran', 2010, 5),
('2.0', 2018, 5),
('Pulp Fiction', 1994, 6),
('Django Unchained', 2012, 6);

INSERT INTO Actors (Name) VALUES
('Leonardo DiCaprio'),
('Christian Bale'),
('Prabhas'),
('Ram Charan'),
('Vikram'),
('Aishwarya Rai'),
('Brad Pitt'),
('Morgan Freeman'),
('Rajinikanth'),
('Amitabh Bachchan');

INSERT INTO MovieActors (MovieId, ActorId) VALUES
(1, 1), -- Inception: Leonardo DiCaprio
(2, 2), -- The Dark Knight: Christian Bale
(3, 3), -- Baahubali: Prabhas
(4, 4), -- RRR: Ram Charan
(5, 5), -- Ponniyin Selvan: Vikram
(5, 6), -- Ponniyin Selvan: Aishwarya Rai
(6, 5), -- Guru: Vikram
(6, 6), -- Guru: Aishwarya Rai
(7, 7), -- Fight Club: Brad Pitt
(8, 7), -- Se7en: Brad Pitt
(8, 8), -- Se7en: Morgan Freeman
(9, 9), -- Enthiran: Rajinikanth
(10, 9), -- 2.0: Rajinikanth
(11, 7), -- Pulp Fiction: Brad Pitt
(12, 1); -- Django Unchained: Leonardo DiCaprio
 
Select * from Movies
Inner Join Directors 
on Movies.DirectorId = Directors.DirectorId

Select * from Movies
Inner Join MovieActors 
on Movies.MovieId = MovieActors.MovieId
Inner Join Actors
on Actors.ActorId = MovieActors.ActorId
has context menu