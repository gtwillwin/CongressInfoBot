#CongressInfoBot v1.0
#Created by gtwillwin

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
        user_agent="Congress Info Bot v1.0"
    )
    return reddit


def run_bot(replied_to):
    reddit = authenticate()
    legislators = get_legislator_name()
    while True:
        for mention in reddit.inbox.mentions(limit=25):
            if mention.id not in replied_to:
                for legislator in legislators:
                        if legislator['name']['official_full'] in mention.body:
                            mention.reply(
                                get_legislator_info(legislator)
                            )
                            replied_to.append(mention.id)
                            with open("replied_to.txt", "a") as f:
                                f.write(mention.id + "\n")

        time.sleep(10)


def get_legislator_name():
    response = requests.get('https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml')
    legislators = yaml.load(response.content)
    return legislators


def get_legislator_info(legislator):
        return (
            "**{name}**\n\n Phone: {phone}\n\n Fax: {fax} \n\n Address: {address}".format(
                name=legislator['name']['official_full'],
                phone=legislator['terms'][-1]['phone'],
                address=legislator['terms'][-1]['address'],
                fax=legislator['terms'][-1]['fax']
            )
        )


def get_saved_mentions():
    if not os.path.isfile("replied_to.txt"):
        replied_to = []
    else:
        with open("replied_to.txt", "r") as f:
            replied_to = f.read()
            replied_to = replied_to.split("\n")

    return replied_to


replied_to = get_saved_mentions()


if __name__ == '__main__':
    run_bot(replied_to)
