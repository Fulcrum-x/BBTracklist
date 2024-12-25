import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
from datetime import datetime, timedelta

def get_spotify_client():
    try:
        client_credentials_manager = SpotifyClientCredentials()
        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    except Exception as e:
        print(f"Error connecting to Spotify API: {e}")
        sys.exit(1)

def format_duration(ms):
    """Convert milliseconds to MM:SS format"""
    seconds = ms // 1000
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"

def format_total_duration(total_ms):
    """Convert milliseconds to HH:MM:SS format"""
    seconds = total_ms // 1000
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{remaining_seconds:02d}"
    else:
        return f"{minutes:02d}:{remaining_seconds:02d}"

def format_track_features(track):
    """Format track featuring artists in BBCode format"""
    featuring = []
    if len(track['artists']) > 1:
        featuring = [f"[artist]{artist['name']}[/artist]" for artist in track['artists'][1:]]
    
    if featuring:
        return f" (feat. {' & '.join(featuring)})"
    return ""

def generate_album_bbcode(artist_name, album_name):
    sp = get_spotify_client()
    
    # Search for the album
    results = sp.search(q=f"album:{album_name} artist:{artist_name}", type='album', limit=1)
    
    if not results['albums']['items']:
        print(f"Could not find album '{album_name}' by {artist_name}")
        return None
    
    album = results['albums']['items'][0]
    
    # Get full album details including tracks
    album_details = sp.album(album['id'])
    tracks = album_details['tracks']['items']
    
    # Format release date
    release_date = album_details['release_date']
    if len(release_date) == 4:  # If only year is available
        formatted_date = release_date
    else:
        try:
            date_obj = datetime.strptime(release_date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%B %d, %Y')
        except:
            formatted_date = release_date
    
    # Calculate total duration
    total_duration = sum(track['duration_ms'] for track in tracks)
    
    # Generate BBCode
    bbcode = f"""[size=4][b][artist]{artist_name}[/artist] - {album_name}[/b][/size]
{formatted_date}

[b]Tracklist:[/b]
"""
    
    # Add tracks with duration
    for i, track in enumerate(tracks, 1):
        track_features = format_track_features(track)
        duration = format_duration(track['duration_ms'])
        bbcode += f"[b]{i}.[/b] {track['name']}{track_features} [i]({duration})[/i]\n"
    
    # Add total length
    bbcode += f"\n[b]Total length:[/b] {format_total_duration(total_duration)}"
    
    return bbcode

def main():
    if len(sys.argv) < 3:
        print("Usage: python album_bbcode.py 'Artist Name' 'Album Name'")
        sys.exit(1)
    
    artist_name = sys.argv[1]
    album_name = sys.argv[2]
    
    try:
        bbcode = generate_album_bbcode(artist_name, album_name)
        if bbcode:
            # Write to temp file for clipboard and print to console
            with open("temp_bbcode.txt", "w", encoding="utf-8") as f:
                f.write(bbcode)
            print("\nGenerated BBCode:")
            print("-----------------")
            print(bbcode)
            print("\nBBCode has been saved for clipboard copying!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()