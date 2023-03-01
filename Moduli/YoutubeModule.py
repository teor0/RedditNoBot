"""YoutubeModule

Questo modulo contiene le seguenti funzioni:
    * get_all_playlist - ritorna tutte le playlist di un canale con all'interno anche i video 
    * get_videos - ritorna tutti i video di una playlist
    * get_last_upload - ritorna l'ultimo video caricato da un canale
    * get_playlist_duration - ritorna la durata totale di una playlist 

License:
    MIT License

    Copyright (c) 2022 Matteo Orlando

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


import re
from datetime import timedelta


def get_all_playlist(service, channel_id):
    """Funzione per ottenere tutte le playlist da un canale Youtube
    
    Parameters
    ---------
    service : Resource Object
        Oggetto ottenuto tramite il metodo build della API
    channel_id : str
        ID del canale Youtube
    
    Returns
    -------
    dict
        dictionary contenente {titolo playlist:{titolo video:link}}
    """
    next_page_token = None
    dic = {}
    while True:
        pl_request = service.playlists().list(
            part='contentDetails,snippet',
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        )
        pl_response = pl_request.execute()
        for pid in pl_response['items']:
            play_title = pid['snippet']['title']
            video = get_videos(service, pid['id'])
            dic[play_title] = video
        next_page_token = pl_response.get('nextPageToken')
        if not next_page_token:
            break
    return dic


def get_videos(service, playlist_id):
    """Funzione per ottenere tutte i video da una playlist Youtube
    
    Parameters
    ---------
    service : Resource Object
        Oggetto ottenuto tramite il metodo build della API
    playlist_id : str
        ID della playlist Youtube
    
    Returns
    -------
    dict
        dictionary contenente {titolo video:link}
    """
    next_page_token = None
    video = {}
    while True:
        pl_request = service.playlistItems().list(
            part='contentDetails,snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        pl_response = pl_request.execute()
        for item in pl_response['items']:
            title = item['snippet']['title']
            link = 'https://www.youtube.com/watch?v=' + item['contentDetails']['videoId']
            video[title] = link
        next_page_token = pl_response.get('nextPageToken')
        if not next_page_token:
            break
    return video


def get_last_upload(service,channel_id):
    """Funzione per ottenere l'ultimo video caricato da un canale Youtube
    
    Parameters
    ---------
    service : Resource Object
        Oggetto ottenuto tramite il metodo build della API
    channel_id : str
        ID del canale Youtube
    
    Returns
    -------
    tuples
        tupla formata da titolo video, link
    """
    play_id='UU'+channel_id[2:]
    v_request = service.playlistItems().list(
        part='contentDetails,snippet',
        playlistId=play_id,
    )
    v_response = v_request.execute()
    title = v_response['items'][0]['snippet']['title']
    link = 'https://www.youtube.com/watch?v=' + v_response['items'][0]['snippet']['resourceId']['videoId']
    return title,link


def get_playlist_duration(service, play_id):
    """Funzione per la durata complessiva di una playlist youtube

    Parameters
    ---------
    service : Resource Object
        Oggetto ottenuto tramite il metodo build della API
    play_id : str
        ID della playlist Youtube

    Returns
    -------
    str
        stringa contenente la durata totale della playlist espressa in HH:MM::SS    
    """
    regex_hour = re.compile(r'(\d+)H')
    regex_min = re.compile(r'(\d+)M')
    regex_sec = re.compile(r'(\d+)S')
    total_seconds = 0
    nextPageToken = None
    while True:
        pl_request = service.playlistItems().list(
            part='contentDetails',
            playlistId=play_id,
            maxResults=50,
            pageToken=nextPageToken
        )
        pl_response = pl_request.execute()

        vid_ids = []
        for item in pl_response['items']:
            vid_ids.append(item['contentDetails']['videoId'])

        vid_request = service.videos().list(
            part="contentDetails",
            id=','.join(vid_ids)
        )
        vid_response = vid_request.execute()
        for item in vid_response['items']:
            duration = item['contentDetails']['duration']

            hours = regex_hour.search(duration)
            minutes = regex_min.search(duration)
            sec = regex_sec.search(duration)

            hours = int(hours.group(1)) if hours else 0
            minutes = int(minutes.group(1)) if minutes else 0
            sec = int(sec.group(1)) if sec else 0

            video_seconds = timedelta(
                hours=hours,
                minutes=minutes,
                seconds=sec
            ).total_seconds()

            total_seconds += video_seconds
        nextPageToken = pl_response.get('nextPageToken')
        if not nextPageToken:
            break
    total_seconds = int(total_seconds)
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return str(hours) + ':' + str(minutes) + ':' + str(seconds)
