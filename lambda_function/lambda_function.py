from datetime import datetime, timezone, timedelta
import json
import random
import requests
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def _day_suffix(n):
    return "th" if 4<=n%100<=20 else {1:"st",2:"nd",3:"rd"}.get(n%10, "th")


def lambda_handler(event, context):
    secrets = yaml.load(open('secrets.yaml'), Loader=Loader)

    SEED = 1
    random.seed(SEED)
    quotes = json.load(open("quotes.json"))
    quotes = sorted(quotes, key=lambda i: random.random())

    nicknames = json.load(open("nicknames.json"))
    nicknames = sorted(nicknames, key=lambda i: random.random())

    # Get today's date in the Pacific timezone
    timezone_offset = -8.0  # Pacific Standard Time (UTC−08:00)
    tzinfo = timezone(timedelta(hours=timezone_offset))
    today = datetime.now(tzinfo).date()

    # Start over every 6 months.
    tm_yday = today.timetuple().tm_yday
    quote_dict = quotes[(tm_yday - 1) % len(quotes)]
    nickname = nicknames[(tm_yday - 1) % len(nicknames)]

    # Build the message
    date_str = (today.strftime('%B %-d{th}, %Y')
                .replace('{th}', _day_suffix(today.day)))
    msg = (f"Good morning {nickname},\n\nHere's your daily dose of lurv for "
           f"{date_str}:\n\n{quote_dict['quote']}")
    if "author" in quote_dict:
        msg += f"\n\n<i>- {quote_dict['author']}</i>"

    for user_chat_id in secrets['USER_CHAT_IDS']:
        url = (f"https://api.telegram.org/bot{secrets['TELEGRAM_TOKEN']}/"
               f"sendMessage?chat_id={user_chat_id}&text={msg}&parse_mode=html")
        # Send the message
        print(requests.get(url).json())
