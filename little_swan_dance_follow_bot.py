from dotenv import load_dotenv

load_dotenv()

from instapy import InstaPy
from instapy import smart_run
from instapy import set_workspace
from os import getenv

import schedule
import time

set_workspace(path=getenv('LITTLE_SWAN_DANCE_WORKSPACE'))


def job():
    session = InstaPy(username=getenv('LITTLE_SWAN_DANCE_USERNAME'), password=getenv('LITTLE_SWAN_DANCE_PASSWORD'),
                      headless_browser=True).login()
    session.set_quota_supervisor(enabled=True,
                                 sleep_after=["likes", "comments_d", "follows", "unfollows", "server_calls_h"],
                                 sleepyhead=True, stochastic_flow=True, notify_me=False,
                                 peak_likes_hourly=20,
                                 peak_likes_daily=100,
                                 peak_comments_hourly=12,
                                 peak_comments_daily=180,
                                 peak_follows_hourly=20,
                                 peak_follows_daily=150,
                                 peak_unfollows_hourly=10,
                                 peak_unfollows_daily=50,
                                 peak_server_calls_hourly=None,
                                 peak_server_calls_daily=4000)

    session.set_use_clarifai(enabled=True, api_key=getenv('CLARIFAI_API_KEY'))

    with smart_run(session):
        session.set_do_like(enabled=False)
        session.set_do_comment(enabled=False)
        session.set_dont_like(["naked", "nsfw"])
        session.set_do_follow(True, percentage=70, times=1)
        session.follow_by_tags(['dancestudioownerlife', 'dancestudioowner', 'danceteacher'], amount=30)
        session.follow_user_followers(
            ['twinklestardance', 'confettionthedancefloor', 'toddlerandpreschoolballet', 'studiotogodance',
             'leapnlearn'],
            amount=20, randomize=True, sleep_delay=30, interact=False)
        session.follow_likers(
            ['twinklestardance', 'confettionthedancefloor', 'toddlerandpreschoolballet', 'studiotogodance',
             'leapnlearn'],
            photos_grab_amount=3, follow_likers_per_photo=5, randomize=True, sleep_delay=30, interact=False)
        session.follow_commenters(
            ['twinklestardance', 'confettionthedancefloor', 'toddlerandpreschoolballet', 'studiotogodance',
             'leapnlearn'],
            amount=3, daysold=180, max_pic=20, sleep_delay=30, interact=False)
        session.unfollow_users(amount=50, nonFollowers=True, style='RANDOM', unfollow_after=432000, sleep_delay=30)

        # session.end()


schedule.every().day.at("11:50").do(job)

while True:
    schedule.run_pending()
    time.sleep(10)
