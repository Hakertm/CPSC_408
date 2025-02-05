# Import Library
import mysql.connector
import csv

# Contains all the operations that are conducted for the basic test program for rideshare.
class operations():
    #===============================================#
    #-------------Logistical Functions--------------#
    #===============================================#

    # FUNCTION: Create connection + cursor object.
    def __init__(self, db_name):
        # Establish Connection.
        self.conn = mysql.connector.connect(host = "localhost", # Always stays the same.
                                            user = "root",      # Always stays the same.
                                            password = "dolphinmuncha69$",
                                            auth_plugin = "mysql_native_password", # Always stays the same.
                                            database = db_name) 
        # Create Cursor.
        self.cursor = self.conn.cursor()

        self.user_name = ""
        self.user_pass = ""

        print("Connection Established.") # Confirmation.


    # FUNCTION: Close the database connections.
    def close_connections(self):
        self.cursor.close()
        self.conn.close()
        print('Connection Closed.') # Confirmation.


    # FUNCTION: Create the drivers, riders, and rides tables.
    def create_tables(self):
        # Create the 'drivers' table; 4 values.
        q1 = '''
        CREATE TABLE drivers(
            driverID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            active INT NOT NULL);
        '''

        # Create the 'riders' table; 3 values.
        q2 = '''
        CREATE TABLE riders(
            riderID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL);
        '''

        # Create the 'rides' table; 6 values.
        q3 = '''
        CREATE TABLE rides(
            rideID INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
            driverID INT,
            riderID INT,
            pickupLoc VARCHAR(50) NOT NULL,
            dropoffLoc VARCHAR(50) NOT NULL,
            driverRating REAL NOT NULL,
            FOREIGN KEY (driverID) REFERENCES driver(driverID),
            FOREIGN KEY (riderID) REFERENCES riders(riderID));
        '''

        queries = [q1, q2, q3]

        # Execute + Commit each query.
        for i in range (0, len(queries)):
            self.cursor.execute(queries[i])
            self.conn.commit()

        print("New tables successfully created.") # Confirmation.


    #==========Intake Functions==========#
    # FUNCTION: For DRIVERS | Intake data from a .csv file for the 'drivers' table.
    def intake_drivers(self, csv_file):
        # Insert query; 4 values.
        query = '''
            INSERT INTO drivers VALUES(%s, %s, %s, %s);
        '''

        # Open the csv file in read mode.
        with open(csv_file, mode = 'r') as file:
            file = csv.reader(file)

            # Skip the header.
            next(file)

            # Insert the data into the table.
            for line in file:
                self.cursor.execute(query, line)
        
        # Commit to the DB
        self.conn.commit()
        print("\nSuccessfully intaked drivers.")


    # FUNCTION: For RIDERS | Intake data from a .csv file for the 'riders' table.
    def intake_riders(self, csv_file):
        # Insert query; 3 values.
        query = '''
            INSERT INTO riders VALUES(%s, %s, %s);
        '''

        # Open the csv file in read mode.
        with open(csv_file, mode = 'r') as file:
            file = csv.reader(file)

            # Skip the header.
            next(file)

            # Insert the data into the table.
            for line in file:
                self.cursor.execute(query, line)
        
        # Commit to the DB
        self.conn.commit()
        print("\nSuccessfully intaked riders.")


    # FUNCTION: For RIDES | Intake data from a .csv file 'rides' table.
    def intake_rides(self, csv_file):
        # Insert query; 6 values.
        query = '''
            INSERT INTO rides VALUES(%s, %s, %s, %s, %s, %s);
        '''

        # Open the csv file in read mode.
        with open(csv_file, mode = 'r') as file:
            file = csv.reader(file)

            # Skip the header.
            next(file)

            # Insert the data into the table.
            for line in file:
                self.cursor.execute(query, line)
        
        # Commit to the DB
        self.conn.commit()
        print("\nSuccessfully intaked rides.")

    #===============================================#
    #--------------Auxilary Functions---------------#
    #===============================================#

    # FUNCTION: Used for testing/debugging if the tables exist.
    def show_tables(self):
        # Shows all tables currently in the DB.
        self.cursor.execute("SHOW TABLES;")

        # Print results.
        for row in self.cursor:
            print(row)

    #===============================================#
    #---------------Login Functions-----------------#
    #===============================================#

    # FUNCTION: Sets the user_name and user_pass to the users login input. Checks if they exist.
    def existing_account(self, login_type):
        # Get the user input for their username and password.
        self.user_name = input("\nUsername: ")
        self.user_pass = input("Password: ")
        search = (self.user_name, self.user_pass) # Insert into a tuple.

        query = ""

        # Set the query based on the login type. 
        # Login for a Driver.
        if(login_type == "driver"):
            query = '''
                SELECT *
                FROM drivers
                WHERE username = %s AND password = %s;
            '''
        # Login for a Rider.
        elif(login_type == "rider"):
            query = '''
                SELECT *
                FROM riders
                WHERE username = %s AND password = %s;
            '''
        
        # Execute the query.
        self.cursor.execute(query, search)
        results = self.cursor.fetchall()
        # print(results)

        # Checks if the username and password exists.
        if(not results):
            print("Login credentials invalid.\n")
            return False
        else:
            print("Successfully logged in.\n")
            return True


    # FUNCTION: Create either a new Driver or Rider account.
    def create_account(self, login_type):
        # Get the username and password from the user.
        self.user_name = input("\nUsername: ")
        self.user_pass = input("Password: ")
        insert_vals = (self.user_name, self.user_pass) # Insert into a tuple.

        query = ""

        # Create an account for a Driver.
        if(login_type == "driver"):
            query = '''
            INSERT INTO drivers VALUES(NULL, %s, %s, 0);
            '''
        # Create an account for a Rider.
        elif(login_type == "rider"):
            query = '''
            INSERT INTO riders VALUES(NULL, %s, %s);
            '''

        # Execute and commit to the DB.
        self.cursor.execute(query, insert_vals)
        self.conn.commit()
        print("New account created successfully.\n")

    #===============================================#
    #------------Driver Menu Functions--------------#
    #===============================================#

    # FUNCTION: Display the average of all ratings.
    def view_ratings(self):
        # Gets the average of all the ratings for the driver.
        query = '''
        SELECT AVG(driverRating) as AvgRating
        FROM rides
        WHERE driverID = (SELECT driverID
                          FROM drivers
                          WHERE username = %s AND password = %s);
        '''
        
        vals = (self.user_name, self.user_pass) # Used in the select query.

        # Execute the query and store the results.
        self.cursor.execute(query, vals)
        results = self.cursor.fetchall()
        
        # Only prints what's in results if it's not empty (NoneType).
        for row in results:
            if(row[0] is not None):
                print("\nAverage Rating: " + str(row[0]) + "\n")
            else:
                print("\nNo ratings exist for you at the moment.\n")


    # FUNCTION: Displays a list of all rides that the driver has given.
    def view_driver_rides(self):
        # Selects each row that the matches the driver's ID, or rides they have given.
        query = '''
        SELECT rideID, riderID, pickupLoc, dropoffLoc, driverRating
        FROM rides
        WHERE driverID = (SELECT driverID
                          FROM drivers
                          WHERE username = %s AND password = %s);
        '''
        
        vals = (self.user_name, self.user_pass) # Used in the select query.

        # Execute the query and store the results.
        self.cursor.execute(query, vals)
        results = self.cursor.fetchall()

        # Only prints this statement if no records exist.
        if(not results):
            print("\nNo records of rides exist for you.\n")
            return

        # Headers
        headers = ["RideID", "RiderID", "Pickup Location", "Dropoff Location", "Rating"]
        print(f"{headers[0]:<10} {headers[1]:<10} {headers[2]:<30} {headers[3]:<30} {headers[4]:<10}")

        # Separator
        print("-"*100)

        # Prints each row in the results formatted.
        for row in results:
            rideid, riderid, pickup, dropoff, rating = row
            print(f"{rideid:<10} {riderid:<10} {pickup:<30} {dropoff:<30} {rating:<10}")
        print()


    # FUNCTION: Activate or deactivate driver mode.
    def driver_mode(self):
        # 
        query = '''
        SELECT active
        FROM drivers
        WHERE username = %s AND password = %s;
        '''

        vals = (self.user_name, self.user_pass) # Used in the select query

        # Execute the query and store the results.
        self.cursor.execute(query, vals)
        results = self.cursor.fetchall()
        active_val = results[0] # Used to check for which query to execute.

        # Determines whether or not to enable or disable driver mode.
        # Enable driver mode.
        if(active_val[0] == 0):
            # Set driver mode to 1 to indicate it's enabled.
            query = '''
            UPDATE drivers
            set active = 1
            WHERE username = %s AND password = %s;
            '''

            print("\nDriver mode enabled.\n")

        # Disable driver mode. 
        else:
            query = '''
            UPDATE drivers
            set active = 0
            WHERE username = %s AND password = %s;
            '''

            print("\nDriver mode disabled.\n")

        # Execute and commit the query.
        self.cursor.execute(query, vals)
        self.conn.commit()

    #===============================================#
    #-------------Rider Menu Functions--------------#
    #===============================================#

    # FUNCTION: Display a list of rides the riders has received.
    def view_rider_rides(self):
        # Selects every ride that the rider has taken.
        query = '''
        SELECT rideID, driverID, pickupLoc, dropoffLoc, driverRating
        FROM rides
        WHERE riderID = (SELECT riderID
                         FROM riders
                         WHERE username = %s AND password = %s);
        '''

        vals = (self.user_name, self.user_pass) # Used in the query.

        # Execute the query and store the results.
        self.cursor.execute(query, vals)
        results = self.cursor.fetchall()

        # Only prints this statement if no records exist.
        if(not results):
            print("\nYou haven't taken any rides yet.\n")
            return 0

        # Headers
        headers = ["RideID", "DriverID", "Pickup Location", "Dropoff Location", "Rating"]
        print(f"{headers[0]:<10} {headers[1]:<10} {headers[2]:<30} {headers[3]:<30} {headers[4]:<10}")

        # Separator
        print("-"*100)

        # Prints each row in the results formatted.
        for row in results:
            rideid, driverid, pickup, dropoff, rating = row
            print(f"{rideid:<10} {driverid:<10} {pickup:<30} {dropoff:<30} {rating:<10}")
        print()


    # FUNCTION: Finds the first available driver for a rider and asks for the pick up and drop off
    # location. Creates a new ride record given the information.
    def find_driver(self):
        # Select all active drivers.
        query = '''
        SELECT driverID
        FROM drivers
        WHERE active = 1;
        '''
        
        # Execute the query and store the results.
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        # Checks whether or not any drivers are available/active.
        if(not results):
            print("\nNo drivers are active/available at this moment.\n")
            return

        # Store the results in a list, will be displayed later.
        dID_list = []
        for row in results:
            dID_list.append(row[0])

        print("Select a Driver ID to receive a ride from:")
        
        # Display the available drivers.
        for i in range(len(dID_list)):
            print(f"{i+1}. {dID_list[i]}")

        choice = input("\nInput: ") # Get the user input.

        # Only triggers if the input is not an integer, zero, or out of bounds of the artist_list.
        while(not (choice.isnumeric()) or int(choice) == 0 or int(choice) > len(dID_list)):
            print(f"Invalid input. Must be between 1 and {len(dID_list)}")
            
            choice = input("Input: ")

        dID = results[int(choice)-1] # Store the select driver's ID.
        
        # Get the pick up and drop off location.
        print("\nInput your pick up and drop off location-->")
        pickup = input("Pick Up Location: ")
        dropoff = input("Drop Off Location: ")

        # Get the riderID given their username and password.
        query = '''
        SELECT riderID
        FROM riders
        WHERE username = %s AND password = %s;
        '''
        rider_vals = (self.user_name, self.user_pass) # Used for the riderID search query.

        # Execute query and store the results.
        self.cursor.execute(query, rider_vals)
        results = self.cursor.fetchall()
        rID = results[0] # Store the rider's ID.

        insertion_vals = (dID[0], rID[0], pickup, dropoff) # Used in the insertion query below.

        # Insertion query into the 'rides' table.
        query = '''
        INSERT INTO rides VALUES(NULL, %s, %s, %s, %s, 0);
        '''

        # Execute and commit the query.
        self.cursor.execute(query, insertion_vals)
        self.conn.commit()
        print()


    # FUNCTION: Provides a list of all rides the rider has taken and asks them to rate a ride.
    def rate_driver(self):
        # Display the rider's rides. Returns if they haven't taken any rides yet.
        if(self.view_rider_rides() == 0):
            return

        print("Note: Any rides with a rating of zero are rides that have not been rated yet.")

        # Selects all the rideIDs of the rider.
        query = '''
        SELECT rideID
        FROM rides
        WHERE riderID = (SELECT riderID
                         FROM riders
                         WHERE username = %s AND password = %s);
        '''

        vals = (self.user_name, self.user_pass) # Used in the placeholders for the query.

        # Execute the query and store the results.
        self.cursor.execute(query, vals)
        results = self.cursor.fetchall()

        # Store the results in a list, will be displayed later.
        ridesID_list = []
        for row in results:
            ridesID_list.append(row[0])

        print("\nSelect a ride ID to rate:")
        
        # Display the taken rides.
        for i in range(len(ridesID_list)):
            print(f"{i+1}. {ridesID_list[i]}")

        choice = input("\nInput: ") # Get the user input.

        # Only triggers if the input is not an integer, zero, or out of bounds of the artist_list.
        while(not (choice.isnumeric()) or int(choice) == 0 or int(choice) > len(ridesID_list)):
            print(f"Invalid input. Must be between 1 and {len(ridesID_list)}")
            
            choice = input("Input: ")

        rID = ridesID_list[int(choice) - 1] # Store the selected ride's ID.

        # Get the user input for a rating.
        choice = input("Give a rating between 1-5 for this ride: ")

        # Only enters the loop if the input is non-numeric and not between 1 and 5.
        while(not (choice.isnumeric()) or int(choice) < 1 or int(choice) > 5):
            print("Invalid input. Must be a non-negative integer value between 1 and 5.")
            choice = input("Give a rating between 1-5 for this ride: ")

        rating = int(choice) # Store the input rating.

        # Update the rideID to be the new rating.
        query = '''
        UPDATE rides
        set driverRating = %s
        WHERE rideID = %s;
        '''
        q_vals = (rating, rID) # Used in the query.

        # Execute and commit the query.
        self.cursor.execute(query, q_vals)
        self.conn.commit()
        print("\nSuccessfully updated the driver's rating.\n")
