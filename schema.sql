Create Database HexawareMoviesDB;
use HexawareMoviesDB;

CREATE TABLE Movies (
    MovieId INT PRIMARY KEY IDENTITY(1,1),
    Title NVARCHAR(100),
    Year INT,
    DirectorId INT
);
CREATE TABLE Directors (
    DirectorId INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100)
);
CREATE TABLE Actors (
    ActorId INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100)
);

-- This is my In-junction table
CREATE TABLE MovieActors (
    MovieId INT,
    ActorId INT,
    PRIMARY KEY (MovieId, ActorId),
    FOREIGN KEY (MovieId) REFERENCES Movies(MovieId),
    FOREIGN KEY (ActorId) REFERENCES Actors(ActorId)
);
 