import psycopg2
import config


try:
    connection = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password
    )
    cursor = connection.cursor()
    
    print("Succesfully connected to database")
    
except psycopg2.Error as e:
    print("Error connecting database")

finally:
    if connection:
        connection.close()
