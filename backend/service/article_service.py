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

#CP url
#Klik create knap og validerings process startes.
#indsætter alt dataen.

def validate_article_service(url):

    #Validation skal sende kun url. Resten skal være tomme strings, så den går igennem.
    site_id = 2
    title = 'test'
    teaser = 'test'
    content = 'test'
    img = 'test'
    prompt_instruction = 'test'
    user_id = 2
    category_id = 2
    url = url

    print(url, 'test')

    '''
    opret conn til db og tilføj til db
    ud fra hvilket felter der er tilgængelige fra bs4 kan vi vælge hvilken
    status artiklen kan have mm. og derved hvor og hvordan den vises på frontend.
    '''




    #Ud fra hvilken data der er til stede kan vi vælge status, respons. mm.
    #conn = connect_to_database()
    #try:
    #    with conn.cursor() as cursor:
    #        cursor.execute(
    #            "INSERT INTO articles (site_id, title, teaser, content, img, status, scheduled_publish_at, published_at, url, prompt_instruction, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    #            (article.site_id, article.title, article.teaser, article.content, article.img, article.status, article.scheduled_publish_at, article.published_at, article.url, article.prompt_instruction, article.category_id)
    #        )
    #        conn.commit()
    #        return title, teaser, content, img, url
    #except pymysql.MySQLError as e:
    #    return {"error": "Fejl under oprettelse af artikel", "detail": str(e)}
    #finally:
    #    conn.close()


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
            cursor.execute("SELECT * FROM articles WHERE site_id = %s AND status = 'unvalidated'", (site_id,))
            articles = cursor.fetchall()
            return articles
    except pymysql.MySQLError as e:
        return {"error": "Fejl under hentning af ikke validerede artikler", "detail": str(e)}
    finally:
        conn.close()
