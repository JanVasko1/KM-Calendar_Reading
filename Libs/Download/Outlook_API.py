import requests
import json
#! Dodělat

# Replace these with your actual values
client_id = "19db86c3-b2b9-44cc-b339-36da233a3be2"
client_secret = "YOUR_CLIENT_SECRET"
tenant_id = "17f69c66-2114-4826-9fb1-6e496607aebc"
username = "Jan.Vasko@konicaminolta.eu"
password = ""

# Get access token
url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
payload = {
    "grant_type": "password",
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": "https://graph.microsoft.com/.default",
    "username": username,
    "password": password}
response = requests.post(url, data=payload)
tokens = response.json()
access_token = tokens["access_token"]

# Get calendar events
start_date = "2024-10-01"
end_date = "2024-10-01"

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"}

params = {
    "$filter": f"start/dateTime ge {start_date} and end/dateTime le {end_date}"
}

events_url = f"https://graph.microsoft.com/v1.0/me/events"
events_response = requests.get(events_url, headers=headers, params=params)
events = events_response.json()

# Print events
print(json.dumps(events, indent=2))