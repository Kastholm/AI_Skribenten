import os
import pymysql

from service.database.connect import connect_to_database

from dotenv import load_dotenv

load_dotenv()  # Læs .env

host     = os.getenv('DB_HOST')
port     = int(os.getenv('DB_PORT', 3306))
user     = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
dbname   = os.getenv('DB_NAME')


def get_categories_service(site_id: int):
    conn = connect_to_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM categories WHERE site_id = %s", (site_id,))
            categories = cursor.fetchall()
            return categories
    except pymysql.MySQLError as e:
        print("Fejl under hentning af kategorier:", e)
    finally:
        conn.close()