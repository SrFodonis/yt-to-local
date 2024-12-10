import json, subprocess, shlex, pathlib
from time import sleep
from yt_dlp import utils

PLAYLIST_URLS = [
    "https://www.youtube.com/playlist?list=PLhmaCTLQti_CQ50HGv1lvmVgSsUrpIqUj"
    ,"https://www.youtube.com/playlist?list=PLhmaCTLQti_AOxL76JWDu6UEpsWc1h2DQ"
]
YT_DLP_OPTIONS = "--skip-download --flat-playlist -J"

PULL_FROM_YT = True

def download_JSON() -> list:
    playlists = list()
    
    # Empty last_used_command.txt
    #! pathlib.Path.unlink("last_used_command.txt")

    for url in PLAYLIST_URLS:
        # Write commands to be used & download JSON
        ytdlp_command = f"yt-dlp {url} {YT_DLP_OPTIONS}"
        
        with open("last_used_command.txt", "a") as file:
            file.write(ytdlp_command)

        try:
            yt_json = subprocess.check_output(
                shlex.split(ytdlp_command)
            )
        except:
            print("-- ERROR! --")
            print(f"Error handling playlist: {url}\nIs the playlist private?")
            exit()

        playlists.append(
            json.loads(yt_json)
        )
        sleep(2) # Anti rate-limitting measure
    
    return playlists
    

def load_local_JSON():
    with open("test_file.json", "r") as file:
        playlists = json.loads(
            file.read()
        )
    
    return playlists

if PULL_FROM_YT:
    playlists = download_JSON()
    # Write YT JSON info to file
    with open("test_file.json", "w") as file:
        file.write(
            json.dumps(playlists, indent=4)
        )
else:
    playlists = load_local_JSON()



# Get playlist_control-style formatted file
# Get a list of all the video entries in the playlist
# entries = list()
# for entry in playlist_json_1["entries"]:
#     entries.append(
#         {
#             "id": entry["id"],
#             "url": entry["url"],
#             "title": entry["title"],
#             "file_type": "TBD"
#         }
#     )

# # Create full playlist_control info
# playlist_control = {
#     "id": playlist_json_1["id"],
#     "title": playlist_json_1["title"],
#     "playlist_count": playlist_json_1["playlist_count"],
#     "entries": entries
# }


# with open("test_playlist_control.json", "w") as file:
#     file.write(
#         json.dumps(playlist_control, indent=4)
#     )