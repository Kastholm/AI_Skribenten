import json
import os
import bs4
import requests
from medier import victoria_data, victoria_used_data


class ArticleParser:

    def __init__(self, urls, all_articles, already_used_articles, elements, json_file):
        self.urls = urls
        self.all_articles = all_articles
        self.already_used_articles = already_used_articles
        self.elements = elements[0]
        self.json_file = json_file
        
    def parse_article(self):
        if self.urls != []:
            for url in self.urls:
                response = requests.get(url)
                soup = bs4.BeautifulSoup(response.text, 'html.parser')

                urls = soup.find_all(self.elements["sitemap_url_element"])
                for url in urls:
                    url = url.text.strip().strip('<*>').strip('</*>')
                    if url not in self.all_articles and url not in self.already_used_articles:
                        self.all_articles.append(url)
            
            # Load existing JSON structure
            with open(self.json_file, 'r') as f:
                json_data = json.load(f)
            
            json_data['articles'] = self.all_articles
            
            with open(self.json_file, 'w') as f:
                json.dump(json_data, f, indent=4)

        else:
            print("No urls to parse")


parse_medier = {
    "24victoria": {
        "enabled": True,
        "json_file": "medier/victoria/victoria.json",
        "urls": victoria_data.get("urls", []),
        "articles": victoria_data.get("articles", []),
        "already_used_articles": victoria_used_data.get("articles", []),
        "elements": victoria_data.get("elements", [])
    }
}

for medie in parse_medier:
    if parse_medier[medie]["enabled"]:
        article_parser = ArticleParser(
            parse_medier[medie]["urls"],
            parse_medier[medie]["articles"],
            parse_medier[medie]["already_used_articles"],
            parse_medier[medie]["elements"],
            parse_medier[medie]["json_file"]
        )
        article_parser.parse_article()