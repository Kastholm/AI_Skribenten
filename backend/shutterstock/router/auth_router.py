from fastapi import APIRouter, HTTPException, Query
import requests
from shutterstock.main import CLIENT_ID, CLIENT_SECRET, get_collections, get_images_from_collection
from urllib.parse import urlencode

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    )

REDIRECT_URI = "https://db14-86-52-42-195.ngrok-free.app/callback"
SCOPE = "collections.view"

@router.get("/start-auth")
def start_auth():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
    }
    auth_url = f"https://www.shutterstock.com/oauth/authorize?{urlencode(params)}"
    return {"auth_url": auth_url}

@router.get("/callback")
def shutterstock_callback(code: str):
    url = "https://api.shutterstock.com/v2/oauth/access_token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    tokens = resp.json()
    # Gem tokens (fx i session/cookie)
    return tokens

@router.get("/my-collections")
def my_collections(access_token: str = Query(...)):
    # access_token fra callback/user
    try:
        return get_collections(access_token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my-collection-images")
def my_collection_images(
    access_token: str = Query(...),
    collection_id: str = Query(...),
    query: str = Query(None),
    per_page: int = Query(3)
):
    try:
        return get_images_from_collection(access_token, collection_id, query, per_page)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))