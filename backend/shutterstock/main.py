import requests
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.getenv("SHUTTERSTOCK_KEY")
CLIENT_SECRET = os.getenv("SHUTTERSTOCK_SECRET_KEY")

def get_collections(access_token):
    """
    Hent alle dine collections på Shutterstock (kræver OAuth user-access_token)
    """
    url = "https://api.shutterstock.com/v2/images/collections"
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def get_images_from_collection(access_token, collection_id, query=None, per_page=3):
    """
    Hent billeder fra en given collection.
    - access_token: din user-access_token fra OAuth (IKKE client credentials)
    - collection_id: id på din collection
    - query: (valgfri) søgeord
    - per_page: antal billeder der skal returneres
    """
    url = f"https://api.shutterstock.com/v2/images/collections/{collection_id}/items"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"per_page": per_page}
    if query:
        params["query"] = query
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()

# Valgfri: Test direkte (indsæt access_token og collection_id fra dit eget flow)
if __name__ == "__main__":
    access_token = "INDSÆT_DIN_ACCESS_TOKEN_HER"
    collection_id = "INDSÆT_DIN_COLLECTION_ID_HER"
    print(get_collections(access_token))
    print(get_images_from_collection(access_token, collection_id, query="Jonas Vingegaard", per_page=3))
