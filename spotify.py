import spotipy
from requests_oauthlib import OAuth2Session
import base64
from time import time
#from flask import request, redirect, session, url_for, Flask
from flask.json import jsonify


class Spotify:
    scope = "user-read-playback-state"
    client_id= "a7a5ce8cb297457c878ddc5c84e252a4"
    client_secret="c40fe9f626bf41c9a36b60f8b871dc83"
    redirect_uri= "https://sites.google.com/view/pras-spotify/home"
    redirect_uri_encoded = "https%3A%2F%2Fsites.google.com%2Fview%2Fpras-spotify%2Fhome"
    authorization_base_url = "https://accounts.spotify.com/authorize"
    token_url = "https://accounts.spotify.com/api/token"
    refresh_url = token_url
    SPOTIPY_CLIENT_ID = client_id
    SPOTIPY_CLIENT_SECRET = client_secret
    token = None
    soa = spotipy.oauth2.SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, username= "srinivas.prasanna.k")


    def step1(self):
        s = OAuth2Session(self.client_id, scope=self.scope, redirect_uri=self.redirect_uri)
        authorization_url = s.authorization_url(self.authorization_base_url,access_type="offline", prompt="select_account")
        print (authorization_url)
        return authorization_url

    def step2_fetch_token(self):
        s=OAuth2Session(client_id=self.client_id,redirect_uri=self.redirect_uri)
        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_b64 = base64.b64decode(client_creds.encode())
        header ={"Authorization": f"Basic {client_creds_b64}"}
        print("After completing Step 1, type Authorization code here: ")
        auth_code = input()
        token = s.fetch_token(token_url=self.token_url, client_secret=self.client_secret,code=auth_code, headers=header)
        self.token = token
        return token

    def auto_refresh(self, token):
        token['expires_at'] = time()-10
        extra = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        def token_updater(token):
            self.token['access_token'] = token
        s = OAuth2Session(client_id=self.client_id, token=token, auto_refresh_kwargs=extra, auto_refresh_url=self.refresh_url, token_updater=token_updater)

        jsonify(s.get('https://api.spotify.com/v1/me/player/currently-playing)').json)
        return token
    def manual_refresh(self, refresh_token):
        token = self.token
        extra = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        s= OAuth2Session(client_id=self.client_id, token=token)
        self.token = s.refresh_token(token_url=self.token_url, refresh_token=refresh_token, **extra)
        return self.token
    '''
    print("After completing Step 1, type Authorization code here: ")
    auth_code = input()
    access_token = soa.get_access_token(as_dict= False ,code=auth_code)
    
    sp = spotipy.Spotify(access_token)
    
    print (sp.currently_playing())
    '''