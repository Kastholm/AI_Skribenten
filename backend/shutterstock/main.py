import requests
import base64

# Sæt dine Shutterstock API klient info her
CLIENT_ID = 'DIN_CLIENT_ID'
CLIENT_SECRET = 'DIT_CLIENT_SECRET'

def get_access_token(client_id, client_secret):
    auth_str = f"{client_id}:{client_secret}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_str}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    resp = requests.post("https://api.shutterstock.com/v2/oauth/access_token", headers=headers, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]

def search_image(query, token):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"query": query, "per_page": 1}
    resp = requests.get("https://api.shutterstock.com/v2/images/search", headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    if data["data"]:
        return data["data"][0]["assets"]["preview"]["url"]
    return None

if __name__ == "__main__":
    token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    url = search_image("nature landscape", token)
    if url:
        print("Billede URL:", url)
    else:
        print("Ingen billeder fundet")