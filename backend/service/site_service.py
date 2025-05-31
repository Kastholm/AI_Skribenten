import os
import pymysql
import base64
from service.database.connect import connect_to_database

from dotenv import load_dotenv

load_dotenv()  # Læs .env

host     = os.getenv('DB_HOST')
port     = int(os.getenv('DB_PORT', 3306))
user     = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
dbname   = os.getenv('DB_NAME')


def admin_get_all_sites() -> dict:
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

def create_site(name: str, logo_base64: str, description: str, page_url: str):
    #TODO Sørg for at user er admin
    try:
        logo_bytes = base64.b64decode(logo_base64)
    except Exception as e:
        return {"message": "Ugyldig Base64 for logo", "error": str(e)}
    
    conn = connect_to_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO sites (name, logo, description, page_url) VALUES (%s, %s, %s, %s)", (name, logo_bytes, description, page_url))
            conn.commit()
            return {"message": "Site created successfully", "site": {"name": name, "description": description, "page_url": page_url}}
    except pymysql.MySQLError as e:
        print("Fejl under oprettelse af site:", e)
    finally:
        conn.close()

def admin_link_site_service(user_id: int, site_id: int, role: str):
    conn = connect_to_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO user_sites (user_id, site_id, role) VALUES (%s, %s, %s)", (user_id, site_id, role))
            conn.commit()
            return {"message": "Site linked successfully"}
    except pymysql.MySQLError as e:
        print("Fejl under linkning af site:", e)
    finally:
        conn.close()