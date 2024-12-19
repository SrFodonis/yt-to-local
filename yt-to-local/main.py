import re
from os import path, makedirs

TARGET_DIR = "/home/phoenix_wsl/yt-to-local/test_target"

def main():
    preflight_checks()
    urls = url_parser("playlist_urls.txt")


def preflight_checks():

    # Make sure all necessary directories and files exist
    ## Target directory for all operations
    if target_existance_checker("dir", TARGET_DIR, False):
        print(f"Target directory {TARGET_DIR} not found.")
        raise FileNotFoundError("Target directory does not exist")
    
    ## Downloads folder
    target_existance_checker("dir", f"{TARGET_DIR}/downloads", True)

    ## JSONs folder
    target_existance_checker("dir", f"{TARGET_DIR}/jsons", True)

    ## playlists_urls.txt 
    if not path.exists(f"{TARGET_DIR}/playlist_urls.txt"):
        # Create playlist_urls.txt
        with open("playlist_urls.txt", "w") as file:
            file.write(
                """
                -- Paste playlists URLs here, separated by new lines\n
                -- coments may be used by typing -- at the beggining of a line\n
                """
            )


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
        raise ValueError("Type must be 'file' or 'dir'")
        
    # Create if missing and requested
    if not exists and if_missing_create:
        if type.lower() == "dir":
            makedirs(full_path)
        elif type.lower() == "file":
            open(full_path, 'a').close()
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