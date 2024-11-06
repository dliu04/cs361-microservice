import requests

def test_search_genius(artist, song):
    url = "http://127.0.0.1:5000/search_genius"
    params = {'artist': artist, 'song': song}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def test_scrape_lyrics(genius_url):
    url = "http://127.0.0.1:5000/scrape_lyrics"
    params = {'genius_url': genius_url}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    artist = input("Enter the artist name: ")
    song = input("Enter the song name: ")
    
    search_result = test_search_genius(artist, song)
    genius_url = search_result.get("genius_link")
    
    if genius_url:
        lyrics_result = test_scrape_lyrics(genius_url)
        print(lyrics_result.get("lyrics"))
    else:
        print("Could not find the song.")