# Imports
from operations import operations

# Global variable.
db_ops = operations("rideshare")

# Starts the database by creating the tables and intaking data.
def start():
    print("Welcome to Rideshare! Prototype Edition!\n")
    
    # Create the database tables. -> Run only if the tables don't exist or this has already been run.
    # db_ops.create_tables()            
    # db_ops.show_tables()

    # Intake data from csv files. -> Run only if the data hasn't been intaked yet.
    # db_ops.intake_drivers("drivers.csv")
    # db_ops.intake_riders("riders.csv")
    # db_ops.intake_rides("rides.csv")


# Beginning login menu for the user.
def login_menu():
    while(True):
        # Present login options to the user.
        print('''\tLogin to Rideshare:
                1. Existing Rider
                2. Existing Driver
                3. Create new Rider Account
                4. Create new Driver Account
                5. Quit''')
        
        user_choice = input("\tInput: ")

        # Perform the operation given the user input.
        match user_choice:
            # Login as an existing Rider. Presents the Rider menu if successful.
            case "1":
                if(db_ops.existing_account("rider")):
                    rider_menu()
                    break

            # Login as an existing Driver. Presents the Driver menu if successful.
            case "2":
                if(db_ops.existing_account("driver")):
                    driver_menu()
                    break

            # Create a new Rider account. Presents the Rider menu afterwards.
            case "3":
                db_ops.create_account("rider")
                rider_menu()
                break

            # Create a new Driver account. Presents the Driver menu afterwards.
            case "4":
                db_ops.create_account("driver")
                driver_menu()
                break

            # Quit the application.
            case "5":
                break

            # Checks for invalid input.
            case _:
                print("\tInvalid input. Must be a number 1-5.")
    
    print("Goodbye!")


# The menu that appears upon a Driver login.
def driver_menu():
    while(True):
        # Present login options to user.
        print('''\tDriver Account Menu:
            1. View Rating
            2. View Rides
            3. Activate/Deactivate Driver Mode
            4. Quit
        ''')

        choice = input("\tInput: ")

        # Perform the proper action given the user's choice.
        match choice:
            # Shows the average rating of all the rides the driver has given.
            case "1":
                db_ops.view_ratings()
            
            # Shows all the rides that the driver has given.
            case "2":
                db_ops.view_driver_rides()
            
            # Enables or Disables driver mode for the driver.
            case "3":
                db_ops.driver_mode()
            
            # Quits the menu.
            case "4":
                break
            
            # Checks for invalid input.
            case _:
                print("\tInvalid input. Must be a number 1-4.")


# The menu that appears for the Rider login.
def rider_menu():
    while(True):
        # Present login options to user.
        print('''\tRider Account Menu:
            1. View Rides
            2. Find a Driver
            3. Rate my Driver
            4. Quit
        ''')

        choice = input("\tInput: ")

        # Perform the proper action given the user's choice.
        match choice:
            # Shows all rides the rider has taken.
            case "1":
                db_ops.view_rider_rides()
            
            # Finds an driver for the rider.
            case "2":
                db_ops.find_driver()
            
            # Rates one of the rides given.
            case "3":
                db_ops.rate_driver()
            
            # Quits the menu.
            case "4":
                break
            
            # Checks for invalid input.
            case _:
                print("\tInvalid input. Must be a number 1-4.")


# Main method.
def main():
    start()
    login_menu()

    # Close connections.
    db_ops.close_connections()

if __name__ == "__main__":
    main()
