import requests
from bs4 import BeautifulSoup
import urllib.parse

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
        print(f"\n{first_lyrics.strip()}\n")  # Print first container lyrics

        # Ask if the user wants to see the rest of the lyrics
        view_more = input("Would you like to see the rest of the lyrics? (yes/no): ").strip().lower()

        if view_more == 'yes':
            combined_lyrics = []
            for container in lyrics_containers:
                # Get the text of the lyrics and strip unnecessary whitespace
                lyrics = container.get_text(separator="\n").strip()
                combined_lyrics.append(lyrics)

            # Join all the lyrics without adding extra line breaks
            formatted_lyrics = "\n".join(combined_lyrics)
            print(f"\n{formatted_lyrics.strip()}\n")  # Print all lyrics
        else:
            print("Okay, have a great day!")
    else:
        print("No lyrics containers found.")

def main():
    artist = input("Enter the artist name: ")
    song = input("Enter the song name: ")
    
    genius_url = search_genius(artist, song)
    if genius_url:
        scrape_lyrics(genius_url)
    else:
        print("Could not find the song.")

if __name__ == "__main__":
    main()