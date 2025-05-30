import os
from textwrap import dedent
import pymysql
from dotenv import load_dotenv

load_dotenv()  # Læs .env

host     = os.getenv('DB_HOST')
port     = int(os.getenv('DB_PORT', 3306))
user     = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
dbname   = os.getenv('DB_NAME')


def connect_to_database():
    """
    Connects to the configured database. If the database does not exist,
    creates it and then reconnects.
    Returns:
        A pymysql Connection object connected to the target database.
    """
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
            raise

        print(f"Database `{dbname}` findes ikke – opretter den nu…")

    # 2) Connect uden db for at oprette databasen
    tmp_conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        charset='utf8mb4',
        connect_timeout=10
    )
    try:
        with tmp_conn.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{dbname}` "
                "CHARACTER SET utf8mb4 "
                "COLLATE utf8mb4_unicode_ci;"
            )
        tmp_conn.commit()
        print(f"Database `{dbname}` oprettet.")
    finally:
        tmp_conn.close()

    # 3) Connect igen – nu til den nyskabte database
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        db=dbname,
        charset='utf8mb4',
        connect_timeout=10
    )
    print(f"Forbundet til database `{dbname}` efter oprettelse.")
    return conn

def create_database():
    conn = connect_to_database()

    try:
        with conn.cursor() as cursor:
            print(f"Opretter database `{dbname}` hvis den ikke findes…")
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{dbname}` "
                "CHARACTER SET utf8mb4 "
                "COLLATE utf8mb4_unicode_ci;"
            )
        conn.commit()
        print("Database oprettet eller eksisterer allerede.")
    except pymysql.MySQLError as e:
        print("Fejl under oprettelse af database:", e)
    finally:
        conn.close()
        print("Forbindelse til MySQL lukket.")


def create_tables():
    """
    Opretter alle nødvendige tabeller i skribenten-databasen.
    Forudsætter at connect_to_database() returnerer en åben pymysql-tilkobling.
    """
    conn = connect_to_database() 

    table_ddls = {
        #🔵USERS
        "users": """
            CREATE TABLE IF NOT EXISTS `users` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `name` VARCHAR(100) NOT NULL,
                `username` VARCHAR(50) NOT NULL UNIQUE,
                `password` VARCHAR(255) NOT NULL,
                `role` ENUM('viewer','editor','admin') NOT NULL DEFAULT 'viewer',
                `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        #🔵SITES
        "sites": """
            CREATE TABLE IF NOT EXISTS `sites` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `name` VARCHAR(100) NOT NULL,
                `logo_url` VARCHAR(255),
                `description` TEXT,
                `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        #🔵USER_SITES
        "user_sites": """
            CREATE TABLE IF NOT EXISTS `user_sites` (
                `user_id` INT NOT NULL,
                `site_id` INT NOT NULL,
                PRIMARY KEY (`user_id`, `site_id`),
                FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
                FOREIGN KEY (`site_id`) REFERENCES `sites` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        #🔵CATEGORIES
        "categories": """
            CREATE TABLE IF NOT EXISTS `categories` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `name` VARCHAR(50) NOT NULL UNIQUE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        #🔵TAGS
        "tags": """
            CREATE TABLE IF NOT EXISTS `tags` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `name` VARCHAR(50) NOT NULL UNIQUE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        #🔵ARTICLES
        "articles": """
            CREATE TABLE IF NOT EXISTS `articles` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `site_id` INT NOT NULL,
                `title` VARCHAR(255) NOT NULL,
                `teaser` TEXT NOT NULL,
                `content` TEXT NOT NULL,
                `img` VARCHAR(255) NOT NULL,
                `status` ENUM('scheduled','published','archived') NOT NULL DEFAULT 'scheduled',
                `scheduled_publish_at` DATETIME NULL,
                `published_at` DATETIME NULL,
                `url` VARCHAR(255) NULL,
                `category_id` INT NOT NULL,
                `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (`site_id`) REFERENCES `sites` (`id`) ON DELETE CASCADE,
                FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE RESTRICT
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        #🔵ARTICLE_TAGS
        "article_tags": """
            CREATE TABLE IF NOT EXISTS `article_tags` (
                `article_id` INT NOT NULL,
                `tag_id` INT NOT NULL,
                PRIMARY KEY (`article_id`, `tag_id`),
                FOREIGN KEY (`article_id`) REFERENCES `articles` (`id`) ON DELETE CASCADE,
                FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        #🔵SITE_CATEGORIES
        "site_categories": """
            CREATE TABLE IF NOT EXISTS `site_categories` (
                `site_id` INT NOT NULL,
                `category_id` INT NOT NULL,
                PRIMARY KEY (`site_id`, `category_id`),
                FOREIGN KEY (`site_id`) REFERENCES `sites` (`id`) ON DELETE CASCADE,
                FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        #🔵SITE_TAGS
        "site_tags": """
            CREATE TABLE IF NOT EXISTS `site_tags` (
                `site_id` INT NOT NULL,
                `tag_id` INT NOT NULL,
                PRIMARY KEY (`site_id`, `tag_id`),
                FOREIGN KEY (`site_id`) REFERENCES `sites` (`id`) ON DELETE CASCADE,
                FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        #🔵PROMPTS
        "prompts": """
            CREATE TABLE IF NOT EXISTS `prompts` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `name` VARCHAR(100) NOT NULL,
                `description` TEXT NOT NULL,
                `user_id` INT NOT NULL,
                `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """,
        #🔵PROMPT_INSTRUCTIONS
        "prompt_instructions": """
            CREATE TABLE IF NOT EXISTS `prompt_instructions` (
                `id` INT AUTO_INCREMENT PRIMARY KEY,
                `prompt_id` INT NOT NULL,
                `instruction` TEXT NOT NULL,
                `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (`prompt_id`) REFERENCES `prompts` (`id`) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
    }

    try:
        for name, ddl in table_ddls.items():
            print(f"Opretter {name} tabellen…")
            with conn.cursor() as cursor:
                cursor.execute(dedent(ddl))
            conn.commit()
            print(f"{name} tabellen oprettet eller eksisterer allerede.")
    except pymysql.MySQLError as e:
        print("Fejl under oprettelse af tabeller:", e)
    finally:
        conn.close()
        print("Forbindelse til MySQL lukket.")


def delete_all_tables():
    """
    Sletter alle tabeller i databasen.
    """
    conn = connect_to_database()

    try:
        with conn.cursor() as cursor:
            # Fetch all table names in the current database
            cursor.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = %s",
                (dbname,)
            )
            tables = [row[0] for row in cursor.fetchall()]
            if not tables:
                print("Ingen tabeller at droppe.")
                return
            
            # Construct and execute DROP TABLE statement
            table_list = ", ".join(f"`{t}`" for t in tables)
            cursor.execute(f"DROP TABLE IF EXISTS {table_list};")
            conn.commit()
            print(f"Dropper tabeller: {table_list}")
    except pymysql.MySQLError as e:
        print("Fejl under sletning af tabeller:", e)
    finally:
        conn.close()
        print("Forbindelse til MySQL lukket.")
    

if __name__ == "__main__":
    create_database()
    create_tables()