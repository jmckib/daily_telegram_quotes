import json
import requests
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def lambda_handler(event, context):
    secrets = yaml.load(open('secrets.yaml'), Loader=Loader)

    message = json.load(open('quotes.json'))[100]['quote']
    url = (f"https://api.telegram.org/bot{secrets['TELEGRAM_TOKEN']}/"
           f"sendMessage?chat_id={secrets['USER_CHAT_ID']}&text={message}")
    # Send the message
    print(requests.get(url).json())
