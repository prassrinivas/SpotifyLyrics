import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString
import os
import re

class Genius:
    token = "hEsGkv7TZOJjJPZF-5cXJMO8OQgFRl4AsmuqIB67sb3_SDUTGVfI6SSb2okPaWyd"
    client_id = "aKqvg17Fd5YMSHGfWc1TYfcy58kYrNGNO0GFaFexIO2-Fstwc6viELmc6qqdIA-W"
    client_secret = "vv0CU_BK6mbuCLi6FQHlVxs4NtF_2_WPiEaAbuKKliB7lAygqaWLz-dw9RZ8GxMjrikDFtIHrXyPeTt4S6GY9g"
    base_url = "http://api.genius.com"
    headers = {"Authorization" : f"Bearer {token}"}
    search_url = base_url + "/search"
    song_title = ""
    artist_name = ""

    def __init__(self, song_title = None, artist_name = None):
        self.song_title= song_title
        self.artist_name = artist_name

    def set_search_info(self,song_title, artist_name):
        self.song_title = song_title
        self.artist_name = artist_name
    def search(self, second_attempt = False):
        if second_attempt == False:
            params= {'q': self.song_title}
        else:
            params = {'q': f"{self.song_title} {self.artist_name}"}

        response = requests.get(url=self.search_url, params=params, headers=self.headers)
        return response.json()

    def lyrics_from_song_api_path(self, song_api_path):
        song_url = self.base_url + song_api_path
        response = requests.get(url=song_url, headers=self.headers)
        song_page_result = response.json()
        path = song_page_result["response"]["song"]["path"]
        page_url = "https://genius.com" + path
        page = requests.get(page_url)

        html = BeautifulSoup(page.text, 'html.parser')
        lyrics = html.find('div', class_='lyrics')
        # remove identifiers like chorus, verse, etc
        lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
        # remove empty lines
        lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])
        html = BeautifulSoup(page.text, "html.parser")
        #[h.extract() for h in html('script')]
        lyrics_containers = html.find_all('div', class_='Lyrics__Container-sc-1ynbvzw-7 dVtOne')
        lyrics = ""
        for container in lyrics_containers:
            for line in container.contents:

                if type(line) is NavigableString:
                    lyrics += line
                elif (line.name == "br"):
                    lyrics += '\n'
                elif(line.name == 'a'):
                    link_contents = line.find("span").contents
                    for link_line in link_contents:
                        if type(link_line) is NavigableString:
                            lyrics += link_line
                        elif (link_line.name == "br"):
                            lyrics += '\n'


        return lyrics

    def run(self):
        data = {'q': self.song_title}
        response = requests.get(url=self.search_url, data=data, headers=self.headers)
        json = response.json()
        song_info = None
        i = 1
        for hit in json["response"]["hits"]:

            if hit["result"]["primary_artist"]["name"] == self.artist_name:
                song_info = hit
                search_result_name=hit["result"]["primary_artist"]["name"]
                #print (f"{search_result_name} is the same as {self.artist_name}")
                break
            if i == len(json["response"]["hits"]):
                print ("couldn't find song from genius search")
            i+=1

        if song_info:
            song_api_path = song_info["result"]["api_path"]
            print(self.lyrics_from_song_api_path(song_api_path))
