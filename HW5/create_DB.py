'''
ABOUT: Run this file ONLY once if the database has not been created yet.
       Primarily used for quick setup and testing.
'''

# Import Library
import mysql.connector

# Establish Connection
conn = mysql.connector.connect(host = "localhost", # Always stays the same.
                               user = "root",      # Always stays the same.
                               password = "dolphinmuncha69$",
                               auth_plugin = "mysql_native_password")

# Cursor Object
cur_obj = conn.cursor()

# Create the Schema/DB.
# cur_obj.execute("CREATE DATABASE rideshare;") # Run this ONLY if it doesn't exist.

# Confirm the execution worked.
cur_obj.execute("SHOW DATABASES;")

# Print each database; confirm it exists.
for row in cur_obj:
    print(row)

# Print out the connection.
print(conn)
conn.close()
