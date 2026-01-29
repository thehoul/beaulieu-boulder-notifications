import os
from datetime import datetime, timedelta
import dotenv # type: ignore
import requests
from util.config import get_section 

dotenv.load_dotenv()

lm_config = get_section("LISTMONK")
lm_api_url = lm_config["API_URL"]
list_id = int(lm_config["LIST_ID"])

def send_campaign(body, subject):
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