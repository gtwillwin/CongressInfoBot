import praw
import config
import time
import os

#sheet = client.open('Legislators 2017').sheet1
#legislators = sheet.get_all_records()
#print(legislators)


def authenticate():
    reddit = praw.Reddit(
        username=config.username,
        password=config.password,
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent="Congress Info Bot v0.1"
    )
    return reddit


def run_bot():
    reddit = authenticate()
    for mention in reddit.inbox.mentions(limit=25):
        mention.reply(
            "Placeholder"
            )


if __name__ == '__main__':
    run_bot()
