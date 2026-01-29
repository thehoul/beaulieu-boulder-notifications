import os
from datetime import datetime, timedelta
import dotenv # type: ignore
import requests
from util.config import get_section 

dotenv.load_dotenv()

lm_api_url = get_section("URLS")["LM_API_URL"]

def send_campaign(list_id, body, subject):
    pwd = os.getenv("LISTMONK_PWD")
    user = os.getenv("LISTMONK_USR")

    resp = requests.post(
        f"{lm_api_url}/campaigns",
        auth=(user, pwd),
        json={
            "name": "New boulders",
            "subject": subject,
            "body": body,
            "send_at": (datetime.now() + timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "lists": [list_id],
        },
    )

    resp.raise_for_status()

    # Change status to scheduled
    campaign_id = resp.json()["data"]["id"]
    schedule_campaign(campaign_id)

def get_list_ids():
    ls = get_lists()
    keys = list(ls.keys())
    return keys

def schedule_campaign(campaign_id):
    pwd = os.getenv("LISTMONK_PWD")
    user = os.getenv("LISTMONK_USR")

    resp = requests.put(f"{lm_api_url}/campaigns/{campaign_id}/status",
        auth=(user, pwd),
        json={
            "status": "scheduled"
        },
    )
    resp.raise_for_status()

def get_lists():
    pwd = os.getenv("LISTMONK_PWD")
    user = os.getenv("LISTMONK_USR")

    resp = requests.get(f"{lm_api_url}/lists",
        auth=(user, pwd),
    )

    resp.raise_for_status()
    data = resp.json()["data"]["results"]
    ls = {}
    for l in data:
        ls[l["id"]] = l["name"]
    return ls


def get_media(media_id):
    pwd = os.getenv("LISTMONK_PWD")
    user = os.getenv("LISTMONK_USR")
    url = f"{lm_api_url}/media/{media_id}"
    resp = requests.get(url,
        auth=(user, pwd)
    )
    resp.raise_for_status()
    return resp.json()["data"]
    
def upload_media(file_path):
    with open(file_path, "rb") as f:
        files = {'file': f}
        pwd = os.getenv("LISTMONK_PWD")
        user = os.getenv("LISTMONK_USR")

        resp = requests.post(f"{lm_api_url}/media",
            auth=(user, pwd),
            files=files
        )
        resp.raise_for_status()
        return resp.json()["data"]
    
def delete_media(media_id):
    pwd = os.getenv("LISTMONK_PWD")
    user = os.getenv("LISTMONK_USR")
    url = f"{lm_api_url}/media/{media_id}"
    resp = requests.delete(url,
        auth=(user, pwd)
    )
    resp.raise_for_status()
    return resp.json()["data"]


def get_all_media():
    pwd = os.getenv("LISTMONK_PWD")
    user = os.getenv("LISTMONK_USR")
    url = f"{lm_api_url}/media"
    resp = requests.get(url,
        auth=(user, pwd)
    )
    resp.raise_for_status()
    return resp.json()["data"]["results"]