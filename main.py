import os
import bs4
from dotenv import load_dotenv
import feedparser
from openai import OpenAI
import requests
from medier import victoria_data

class Skribenten():

    def __init__(self):
        load_dotenv()
        self.gpt_key = os.getenv("GPT_KEY")
        if self.gpt_key:
            self.client = OpenAI(
                api_key=self.gpt_key,
            )
        else:
            print("None or not usable API key provided")



    def send_prompt(self, element, prompt):
        if self.client:
            try:
                if element == "Text":
                    response = self.client.responses.create(
                        model="gpt-4o",
                        instructions="You are awesome",
                        input=prompt,
                    )
                    return response.output_text
                elif element == "Image":
                    response = self.client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        n=1,
                        size="1024x1024"
                    )
                    return response
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("No client available")


    def generate_article(self, articles):
        r = requests.get(articles["articles"][1])
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        title = soup.find(articles["elements"][0]["title_element"])
        teaser = soup.select_one(articles["elements"][0]["teaser_element"])
        content = soup.select_one(articles["elements"][0]["content_element"])

        text_prompt = f"""
        Du er en professionel dansk journalist. Din hovedopgave er at generere dybdegående, spændende og fængende artikler på dansk baseret på modtaget indhold.
        Uanset hvilket sprog det modtagne indhold er på, skal du altid skrive artiklen på dansk.
        Du skal producere en unik dansk artikel, der er forskellig fra det oprindelige indhold for at undgå duplikationsproblemer med Google.
        Artiklen skal baseres på følgende indhold: {content.text} og være mindst 600 ord lang.
        Din skrivning skal inkludere en fangende clickbait-titel baseret på {title.text}.
        Titlen skal være i almindelig sætningstilfælde (ikke camelcase), hvilket betyder, at kun det første ord og egennavne starter med stort bogstav.
        Derefter skal du skrive en teaser baseret på {teaser.text}.
        Returnér dit output i præcis følgende JSON-format uden yderligere tekst eller forklaringer:
        {{
        "title": "Her skriver du titlen",
        "teaser": "Her skriver du teaseren",
        "content": "Her skriver du artiklens indhold i HTML-format med KUN <p>, <h3> og <a> tags"
        }}
        """
        image_prompt = (
            f"Skab et hyperrealistisk pressefoto til en nyhedsartikel baseret på denne tekst: “{content.text}”. "
            "Hvis teksten beskriver en person eller bygning, placér motivet i et autentisk miljø med naturligt lys, "
            "livagtige detaljer og klassisk journalistisk komposition. Undgå alle AI-artefakter – billedet skal fremstå som et ægte foto."
        )


        article = self.send_prompt(element="Text", prompt=text_prompt)
        image = self.send_prompt(element="Image", prompt=image_prompt)

        print(article)

        return article, image


        #print(articles["articles"][1])
        #for article in articles:
        #    print(article)

skribent = Skribenten()
text, image = skribent.generate_article(victoria_data)

print(text)
print(image)