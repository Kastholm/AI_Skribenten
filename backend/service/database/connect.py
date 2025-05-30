import os
import pymysql
from dotenv import load_dotenv

load_dotenv()  # Læs .env

host     = os.getenv('DB_HOST')
port     = int(os.getenv('DB_PORT', 3306))
user     = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
dbname   = os.getenv('DB_NAME')


def connect_to_database():
    # 1) Forsøg at forbinde direkte til databasen
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=dbname,
            charset='utf8mb4',
            connect_timeout=10
        )
        print(f"Forbundet til database `{dbname}`.")

        return conn
    
    except pymysql.err.OperationalError as e:
        # Kode 1049 = Ukendt database
        if e.args[0] != 1049:
            print("Fejl ved forbindelse:", e)
            return None

        print(f"Database `{dbname}` findes ikke ")
        raise