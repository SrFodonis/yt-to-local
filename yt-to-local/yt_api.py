# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

# import os
import constants
import json
import googleapiclient.discovery

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = constants.YT_API_KEY

    youtube = googleapiclient.discovery.build(
        api_service_name,
        api_version,
        developerKey = DEVELOPER_KEY
        )

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId="PLhmaCTLQti_BUDyiYdDHae7bErXZZdGSe"
    )
    response = request.execute()
    print(type(response))

    with open("example.json", "w") as file:
        file.write(json.dumps(response, indent=4))
    
    print(f"Playlist title: {response['items'][0]['snippet']['title']}")

if __name__ == "__main__":
    main()