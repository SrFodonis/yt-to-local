import subprocess
import shlex
import json
import os
import os.path

PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLhmaCTLQti_CQ50HGv1lvmVgSsUrpIqUj"
PLAYLIST_URL_GENERIC = "https://www.youtube.com/playlist?list="

def main():
    preflight_check()

    # trash_manager()

    playlist_contorl = load_playlist_control()

    playlist = get_playlist_info_json(PLAYLIST_URL, only_id=False)

    playlist_title_snake_case = playlist["title"].replace(" ", "_")

    with open(f"playlists/{playlist_title_snake_case}.json", "w") as file:
        file.write(json.dumps(playlist))

    with open(f"playlists/{playlist_title_snake_case}-pretty.json", "w") as file:
        file.write(json.dumps(playlist, indent=4))


def load_playlist_control() -> str:
    with open("playlist_control.json") as file:
        playlist_control = json.loads(file.read())

    # Check if playlist_control is empty
    if playlist_control["empty"]:
        print("playlist_control.json is empty, ")

    return "hi"


def preflight_check():
    # Make sure playlist_control.json exists
    if not os.path.isfile("playlist_control.json"):
        with open("playlist_control.json", "w") as file:
            file.write(json.dumps({
                "empty": True
            }))

    # Make sure playlists/ dir exists
    if not os.path.isdir("playlists"):
        os.makedirs("playlists")


def get_playlist_info_json(url: str, only_id: bool) -> str:
    if only_id:
        url = f"{PLAYLIST_URL_GENERIC}{url}"

    raw_json = subprocess.check_output(
        shlex.split(f"yt-dlp {url} --skip-download --flat-playlist -J")
    )

    return json.loads(raw_json)


# def get_discrepancy(playlist_local: dict, playlist_yt: dict) -> list:

if __name__=="__main__":
    main()