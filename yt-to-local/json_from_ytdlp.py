import json, subprocess, shlex

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLhmaCTLQti_CQ50HGv1lvmVgSsUrpIqUj"
PULL_FROM_YT = False

ytdlp_command = f"yt-dlp {PLAYLIST_URL} --skip-download --flat-playlist -J"

with open("last_used_command.txt", "w") as file:
    file.write(ytdlp_command)

if PULL_FROM_YT:
    print("Pulling JSON from YT")
    playlist_json = json.loads(
        subprocess.check_output(
            shlex.split(ytdlp_command)
        )
    )
else:
    print("Using local JSON file")
    with open("test_file.json", "r") as file:
        playlist_json = json.loads(file.read())

formatted_json = json.dumps(playlist_json, indent=4)

with open("test_file.json", "w") as file:
    file.write(formatted_json)

# Get playlist_control-style formatted file
# Get a list of all the video entries in the playlist
entries = list()
for entry in playlist_json["entries"]:
    entries.append(
        {
            "id": entry["id"],
            "url": entry["url"],
            "title": entry["title"],
            "file_type": "TBD"
        }
    )

# Create full playlist_control info
playlist_control = [{
    "id": playlist_json["id"],
    "title": playlist_json["title"],
    "playlist_count": playlist_json["playlist_count"],
    "entries": entries
}]


with open("test_playlist_control.json", "w") as file:
    file.write(
        json.dumps(playlist_control, indent=4)
    )