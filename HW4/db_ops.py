'''
    TABLE OF CONTENTS

#---Logistical Functions---#
    L32 --> __init__(self)
    L39 --> create_new_table(self)
    L59 --> close_connections(self)
    L66 --> intake_songs(self, csv_file) 

#---Core Functions---#
    L124 --> find_songs_artist(self)
    L170 --> find_songs_genre(self)
    L216 --> add_songs(self)
    L229 --> display_songs(self)
    L255 --> delete_songs(self)
    L288 --> update_songs(self)
    L410 --> stats(self)
'''

# Import Libraries
import sqlite3
import csv
import os

# Various operations that can be performed on the playlist database. Consists of 7 core functions.
class db_ops():
    #===============================================#
    #-------------Logistical Functions--------------#
    #===============================================#

    # FUNCTION: Create connection + cursor object.
    def __init__(self, con_path):
        self.connection = sqlite3.connect(con_path) 
        self.cursor = self.connection.cursor()
        print("Connection Established.") # For debugging/testing.


    # FUNCTION: Create the songs table.
    def create_new_table(self):
        # Create table query; 6 values.
        query = '''
        CREATE TABLE songs(
            ID TEXT PRIMARY KEY NOT NULL,
            song_name VARCHAR(50) NOT NULL,
            artist_name VARCHAR(50) NOT NULL,
            album VARCHAR(50),
            genre VARCHAR(50) NOT NULL,
            song_length_sec REAL NOT NULL);
        '''
        # Note: 'album' isn't set to NOT NULL to allow for singles.

        # Execute + Commit to DB
        self.cursor.execute(query)
        self.connection.commit()
        print("New table successfully created.") # For debugging/testing.


    # FUNCTION: Close the database connections.
    def close_connections(self):
        self.cursor.close()
        self.connection.close()
        print('Connection Closed') # For debugging/testing.


    # FUNCTION: Intake data from a .csv file.
    def intake_songs(self, csv_file):
        # Insert query; 6 values.
        query = '''
            INSERT INTO songs VALUES(?, ?, ?, ?, ?, ?);
        '''

        # Select each song and artist. Used to check if a song already exists in the DB.
        check_query = '''
        SELECT song_name, artist_name
        FROM songs;
        '''
        
        # Store the results from the check_query.
        results = self.cursor.execute(check_query)
        
        # Append each song and their artist to the respective list. Used to check if
        # a song already exists in the DB.
        song_list = []
        artist_list = []
        for row in results:
            song_list.append(row[0])
            artist_list.append(row[1])

        # Open the input csv file.
        with open(csv_file, mode = 'r') as file:
            file = csv.reader(file)

            # Skip the header.
            next(file)

            # Iterates through each line in the input file and compares its song and artist to
            # each song and artist in the current database to ensure duplicates don't occur.
            # Inserts the song if it isn't a duplicate.
            for line in file:
                insert_song = True

                # Iterate through each song already in the playlist.
                for i in range(0, len(song_list)):
                    # Checks if the song and artist are the same.
                    if(line[1] == song_list[i] and line[2] == artist_list[i]):
                        print(line[1] + " by " + line[2] + " already exists in the DB.")
                        insert_song = False
                        break

                # Insert if the song doesn't exist.
                if(insert_song):
                    self.cursor.execute(query, line)
                    print(line[1] + " by " + line[2] + " inserted.")

        # Commit to DB
        self.connection.commit()
        print("\nSuccessfully intaked songs.")

    #===============================================#
    #----------------Core Functions-----------------#
    #===============================================#

    # FUNCTION: Find songs made by a specific Artist.
    def find_songs_artist(self):
        # Select all artists currently in the songs table.
        query = '''
            SELECT DISTINCT artist_name
            FROM songs;
        '''

        # Execute
        results = self.cursor.execute(query)

        # Store results in an array to display to the user in a clean format.
        artist_list = []
        for row in results:
            artist_list.append(row[0])

        print("Select an artist to search on:")

        # Display artists.
        for i in range(len(artist_list)):
            print(f"{i+1}. {artist_list[i]}")
 
        # Get user input.
        choice = input("Choice: ")

        # Only triggers if the input is not an integer, zero, or out of bounds of the artist_list.
        while(not (choice.isnumeric()) or int(choice) == 0 or int(choice) > len(artist_list)):
            print(f"Invalid input. Must be between 1 and {len(artist_list)}")
            
            choice = input("Choice: ")

        # Find all songs made by the chosen artist.
        search_query = '''
        SELECT song_name
        FROM songs
        WHERE artist_name = '%s';
        '''

        # Execute the search query given the user's choice.
        song_results = self.cursor.execute(search_query % artist_list[int(choice) - 1])

        # Print the resulting songs.
        for song in song_results:
            print(song[0])


    # FUNCTION: Find songs by Genre.
    def find_songs_genre(self):
        # Select all genres currently in the songs table.
        query = '''
            SELECT DISTINCT genre
            FROM songs;
        '''

        # Execute
        results = self.cursor.execute(query)

        # Store results in an array to display to the user in a clean format.
        genre_list = []
        for row in results:
            genre_list.append(row[0])

        print("Select genre to search on:")

        # Display genres.
        for i in range(len(genre_list)):
            print(f"{i+1}. {genre_list[i]}")

        # Get user input.
        choice = input("Choice: ")

        # Only triggers if the input is not an integer, zero, or out of bounds of the genre_list.
        while(not (choice.isnumeric()) or int(choice) == 0 or int(choice) > len(genre_list)):
            print(f"Invalid input. Must be between 1 and {len(genre_list)}")
            
            choice = input("Choice: ")

        # Find all songs of the genre type.
        search_query = '''
        SELECT song_name
        FROM songs
        WHERE genre = '%s';
        '''

        # Execute the search query given the user's choice.
        song_results = self.cursor.execute(search_query % genre_list[int(choice) - 1])

        # Print the resulting songs.
        for song in song_results:
            print(song[0])


    # FUNCTION: Add new songs to the playlist given a csv file.
    def add_songs(self):
        # Get file name from the user.
        file_name = input("Enter the name of your file containing your new songs: ")
        
        # Check if the file exists.
        if(not (os.path.exists(file_name))):
            print("File does not exist. Aborting operation.")
            return
        
        self.intake_songs(file_name)


    # FUNCTION: Display all songs and their respective attributes that are in the database.
    def display_songs(self):
        # Select all songs and their respective attributes (ID excluded).
        query = '''
        SELECT song_name, artist_name, album, genre, song_length_sec
        FROM songs;
        '''

        # Execute query.
        results = self.cursor.execute(query)

        # Formated print using headers and separator.
        headers = ["Song Name", "Artist", "Album", "Genre", "Song Length(SEC)"]

        # Headers
        print(f"{headers[0]:<30} {headers[1]:<20} {headers[2]:<30} {headers[3]:<20} {headers[4]:<15}")

        # Separator
        print("-"*150)

        # Iterate through results.
        for row in results:
            song_name, artist_name, album, genre, song_len_sec = row
            print(f"{song_name:<30} {artist_name:<20} {album:<30} {genre:<20} {song_len_sec:<15}")


    # FUNCTION: Delete song(s) given a song and artist name.
    def delete_songs(self):
        # Will continue prompting until the user presses enter on either prompt.
        while(True):
            # Display the songs in the database.
            self.display_songs()

            print("\nEnter a song and artist name in order to delete a song from the playist.")
            print("Press enter once or twice to quit this operation.")

            # Get user input for the song and artist.
            song = input("Song: ")
            artist = input("Artist: ")

            # End the loop if either inputs are empty (enter).
            if(song == "" or artist == ""):
                print("Exiting operation.")
                break

            # Placeholder filler list used in the query.
            search_list = [song, artist]

            # Delete the song where the song and artist name are equal.
            delete_query = '''
            DELETE FROM songs WHERE song_name LIKE ? AND artist_name LIKE ?;
            '''

            # Execute query and commit the change.
            self.cursor.execute(delete_query, search_list)
            self.connection.commit()
            print("Successfully deleted the song.")


    # FUNCTION: Update song(s) given a song and artist name.
    def update_songs(self):
        # Will continue prompting until the user presses enter on either prompt.
        while(True):
            # Display the songs in the database.
            self.display_songs()

            print("\nEnter a song and artist name in order to update a song from the playist.")
            print("Press enter once or twice to quit this operation.")

            # Get user input for the song and artist.
            song = input("Song: ")
            artist = input("Artist: ")

            # End the loop if either inputs are empty (enter).
            if(song == "" or artist == ""):
                print("Exiting operation.")
                break

            # List of choices for the user.
            user_input = input('''
            ENTER A NUMBER TO SELECT WHICH ATTRIBUTE TO UPDATE:

            1. Song Name
            2. Artist Name
            3. Album Name
            4. Genre
            5. Song Length (seconds)
            6. Cancel

            Input: ''')

            # List used for the placeholders in the query.
            search_list = [song, artist]

            query = ""
            success = True

            # Match the user's choice to the respective attribute.
            match user_input:
                # Update the song name.
                case "1":
                    # Get user input and insert to the start of the placeholder list.
                    user_input = input("Enter a new song name: ")
                    search_list.insert(0, user_input)
                    
                    # Update query.
                    query = '''
                    UPDATE songs 
                    SET song_name = ?
                    WHERE song_name LIKE ? AND artist_name LIKE ?;
                    '''
                
                # Update the artist name.
                case "2":
                    # Get user input and insert to the start of the placeholder list.
                    user_input = input("Enter a new artist name: ")
                    search_list.insert(0, user_input)
                    
                    # Update query.
                    query = '''
                    UPDATE songs 
                    SET artist_name = ?
                    WHERE song_name LIKE ? AND artist_name LIKE ?;
                    '''
                
                # Update the album name.
                case "3":
                    # Get user input and insert to the start of the placeholder list.
                    user_input = input("Enter a new album name: ")
                    search_list.insert(0, user_input)
                    
                    # Update query.
                    query = '''
                    UPDATE songs 
                    SET album = ?
                    WHERE song_name LIKE ? AND artist_name LIKE ?;
                    '''
                
                # Update the genre.
                case "4":
                    # Get user input and insert to the start of the placeholder list.
                    user_input = input("Enter a new genre name: ")
                    search_list.insert(0, user_input)
                    
                    # Update query.
                    query = '''
                    UPDATE songs 
                    SET genre = ?
                    WHERE song_name LIKE ? AND artist_name LIKE ?;
                    '''
                
                # Update the song length.
                case "5":
                    # Get user input and insert to the start of the placeholder list.
                    user_input = input("Enter a new song duration length (in seconds): ")
                    search_list.insert(0, user_input)
                    
                    # Update query.
                    query = '''
                    UPDATE songs 
                    SET song_length_sec = ?
                    WHERE song_name LIKE ? AND artist_name LIKE ?;
                    '''
                
                # Stop updating the same song.
                case "6":
                    print("Canceling Operation.")
                    success = False
                
                # Invalid input check.
                case _:
                    print("Invalid input. Must be a number between 1-6.")
                    success = False

            # Prevents invalid input from going through.
            if(success):
                self.cursor.execute(query, search_list)
                self.connection.commit()
                print("Successfully updated the song's attribute.")


    # FUNCTION: Show various stats for the playlist.
    def stats(self):
        # Compute the total playlist time (in seconds).
        playlist_len_query = '''
        SELECT SUM(song_length_sec) AS PlaylistLength
        FROM songs;
        '''

        # Compute the total number of songs in the playlist.
        total_songs_query = '''
        SELECT COUNT (*) AS TotalSongs
        FROM songs;
        '''

        # Compute the total of number of songs for each artist.
        songs_by_artist_query = '''
        SELECT artist_name, COUNT(song_name) AS TotalSongs
        FROM songs
        GROUP BY artist_name;
        '''

        # Execute the 1st query.
        q1 = self.cursor.execute(playlist_len_query)
        total_length_min = 0

        for row in q1: # Store the result.
            total_length_min = (row[0])/60 # Convert to minutes.

        # Execute the 2nd query.
        q2 = self.cursor.execute(total_songs_query)
        num_songs = 0

        for row in q2: # Store the result.
            num_songs = row[0]

        # Execute the 3rd query.
        q3 = self.cursor.execute(songs_by_artist_query)
        artist_list = []
        songs_count = []

        for row in q3: # Store the results.
            artist_list.append(row[0])
            songs_count.append(row[1])

        # Display the stats to user in a clean format.
        print("Total Playlist Length (in minutes): " + f"{total_length_min: .2f}")
        print("Total Number of Songs: " + f"{num_songs}")
        print("Total Number of Songs By Each Artist:")

        # Formated print using headers and separator.
        headers = ["Artist", "Total Songs"]

        # Headers
        print(f"{headers[0]:<20} {headers[1]:<10}")

        # Separator
        print("-" * 40)

        # Iterate through results.
        for i in range (0, len(artist_list)):
            print(f"{ artist_list[i]:<20} {songs_count[i]:<10}")
