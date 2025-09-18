from dotenv import load_dotenv  
import os
import base64
import requests
import time

load_dotenv()

client_id = "your_client _id"
client_secret ="your_client_secret"
refresh_token ="your_refresh_token"
redirect_url ="your_redirect_url"


def get_access_token_from_refresh():
    """
    Use stored refresh token to get a new access token.
    Call this before making API calls that require a user's token.
    """
    token_url = "https://accounts.spotify.com/api/token"
    auth_str = f"{client_id}:{client_secret}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    resp = requests.post(token_url, headers=headers, data=data)
    resp.raise_for_status()
    j = resp.json()
    access_token = j["access_token"]
    expires_in = j.get("expires_in")   # seconds
    return access_token, expires_in


def get_now_playing():
    token, _ = get_access_token_from_refresh()
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)
    if r.status_code == 204:
        print("Nothing is playing right now.")
        return None
    r.raise_for_status()
    data = r.json()
    # Example extraction:
    item = data.get("item")
    if not item:
        print("No item data")
        return None
    return data

def format_progress_bar(progress_ms, duration_ms, bar_length=30):
    progress_ratio = progress_ms / duration_ms
    filled_length = int(bar_length * progress_ratio)
    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    progress_sec = progress_ms // 1000
    duration_sec = duration_ms // 1000
    return f"[{bar}] {progress_sec}s / {duration_sec}s"



if __name__ == "__main__":
   last_track_id = None
   was_playing = False  # tracks if something was playing last poll
   print("Nothing is Playing")

   while True:
        try:
            data = get_now_playing()

            if data:
                current_track_id = data["item"]["id"]

                # Extract progress and duration for progress bar
                progress_ms = data.get("progress_ms", 0)
                duration_ms = data["item"]["duration_ms"]

                if current_track_id != last_track_id:
                    title = data["item"]["name"]
                    artists = ", ".join([a["name"] for a in data["item"]["artists"]])
                    print("-----------------------")
                    print("NOW PLAYING.....")
                    print(f"{title}")
                    print(f"{artists}")
                    print("-------------------------")
                    last_track_id = current_track_id

                # Print progress bar
                progress_bar = format_progress_bar(progress_ms, duration_ms)
                print(progress_bar)

                was_playing = True

            else:
                if was_playing:
                    print("Nothing is playing right now.")
                was_playing = False
                # Do NOT reset last_track_id here

            time.sleep(5)

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)