import os
import listmonk # type: ignore
from datetime import datetime, timedelta
import dotenv # type: ignore
import requests

dotenv.load_dotenv()

def send_campaign(list_id, body, subject):
    pwd = os.getenv("LISTMONK_PWD")
    user = os.getenv("LISTMONK_USR")

    resp = requests.post(
        "http://192.168.1.37:9000/api/campaigns",
        auth=(user, pwd),
        json={
            "name": "New boulders",
            "subject": subject,
            "body": body,
            "send_at": (datetime.now() - timedelta(hours=1) + timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "lists": [list_id],
        },
    )

    resp.raise_for_status()

    # Change status to scheduled
    campaign_id = resp.json()["data"]["id"]
    schedule_campaign(campaign_id)

def get_campaign_id(campaign_name):
    ls = get_lists()
    for name, key in ls.items():
        if name == campaign_name:
            return key
    return None

def schedule_campaign(campaign_id):
    pwd = os.getenv("LISTMONK_PWD")
    user = os.getenv("LISTMONK_USR")

    resp = requests.put("http://192.168.1.37:9000/api/campaigns/{campaign_id}/status".format(campaign_id=campaign_id),
        auth=(user, pwd),
        json={
            "status": "scheduled"
        },
    )
    resp.raise_for_status()

def get_lists():
    pwd = os.getenv("LISTMONK_PWD")
    user = os.getenv("LISTMONK_USR")

    resp = requests.get("http://192.168.1.37:9000/api/lists",
        auth=(user, pwd),
    )

    resp.raise_for_status()
    data = resp.json()["data"]["results"]
    ls = {}
    for l in data:
        ls[l["id"]] = l["name"]
    return ls

#send_campaign("<h1>Test</h1>", "Test Subject")
ls = get_campaign_id()
print(ls)

