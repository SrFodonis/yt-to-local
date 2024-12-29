import re
import json
import argparse
from os import path, makedirs

TARGET_DIR = "/home/phoenix_wsl/repos/yt-to-local/test_target"

def main():
    config = load_config()
    preflight_checks(config=config)
    urls = url_parser("playlist_urls.txt")
    print(urls, config)


def preflight_checks(config: dict):

    target_dir = config["target_dir"]

    # Make sure all necessary directories and files exist
    ## Target directory for all operations
    target_existance_checker("dir", target_dir, True)
    
    ## playlists_urls.txt
    if not target_existance_checker("file", f"{target_dir}/playlist_urls.txt", False):
        # Write default content
        with open(f"{target_dir}/playlist_urls.txt", "w") as file:
            file.write(
                (
                "-- Paste playlists URLs here, separated by new lines\n"
                "-- Comments may be used by typing -- at the beggining of a line\n"
                "-- Remember to write the name of the playlist for ease of use\n"
                )
            )
        
        print(f"Created file at {target_dir}/playlist_urls.txt")

    ## Downloads folder
    target_existance_checker("dir", f"{target_dir}/downloads", True)

    ## JSONs folder
    target_existance_checker("dir", f"{target_dir}/jsons", True)

    ## jsons/ config.json
    target_existance_checker("file", f"{target_dir}/jsons/config.json", True)

    ## jsons/ playlist_control.json
    target_existance_checker("file", f"{target_dir}/jsons/playlist_control.json", True)

def load_config() -> dict:
    """
    If the configuration already exists, load it and return as dictionary.
    If not, prompt user for configuration, save and return as dictionary.
    """

    args = get_cli_args()
    if args.reset_config:
        return get_config()

    with open(f"{TARGET_DIR}/jsons/config.json", "r") as file:
        try:
            config = json.load(file)
        except json.JSONDecodeError:
            return get_config()

    return config
        



def get_config() -> dict:
    """
    Prompt user for configuration, return it and save it to config.json
    """

    config = dict()

    # Get target directory
    print("\nPlease enter the following information to configure the program:\n")
    target_dir = input("Enter the full path of the target directory: ")
    if not path.isdir(target_dir):
        print("Path not found, directory and all necessary files will be automatically created.")
        print(f"Path: {target_dir}")
        confirmation = input("Do you wish to proceed? (y/n): ")
        if not confirmation.lower() in ["y", "yes"]:
            print("Exiting program...")
            exit()

    config["target_dir"] = target_dir
    print(f"Path: {target_dir} selected")

    # Create all necessary files and directories
    preflight_checks(config=config)

    # Save configuration
    with open(f"{target_dir}/jsons/config.json", "w") as file:
        json.dump(config, file, indent=4) # Pretty print for easier user modification

    return config
    

    
def get_cli_args() -> argparse.Namespace:
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

        parser.add_argument(
            "-rc", 
            "--reset-config", 
            action="store_true", 
            help="Prompt user for program config."
            )

        return parser.parse_args()


def target_existance_checker(type: str, full_path: str, if_missing_create: bool) -> bool:

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

        print(f"Created {type} at {full_path}")
        return True
        
    return exists


def url_parser(text_file) -> list:
    """
    Parse a text file containing YouTube URLs and return a list of cleaned URLs.\n
    This function reads a text file containing YouTube URLs, processes each line by:
    1. Filtering out lines without valid YouTube URLs
    2. Removing comments (denoted by '--')
    3. Removing leading/trailing whitespace

    Parameters:
    ----------
    text_file : str
    """

    COMMENT_PATTERN = re.compile("--")
    # Tested url pattern on mobile, the share button returns the full URL
    YT_URL_PATTERN = re.compile("https://www.youtube.com")

    with open(text_file) as file:
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


if __name__=="__main__":
    main()