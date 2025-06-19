from io import BytesIO
import json
import re
from bs4 import BeautifulSoup
import requests
from PIL import Image
from artificial_intelligence.gpt_4o import gpt4o

gpt4o = gpt4o()


def extract_json_from_text(text):
    match = re.search(r'\{.*\}', text, flags=re.DOTALL)
    if match:
        return json.loads(match.group(0))
    return None


def validate_article_content(url, instructions):

    image = ''

    response = requests.get(url)
    #Remove class and ids
    clean_response = re.sub(r'(class|id)="[^"]*"', '', response.text)
    soup = BeautifulSoup(clean_response, 'html.parser')
    #Remove SVG
    for svg in soup.find_all('svg'):
        svg.decompose()
        
    try:
        if soup.find('article'):
            html_content = soup.find('article')
        elif soup.find('body'):
            html_content = soup.find('body')
        else:
            raise Exception('No article or body found')
        
        if soup.find('body').find('img'):
            all_images = soup.find('body').find_all('img')
            for img in all_images:
                try:
                    img_url = img['src']
                    img_response = requests.get(img_url, timeout=5)
                    img_file = Image.open(BytesIO(img_response.content))
                    width, height = img_file.size
                    if width > 700 and height > 300:
                        image = img_url
                        break
                except:
                    continue
                image = html_content.find('img')['src']

        clean_article = re.sub(r'src="[^"]*"', '', html_content.text)
        #Strip for mellemrum
        article_content = re.sub(r'\s+', ' ', clean_article).strip()

        ai_content = gpt4o.send_prompt(element="Text",prompt = f"""
        Dette content er kopiret fra en artikel. Se derfor bort fra 'Læs mere' bokse, sociale medie delinger, kommentarer og andet indhold, der ikke er en del af artiklen.
        Skriv på dansk hvad denne artikel handler om. Teksten du skriver skal senere bruges til at generere en artikel.
        Vær grundig med at beskrive alt hvad artiklen handler om og dens vigtigste punkter, således at det er let at generere en fangende artikel ud fra det.
        Læs mediets beskrivelse hvor artiklen skal udgives {instructions}.
        
        Ud fra artikel content og mediets beskrivelse skal du generere en prompt til en proffesionel
        journalist som skal skrive en spændende, fangende og dybdegående artikel.
        Indsæt denne url til i image_url feltet {image}.
        VIGTIGT: Udskriv i dette JSON format:
        {{
            "title": "Titel på artiklen",
            "teaser": "En kort beskrivelse af artiklen",
            "content": "Indholdet i artiklen",
            "prompt": "Fokus punkter og prompt til AI journalisten",
            "image_url": "url til licensfrit billede
        }}
        {article_content}
        """)

        #Ekstra prompt evt til at søge internettet og tilføje til artikel beskrivelse

        ai_content = extract_json_from_text(ai_content)
        #print(ai_content)
        title = ai_content['title']
        clean_article = ai_content['content']
        teaser = ai_content['teaser']
        prompt = ai_content['prompt']
        image_url = ai_content['image_url']


        valid_article = True

    except AttributeError:
        print('No article in this url')
        valid_article = False

 
    return title, image_url, clean_article, teaser, prompt, valid_article








        # IMage logic for later
        #web_image = gpt4o.send_prompt(model="gpt-4o-mini-search-preview", element="Web", prompt = f"""
        #Søg online og find et licensfrit billede som passer til denne artikel.
        #Billedet skal som minimum være 1024x600 pixels.
        #URL skal enten ende på .png .jpg .jpeg .svg, søg efter billeder indtil dette er gyldigt.
        #Tag URL ud af HTML koden fra den side du tilgår.
        #Titel: {title}
        #Teaser: {teaser}
        #Content: {clean_article}
        #Returner nu kun 1 plain URL tilbage. Intet tekst eller andet udover en ren URL.                
        #""")
        #print(web_image)
        #image = web_image
        
        #""" try:
        #    image = unsplash_collect_image(ai_content['image'])
        #except Exception as e:
        #    print(e) """


""" def unsplash_collect_image(search_word):

    search_word.replace(' ','-')
    print(search_word)
    url = f"https://unsplash.com/s/photos/{search_word}?license=free"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    image_container = soup.find("div", attrs={"data-testid": "search-photos-route"})

    #find 1 figure in image_container
    figure = image_container.find('figure')
    print(figure)
    #Direct to the href
    href = figure.find('a')['href']
    print(href)
    image_url = requests.get(f'https://unsplash.com/photos/{href}')

    soup = BeautifulSoup(image_url.text, 'html.parser')
    print(soup)
    #Copy img src
    image = soup.find('img')['src']

    return image """