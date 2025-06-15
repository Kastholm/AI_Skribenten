import os
import pymysql

from service.database.connect import connect_to_database

from dotenv import load_dotenv

load_dotenv()

host     = os.getenv('DB_HOST')
port     = int(os.getenv('DB_PORT', 3306))
user     = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
dbname   = os.getenv('DB_NAME')


def admin_get_all_users(role: str) -> dict:
    if role == "admin":
        conn = connect_to_database()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users")
                users = cursor.fetchall()
                return {"users": users}
        except pymysql.MySQLError as e:
            print(f"Database error during login: {e}")
            return {"success": False, "error": f"Database error occurred: {str(e)}"}
        finally:
            conn.close()
    else:
        return {"success": False, "error": "Du har ikke tilladelse til at se alle brugere"}

def admin_get_all_sites(role: str) -> dict:
    if role == "admin":
        conn = connect_to_database()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, name, description, page_url FROM sites")
                sites = cursor.fetchall()
                return {"sites": sites}
        except pymysql.MySQLError as e:
            print("Fejl under hentning af sites:", e)
        finally:
            conn.close()
    else:
        return {"success": False, "error": "Du har ikke tilladelse til at se alle sites"}