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
