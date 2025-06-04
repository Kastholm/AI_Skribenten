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


def create_prompt(name: str, description: str, user_id: int):
    conn = connect_to_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO prompts (name, description, user_id) VALUES (%s, %s, %s)",
                (name, description, user_id)
            )
            conn.commit()
            return {
                "message": "Prompt created successfully",
                "prompt": {"name": name, "description": description, "user_id": user_id}
            }
    except pymysql.MySQLError as e:
        return {"error": "Fejl under oprettelse af prompt", "detail": str(e)}
    finally:
        conn.close()

def get_all_prompts(user_id: int):
    conn = connect_to_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM prompts WHERE user_id = %s", (user_id,))
            prompts = cursor.fetchall()
            return {"prompts": prompts}
    except pymysql.MySQLError as e:
        print("Fejl under hentning af prompts:", e)
    finally:
        conn.close()
