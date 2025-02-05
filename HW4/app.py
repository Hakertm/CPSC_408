'''
    TABLE OF CONTENTS

    L18: start_app()
    L29: main_menu()
    L91: main()

'''


# Import db_ops Class
from db_ops import db_ops

# Global Variable
db_operations = db_ops("playlist.db")

# FUNCTION: Creates the initial playlist database table.
def start_app():
    print("Welcome to your sooper dooper playlist!")

    # Create the songs table. -> run this ONLY once.
    # db_operations.create_new_table()

    # Intake data from the songs.csv file. -> run this ONLY once.
    # db_operations.intake_songs("songs.csv")
        

# FUNCTION: Provides the user with different choices to interact with the playlist database.
def main_menu():
    user_choice = "0"
    
    # Runs the menu so long as the user doesn't decide to quit(7).
    while(user_choice != "8"):
        user_choice = input('''
        ENTER A NUMBER BASED ON THE MENU:
        
        1. Find songs by artist.
        2. Find songs by genres.
        3. Add new song(s) to the playlist.
        4. Show all songs.
        5. Delete a song.
        6. Update a song.
        7. Songs Stats.
        8. Quit
                            
        Input: ''')

        # Determines what action or function is called based on the user's choice.
        match user_choice:
            # Finds songs made by a specific artist.
            case "1":
                db_operations.find_songs_artist()

            # Finds songs of a specific genre.
            case "2":
                db_operations.find_songs_genre()

            # Add songs to the DB given a csv file name.
            case "3":
                db_operations.add_songs()

            # Display all songs in the database.
            case "4":
                db_operations.display_songs()

            # Delete a song given a song and artist name.
            case "5":
                db_operations.delete_songs()

            # Update one of the 5 song's attributes given a song's name and artist.
            case "6":
                db_operations.update_songs()

            # Display various stats of the playlist.
            case "7":
                db_operations.stats()

            # Quit the program.
            case "8":
                print("\tGoodbye!")
                
            # Invalid input check.
            case _:
                print("\tInvalid input. Must be a number between 1-7.")
    
        # Functions as a pause to allow the user to read their input before continuing.
        user_continue = input("\nPress any enter to continue ")


# Main method.
def main():
    start_app()
    main_menu()

    # Close the connections before the program ends.
    db_operations.close_connections()


if __name__ == "__main__":
    main()