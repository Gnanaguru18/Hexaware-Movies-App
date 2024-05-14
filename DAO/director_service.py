from Utility.DBconn import DBconnection

class DirectorService(DBconnection):


    def read_director(self):
        try:
            self.cursor.execute("Select * from Directors")
            #movies = cursor.fetchall()
            for director in self.cursor:
                print(director)
        except Exception as e:
            print(e)
     
    def create_director(self,Name):
        try:
            self.cursor.execute(
                "INSERT INTO directors (Name) VALUES (?)",
                (Name)
            )
            self.conn.commit()   # Permanent storing | If no commit then no data | Before commiting we can change the values and redo
        except Exception as e:
            print(e)
    
    def delete_director(self,director_id):
        try:
            self.cursor.execute("""
            delete from Movies
            where """
            )
        except Exception as e:
            print(e)