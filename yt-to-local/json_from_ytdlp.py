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
class playlist_simple:
    def __init__(self, id:str, title:str, playlist_count:str, entries: list):
        self.id = id
        self.title = title
        self.playlist_count = playlist_count
        self.entries = entries
        pass

class playlist_entry:
    def __init__(self, id:str, url: str, title:str, file_type:str):
        self.id = id
        self.url = url
        self.title = title
        self.file_type = file_type
        pass

videos = list()
for entry in playlist_json["entries"]:
    videos.append(
        playlist_entry(
            id=entry["id"],
            url=entry["url"],
            title=entry["title"],
            file_type="TBD"
        )
    )

# Test dump
with open("test_dump.json", "w") as file:
    for video in videos:
        file.write(
            f"{video.id}\n{video.url}\n{video.title}\n{video.file_type}\n\n"
        )