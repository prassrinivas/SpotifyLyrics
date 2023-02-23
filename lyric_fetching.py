import spotify
import spotipy
import genius
import requests
import json
from tkinter import *
from os import path




class lyrics:
    lyric = ""
    title= ""
    refresh_token = 'AQDh6xM-Omre751Z7RM29eWe5ZXP0IkTkD5J6Iv_skjC42Z_ZLQH0nKhACmy4fgifBiG_P5od4ESc8eh1fhlBRJj6oFjXDwfNKnXS-NI-Spb8-yoDmco32MfX9CkSm2wJhY'
    cached_song_title = ""
    manual_song_replacement ={"Yesterday - Remastered 2009":"Yesterday",
                              "Lose Yourself - From \"8 Mile\" Soundtrack" :"Lose Yourself",
                              "Hot (Remix) [feat. Gunna and Travis Scott]": "Hot",
                              "Can't Hold Us - feat. Ray Dalton": "Can't Hold Us",
                              "Fantasy": "Fantasy Bazzi",
                              "Why": "Why Bazzi",
                              "Myself": "Myself Bazzi",
                              "3:15":"3:15 Bazzi",
                              "Thrift Shop (feat. Wanz)" : "thrift shop macklemore",
                              "Same Love - feat. Mary Lambert": "Same Love Macklemore"
                              }



    g = genius.Genius()
    sp = spotify.Spotify()
    token_response_dict = sp.manual_refresh(refresh_token=refresh_token)
    access_token = token_response_dict.get('access_token')
    refresh_token = token_response_dict.get('refresh_token')
    p = spotipy.Spotify(auth=access_token)
    i = 1
    j = 2

    def getlyrics(self):
        return self.lyric

    def update_song_replacement_dict(self):
        if not path.exists("song_title_replacement.txt"):
            print("song_title_replacement doesn't exist")
            with open("song_title_replacement.txt", "w") as file:
                json.dump(self.manual_song_replacement, file)
        with open("song_title_replacement.txt", "r") as file2:
            self.manual_song_replacement = json.load(file2)

    def refine_search_term(self, title, new_search_term):
        self.manual_song_replacement[title] = new_search_term
        if path.exists("song_title_replacement.txt"):
            #print("song_title_replacement doesn't exist")
            with open("song_title_replacement.txt", "w") as file:
                json.dump(self.manual_song_replacement, file)
        with open("song_title_replacement.txt", "r") as file2:
            self.manual_song_replacement = json.load(file2)

    def get_lyrics_loop(self, second_attempt = False):
            #import gui_spotify
            #gui = gui_spotify.gui_Spotify()
        try:
                #while(True):
            current_song_dict = self.p.currently_playing()
            if (self.i%900 ==0):
                token_response_dict = self.sp.manual_refresh(refresh_token=self.refresh_token)
                self.access_token = token_response_dict.get('access_token')
                self.refresh_token = token_response_dict.get('refresh_token')
                self.p = spotipy.Spotify(auth=self.access_token)
                self.j+=1  #refresh every half hour

            if (current_song_dict['is_playing'] == True and current_song_dict['currently_playing_type'] == "track"):
                song_title = current_song_dict['item']['name']
                self.title = song_title
                if song_title in self.manual_song_replacement:
                    song_title = self.manual_song_replacement[song_title]
                if self.cached_song_title != song_title or self.lyric == "couldn't find song from genius search" :
                    self.g.set_search_info(song_title=song_title, artist_name=current_song_dict['item']['artists'][0]['name'])
                    print(f"{self.i}, {self.j}, {current_song_dict['item']['name']}, by {current_song_dict['item']['artists'][0]['name']}")
                    self.title = f"{current_song_dict['item']['name']}, by {current_song_dict['item']['artists'][0]['name']}"
                    genius_result_dict = self.g.search(second_attempt=second_attempt)
                    song_info = None
                    for hit in genius_result_dict["response"]["hits"]:
                        artist_name = current_song_dict['item']['artists'][0]['name']
                        artist_name = artist_name.replace("&","|")
                        artist_name= artist_name.replace(",", "|")
                        artist_name = artist_name.replace(" ", "|")
                        if  any (re.findall(artist_name , hit["result"]["primary_artist"]["name"])) and requests.get("https://genius.com"+ hit['result']['api_path']).url.endswith('lyrics'):
                            song_info = hit
                            #search_result_name = hit["result"]["primary_artist"]["name"]
                            break
                        if self.i == len(genius_result_dict["response"]["hits"]):
                            self.lyric = "couldn't find song from genius search"
                            break
                        self.i += 1
                    if song_info != None:
                        song_api_path = song_info["result"]["api_path"]

                        lyr = self.g.lyrics_from_song_api_path(song_api_path)
                        self.lyric = lyr
                        #gui.set_lyrics(lyr)

                        #print(genius_result_dict['response']['hits'])
                    self.cached_song_title = song_title
            else:
                self.lyric = "Playing Ad rn or not playing at all"
                self.cached_song_title = "None"

            self.i += 1
           #time.sleep(2)
        #except TypeError:
            #self.lyric = "Playing Ad rn or not playing at all"
            #self.cached_song_title = "None"
        except (requests.HTTPError, spotipy.SpotifyException):
            self.lyric = "I typed your symptoms into the thing up here and it said you have Network Connectivity Problems"





if __name__=="__main__":
    l = lyrics()
    print(l.p.currently_playing()['item']['duration_ms'])

#to find the song title in the current_song_dict, look for current_song_dict['item']['name']
#to find the artist name, current_song_dict['item']['artists'][0]['name']'''