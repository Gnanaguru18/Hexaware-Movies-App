from Utility.DBconn import DBconnection

class MovieService(DBconnection):


    def read_movies(self):
        try:
            self.cursor.execute("Select * from Movies")
            #movies = cursor.fetchall()
            for movie in self.cursor:
                print(movie)
        except Exception as e:
            print(e)
     

    def create_movie(self):
        try:
            movie=self.input_movies()
            self.cursor.execute(
                "INSERT INTO Movies (Title, Year, DirectorId) VALUES (?, ?, ?)",
                (movie[0],movie[1],movie[2])
            )
            self.conn.commit()   # Permanent storing | If no commit then no data | Before commiting we can change the values and redo
        except Exception as e:
            print(e)
      

    def delete_movie(self,id):
        try:     
            self.cursor.execute(
                "delete from Movies where MovieId = ?",
                (id)
            )
            self.conn.commit()
        except Exception as e:
            print(e)
      

    def update_movie(self,id):
        try:
            movie=self.input_movies()
            self.cursor.execute(
                "update Movies set title = ?,year = ? , DirectorId = ? where MovieId = ?",
                (movie[0],movie[1],movie[2],id)
            )
            self.conn.commit()
        except Exception as e:
            print(e)
      

    def input_movies(self):
        try:
            title=input("Title:")
            year=int(input("Year:"))
            directorId=int(input("DirectorID:"))
            movie=[title,year,directorId]
            return movie
        except Exception as e:
            print(e)
       
