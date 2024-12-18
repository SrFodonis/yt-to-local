import re

COMMENT_PATTERN = re.compile("--")
# Tested url pattern on mobile, the share button returns the full URL
YT_URL_PATTERN = re.compile("https://www.youtube.com")

# Takes in the name/dir of the playlist_urls.txt file and returns a list with all the playlists
def url_parser(text_file) -> list:
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


urls = url_parser("playlist_urls.txt")

print(urls)

for url in urls:
    print(url)