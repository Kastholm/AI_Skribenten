import datetime
import json
import os
import re
import pymysql
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

from artificial_intelligence.gpt_4o import gpt4o
from service.database.connect import connect_to_database

load_dotenv()  # Læs .env
wp_name = 'root'
wp_pass = os.getenv('WP_AUTH')
curr_site = 'opdateret.dk'

gpt4o_instance = gpt4o()

def article_publish_service(article_id: int, status: str, published_at: datetime):
    conn = connect_to_database()
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE articles SET status = %s, published_at = %s WHERE id = %s", (status, published_at, article_id))
            conn.commit()
    except pymysql.MySQLError as e:
        return {"error": "Fejl under opdatering af artikelstatus", "detail": str(e)}
    finally:
        conn.close()


def extract_json_from_text(text):
    match = re.search(r'\{.*\}', text, flags=re.DOTALL)
    if match:
        return json.loads(match.group(0))
    return None

def get_and_set_category(article):
    url_categories = f"https://{curr_site}/wp-json/wp/v2/categories"
    response_categories = requests.get(url_categories, auth=HTTPBasicAuth(wp_name, wp_pass))

    ai_response = gpt4o_instance.send_prompt(element="Text", model="gpt-4o-mini", prompt = f"""
    Her har du alt data fra en artikel, det site du skal skrive på, samt yderligere informationer {article}.
    Du kan se alle kategorier her: {response_categories.json()}.
    Returner kategoriens id som du mener passer til artiklen.
    Hvis der ikke er nogen kategorier som du mener passer til artiklen.
    Return nedenstående JSON struktur med kategoriens navn.
    {{
      "name": "Ny kategori navn"
    }}
    Ellers returner kun kategoriens id og intet andet.
    """)


    ai_response = extract_json_from_text(ai_response)
    if ai_response is str:
        response = requests.post(url_categories, json=ai_response, auth=HTTPBasicAuth(wp_name, wp_pass))
    
    print(ai_response)

    return ai_response



   # print(article)
   # print(article.title)
    # Vælg kategori
    # Vælg tag
    # Vælg journalist
    # WP url MANGLER fra frontend
    #Endpoint = WP_URL/wp-json/wp/v2/posts

    #category = get_and_set_category(article)

def write_article_content(article):

    data = gpt4o_instance.send_prompt(element="Text", model="gpt-4o", prompt = f"""
    Her har du alt data fra en artikel, det site du skal skrive på, samt yderligere informationer {article}.
    
    Skriv en professionel, fængende artikel til publicering på en WordPress-hjemmeside. 
    Artiklen skal have en mild clickbait-agtig titel, 
    der vækker nysgerrighed uden at være misvisende. 
    Skriv i en let læselig og journalistisk stil, som en erfaren journalist.
    Strukturer teksten korrekt med HTML-tags: som for eksempel <h2>, <h3> <p>.
    Sørg for at underoverskrifter i <h2> og eventuelle underafsnit i <h3>.
    Artiklens indhold skal være informativt, relevant og engagerende for læseren.
    Returner din artikel i dette JSON format. Retuner kun denne JSON struktur, ikke andet tekst eller lignende.
    {{
        "title": "Skriv titlen her",
        "content": "Skriv content her",
        "status": "draft"
    }}
    """
    )

    url = f"https://{curr_site}/wp-json/wp/v2/posts"

    data = extract_json_from_text(data)

    print(data)

    response = requests.post(url, json=data, auth=HTTPBasicAuth(wp_name, wp_pass))
    if response.status_code == 201:
        article_publish_service(article.id, "published", published_at = datetime.datetime.now())
        return {"message": "Artikel oprettet", "status_code": response.status_code, "article_id": response.json()["id"]}
    else:
        return {"message": "Fejl under oprettelse af artikel", "status_code": response.status_code, "article_id": None}


    # Step 1 = Skriv artikel og udgiv til CMS
    # Sted 2 = If success, skift artikel status til published