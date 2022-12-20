import requests
import spotipy
import calendar
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

billboard_url = "https://www.billboard.com/charts/hot-100/"
Client_ID = "Your Client ID"
Client_Secret= "Your Client Secret"
redirect_URI="http://example.com"

#input date 
user_date = input("Enter the date you would like to go back to...\nFormat: YYYY-MM-DD\n")

#request to billboard.com
response = requests.get(url=f"{billboard_url}/{user_date}/")
billboard_response = response.text

soup = BeautifulSoup(billboard_response,"html.parser")

#get song titles and artist names
song_titles=[song.getText().strip() for song in soup.select(selector="li #title-of-a-story")]
artist_names=[artist.getText().strip() for artist in soup.select(selector="li > span.a-no-trucate")]

#make your search criteria more search friendly by removing speacial characters, line breaks, and unwanted words
processed_titles = [t.replace("\n", "").replace("\t", "") for t in song_titles]
processed_artists = [a.replace("\n", "").replace("\t", "").replace(" & ", " ").replace(" Featuring ", " ").replace(" x ", " ").replace(" X ", " ").replace("(", "").replace(")", "").replace(" Or ", " ").replace("'", "").replace(".", "").replace(" / ", " ").replace(" With ", " ").replace(" + ", " ").replace(",", "") for a in artist_names]

#authenticate with Spotify
spotify_auth = spotipy.oauth2.SpotifyOAuth(
    client_id = Client_ID,
    client_secret = Client_Secret,
    redirect_uri = redirect_URI,
    scope = "playlist-modify-private",
    show_dialog = True,
    cache_path = "token.txt"
)

spotify_auth.get_access_token(as_dict=False)
s = spotipy.Spotify(oauth_manager=spotify_auth)
user_id = s.current_user()["id"]
#print (user_id) #prints your User_ID

#search for song titles on Spotify
song_uris = []
year = user_date.split("-")[0]
month = user_date.split("-")[1]
day = user_date.split("-")[2]
int_day = int(day)
int_month = int(month)
month_name = calendar.month_name[int_month]
for song, artist in zip(processed_titles, processed_artists):
    result = s.search(q=f"track:{song} artist:{artist}", type="track", limit=1)
    #print(result) #prints the result
    try:
        #handling exception for when the song cannot be found. It is skipped in this case.
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} by {artist} could not be found. It was skipped.")

#create playlist on Spotify
playlist = s.user_playlist_create(user_id,name=f"Billboard 100 - Week of {int_day} {month_name} {year}",public=False, description=f"Enjoy some of the best tunes from around the world from the week of {int_day} {month_name} {year}")

#add songs to the playlist
s.playlist_add_items(playlist_id=playlist['id'], items=song_uris)
print("Your playlist has been successfully created.")
