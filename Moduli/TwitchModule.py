"""TwitchModule

Questo modulo contiene le seguenti funzioni:
    * get_oauth - ritorna e salva un access token su un file json
    * get_stream_info - ritorna informazioni utili sulla live di uno specifico streamer
    * is_stream_off - ritorna true se lo streamer è offline
License:
    MIT License

    Copyright (c) 2023 Matteo Orlando

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

Author:
    Matteo Orlando
"""
import requests
import json
import os.path

def get_oauth(client_id,client_secret):
    """Funzione per ottenere un access token

    Parameters
    ---------
    client_id : str
        Stringa che identifica il client id dell'applicazione che si interfaccia all'API
    client_secret : str
        Stringa che identifica il client_secret dell'applicazione che si interfaccia all'API

    Returns
    -------
    dict
        Dictionary contenente i campi dell'access token
    """

    body = {
        'client_id': client_id,
        'client_secret': client_secret,
        "grant_type": 'client_credentials'
    }
    r = requests.post('https://id.twitch.tv/oauth2/token', body)
    keys = r.json();
    with open("/tmp/keys.json", "w") as output:
        json.dump(keys, output)
    return keys


def get_stream_info(client_id, client_secret, streamer):
    """Funzione per ottenere informazioni utili sulla live di una streamer

    Parameters
    ---------
    client_id : str
        Stringa che identifica il client id dell'applicazione che si interfaccia all'API
    client_secret : str
        Stringa che identifica il client_secret dell'applicazione che si interfaccia all'API
    streamer : str
        Stringa che identifica il nickname di uno streamer

    Returns
    -------
    dict
        Dictionary contenente informazioni utili
    """
    if(os.path.exists("/tmp/keys.json")):
        with open("/tmp/keys.json", "r") as f:
            keys=json.load(f)
    else:
        keys=get_oauth(client_id, client_secret)
    headers = {
        'Client-ID': client_id,
        'Authorization': 'Bearer ' + keys['access_token']
    }
    stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer, headers=headers)
    if(stream.status_code==200):
       stream_data = stream.json()
       if len(stream_data['data']) == 1:
            game = stream_data['data'][0]['game_name']
            title = stream_data['data'][0]['title']
            return True,game,title
       else:
           return False,None,None
    else:
        keys=get_oauth(client_id,client_secret)
        headers = {
            'Client-ID': client_id,
            'Authorization': 'Bearer ' + keys['access_token']
        }
        new_stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + target_streamer, headers=headers)
        stream_data = new_stream.json()
        if len(stream_data['data']) == 1:
            game = stream_data['data'][0]['game_name']
            title = stream_data['data'][0]['title']
            return True,game,title
        else:
            return False,None,None

def is_stream_off(client_id, client_secret, streamer):
    """Funzione per verificare se uno streamer è in live

    Parameters
    ---------
    client_id : str
        Stringa che identifica il client id dell'applicazione che si interfaccia all'API
    client_secret : str
        Stringa che identifica il client_secret dell'applicazione che si interfaccia all'API
    streamer : str
        Stringa che identifica il nickname di uno streamer

    Returns
    -------
    Boolean
        True se lo streamer è offline, false altrimenti
    """
    if(os.path.exists("/tmp/keys.json")):
        with open("/tmp/keys.json", "r") as f:
            keys=json.load(f)
    else:
        keys=get_oauth(client_id, client_secret)
    headers = {
        'Client-ID': client_id,
        'Authorization': 'Bearer ' + keys['access_token']
    }
    stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer, headers=headers)
    if(stream.status_code==200):
       stream_data = stream.json()
       return len(stream_data['data']) == 0
    else:
        keys=get_oauth(client_id,client_secret)
        headers = {
            'Client-ID': client_id,
            'Authorization': 'Bearer ' + keys['access_token']
        }
        new_stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + target_streamer, headers=headers)
        stream_data = new_stream.json()
        return len(stream_data['data']) == 0
