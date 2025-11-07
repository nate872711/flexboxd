import requests, time, json

CLIENT_ID = input("Enter your Trakt Client ID: ").strip()
CLIENT_SECRET = input("Enter your Trakt Client Secret: ").strip()

# Step 1: Get Device Code
res = requests.post("https://api.trakt.tv/oauth/device/code", json={"client_id": CLIENT_ID})
data = res.json()

print(f"\nGo to {data['verification_url']} and enter code: {data['user_code']}")
print("Waiting for you to authorize the app...")

# Step 2: Poll for Token
while True:
    time.sleep(data["interval"])
    r = requests.post("https://api.trakt.tv/oauth/device/token", json={
        "code": data["device_code"],
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    if r.status_code == 200:
        tokens = r.json()
        print("\n✅ Authorization successful!")
        print(json.dumps(tokens, indent=2))
        print("\nAdd these to your docker-compose.yml:")
        print(f"  TRAKT_ACCESS_TOKEN={tokens['access_token']}")
        print(f"  TRAKT_REFRESH_TOKEN={tokens['refresh_token']}")
        break
    elif r.status_code == 400:
        continue
    else:
        print(f"Error: {r.status_code} - {r.text}")
        break
