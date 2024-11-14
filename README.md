# cs361-microservice

## Communication Contract

### Requesting Data

To request data from the microservice, you need to make HTTP GET requests to the following endpoints:

1. **Search Genius Link**
   - **Endpoint:** `/search_genius`
   - **Parameters:**
     - `artist`: The name of the artist.
     - `song`: The name of the song.
   - **Example Call:**
     ```python
     import requests

     url = "http://127.0.0.1:5000/search_genius"
     params = {'artist': 'Adele', 'song': 'Hello'}
     response = requests.get(url, params=params)
     response.raise_for_status()
     data = response.json()
     print(data)  # {'genius_link': 'https://genius.com/Adele-hello-lyrics'}
     ```

2. **Scrape Lyrics**
   - **Endpoint:** `/scrape_lyrics`
   - **Parameters:**
     - `genius_url`: The URL of the Genius page to scrape lyrics from.
   - **Example Call:**
     ```python
     import requests

     url = "http://127.0.0.1:5000/scrape_lyrics"
     params = {'genius_url': 'https://genius.com/Adele-hello-lyrics'}
     response = requests.get(url, params=params)
     response.raise_for_status()
     data = response.json()
     print(data)  # {'lyrics': '...'}
     ```

### Receiving Data

To receive data from the microservice, you need to handle the JSON responses from the endpoints:

1. **Search Genius Link Response**
   - **Response Format:**
     ```json
     {
       "genius_link": "https://genius.com/Adele-hello-lyrics"
     }
     ```

2. **Scrape Lyrics Response**
   - **Response Format:**
     ```json
     {
       "lyrics": "..."
     }
     ```

### UML Sequence Diagram

```plaintext
+-------------------+       +-------------------+       +-------------------+
|    Client         |       |    Microservice   |       |    Genius.com     |
+-------------------+       +-------------------+       +-------------------+
          |                          |                          |
          | 1. /search_genius        |                          |
          |------------------------->|                          |
          |                          |                          |
          |                          | 2. search_genius()       |
          |                          |------------------------->|
          |                          |                          |
          |                          | 3. Return genius_link    |
          |                          |<-------------------------|
          | 4. Return JSON response  |                          |
          |<-------------------------|                          |
          |                          |                          |
          | 5. /scrape_lyrics        |                          |
          |------------------------->|                          |
          |                          |                          |
          |                          | 6. scrape_lyrics()       |
          |                          |------------------------->|
          |                          |                          |
          |                          | 7. Return lyrics         |
          |                          |<-------------------------|
          | 8. Return JSON response  |                          |
          |<-------------------------|                          |
          |                          |                          |
+-------------------+       +-------------------+       +-------------------+