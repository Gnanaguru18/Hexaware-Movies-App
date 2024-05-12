import pyodbc

server_name = "TIGGER\\SQLEXPRESS"
database_name = "HexawareMoviesDB"
 
 
conn_str = (
    f"Driver={{SQL Server}};"
    f"Server={server_name};"
    f"Database={database_name};"
    f"Trusted_Connection=yes;"
)

print(conn_str)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

cursor.execute("Select 1")
print("Database connection is successful")


class MovieService:
    def read_movies(self):
        cursor.execute("Select * from Movies")
        #movies = cursor.fetchall()
        for movie in cursor:
            print(movie)

    def create_movie(self):
        movie=self.input_movies()
        cursor.execute(
            "INSERT INTO Movies (Title, Year, DirectorId) VALUES (?, ?, ?)",
            (movie[0],movie[1],movie[2])
        )
        conn.commit()   # Permanent storing | If no commit then no data | Before commiting we can change the values and redo

    def delete_movie(self,id):
        cursor.execute(
            "delete from Movies where MovieId = ?",
            (id)
        )
        conn.commit()

    def update_movie(self,id):
        movie=self.input_movies()
        cursor.execute(
            "update Movies set title = ?,year = ? , DirectorId = ? where MovieId = ?",
            (movie[0],movie[1],movie[2],id)
        )
        conn.commit()

    def input_movies(self):
        title=input("Title:")
        year=int(input("Year:"))
        directorId=int(input("DirectorID:"))
        movie=[title,year,directorId]
        return movie

movie_service = MovieService()

while True:
    print("""
        Choose 
        1: To create movie
        2: View table
        3. Update a movie
        4. To delete movie
        5. Exit""")
    choice=int(input("Enter choice:"))
    if choice==1:
        movie_service.create_movie()
    elif choice==2:
        movie_service.read_movies()
    elif choice==3:
        update_id=int(input("Enter movieid to update:"))
        movie_service.update_movie(update_id)
    elif choice==4:
        movie_service.read_movies()
        id=int(input("Enter Movie Id to delete:"))
        movie_service.delete_movie(id)
    elif choice==5:
        break
    else:
        print("Wrong choice ❌")


cursor.close()
conn.close()