import psycopg2

#
# DB(PostgreSQL) Connection
#
import sys

class Connection:
    def __init__(self):
        self.conn = self.connect()


    
    def connect(self):
        """
        Connect to database and return connection
        """

        print("Connecting to PostgreSQL Database...")

        try:
            conn = psycopg2.connect(host="10.0.1.47", port=5432, dbname="test", user="postgres", password="hansol2014")
            
        except psycopg2.OperationalError as e:
            print("Failed to connect to Database: ", e)
        
        print("Database connection successful !")

        return conn

    
