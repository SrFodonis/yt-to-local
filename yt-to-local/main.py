import re
import json
import argparse
import constants
import googleapiclient.discovery
from os import path, makedirs, environ
from dataclasses import dataclass

YT_API_KEY = constants.YT_API_KEY
CONFIG_DIR = f"/home/{environ['USER']}/.config/yt-to-local"
CONFIG_FILE = f"{CONFIG_DIR}/config.json"

def main():
    args = init_cli_args()
    if args.setup:
        run_setup()
        exit()

    # Preflight checks
    ## Check for configuration file
    if not path.isfile(CONFIG_FILE):
        print("[!] Configuration file not found. Run setup with '-s' flag.")
        exit()

    # Load configuration
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)

    target_path = config["target_path"]

    # Bussiness logic
    #TODO: Get playlist information using YT API
    # Check gcloud api dashboard for docs and credentials)
    urls = url_parser(f"{target_path}/playlist_urls.txt")

    playlists = list()

    for url in urls:
        playlists.append(
            get_playlist_info(extract_playlist_id(url))
        )

    for playlist in playlists:
        print(f"Title: {playlist["items"][0]["snippet"]["title"]}")


def run_setup() -> None:

    """Initialize the application's directory structure and configuration.
    
    This function:
    1. Prompts user for target directory path
    2. Creates necessary directory structure if it doesn't exist
    3. Generates initial configuration file
    4. Saves configuration to JSON file
    
    Returns:
        None
    
    Side Effects:
        - Creates directories and files on filesystem
        - Writes configuration to config.json
        - Exits program if user declines directory creation
    """

    print(f"{"-"*5} Program setup {"-"*5}\n")

    # Get target directory
    target = input("[<<] Enter the full path of the target directory: ").strip()

    # Check if target directory exists
    if not path.isdir(target):
        # Notify user that directory doesn't exist
        print("[!] Path not found, directory and all necessary files will be automatically created.")
        print(f"Path: {target}")
        
        # Ask for user confirmation before creating directory
        confirmation = input("[?] Do you wish to proceed? (y/n): ").strip()
        
        # Exit if user doesn't confirm
        if confirmation.lower() not in ["y", "yes"]:
            print("No action taken.")
            print("[!] Exiting program...")
            exit()

    # Create all necessary files and directories
    create_files(target)

    # Save configuration
    with open(CONFIG_FILE, "w") as file:
        json.dump({"target_path": target}, file, indent=4)

    print(f"\n[!] Configuration saved at {CONFIG_DIR}/config.json")
    print(f"[!!] Setup complete. Please add the URLs to {target}/playlist_urls.txt")
    print("[!!] The program may now be run normally.")


def create_files(target_path : str) -> None:
    # Make sure all necessary directories and files exist
    ## Target directory for all operations
    existance_checker("dir", target_path, True)
    
    ## playlists_urls.txt
    if not existance_checker("file", f"{target_path}/playlist_urls.txt", False):
        # Write default content
        with open(f"{target_path}/playlist_urls.txt", "w") as file:
            file.write(
                (
                "-- Paste playlists URLs here, separated by new lines\n"
                "-- Comments may be used by typing -- at the beggining of a line\n"
                "-- Remember to write the name of the playlist for ease of use\n"
                )
            )
        
        print(f"[>] Created file at {target_path}/playlist_urls.txt")

    ## Downloads folder
    existance_checker("dir", f"{target_path}/downloads", True)

    ## JSONs folder
    existance_checker("dir", f"{target_path}/jsons", True)

    ## Configuration dir and file
    existance_checker("dir", CONFIG_DIR, True)
    existance_checker("file", CONFIG_FILE, True)

    ## jsons/ playlist_control.json
    existance_checker("file", f"{target_path}/jsons/playlist_control.json", True)

# def load_config() -> dict:
#     """
#     If the configuration already exists, load it and return as dictionary.
#     If not, prompt user for configuration, save and return as dictionary.
#     """

#     args = get_cli_args()
#     if args.reset_config:
#         return get_config()

#     with open(f"{TARGET_DIR}/jsons/config.json", "r") as file:
#         try:
#             config = json.load(file)
#         except json.JSONDecodeError:
#             return get_config()

#     return config

