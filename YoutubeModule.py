import re
from datetime import timedelta

# funzione per ottenere tutte le playlist da un canale
def get_and_store_data(service, channel_id):
    next_page_token = None
    # utilizzo un dictionary per memorizzare {nome playlist, link video della playlist}
    # se c'è un modo migliore si utilizza
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


# funzione per ottenere tutti i video da una playlist
def get_videos(service, playlist_id):
    next_page_token = None
    # stesso discorso, utilizzo un dictionary per memorizzare {titolo, link}
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


#funzione per ottenere la durata totale di una playlist
def get_playlist_duration(service, play_id):
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
