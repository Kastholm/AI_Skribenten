import os
import pymysql

from service.article_service.write_article import write_article_content
from service.site_service import get_site_by_id_service
from service.article_service.validate_article import validate_article_content
from service.database.connect import connect_to_database

from dotenv import load_dotenv

load_dotenv()  # Læs .env

host     = os.getenv('DB_HOST')
port     = int(os.getenv('DB_PORT', 3306))
user     = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
dbname   = os.getenv('DB_NAME')

wp_name = 'root'
wp_pass = os.getenv('WP_AUTH')
curr_site = 'opdateret.dk'

#CP url
#Klik create knap og validerings process startes.
#indsætter alt dataen.

def write_article_service(article):
    #print(article)
    #print(article.title)
    # Vælg kategori
    # Vælg tag
    # Vælg journalist
    # WP url MANGLER fra frontend
    #Endpoint = WP_URL/wp-json/wp/v2/posts

    write_article_content(article)
    
    # Step 1 = Skriv artikel og udgiv til CMS
    # Sted 2 = If success, skift artikel status til published

def validate_article_service(url, site_id, user_id):

    #Validation skal sende kun url. Resten skal være tomme strings, så den går igennem.
    status = 'validating'
    response = 'success'
    category_id = 2

    # Get site information including description
    site = get_site_by_id_service(site_id)
    instructions = site[2]
    if not site:
        return {"error": "Site not found"}

    # Get data from ChatGPT
    title, image, content, teaser, prompt_instruction, valid_article = validate_article_content(url, instructions)
    if not valid_article:
        return {"error": "Ingen <article> fundet i den angivne URL"}


    conn = connect_to_database()

    try:
        with conn.cursor() as cursor:
            print("DEBUG: før cursor.execute")
            cursor.execute(
                "INSERT INTO articles (site_id, title, teaser, content, img, status, response, url, prompt_instruction, instructions, user_id, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (site_id, title, teaser, content, image, status, response, url, prompt_instruction, instructions, user_id, category_id)
            )
            print("DEBUG: SQL-statement blev eksekveret")
            conn.commit()
            print("DEBUG: efter commit")
            return {
                "title": title, 
                "content": content, 
                "image": image, 
                "url": url, 
                "instructions": instructions,
            }
    except pymysql.MySQLError as e:
        print("DEBUG: SQL Error:", str(e))
        return {"error": "Fejl under oprettelse af artikel", "detail": str(e)}
    finally:
        conn.close()





    #Teaser? (Men så skal GPT generere en)
    #Titel
    #URL (ikke skift)
    #Content
    #Prompt 
    #scheduled_publish_at
    #Category_id
    #User_id
    #image


def get_article_service(id):
    conn = connect_to_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM articles WHERE id = %s", (id,))
            article = cursor.fetchone()
            return article
    except pymysql.MySQLError as e:
        return {"error": "Fejl under hentning af artikel", "detail": str(e)}
    finally:
        conn.close()

def update_article_service(article):
    # Tjek om alle nødvendige felter er udfyldt
    schedule = all([
        bool(article.title), bool(article.url), bool(article.content),
        bool(article.prompt_instruction), bool(article.scheduled_publish_at),
        bool(article.category_id), bool(article.user_id), bool(article.img),
        bool(article.teaser)
    ])
    status = 'scheduled' if schedule else 'validating'

    conn = connect_to_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE articles SET title=%s, content=%s, img=%s, url=%s, "
                "prompt_instruction=%s, user_id=%s, category_id=%s, "
                "scheduled_publish_at=%s, status=%s, teaser=%s WHERE id=%s",
                (
                    article.title, article.content, article.img, article.url,
                    article.prompt_instruction, article.user_id, article.category_id,
                    article.scheduled_publish_at, status, article.teaser, article.id,
                )
            )
            conn.commit()
    except pymysql.MySQLError as e:
        return {"error": "Fejl under opdatering af artikel", "detail": str(e)}
    finally:
        conn.close()


def delete_article_service(id):
    conn = connect_to_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM articles WHERE id = %s", (id,))
            conn.commit()
    except pymysql.MySQLError as e:
        return {"error": "Fejl under sletning af artikel", "detail": str(e)}
    finally:
        conn.close()

    '''
    opret conn til db og tilføj til db
    ud fra hvilket felter der er tilgængelige fra bs4 kan vi vælge hvilken
    status artiklen kan have mm. og derved hvor og hvordan den vises på frontend.
    '''


#Hvorfor ikke bare hente alle artikler fra db i en lang liste?
#Kun opdelt i scheduled og ikke scheduled?

def get_scheduled_articles_service(site_id: int): #Get scheduled articles for all times
    conn = connect_to_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM articles WHERE site_id = %s AND scheduled_publish_at IS NOT NULL", (site_id,))
            articles = cursor.fetchall()
            return articles
    except pymysql.MySQLError as e:
        return {"error": "Fejl under hentning af scheduled artikler", "detail": str(e)}
    finally:
        conn.close()

def get_unvalidated_articles_service(site_id: int):
    conn = connect_to_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM articles WHERE site_id = %s AND status = 'validating'", (site_id,))
            articles = cursor.fetchall()
            return articles
    except pymysql.MySQLError as e:
        return {"error": "Fejl under hentning af ikke validerede artikler", "detail": str(e)}
    finally:
        conn.close()
