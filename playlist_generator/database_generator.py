import os
import psycopg2
import config
import logging


def get_artist_and_title(file_name):
    try:
        data = file_name.split(" - ", 1)
        return data[0], data[1].rstrip(".mp3")
    except IndexError:
        return None, None


def insert_data_into_db(connection, cursor, artist, title, file_path):
    try:
        sql_query = f"INSERT INTO all_rock_table (main_artist, song_title, file_path) VALUES (%s, %s, %s);"
        cursor.execute(sql_query, (artist, title, file_path))
        connection.commit()
    except psycopg2.Error as err:
        print("PostgreSQL Error:", err)
    except Exception as e:
        print("An error occurred:", e)


def extract_info_from_files(main_folder, connection, cursor):
    for root, _, all_files in os.walk(main_folder):
        for file_name in all_files:
            artist, title = get_artist_and_title(file_name)
            if artist and title:
                file_path = os.path.join(root, file_name).replace(main_folder, "")
                insert_data_into_db(connection, cursor, artist, title, file_path)


try:
    connection = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password
    )
    cursor = connection.cursor()
    
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('psycopg2').setLevel(logging.DEBUG)
    
    root_path = "C:/Dessy/Music"
    files_dir = os.path.join(root_path, 'Rock')

    extract_info_from_files(files_dir, connection, cursor)
    print("Data inserted successfully!")
    
except psycopg2.Error as e:
    print("Error connecting database")

finally:
    if connection:
        connection.close()
