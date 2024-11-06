from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

def search_genius(artist, song):
    query = f"{artist} {song} Genius"
    search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    genius_link = None
    for g in soup.find_all('a'):
        href = g.get('href')
        if href and "genius.com" in href:
            genius_link = href.split("&")[0]
            break
    
    return genius_link

def scrape_lyrics(genius_url):
    response = requests.get(genius_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all lyrics containers
    lyrics_containers = soup.find_all('div', {'data-lyrics-container': 'true'})
    
    if lyrics_containers:
        # Print the first container's lyrics
        first_lyrics = lyrics_containers[0].get_text(separator="\n").strip()
        return first_lyrics
    else:
        return "No lyrics containers found."

@app.route('/search_genius', methods=['GET'])
def search_genius_endpoint():
    artist = request.args.get('artist')
    song = request.args.get('song')
    if not artist or not song:
        return jsonify({"error": "Missing artist or song parameter"}), 400
    
    link = search_genius(artist, song)
    return jsonify({"genius_link": link})

@app.route('/scrape_lyrics', methods=['GET'])
def scrape_lyrics_endpoint():
    genius_url = request.args.get('genius_url')
    if not genius_url:
        return jsonify({"error": "Missing genius_url parameter"}), 400
    
    lyrics = scrape_lyrics(genius_url)
    return jsonify({"lyrics": lyrics})

if __name__ == '__main__':
    app.run(debug=True)