# get_refresh_token.py
import os
import base64
import requests
import urllib.parse

CLIENT_ID = "your-client-id-here"
CLIENT_SECRET = "your-client-secret-here"
REDIRECT_URI = "your-redirect-url-here"

SCOPE = "user-read-currently-playing user-read-playback-state"

# Step A: build auth URL
params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "show_dialog": "true"
}
auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)

print("1) Open this URL in your browser and log in (allow permissions):\n")
print(auth_url)
print("\n2) After you approve, Spotify redirects to your redirect URI with ?code=XXXX")
code = input("\nPaste the 'code' value from the redirect URL here: ").strip()

# Step B: exchange code for tokens
token_url = "https://accounts.spotify.com/api/token"
auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
b64_auth_str = base64.b64encode(auth_str.encode()).decode()

resp = requests.post(token_url, data={
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": REDIRECT_URI
}, headers={
    "Authorization": f"Basic {b64_auth_str}",
    "Content-Type": "application/x-www-form-urlencoded"
})

resp.raise_for_status()
tokens = resp.json()
print("\nResponse JSON:")
print(tokens)

print("\n--- IMPORTANT ---")
print("Copy the value of 'refresh_token' and save it in your .env as SPOTIFY_REFRESH_TOKEN")
