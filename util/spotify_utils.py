import requests

def get_current_song(access_token):
    # request current song
    request_headers = {
        "Authorization": "Bearer" + " " + access_token
    }
    
    currently_playing_response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=request_headers)

    if currently_playing_response.status_code == 200:
        currently_playing_response_body = currently_playing_response.json()
        current_track = currently_playing_response_body["item"]

        return f"[{current_track["name"]}, {current_track["artists"][0]["name"]}]"      
    else:
        return "[not listening]"
