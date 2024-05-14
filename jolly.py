
from Entity.movie import Movie
from DAO.movie_service import MovieService 
from DAO.director_service import DirectorService
class MainMenu:
    movie_service = MovieService()
    director_service = DirectorService()

    def movie_menu(self):
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
                self.movie_service.create_movie()
            elif choice==2:
                self.movie_service.read_movies()
            elif choice==3:
                update_id=int(input("Enter movieid to update:"))
                self.movie_service.update_movie(update_id)
            elif choice==4:
                self.movie_service.read_movies()
                id=int(input("Enter Movie Id to delete:"))
                self.movie_service.delete_movie(id)
            elif choice==5:
                break

    def director_menu(self):
        while True:
            print("""
                Choose 
                1: To create director
                2: View director
                3. Update a director
                4. To delete director
                5. Exit""")
            choice=int(input("Enter choice:"))
            if choice == 1:
                name=input("Enter Director name:")
                self.director_service.create_director(name)
            elif choice == 2:
                self.director_service.read_director()
            elif choice == 3:
                continue
            elif choice == 4:
                continue
            elif choice == 5:
                break


if __name__=="__main__":
    print("Welcome to the movies app")
    main_menu = MainMenu()

    while True:
        print(
            """      
            1. Movie Management
            2. Director Management
            3. Actor Management
            4. Exit
                """
        )

        choice = int(input("Please choose from above options: "))

        if choice == 1:
            main_menu.movie_menu()
        elif choice == 2:
            main_menu.director_menu()
        elif choice == 3:
            main_menu.actor_menu()
        elif choice == 4:
            # movie_service - class variable
            # Error will happen will call exit
            main_menu.movie_service.close()
            main_menu.director_service.close()  
            # main_menu.director_service.close()  # conn2
            break
 

    # cursor.close()
    # conn.close()