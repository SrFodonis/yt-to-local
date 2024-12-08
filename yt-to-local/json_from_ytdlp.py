import json, subprocess, shlex

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLhmaCTLQti_CQ50HGv1lvmVgSsUrpIqUj"

ytdlp_command = f"yt-dlp {PLAYLIST_URL} --skip-download --flat-playlist -J"

with open("last_used_command.txt", "w") as file:
    file.write(ytdlp_command)

raw_json = subprocess.check_output(
    shlex.split(ytdlp_command)
)

formatted_json = json.dumps(json.loads(raw_json), indent=4)

with open("test_file.json", "w") as file:
    file.write(formatted_json)