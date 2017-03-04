import praw
import config
import time
import os
import requests
import yaml


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
    names = get_legislators()
    for mention in reddit.inbox.mentions(limit=25):
        for name in names:
            if name in mention.body:
                mention.reply(
                    "Placeholder"
                    )
        time.sleep(10)


def get_legislators():
    response = requests.get('https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml')
    legislators = yaml.load(response.content)
    names = legislators[0]['name']['official_full']
    return names


if __name__ == '__main__':
    run_bot()
