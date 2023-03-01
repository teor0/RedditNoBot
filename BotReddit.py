import praw
import sys
from RedditModule import delete_specific_post
from RedditModule import submit_post_no_text
from TwitchModule import is_stream_off
from TwitchModule import get_stream_info
from cryptography.fernet import Fernet

USERNAME = 'CostruttoViola'
USERAGENT = 'script:RedditNoBot:v1.3.5 (by /u/CostruttoViola)'
STREAMER="sabaku_no_sutoriimaa"
FLAIR_LIVE = '4f77c9a4-ef7a-11eb-8ee5-aefe156a2d70'
SUBREDDIT = 'SabakuNoMaiku'
MIN_COM = 5
POST_LIMIT = 10

def main():
    with open('/opt/SabakuNoBot/BotEnv/key.txt', 'rb') as f:
        key=f.read()
    f.close()
    fernet=Fernet(key)
    with open('/opt/SabakuNoBot/BotEnv/credentials.txt', 'rb') as f:
        CLIENT_ID_REDDIT=fernet.decrypt(f.readline()).decode()
        API_KEY=fernet.decrypt(f.readline()).decode()
        PASSWORD_REDDIT=fernet.decrypt(f.readline()).decode()
        CLIENT_ID_TWITCH=fernet.decrypt(f.readline()).decode()
        CLIENT_SECRET_TWITCH=fernet.decrypt(f.readline()).decode()
    f.close()
    reddit = praw.Reddit(
        client_id=CLIENT_ID_REDDIT,
        client_secret=API_KEY,
        username=USERNAME,
        password=PASSWORD_REDDIT,
        user_agent=USERAGENT
    )
    command = input()
    match command:
        case "online check":
            info=get_stream_info(CLIENT_ID_TWITCH,CLIENT_SECRET_TWITCH,STREAMER)
            if(info[0]):
                title="Siamo Live! || " + info[1] + " || " + info[2]
                submit_post_no_text(reddit,SUBREDDIT,title,FLAIR_LIVE)
                sys.exit(0)
            else:
                sys.exit(1)
        case "remove post":
            delete_specific_post(reddit,SUBREDDIT,FLAIR_LIVE,MIN_COM,POST_LIMIT)
            sys.exit(0)
        case "offline check":
            if(is_stream_off(CLIENT_ID_TWITCH,CLIENT_SECRET_TWITCH,STREAMER)):
                sys.exit(0)
            else:
                sys.exit(1)
        case other:
            print("Wrong command or nothing done")
            sys.exit(1)


if __name__ == '__main__':
    main()
