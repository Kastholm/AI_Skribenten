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

def create_user(name: str, username: str, password: str) -> dict:

    conn = connect_to_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
                (name, username, password)
            )
            conn.commit()
            return {"id": cursor.lastrowid, "name": name, "username": username}
    
    except pymysql.MySQLError as e:
        print("Fejl under oprettelse af user:", e)
    
    finally:
        conn.close()


def login_user(username: str, password: str) -> dict:
    print(f"Attempting login for user: {username}")
    conn = connect_to_database()
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            print(f"Executing query: {query} with params: ({username}, ****)")
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            if not user:
                print("No user found with provided credentials")
                return {"success": False, "error": "Invalid username or password"}
            
            print(f"User found: {user}")
            return {
                "success": True,
                "user": {
                    "id": user[0],
                    "name": user[1],
                    "username": user[2],
                    "role": user[4]
                }
            }
    except pymysql.MySQLError as e:
        print(f"Database error during login: {e}")
        return {"success": False, "error": f"Database error occurred: {str(e)}"}
    finally:
        conn.close()

def get_user_sites_service(user_id: int) -> dict:
    conn = connect_to_database()
    try:
        with conn.cursor() as cursor:
            # Hent alle sites, som brugeren er tilknyttet
            cursor.execute("""
                SELECT s.id, s.name, s.description, s.page_url
                  FROM sites s
                  JOIN user_sites us ON s.id = us.site_id
                 WHERE us.user_id = %s
            """, (user_id,))
            sites = cursor.fetchall()
            return {"sites": sites}
    except pymysql.MySQLError as e:
        print("Fejl under hentning af sites for user_id:", e)
        return {"error": str(e)}
    finally:
        conn.close()