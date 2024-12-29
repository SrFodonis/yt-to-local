What is the current purpose of yt-to-local?
A: Read a text file to fetch playlist URLs, download those playlists, and then keep the local mirrors updated according to their YT counterparts.

What do I need to accomplish this?
A:
1- Be able to read the text file and identify valid playlist URLs
2- Compare the local mirror against the YT counterpart to check for changes
	2.1- If the playlist does not exist locally, download it and start tracking it
	2.2- If the playlist exists locally and...
		2.2.1- Both instances are the same, do nothing
		2.2.2- The YT instance has more entries, download the missing entries
		2.2.3- The YT instance has less entries, delete the excess entries
		2.2.4- The YT instance has different entries, 






What happens when...
YT has A B C & D entries and the local has A B T & D entries
Comapre the 2
A - A
B - B
C - T
D - D

Find discrepancy
A - A
B - B
C - T <--- T local disparity
D - D

Solve discrepancy
A - A
B - B
C - T <--- Send T to trash
D - D

A - A
B - B
C -   <--- Download C
D - D

A - A
B - B
C - C
D - D

Discrepancy solved




YT has A B C & D and the local has A B & C
Compare the 2
A - A
B - B
C - C
D - 

Find discrepancy
A - A
B - B
C - C
D -   <--- Missing D

Solve discrepancy (download missing)
A - A
B - B
C - C
D - D <--- Download D

Discrepancy solved






YT has A B & C and the local has A B C & D
Compare the 2
A - A
B - B
C - C
  - D

Find discrepancy
A - A
B - B
C - C
  - D <--- Excess D

Sove discrepancy
A - A
B - B
C - C
  -   <--- Send D to trash

New record
A - A
B - B
C - C

Discrepancy solved


--------------


FIRST REMOVE LOCAL NOT IN YT
find the videos in LOCAL that are NOT in YT
send to trash

SECOND DOWNLOAD MISSING
find the videos in YT that are NOT in LOCAL
download those videos <--- multiple YTDLP runs



Find_discrepancy is gonna return a dictionary with lists
{
	"excess": 
	[
		"video_id1",
		"video_id2",
	],
	"missing":
	[
		"video_id1",
		"video_id2",
	]
}

This makes it easier to simply pass the "excess" list to trash
And the "missing" list to the downloader

---------
Next to add:
	- Preflight_checks
		- playlist_control not exists -> create empty
	- config.json
		- Add existance check to preflight_checks
		- add cli argument to reset config
			- Add url passed as argument to playlist_control and playlist_urls.txt
		- Select preferred download format? Select video or audio only?
-----------------------------
!!!!!!!!!!!!!!!!!!!!!! MOVE CONFIG LOADING AND GETTING INTO preflight_checks !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
run programm with -rc flag to see why
/home/phoenix_wsl/repos/yt-to-local/test_2

---------

Target directory file structure
target
	|
	|-playlist_urls.txt
	|	| Text file from where the playlist urls are extracted
	|
	|-downloads/
	|	| All the downloaded videos
	|
	|-JSONs/
		| All the necessary JSONs
			| playlist_control
			| temp_yt_information
			| config?