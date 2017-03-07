#CongressInfoBot v1.0
#Created by gtwillwin

import praw
import config
import time
import os
import requests
import yaml
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


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
    start = '"'
    end = '"'
    comment = "aaa"
    list_names = []
    while True:
        for mention in reddit.inbox.mentions(limit=25):
            if mention.id not in replied_to:
                comment = mention.body
                comment = comment.split(start)[1].split(end)[0]
                with open("replied_to.txt", "a") as f:
                    f.write(mention.id + "\n")
                for legislator in legislators:
                    list_names.append(legislator['name']['official_full'])
                person = process.extractOne(comment, list_names, scorer=fuzz.partial_ratio)
                person = person[0]
                for legislator in legislators:
                    if person == legislator['name']['official_full']:
                            print("Match Found!")
                            mention.reply(
                                get_legislator_info(legislator)
                            )
                            replied_to.append(mention.id)

        time.sleep(10)


def get_legislator_name():
    response = requests.get(
        'https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-current.yaml'
        )
    legislators = yaml.load(response.content)
    return legislators


def get_legislator_info(legislator):
        return (
            "##{title} {name} ({party}-{state}) \n\n **Contact:** \n\n Phone: {phone}\n\n Fax: {fax} \n\n Address: {address} \n\n Email: {contact_form} \n\n **Links:** \n\n [govtrack](https://www.govtrack.us/congress/members/{govtrack}) \n\n [VoteSmart](https://votesmart.org/candidate/political-courage-test/{votesmart})".format(
                name=legislator['name'].get('official_full'),
                phone=legislator['terms'][-1].get('phone', 'N/A'),
                address=legislator['terms'][-1].get('address', 'N/A'),
                fax=legislator['terms'][-1].get('fax', 'N/A'),
                title=legislator['terms'][-1]['type'].upper(),
                contact_form=legislator['terms'][-1].get('contact_form', 'N/A'),
                party=legislator['terms'][-1]['party'][0],
                state=legislator['terms'][-1].get('state', 'N/A'),
                govtrack=legislator['id'].get('govtrack', 'N/A'),
                votesmart=legislator['id'].get('votesmart', 'N/A')

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
