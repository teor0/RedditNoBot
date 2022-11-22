import datetime

FLAIR_LIVE = '4f77c9a4-ef7a-11eb-8ee5-aefe156a2d70'
HOURS_THRESHOLD = 6.0
SABREDDIT = 'SabakuNoMaiku'


def get_number_post_comment(reddit_instance, submission_id):
    submission = reddit_instance.submission(submission_id)
    return len(submission.comments.list())


def get_live_notification_post(reddit_instance):
    subreddit=reddit_instance.subreddit(SABREDDIT)
    for submission in subreddit.new():
        get_number_post_comment(reddit_instance,submission.id)


def delete_live_notification_post(reddit_instance):
    subreddit = reddit_instance.subreddit(SABREDDIT)
    for submission in subreddit.new(limit=10):
        now = datetime.datetime.now()
        dt = datetime.datetime.fromtimestamp(submission.created_utc)
        hours_passed = (now-dt).total_seconds()/3600
        if submission.link_flair_template_id == FLAIR_LIVE and hours_passed > HOURS_THRESHOLD \
                and get_number_post_comment(reddit_instance,submission.id) <= 5:
            submission.mod.remove()
