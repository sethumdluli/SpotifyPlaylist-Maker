# Billboard100 Web Scraper to Spotify Playlist

This is a Python project which uses Beautiful Soup to scrape billboard.com to find the hottest top 100 songs from an inputed date. The script creates a new playlist on Spotify and then adds Billboard100 songs from the specified date on it.

This code was run on VS Code and the following packages were installed from the terminal:
- pip install spotipy
- pip install beautifulsoup4
- pip install requests

**Example**
The code was run for the date 2022-01-01 and the screenshot below shows the results obtained.
To see the hottest songs from 1 January 2022, go to [Billboard Hot 100](https://www.billboard.com/charts/hot-100/2022-01-01).

![result screenshot](https://github.com/sethumdluli/SpotifyPlaylist-Maker/blob/main/screenshot.png?raw=true)

NB! The code adds 96 songs to the playlist because some songs could not be found based on the search criteria. Improvements are still to be done to make sure that the code works 100% accurately.
