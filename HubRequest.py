import json
from platform import python_version
import requests
import base64
import os

from dotenv import load_dotenv
from supabase import create_client, Client

# import balloonTip as bt

# pip install requests
# pip install python-dotenv
# pip install pyodbc
# pip install supabase

load_dotenv("config.env")


def run_web_job():
    id = os.getenv("id")  # "iiotqzna-brewery-v1.0.0"
    secret = os.getenv("secret")  # "vZFm1C7j1Htb9JLJGmit0004VVU2dUvvemcmnlYEayX"
    gateway = os.getenv("gateway")  # "https://gateway.eu1.mindsphere.io/api"
    urlbase = os.getenv("urlbase")  # "https://cxsquvbkilwzouziiavx.supabase.co"
    keybase = os.getenv(
        "keybase"
    )  # "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN4c3F1dmJraWx3em91emlpYXZ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODc4MDU2MzcsImV4cCI6MjAwMzM4MTYzN30.fpw3IYaFfK1kqmc1KuqYYWZNiwVnDsPSESmAgbo6yUI"
    print(python_version())
    key = f"{id}:{secret}"
    _bytes = key.encode("ascii")
    base64token = str(base64.b64encode(_bytes), "ascii")
    _provider = id.split("-")[0]
    _appName = id.split("-")[1]
    _version = id.split("-")[2]

    url = f"{gateway}/technicaltokenmanager/v3/oauth/token"

    payload = {
        "grant_type": "client_credentials",
        "appName": f"{_appName}",
        "appVersion": f"{_version}",
        "hostTenant": f"{_provider}",
        "userTenant": f"{_provider}",
    }
    headers = {
        "content-type": "application/json",
        "X-SPACE-AUTH-KEY": f"Bearer {base64token}",
    }

    r = requests.post(url, data=json.dumps(payload), headers=headers)
    data = r.json()

    url = f"{gateway}/eventmanagement/v3/events?size=1"

    headers = {"Authorization": "Bearer " + data["access_token"]}
    response = requests.get(url, headers=headers)

    eventResponse = response.json()

    event = eventResponse["_embedded"]["events"][0]

    _id = event["entityId"]

    url = f"{gateway}/iottimeseries/v3/timeseries/{_id}/BoilerData"

    response = requests.get(url, headers=headers)

    boilerData = response.json()

    supabase: Client = create_client(urlbase, keybase)

    response = (
        supabase.table("events")
        .select("*", count="exact")
        .eq("id", event["id"])
        .execute()
    )

    if response.count == 0:
        data = {
            "id": event["id"],
            "timestamp": event["timestamp"],
            "entityId": event["entityId"],
            "severity": event["severity"],
            "description": event["description"],
            "source": event["source"],
            "lastReading": str(boilerData),
            "status": 0,
        }
        data, count = supabase.table("events").insert(data).execute()
        log = {"eventId": event["id"], "status": 0}
        log, count = supabase.table("auditlog").insert(log).execute()
        # bt.balloon_tip("Alert", "Temperature is High, Please correct it")
    else:
        print(f"Event id {event['id']} already exists")


if __name__ == "__main__":
    run_web_job()

"""
create table
  public.events (
    id uuid not null,
    created_at timestamp with time zone null default now(),
    timestamp timestamp with time zone null,
    entityId uuid null,
    severity smallint null,
    description text null,
    source text null,
    lastReading text null,
    status smallint null,
    updated_at timestamp with time zone null,
    constraint Alerts_pkey primary key (id)
  ) tablespace pg_default;

create table
  public.auditlog (
    id bigint generated by default as identity not null,
    created_at timestamp with time zone null default now(),
    eventId uuid null,
    status smallint null,
    seconds integer null,
    timestamp timestamp with time zone null,
    completed boolean null default false,
    constraint auditlog_pkey primary key (id)
  ) tablespace pg_default;
"""