# def get_config() -> dict:
    """
    Prompt user for configuration, return it and save it to config.json
    """

    # config = dict()

    # # Get target directory
    # print("\nPlease enter the following information to configure the program:\n")
    # target_dir = input("Enter the full path of the target directory: ")
    # if not path.isdir(target_dir):
    #     print("Path not found, directory and all necessary files will be automatically created.")
    #     print(f"Path: {target_dir}")
    #     confirmation = input("Do you wish to proceed? (y/n): ")
    #     if not confirmation.lower() in ["y", "yes"]:
    #         print("Exiting program...")
    #         exit()

    # config["target_dir"] = target_dir
    # print(f"Path: {target_dir} selected")

    # # Create all necessary files and directories
    # preflight_checks(config=config)

    # # Save configuration
    # with open(f"{target_dir}/jsons/config.json", "w") as file:
    #     json.dump(config, file, indent=4) # Pretty print for easier user modification

    # return config


def init_cli_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            prog="yt-to-local",
            description="Download YouTube playlist's videos to local storage."
        )

        # parser.add_argument(
        #     "-u", 
        #     "--url", 
        #     type=str, 
        #     help="URL of playlist to download and add to tracker."
        #     )

        # parser.add_argument(
        #     "-rc", 
        #     "--reset-config", 
        #     action="store_true", 
        #     help="Prompt user for program config."
        #     )

        parser.add_argument(
            "-s", 
            "--setup", 
            action="store_true", 
            help="Run program setup."
            )

        return parser.parse_args()


def existance_checker(type: str, full_path: str, if_missing_create: bool) -> bool:

    """
    Checks if a target exists, and creates it if missing and requested.\n
    The type parameter must be either 'file' or 'dir'.
    """

    # Check if the target exists
    if type.lower() == "file":
        exists = path.isfile(full_path)
    elif type.lower() == "dir":
        exists = path.isdir(full_path)
    else:
        raise ValueError("\nType must be 'file' or 'dir'")
        
    # Create if missing and requested
    if not exists and if_missing_create:
        if type.lower() == "dir":
            makedirs(full_path)
        elif type.lower() == "file":
            open(full_path, 'a').close()

        print(f"[>] Created {type} at {full_path}")
        return True
        
    return exists


def url_parser(url_file_path: str) -> list:
    """
    Parse a text file containing YouTube URLs and return a list of cleaned URLs.\n
    This function reads a text file containing YouTube URLs, processes each line by:
    1. Filtering out lines without valid YouTube URLs
    2. Removing comments (denoted by '--')
    3. Removing leading/trailing whitespace
    """

    COMMENT_PATTERN = re.compile("--")
    # Tested url pattern on mobile, the share button returns the full URL
    YT_URL_PATTERN = re.compile("https://www.youtube.com")

    with open(url_file_path) as file:
        raw_text = file.read()

    clean_urls = list()

    # Separate by new line
    newlined = raw_text.split("\n") # Returns a list of stringss

    # Search for comments
    for line in newlined:
        # Search for YT URL "https://www.youtube.com" pattern
        valid_yt_url = YT_URL_PATTERN.search(line)

        # If line does not contain a valid URL, skip it
        if not valid_yt_url:
            continue

        # Search the line for the "--" comment pattern
        comment = COMMENT_PATTERN.search(line)
        
        if comment: # If a comment is found
            # Get it's starting location
            comment_start_pos = comment.span()[0]
            # Extract only the contents of the line previous to that starting location
            # Then, remove all trailing white space
            clean_line = line[:comment_start_pos].strip()
        else: # If no comment is found
            # Just remove the trailing white space
            clean_line = line.strip()

        # Skip empty lines, resulting from a comment line with no url
        if clean_line == '':
            continue

        clean_urls.append(clean_line)

    return clean_urls


def extract_playlist_id(url: str) -> str:
    """
    Extract the playlist ID from a YouTube playlist URL.
    """

    # Pattern for playlist URLs
    playlist_pattern = re.compile(r"list=([A-Za-z0-9_-]+)")

    # Search for the pattern in the URL
    playlist_id = playlist_pattern.search(url)

    # If no match is found, return None
    if not playlist_id:
        return None

    # group(1) returns the first captured group in parentheses ([A-Za-z0-9_-]+)
    # For example, in URL "...list=PL1234...", it returns "PL1234"
    return playlist_id.group(1)


def get_playlist_info(playlist_id: str) -> dict:
    """
    Get playlist information from YouTube API and return as dictionary.
    """

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        developerKey = YT_API_KEY
        )

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id
    )
    response = request.execute()

    return response


@dataclass
class playlist:
    title: str
    id: str
    videos: list

@dataclass
class video:
    title: str
    id: str
    url: str

def package_playlist(url: str) -> playlist:
    """
    
    """
    



if __name__=="__main__":
    main()