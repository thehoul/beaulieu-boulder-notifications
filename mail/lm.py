import os
import listmonk # type: ignore
from datetime import datetime, timedelta
import dotenv # type: ignore
import requests
from util.config import get_section 

dotenv.load_dotenv()

lm_base_url = get_section("URLS")["LM_API_URL"]

def send_campaign(list_id, body, subject):
    pwd = os.getenv("LISTMONK_PWD")
    user = os.getenv("LISTMONK_USR")

    resp = requests.post(
        f"{lm_base_url}/campaigns",
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

    resp = requests.put(f"{lm_base_url}/campaigns/{campaign_id}/status",
        auth=(user, pwd),
        json={
            "status": "scheduled"
        },
    )
    resp.raise_for_status()

def get_lists():
    pwd = os.getenv("LISTMONK_PWD")
    user = os.getenv("LISTMONK_USR")

    resp = requests.get(f"{lm_base_url}/lists",
        auth=(user, pwd),
    )

    resp.raise_for_status()
    data = resp.json()["data"]["results"]
    ls = {}
    for l in data:
        ls[l["id"]] = l["name"]
    return ls
